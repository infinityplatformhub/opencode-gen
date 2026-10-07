---
name: opencode-gen-init
description: Initialize or repair project-local ticket control, context, and private/shared storage
---

# Initialize project context

Keep all operations scoped to the selected project. The local installer creates the minimal
context structure, managed AGENTS block, and bootstrap ticket before substantive setup work.
If missing, run the framework checkout's `install.sh <project>` first. Do not initialize the
framework checkout into itself. Resolve assets in `.ctx/local/framework/`, never global config.

Load `opencode-gen-ticket` and resume the bootstrap ticket reported by the installer (check
the private ledger only if its selected visibility was private). Read workflow and config. Ask only
for unresolved conversation language, ticket prefix, visibility policy, and commit preference;
preserve existing choices. Never weaken organization instructions. Manual commits are default.

Check existing AGENTS.md and task systems. Merge only the bounded managed entry block, not
project instructions. Do not generate engineering rules, architecture skills, MCP integrations,
or stack-specific coding skills automatically. Link existing tracker/docs if useful.

For previous installations, inspect old .ctx files and .opencode assets before migration.
Preserve user information. Move task checkpoints into tickets, verified shared knowledge into
memory, and machine/private notes into local/. Keep backups; do not bulk-delete old directories.
Remove a former framework plugin/agent/rule only after establishing ownership and completing
migration. Do not delete custom files merely because they share an old directory.

Verify the local ignore rule and detect already tracked private files. Report any such files;
do not automatically untrack or rewrite Git history. Run the context checker. Verify commands
and skills through a location-scoped OpenCode runtime query. Report unresolved runtime testing
separately. Complete the bootstrap ticket with verification and next steps.
