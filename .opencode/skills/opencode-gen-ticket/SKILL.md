---
name: opencode-gen-ticket
description: Required before substantive project work; create or resume a ticket, checkpoint progress, recover context, and close verified work
---

# Ticket procedure

The project's `.ctx/rules/workflow.md` is authoritative. Read it and `.ctx/index.md` before
work if not already current in context. Resolve the project from its managed root AGENTS.md;
do not create context in the current subdirectory or select another organization's project.

1. Establish visibility from the request and `.ctx/config.json`. For uncertain sensitive work,
   clarify or use private storage. Private tickets use `.ctx/local/tickets/`; shared tickets
   use `.ctx/tickets/`. Never put private identifiers or summaries in shared indexes.
2. Read only the chosen ledger and matching ticket. Resume the session's ticket when its goal
   matches; otherwise create one automatically BEFORE investigation/research/edits/checks.
   Creating tracking records and reading bootstrap policy are the pre-ticket exceptions.
3. For a new ID, use `<ticket_prefix><UTC timestamp>-<8 random hex characters>` (for example
   `T-20261007T120000-a1b2c3d4`) and exclusive file creation; retry on collision. Existing IDs
   remain valid. Use the installed ticket template. Set goal and checkable acceptance criteria.
   Append a one-line ledger entry after re-reading it; never overwrite concurrent entries.
4. Mark in-progress and work. The current session carries its ticket ID; there is no singleton
   project-wide active-task file. Record checkpoints on phase changes, blockers, or handoff.
   If another session owns the same ticket, coordinate or open a separate related ticket.
5. Load research/memory skills only for relevant work. Reference results instead of copying
   them between files. Resume after compaction by reading this workflow and the selected ticket.
6. Verify acceptance criteria, record actual checks and unresolved items, and close only when
   complete. Completion and commit approval are separate. Update one ledger row and archive
   old closed rows if the ledger exceeds its budget. Run the context checker before completion.

The mandatory gate is an agent instruction, not a tool interceptor. Do not claim that the
runtime blocks unticketed tools. If the ticket skill cannot load, read this procedure from its
project file; if neither procedure nor ticket storage is accessible, report the blocker instead
of proceeding with substantive work.
