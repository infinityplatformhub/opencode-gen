# Preference audit against the original framework

Baseline: claude-gen/.claude/agents/project-init-agent.md Phase 0 and bootstrap/CLAUDE.md.tmpl.

| Original behavior | Current contract |
|---|---|
| English / Thai / Other choice | Explicit Thai / English / Other-Custom; no English recommendation |
| Immediate language lock | All questions/progress/reports switch after answer |
| Files/code/commits in English | Preserved |
| Preferences before discovery | Restored; only bootstrap/config reads precede questions |
| Manual / auto commits | Confirm defaults, persist choice; push separately approved |
| Plan once, concise phase updates | Restored |
| Final what/why, changes, next step | Preserved, with actual verification |
| Auto-skill toggle | Superseded by requested mandatory ticket gate; other skills task-triggered |
| Global/project codebase-memory | Removed from default per project-only scope; not silently installed |
| Stack detection including empty/multi-stack projects | Detect evidence or ask planned/custom/undecided stack; selective skill installation restored |
| Skill activation | Matching skills installed after confirmation; lazy task-based invocation, never full-library injection |
| Automatic coding rules | Legacy rule files not imposed; organization conventions preserved |
| Task/context mirrors and imports | Replaced by scoped tickets and explicit context reads |

Missing persisted language and treating seeded defaults as confirmed choices were regressions,
not intentional migration changes. Existing installations must merge missing config fields and
confirm unresolved preferences; never discard user choices. Prompt contract checks are not proof
that every model will render the question correctly; verify first-run and resumed sessions live.

Acceptance: select Thai, then verify the next question, phase updates, table explanations,
verification summary, and final next step are Thai. Reopen the session and verify the persisted
choice. Repeat with English and a custom language. Verify empty/planned, detected multi-stack,
ambiguous, and undecided projects separately. Registry discovery alone does not pass these cases.
