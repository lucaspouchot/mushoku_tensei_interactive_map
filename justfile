set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# Clean every books/*.md (epub conversion) into books/volume_<N>/, one file per chapter
clean:
    python tools/clean_md.py
