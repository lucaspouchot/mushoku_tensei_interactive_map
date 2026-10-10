"""Clean up pandoc's epub -> markdown output and split it into one file per chapter.

Usage: python tools/clean_md.py [input files...]   (default: books/*.md)
Each books/vol_<N>.md becomes books/volume_<N>/ containing:
  00_front-matter.md   title, cover, color inserts and table of contents
  01_<chapter>.md ...  one file per table-of-contents entry, in reading order
The source files are left untouched.
"""
import re
import shutil
import sys
from pathlib import Path

BOOKS_DIR = Path(__file__).resolve().parent.parent / "books"

FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
SECTION_ANCHOR = re.compile(r"^\[\]\{#(section-\d+)\.html\}$")
EMPTY_ANCHOR = re.compile(r"\[\]\{#[^}]*\}")
DIV_FENCE = re.compile(r"^:::.*$", re.M)
IMAGE_ATTRS = re.compile(r"(!\[[^\]]*\]\([^)]*\))\{[^}]*\}", re.S)
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)]*)\)")
# [content]{style="..."} where content may contain one level of [link](url)
SPAN = re.compile(
    r"\[((?:[^\[\]]|\[[^\[\]]*\]\([^)]*\))*)\]\{style=\"([^\"]*)\"\}", re.S)
TOC_LINK = re.compile(r"\[([^\]]+)\]\(\.\./Text/(section-\d+)\.html\)", re.S)
FONT_SIZE = re.compile(r"font-size:\s*([\d.]+)em")
NBSP_ONLY = re.compile(r"^[\s ]*$")
VOLUME_NUMBER = re.compile(r"(\d+)")
HARD_BREAK = "\x00"

# Table-of-contents entries that belong to the front matter file
FRONT_ENTRIES = {"Color Inserts", "Title Page", "Copyrights and Credits",
                 "Table of Contents Page"}
# Table-of-contents entries that are dropped entirely
DROPPED_ENTRIES = {"Newsletter"}


def join_lines(text):
    """Turn a multi-line paragraph into one line, keeping explicit `\\` breaks."""
    text = text.replace("\\\n", HARD_BREAK)
    return re.sub(r"\s*\n\s*", " ", text)


def font_size(style):
    m = FONT_SIZE.search(style)
    return float(m.group(1)) if m else 1.0


def wrap(content, marker):
    """Wrap in emphasis markers, keeping surrounding whitespace outside them."""
    stripped = content.strip()
    if not stripped:
        return content
    lead = content[: len(content) - len(content.lstrip())]
    trail = content[len(content.rstrip()):]
    return f"{lead}{marker}{stripped}{marker}{trail}"


def render_span(match):
    content, style = match.group(1), match.group(2)
    size = font_size(style)
    if size >= 2.0:  # drop cap: just the letter
        return content
    marker = ""
    if "bold" in style and size <= 1.0:
        marker += "**"
    if "italic" in style:
        marker = "***" if marker else "*"
    return wrap(content, marker) if marker else content


def heading_of(par):
    """If the paragraph is a single big bold span, return its text."""
    m = SPAN.fullmatch(par)
    if not m:
        return None
    style = m.group(2)
    if "bold" in style and 1.0 < font_size(style) < 2.0:
        return join_lines(m.group(1)).replace(HARD_BREAK, " ").strip()
    return None


def render_paragraph(par):
    if re.match(r"-\s", par):  # bullet list: one line per item
        items = re.split(r"\n(?=-\s)", par)
        par = "\n".join("- " + join_lines(i[1:]).strip() for i in items)
    else:
        par = join_lines(par)
    # spans may be nested (e.g. a link inside a span): repeat until stable
    while True:
        new = SPAN.sub(render_span, par)
        if new == par:
            break
        par = new
    par = re.sub(r"\*\*\s*\*\*", " ", par)  # merge adjacent bold runs
    par = re.sub(r" {2,}", " ", par).strip()
    par = par.replace(HARD_BREAK, "\\\n")
    if par == r"\*\*\*":
        return "* * *"
    # pandoc's smart-punctuation escapes
    return par.replace("---", "—").replace("--", "–")


