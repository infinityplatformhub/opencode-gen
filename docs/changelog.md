# Changelog

For the OpenCode v2 conversion, see [the current changelog](../CHANGELOG.md).
Entries below are retained historical records of the pre-migration framework.

## v3.3 — 2026-07-26

- **`.claude/rules/` was never loaded.** `CLAUDE.md.tmpl` said "(auto-loaded)" and
  `dev-workflow.md` said "Auto-loaded every session", but nothing imported them — init copied
  the files and stopped. The rules the framework depended on never reached context. Fixed by
  importing the two that apply to every action (`task-tracking.md` + each stack rule) and
  labelling the rest honestly as read-on-demand (`dev-workflow.md`, `project-reference.md`).
  Cost of making it real: ~2.7k–4.4k tokens per session depending on profile.
- **`dev-workflow.md` shipped four stacks' worth of guidance to every project** — route greps
  for Gin/Express/Laravel/FastAPI, component scans for Vue and React, Playwright conventions,
  a DB migration checklist. Each moved into its own stack rule; `migration-database` owns the
  DB checklist. 9,046 → 6,827 B. `Start of Session` deleted (it duplicated CLAUDE.md's Token
  Discipline — two homes for one rule is a contradiction waiting to happen).
- **`ctx-budget.sh` now also runs on SessionStart.** PostToolUse only fires when a file is
  written, so a file that bloated before the hook existed was never caught. The sweep reports
  total bytes every session — the number nobody was looking at. Budgets extended to `CLAUDE.md`
  (10 KB) and `.claude/rules/*.md` (8 KB each), one table serving both events.
- **Credential guard.** `NOTES.md` and `.ctx/learned.md` are git-tracked and pushed, so the
  hook blocks a write that introduces a vendor-prefixed key, a PEM block, or an assignment with
  a real-looking secret value. Bare env var names do not trigger it. `.ctx/local.md` is exempt —
  gitignored, and the designated home for machine-specific values.
- **`## Where Things Go` replaces "never generate throwaway files".** A prohibition with no
  destination gets worked around; one project accumulated 27 files in `tmp/` while replies to
  other teams leaked into `docs/` and left dangling pointers in its CHANGELOG. Now there are
  four homes with a one-sentence test each, plus `NOTES.md` — a tagged, greppable, never-imported
  store, so keeping a note costs nothing until someone searches for it. Task-bound research
  lives in `tmp/T-xxx-topic.md` and must be disposed of when the task closes.
- **`NOTES.md` does have a budget after all — 16 KB, and it archives instead of trimming.**
  "Not imported" was mistaken for "free": a single full Read charges every byte at once, and
  "grep, don't read it whole" is a habit, which is the failure mode this release exists to
  remove. So the cap bounds the accident, and over budget the OLDEST blocks move to
  `notes/YYYY-MM.md` — the one budget in the framework that relocates rather than deletes,
  because keeping a note has to stay free or the store stops being used. `notes/` is
  git-tracked; it is the archive, not scratch.
- **`NOTES.md` is an index, not a container.** A note over ~3 lines becomes its own file with a
  one-line pointer left behind — otherwise one long write-up crowds out the notes that make the
  index worth grepping. The `docs/` row had been narrowed to "explains how a subsystem works",
  which silently excluded research records; `docs/` now explicitly holds research that changes a
  future decision and is still true after its task ends. Two kinds of file, two naming rules:
  archive buckets get no topic in the name (`notes/YYYY-MM.md` — they hold unrelated notes, so a
  title would be a lie), research records get a topic and a date. Four-digit year, because
  `26-7` sorts after `26-11`.
- **Consistency audit across every template** — the additions above were checked against
  everything already shipping, and eleven conflicts turned up, most of them older than this
  release:
  - `TODO.md.tmpl` listed `{{TASK_PREFIX}}901` in two sections while `task-tracking.md` says a
    task ID appears in exactly one. The shipped template broke the framework's own rule.
  - `task-tracking.md` claimed `TODO.md` "is loaded into every future session". It is not
    imported — `CLAUDE.md` and the hook both say so. Now stated as: re-read whole after a compact.
  - The "Done" definition required user confirmation, which auto commit mode never asks for,
    so no task could be Done in that mode. Now mode-aware.
  - `learned.md` routed file-specific gotchas to "path-scoped `.claude/rules/`" — a loading
    mechanism that does not exist. They go to `NOTES.md`.
  - `dev-workflow.md` listed `notes.md` as a bad filename while the framework now ships
    `NOTES.md`, and sent debug scripts to `debug-scripts/` — a second, un-gitignored home for
    throwaways. Both now point at `tmp/`.
  - `docs/NN-*.md` imposed a numbering convention most projects do not use → plain `docs/`.
  - `PM Task Autonomy` pointed at a "Commit Discipline" section that does not exist; the real
    name is Commit Policy. Committing and pushing were also specified twice, in two places.
  - `docs/changelog.md` was hardcoded as the one home for task prose but nothing created it, and
    a project with a root `CHANGELOG.md` would end up with two. It is now `{{CHANGELOG}}`, filled
    from detection: an existing changelog always wins, whatever it is called.
  - `task-tracking.md` reached 8,408 B — over the 8 KB budget it defines for itself. Trimmed to
    7,697 B by deleting a Branch Naming section already covered one page earlier and a Bug Fix
    flow that `dev-workflow.md` covers in more detail.
