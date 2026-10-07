---
name: opencode-gen-add-skill
description: List or activate selected skills from the OpenCode Gen curated library
---

# Activate a skill

First load `opencode-gen-ticket` and establish a ticket. Coding skills are opt-in, not default.
Library: `skills-library/` in the checkout recorded by `.ctx/local/framework/source.json`.
If unavailable, ask for the source path; do not guess a remote. Read `_index.json` before
resolving any requested name. Cache missing downloads privately under `.ctx/local/`.

- No name: list relevant inactive skills with descriptions and installed status.
- Validate the exact skill ID against the index; never use arbitrary user input as a path.
- Existing `.opencode/skills/<id>`: compare and preserve customizations; do not overwrite silently.
- Copy the entire local `<id>/` or external `_cache/<id>/` directory, including references.
- If missing, resolve repository, source path, and pinned SHA from `_registry.json`;
  fetch into a unique temporary directory, checkout that exact SHA, and validate all listed
  files and file_count before activating. Network failure leaves the existing copy intact.
- Apply any explicitly requested skill-visibility preference only to the active copy; never
  hide the mandatory ticket skill. Do not add a routing table to AGENTS.md. Report the activated ID.

Do not register the entire library as a skills source. Community IDs such as golang-pro
remain unchanged; framework management skills use the `opencode-gen-*` namespace.
