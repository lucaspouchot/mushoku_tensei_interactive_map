# Source data as YAML in git, translations keyed by English hash

Readers report defects through GitHub issues and pull requests, and the project has no backend. The data must therefore be something an outsider can find, edit and review as a diff. We store all source data as YAML files under `data/`: one file per Character and per Location, and Facts grouped by the chapter of their first Source Reference. Git is the database. A TypeScript data build turns these files into one read-only bundle set per locale, and that bundle is never committed.

Translations of texts live in separate per-locale files that mirror the source paths. Each entry is keyed by the **hash of the English text**, with a copy of the English for context, rather than by where the text sits in the source. A corrected English text then simply has no translation, and the build reports it as missing; the old entry becomes an orphan and is pruned. Proper names are the exception: they are keyed by slug because they carry editions and per-name choices.

## Considered Options

- **A database** (SQLite in the repo or a hosted one with an admin UI). Rejected: a binary file gives no reviewable diff, and a hosted database needs the backend the app deliberately does without.
- **JSON or TOML.** Rejected: JSON is painful to edit by hand and has no comments; TOML handles nested lists of Facts poorly.
- **Translations inline in the source files.** Rejected: files four times larger, Japanese in files English reviewers read, and machine regeneration mixed into the diffs of Fact corrections.
- **Translations keyed by location** (owner id + field path). Rejected: paths through lists break when a list is reordered, and staleness would need a separate hash comparison anyway.

## Consequences

- One canonical serializer writes every data file, so diffs only show real changes.
- Two identical English texts share one translation.
- Without CI, `just data-check` on the maintainer's machine is the merge gate. It is the only place the corpus (`books/`, not versioned) and git history are available. The Docker build re-checks everything else, strictly.