- **`/claude-gen-update` no longer overwrites framework rules with `cp`.** That would have
  destroyed project-authored content (one project had invented an evidence-tag policy the
  framework lacked). It now diffs and classifies every difference as FRAMEWORK / ENFORCED
  NUMBER / PROJECT before writing, and backs up `.ctx/`, `CLAUDE.md` and `TODO.md`, which
  later steps rewrite. The report block claimed "Not touched: .ctx/" while Step 4c compressed
  it — corrected.

## v3.2 — 2026-07-22

- **`report-guard` hook REMOVED** — the Stop hook blocked ending a work turn until the reply
  carried a `→ next step` line. In real use it interrupted the flow (it fires on any turn
  with ≥2 tool calls, including trivial ones), so it is gone: script deleted, `Stop` wiring
  dropped from `settings.json.tmpl`, and the `{REPORT_GUARD}` question removed from init
  Phase 0. Status reports remain a **CLAUDE.md guideline** (what happened / what was done /
  what's next) — the `→ ` marker rule is dropped too. `/claude-gen-update` Step 4d now
  *removes* the hook from existing projects automatically (no prompt); it only touches the
  `Stop` block that references `report-guard.sh`, never the user's own Stop hooks.
- **New: optional `codebase-memory` code knowledge graph** — init Phase 0 question 4 offers
  it with a plain-language explanation (indexes the repo into a tree-sitter graph served
  over MCP; answers "who calls this / what breaks / show the architecture" from the graph
  instead of grepping; native binary, no LLM or API key; ~258 MB + a per-repo index).
  Three choices: `no` / `global` (MCP + skill + hooks in `~/.claude`, every project, also
  configures other detected agents) / `project` (binary + index + project-scoped MCP only).
  `/claude-gen-update` Step 4e asks the same question **only when it is not already
  installed**; if it is, the repo index is just refreshed. Install failure never aborts
  init/update — it is optional by design.

## v3.1 — 2026-07-03

- **Opt-in `contract-first-api` skill** — API as single source of truth: OpenAPI generated
  from code, one markdown handbook served everywhere, `/llms.txt` agent on-ramp, generated
  client types, docs↔guard drift test. Offered at init/update when a backend is detected;
  not auto-loaded by any profile. (19 skills total: 13 external + 6 local)
- **`report-guard` status-report hook is now opt-in** — new `{REPORT_GUARD}` preference at
  init (Phase 0); `/claude-gen-update` Step 4d toggles it on/off for existing projects.
  Status reports stay a CLAUDE.md guideline when the hook is off.
- **init** — Phase 2 adds a backend-conditional Contract-First API question; update Step 8b
  offers it to existing backend projects (install-only or build-now, with a review-supervised
  sub-agent fan-out option).

## v1.0 — 2026-03-22

Initial release.

- Hybrid registry + cache architecture for skills (pinned SHA, offline-ready)
- 18 curated skills (13 external + 5 local), 12 stack profiles, 7 stack rules
- Plugin install: `/plugin install infinityplatformhub/claude-gen` (all platforms)
- CLI installer: `curl | sh` with auto-backup (Mac/Linux/WSL)
- 9-phase auto-init agent with stack detection
- Task tracking, commit discipline, PM autonomy, pre-commit checklist
- Roadmap & Ideas sections in TODO.md for deferred work
- File naming conventions, TODO archiving, no-unsolicited-docs rules
- Progress display during /claude-gen-init with /exit recommendation
- `.claude/skills/_library/` gitignored (re-downloaded on install)
- Commands: /claude-gen-init, /claude-gen-update, /claude-gen-add-skill, /claude-gen-sync-skills
