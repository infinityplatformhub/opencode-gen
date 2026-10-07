---
name: opencode-gen-init
description: Initialize or repair project-local ticket control, context, and private/shared storage
---

# Initialize project context

Keep all operations scoped to the selected project. The local installer creates the minimal
context structure, managed AGENTS block, and bootstrap ticket before substantive setup work.
If missing, run the framework checkout's `install.sh <project>` first. Do not initialize the
framework checkout into itself. Resolve assets in `.ctx/local/framework/`, never global config.

## Phase 0 — Preferences before discovery

Read only existing config/workflow needed to recover preferences first. Installer-seeded defaults
are NOT confirmed user choices. On first setup (`preferences_confirmed` absent/false), confirm
language, commit mode, ticket prefix, and shared/private default together using the question tool.
On repeat setup preserve confirmed values and ask only for missing values or requested changes.

Language question: `Language for our conversations? / ภาษาที่ใช้สนทนา?`
Always present these explicit options, in this order:
- `Thai (ภาษาไทย)` — `Use Thai for conversations, questions, progress, and reports. Save th.`
- `English` — `Use English for conversations, questions, progress, and reports. Save en.`
- `Other / Custom` — `Specify another language. / ระบุภาษาอื่น`
The tool's built-in free-text answer is also accepted. If Other/Custom is chosen without a
language, ask which language before continuing. Do not replace Thai with No preference, omit
an option based on current config, or recommend English automatically. Null/empty/No preference
does not complete language setup. Store the actual custom language, not the string "custom".
Migrate an existing explicit `language` value into `conversation_language` if unambiguous;
never overwrite a valid existing choice. Missing fields must be merged, not replace the config.

Commit options: `Manual` (default; ask and wait) and `Auto` (commit verified work only).
Explain that push always requires separate approval. Confirm the seeded prefix and visibility;
do not describe them as user-selected just because the installer wrote them.

Immediately after the language answer, switch EVERY user-facing message to that language:
follow-up questions, option descriptions, plans, progress, confirmations, and final report.
Only code, comments, identifiers, commits, and document contents remain English. Persist choices
in `.ctx/config.json` and set `preferences_confirmed: true` only after the answers are complete.
This lock applies on subsequent sessions and after compaction via the AGENTS entrypoint.
If a confirmed language already exists, use it from the first message; do not ask it again.
Before every user-facing output, check the saved language. For `th`, headings, explanatory
tables, question descriptions, verification summaries, and next-step prose MUST be Thai.
For example use `ผลการตรวจสอบ` and `ขั้นตอนถัดไป`, not an English report headed Verification
and Next step. English filenames/commands/IDs remain unchanged; file-content language does
not authorize English chat. A short Thai greeting followed by an English report still fails.

## Phase 1 — Resume setup and discover

Load `opencode-gen-ticket` and resume the bootstrap ticket reported by the installer (check
the private ledger only if its selected visibility was private). Never weaken organization
instructions. Discover existing task/docs conventions before asking redundant questions.
Display the setup plan once in the chosen language, then concise phase updates rather than
repeating the plan. Do not install MCP integrations as part of preferences.

### Stack discovery — existing, empty, and undecided projects

Read README, package/dependency manifests, build scripts, and relevant directory names to
discover ALL components, including monorepos. Do not infer dependencies from directory names
alone or treat absent source code as an error. Do not read secrets to discover the stack.

- Existing clear stack: show detected components with file evidence, offer correction, and
  reuse confirmed settings. Do not ask the user to re-enter information the files establish.
- Empty project: explicitly ask what they plan to build and which stack they intend to use.
  Offer backend/frontend/full-stack/library-or-CLI/docs-or-other and a custom answer; then ask
  language/framework only for the selected components. ALWAYS offer `Not decided yet`.
- Ambiguous/mixed project: show what is known and ask only about missing/conflicting components.
  Accept multiple backends/frontends; do not force a single profile.
- Undecided: persist `stack.status=undecided`; finish ticket/context setup without inventing a
  framework, creating application scaffolding, or activating unrelated coding skills. Offer
  a stack-selection research ticket only when the user wants help deciding.
- Known but unsupported: persist the actual stack as custom components. Missing a profile
  does not block init and must not be replaced with a similar but incorrect framework.

Store `stack` in config as `{status, components, profiles}`. Status is `detected`, `planned`,
`custom`, or `undecided`; components are concise strings from evidence or explicit choices;
profiles are actual matching IDs from `_index.json`. Keep organization-specific detail in
existing project docs, not AGENTS.md. Revisit an undecided stack when manifests arrive or the
user chooses it; merge new matches without silently removing customized skills.

### Selective skill activation and automatic use

Auto-use of relevant skills defaults to true (`skills.auto`); preserve an explicit previous
choice. The ticket gate remains mandatory regardless of coding-skill auto-use preferences.
Resolve the library from the recorded checkout or official archive using the add-skill procedure.
Read only `_index.json`/registry metadata first, not every SKILL.md. Union/deduplicate matched
profiles, then FILTER candidates against confirmed components: React is not evidence for Next.js,
PHP is not evidence for Laravel, and a JavaScript project need not use TypeScript or Vitest.
Include Docker and database migration skills only when those capabilities exist or are planned.
Universal debugging/git/security skills may be made discoverable without loading their bodies.
Offer contract-first-api only for a confirmed/planned backend API and activate it only on opt-in.

Once the stack is confirmed, automatically copy only matching complete skill directories into
`.opencode/skills/<id>/` (including references); do not require separate add-skill commands.
Preserve customized active copies and report conflicts or missing cache/network access honestly.
Record only actually installed coding IDs in `skills.installed`; do not list skipped skills as ready.
Validate selected frontmatter/reference availability without dumping all contents into context.
For a custom stack with no matching skill, report the gap; do not generate unverified expertise.

Installation/discovery is NOT invocation. OpenCode advertises descriptions; the agent invokes
only the skill(s) whose description fits the CURRENT task, before doing that specialized work.
Never eagerly call every installed skill during init/startup. Do not concatenate skill bodies,
reference files, profile rules, or routing tables into AGENTS.md, workflow, or model instructions.
Lazy automatic use follows `skills.auto`; false means explicit coding-skill requests only.

Check existing AGENTS.md and task systems. Merge only the bounded managed entry block, not
project instructions. Do not generate engineering rules, architecture skills, or MCP integrations
automatically. Activate existing matched coding skills as above; do not invent new skills or
impose the legacy profile's rule files. Link existing tracker/docs if useful.

For previous installations, inspect old .ctx files and .opencode assets before migration.
Preserve user information. Move task checkpoints into tickets, verified shared knowledge into
memory, and machine/private notes into local/. Keep backups; do not bulk-delete old directories.
Remove a former framework plugin/agent/rule only after establishing ownership and completing
migration. Do not delete custom files merely because they share an old directory.

Verify the local ignore rule and detect already tracked private files. Report any such files;
do not automatically untrack or rewrite Git history. Run the context checker. Verify commands
and skills through a location-scoped OpenCode runtime query. Report unresolved runtime testing
separately. Complete the bootstrap ticket with verification and next steps.
Discovery of commands/skills proves registry loading ONLY. Never claim all runtime checks
passed from that result. Confirm saved preferences by re-reading config; distinguish language
adherence, stack selection, ticket execution, sidebar rendering, and recovery tests explicitly.
If a behavior was not exercised, mark it untested instead of claiming initialization fully verified.
The final report must use the saved conversation language and state what/why, changes,
actual verification, and the next step. Include ticket title with its ID on first mention.
