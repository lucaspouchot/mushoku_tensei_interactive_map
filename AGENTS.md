# Agents

## Agent skills

### Issue tracker

Issues and specs live as local markdown files under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default canonical labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`), recorded as `Status:` lines in issue files. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Language policy

Everything written or modified inside the project MUST be in English, including code, identifiers, comments, documentation, tests, logs, configuration, and generated project content.

For user-facing communication, use the language specified in `.agent-lang`. Read only this file for the language preference.

Keep standard software engineering terminology in English when it is commonly used as such by developers. Do not force localized translations of terms such as `commit`, `branch`, `pull request`, `endpoint`, `middleware`, `runtime`, `build`, or `deploy`.

The user's language applies only to conversation. Project content MUST always remain in English.