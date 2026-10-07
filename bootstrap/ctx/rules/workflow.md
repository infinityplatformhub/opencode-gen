# Project workflow — authoritative OpenCode Gen policy

## Scope and precedence

This system manages tickets, research, and memory for this project only. Existing organization
and engineering instructions still apply. Do not install global rules, skills, or configuration.
`config.json` supplies preferences; this file supplies workflow; skills supply procedures.
When project instructions conflict, surface the concrete conflict before the affected action;
never silently override organization policy. Do not copy these rules into other documents.

## Ticket gate

No substantive investigation, research, implementation, or verification without a ticket.
Before starting, load `opencode-gen-ticket` if not already loaded, read the ticket ledger,
and resume matching work or create a ticket automatically. Do not ask permission merely to
track requested work. Reading workflow, config, and the ledger to establish a ticket is allowed.
Greetings and clarification-only replies are exempt. Record unsolicited discoveries as a
follow-up, not a silent expansion of scope. Init/update work uses a ticket too: initialization
may first create the minimal context directories needed to record its bootstrap ticket.

For private requests, use `local/tickets/` with `local/tickets/index.md`; do not put their titles,
IDs, paths, or summaries in the shared ledger. If visibility is ambiguous, clarify or start
privately. Shared storage is for information approved to be committed to this project.

Ticket states: `open`, `in-progress`, `blocked`, `done`. One line per ledger entry:
`- T-001 | in-progress | Short title`. The ticket is the only home for goal, acceptance criteria,
checkpoint (done/next/blocker), references, and verification. Update checkpoints at meaningful
boundaries or handoff, not every tool call. Read fresh state before editing; preserve concurrent
changes. Multiple sessions should use separate tickets or explicitly coordinate shared work.

Complete when acceptance criteria and applicable checks pass; record unverified items honestly.
Completion does not require a commit. `commit_mode=manual` requires explicit approval; `auto`
allows verified intended changes only if organization rules also permit it. Push always needs
explicit approval. Preserve unrelated work. Include a ticket ID in commit messages.

## Context and growth

Startup/recovery reads: index, workflow, then the selected ticket. Read config when changing
framework state. Search research/memory indexes by relevance; do not load whole archives.
Do not reread content still available and current in context. No runtime auto-import is implied.
Never expand AGENTS.md with progress, learned facts, skill lists, or generated stack policies.

Suggested hard check limits: root index 2 KiB; workflow 8 KiB; each ledger/index 8 KiB;
each ticket/research/memory document 12 KiB; managed AGENTS block 2 KiB.
The explicit checker reports violations; it never removes or truncates content.
Archive closed ledger entries into `tickets/archive/YYYY-MM.md` before removing them from
the current ledger. Ticket files remain addressable. Split long research/memory by topic,
retain short pointers, and remove duplicated prose. Do not mirror state into TODO, recent-changes,
active-tasks, or changelogs. Link existing external trackers rather than duplicating their backlog.

## Research and learned knowledge

Scratch/experiments belong in `local/tmp/`. Retain research only when it helps future work:
question, dated evidence/sources, findings, uncertainty, conclusion, and ticket reference.
Use `opencode-gen-research` for substantial research. Keep speculation labeled.
Use `opencode-gen-memory` when discovering a reusable verified fact, correcting stale knowledge,
or recalling project gotchas. Memory records scope, source, and last verification date.
Do not promote every task result to memory. Private material stays private on promotion.
Architecture/coding policy stays in existing project docs; reference it instead of copying it.

## Shared and local data

Everything under `.ctx/local/` is private to this project and ignored by Git: host/port/path
notes, temporary files, private tickets, confidential research, and local memory. Read only
specific files needed for the task. Ignore rules do not prevent reads or transmission to a model.
Store credential references in environment notes; if raw secrets must be stored locally, keep
them in a separate local/secrets/ directory and never automatically load it. Prefer using secret
stores or environment variables without printing values. Never copy private data into shared
files, commit messages, generated summaries, or another project's memory without explicit consent.

Before completion run `python3 .ctx/local/framework/scripts/check-context.py <project-root>`
and inspect intended tracked changes.
Report goal/outcome, verification, next step, and ticket ID in chat; do not generate report files.
