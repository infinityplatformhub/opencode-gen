# OpenCode Gen

Prompt framework specifically for OpenCode v2. This is a framework repository, not an app.

- Speak Thai with the user; write code, comments, and documentation in English.
- Preserve custom project instructions, configuration, and task history during installation.
- Framework command, skill, agent, and plugin IDs use `opencode-gen-*`.
- Never hand-edit `skills-library/_cache/`; preserve upstream provenance and pinned SHAs.
- Community skill IDs and upstream repository names are not framework branding.
- Consult https://opencode.ai/v2/docs/ before changing OpenCode interfaces.
- Use a bounded AGENTS.md entrypoint and project-local commands/skills. Sidebar plugins must not inject context; no custom agents.
- Never put the cached library inside an auto-discovered skills directory.
- Official origin: git@github.com:infinityplatformhub/opencode-gen.git, branch master.
- Do not commit or push without the user's explicit approval.
- Keep reports in chat and update relevant existing documentation.

## Layout

- `.opencode/commands/`, `skills/`: native framework entrypoints.
- `bootstrap/ctx/`: authoritative project workflow and data scaffolding.
- `bootstrap/AGENTS.md.tmpl`: bounded native entrypoint; ticket/research/memory never live here.
- `bootstrap/rules/`: optional legacy engineering references, not deployed or auto-loaded.
- `skills-library/`: curated skills, stack profiles, and pinned registry.
- `scripts/`: installer, explicit context checker, validation, and skill maintenance.
- `docs/`: current usage guides; changelogs retain pre-migration history.

## Verification

Run `python3 scripts/validate.py` and `python3 -B -m unittest discover -s tests` after
installer, workflow, profile, or script changes. Validate shell syntax with `sh -n`.
Verify location-scoped discovery separately from model adherence to the ticket gate.
