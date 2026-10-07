# Migration to project ticket control

1. Inspect existing instructions, tasks, notes, custom skills, and organization policy.
2. Establish a bootstrap ticket; create minimum tracking scaffolding first if needed.
3. Install project-only commands/skills and a bounded AGENTS entrypoint.
4. Move task state into tickets, durable evidence into research, verified facts into memory,
   and local/confidential content into `.ctx/local/`. Preserve visibility and historical IDs.
5. Replace duplicated workflow instructions with a reference to `.ctx/rules/workflow.md`.
6. Remove legacy framework plugin/agent/rules only when ownership and migrated data are verified.
   Preserve custom files and originals/backups until cleanup is approved.
7. Verify discovery, gate adherence, private Git exclusion, nested-root resolution, and other-project isolation.

Former active-tasks/recent-changes/TODO/changelog mirrors are not new data stores in this design.
Existing product changelogs and external trackers retain their independent purpose. Legacy bootstrap
engineering templates are source references only, never deployed by the current installer.

The Pencil diagram in `docs/pencil/architecture-overview.pen` depicts the previous architecture;
use README.md's project layout for the current ticket workspace.
