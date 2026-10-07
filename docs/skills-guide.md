# Skills

`opencode-gen-ticket` is required before substantive work by the project's AGENTS entrypoint.
The model loads it through the skill tool, resumes/creates a ticket, and follows the single policy
in `.ctx/rules/workflow.md`. Avoid repeated loading when instructions are already current.

`opencode-gen-research` handles substantial investigations. `opencode-gen-memory` handles relevant
recall and reusable verified facts. Both first establish a ticket and preserve data visibility.
Init/update/add-skill/sync-skills are explicit management workflows with the same ticket gate.

Skills hold procedures, not project facts. Facts and task state live in `.ctx/`. OpenCode discovers
`.opencode/skills/<id>/SKILL.md`; description advertises applicability, not guaranteed execution.
Do not disable automatic suggestions for the mandatory ticket skill.

Coding expertise is optional: `/opencode-gen-add-skill <id>` activates a complete selected directory
from the source checkout. Source location is `.ctx/local/framework/source.json`; the full cache is
not copied into each project. `/opencode-gen-sync-skills` updates approved pinned versions. Preserve
upstream IDs, attribution, references, and locally customized active copies.
