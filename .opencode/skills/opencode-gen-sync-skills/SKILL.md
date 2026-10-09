---
name: opencode-gen-sync-skills
metadata:
  opencode/autoinvoke: false
description: Check pinned external skills for upstream updates and synchronize approved versions
---

# Sync curated skills

First load `opencode-gen-ticket` and establish a ticket. Resolve the library as in
opencode-gen-add-skill. Read `_registry.json` and `_index.json`.
In an installed project, copy the required registry/cache into `.ctx/local/skill-cache/`
before modifications. Never update a shared source checkout on behalf of one project's sync.
Only maintain the source library directly when the user explicitly requests source maintenance.
List active and cached IDs. Check each source repository's HEAD and compare to its pinned
SHA. Report available updates and ask which to accept. Offline: retain the cache and report.

For approved updates, fetch into a unique temporary directory and checkout the exact
selected commit. Inspect changes, validate SKILL.md and references, and update the registry's
source ref, fetched date, file lists, and file counts consistently for all affected skills.
Stage and validate the entire replacement before touching the existing cache. Back up old
cache and active copies. Compare active copies to the old cache; preserve customizations
and skill-visibility metadata rather than overwriting blindly. Copy full directories.

Suggest newly relevant skills based on the current stack; activate only selected ones.
Validate every active SKILL.md and its references. Report updated, unchanged, and failed
skills. Preserve upstream repository names and provenance; they are not framework branding.
