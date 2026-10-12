# AI work through agent skills, never API-key commands

Extraction of Facts from the novels and translation of the data are AI work. "LLM extraction with the Claude API" recommended batched Claude API requests with structured outputs. Instead, no command in this repo calls an AI API or needs a key. AI work runs as **agent skills** (open Agent Skills format, `.agents/skills/<name>/SKILL.md`, listed in `AGENTS.md`), launched from an agent session, so the provider can change without touching the tooling. `just` recipes keep the deterministic part: preparing context, writing worklists, formatting and validating.

## Considered Options

- **Batch API commands with a cached prefix and structured outputs.** Rejected: they tie the project to one provider and to an API key in the maintainer's environment, though they would have halved the cost and guaranteed the output format.

## Consequences

- Schema validation by `just data-check` replaces the structured-outputs guarantee: a skill corrects its output until validation passes.
- No discount from batch processing. Cost depends on the agent session used.
- Skills live outside `.claude/` (gitignored and provider-specific). A `just` recipe exposes them where a given agent looks for skills.