def slugify(text):
    slug = re.sub(r"[^\w\- ]", "", text.strip().lower())
    return re.sub(r"[\s\-]+", "-", slug).strip("-")


def parse(body):
    """Return (toc, blocks): toc is [(title, section)], blocks is
    [(section, kind, text)] with kind in {"heading", "image", "text"}."""
    body = DIV_FENCE.sub("", body)
    body = IMAGE_ATTRS.sub(r"\1", body)
    body = body.replace("](assets/", "](../assets/")

    toc, blocks = [], []
    section = None
    for par in re.split(r"\n\s*\n", body):
        par = par.strip("\n")
        if m := SECTION_ANCHOR.match(par.strip()):
            section = m.group(1)
            continue
        par = EMPTY_ANCHOR.sub("", par).strip()
        if not par or NBSP_ONLY.match(par):
            continue
        if par.startswith("#") and "Table of Contents" in par:
            continue
        if TOC_LINK.search(par):
            toc += [(join_lines(t).strip(), s) for t, s in TOC_LINK.findall(par)]
            continue
        if (text := heading_of(par)) is not None:
            blocks.append((section, "heading", text))
            continue
        text = render_paragraph(par)
        kind = "image" if IMAGE.fullmatch(text) else "text"
        blocks.append((section, kind, text))

    # quest notices print their rank ("F", "B", "Open"...) in heading style
    for i, (section, kind, text) in enumerate(blocks[:-1]):
        if kind == "heading" and blocks[i + 1][2].startswith("TASK:"):
            blocks[i] = (section, "text", f"**{text}**")
    return toc, blocks


def split_volume(src):
    """Return {filename: markdown} for one volume."""
    fm = FRONT_MATTER.match(src)
    yaml, body = (fm.group(0), src[fm.end():]) if fm else ("", src)
    title_m = re.search(r'^title:\s*"?(.*?)"?\s*$', yaml, re.M)
    title = title_m.group(1) if title_m else "Untitled"

    toc, blocks = parse(body)
    # section -> index of its table-of-contents entry
    entry_of = {section: i for i, (_, section) in enumerate(toc)}

    front, chapters = [], {}  # chapters: toc index -> list of blocks
    current = None  # toc index; None = before the first entry (cover)
    seen_images = set()
    for section, kind, text in blocks:
        if section in entry_of:
            current = entry_of[section]
        if kind == "image":
            path = IMAGE.fullmatch(text).group(1)
            if path in seen_images:  # cover is included twice
                continue
            seen_images.add(path)
        entry = toc[current][0] if current is not None else None
        if entry in DROPPED_ENTRIES:
            continue
        if entry is None or entry in FRONT_ENTRIES:
            front.append((kind, text))
        else:
            chapters.setdefault(current, []).append((kind, text))

    files = {}
    toc_lines = []
    for number, index in enumerate(sorted(chapters), start=1):
        entry = toc[index][0]
        name = f"{number:02d}_{slugify(entry)}.md"
        content = chapters[index]
        # the chapter's own heading is replaced by the table-of-contents title
        if content and content[0][0] == "heading":
            content = content[1:]
        lines = [f"# {entry}"] + [
            f"## {text}" if kind == "heading" else text for kind, text in content]
        files[name] = "\n\n".join(lines) + "\n"
        toc_lines.append(f"- [{entry}]({name})")

    front_lines = [f"# {title}"] + [
        f"## {text}" if kind == "heading" else text for kind, text in front]
    front_lines.insert(2, "## Table of Contents\n\n" + "\n".join(toc_lines))
    files["00_front-matter.md"] = yaml + "\n" + "\n\n".join(front_lines) + "\n"
    return files


def main():
    files = [Path(f) for f in sys.argv[1:]] or sorted(BOOKS_DIR.glob("*.md"))
    for f in files:
        number = VOLUME_NUMBER.search(f.stem)
        out_dir = f.parent / (f"volume_{number.group(1)}" if number else f.stem)
        if out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir()
        chapters = split_volume(f.read_text(encoding="utf-8"))
        for name, content in chapters.items():
            (out_dir / name).write_text(content, encoding="utf-8")
        print(f"{f.name} -> {out_dir.name}/ ({len(chapters)} files)")


if __name__ == "__main__":
    main()
