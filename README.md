# OpenCode Gen

**Project-local ticket control for OpenCode v2.** Track work, retain useful research, and
remember verified facts without turning AGENTS.md into a journal or imposing coding conventions.
No global installation or custom agent. A project-local sidebar plugin displays ticket progress;
it does not inject model context. Model/provider settings are inherited.

## Install

Requires Python 3, curl, tar, and OpenCode v2. Run in the project you want to install into:

```sh
curl -fsSL https://raw.githubusercontent.com/infinityplatformhub/opencode-gen/master/install.sh | sh
```

The installer seeds `.ctx/`, creates a bootstrap ticket, adds a bounded managed section to
AGENTS.md, and installs project commands/skills. Existing organization instructions and config
are preserved. Customized managed files cause a conflict instead of silent replacement.
Run `/opencode-gen-init` in the target to confirm preferences and verify the bootstrap ticket.

To select another project, append `sh -s -- /path/to/project` instead of `sh`.
No clone or GitHub login is needed; the installer downloads and cleans up the official archive.
From an existing checkout, `sh install.sh /path/to/project` also works.
Run `sh install.sh --help` for installer usage. Use `/opencode-gen-update` to update from
the official master branch while preserving project data and local source changes.

## Mandatory ticket workflow

AGENTS.md instructs the agent to load `opencode-gen-ticket` before substantive work, resume
a matching ticket or create one automatically, then proceed. No manual skill invocation is
required for the policy. Greetings and clarification-only replies are exempt; policy/ledger
reads needed to establish a ticket are allowed. Research and memory skills load only as needed.

**This is an instruction-level gate, not runtime tool blocking.** Native skill discovery is
not automatic execution. Verify model adherence in a fresh session; never infer it from discovery.

## Project layout

```text
AGENTS.md                 bounded entrypoint; existing org instructions remain
.opencode/commands/       project slash commands
.opencode/skills/         project workflow skills
.opencode/plugins/        ticket sidebar (OpenCode v2.0.24)
.ctx/config.json          project preferences
.ctx/index.md             compact context map
.ctx/rules/workflow.md    authoritative workflow policy
.ctx/tickets/             ledger + goal/checkpoint/verification per ticket
.ctx/research/            retained evidence and conclusions
.ctx/memory/              verified reusable shared knowledge
.ctx/local/               ignored private data, local tickets, scratch, backups, assets
```

OpenCode natively loads AGENTS.md and discovers project skills/commands. `.ctx/` has no native
auto-import: the agent explicitly reads the entrypoint and relevant files. Do not use @imports
or the inactive V2 `instructions` config field. Rules and data are scoped to this project.

## Skills and commands

| ID (also a slash command) | Activation |
|---|---|
| `opencode-gen-ticket` | Required before substantive work; resume/create/checkpoint/close |
| `opencode-gen-research` | Substantial investigation; ticket first |
| `opencode-gen-memory` | Recall, verify, correct, or retain reusable knowledge; ticket first |
| `opencode-gen-init` | Explicit setup/repair; bootstrap ticket |
| `opencode-gen-update` | Explicit framework update; ticket first |
| `opencode-gen-add-skill` | Optional coding skill activation; ticket first |
| `opencode-gen-sync-skills` | Optional upstream sync; ticket first |

Init detects existing stacks or asks for planned stacks in empty projects, including custom and
undecided choices. It selectively installs skills matching confirmed components from the 19-skill,
12-profile library. Relevant skills are invoked lazily as tasks require them; full bodies are never
preloaded. No complete library copy per project. Upstream provenance and pinned SHAs are retained.

## Private data and bounded context

Shared tickets/research/memory are tracked. `.ctx/local/` is ignored and never preloaded.
Private ticket titles, findings, and memory stay in local indexes. Local hosts, private endpoints,
scratch and confidential notes belong there. Raw secrets, if needed, remain separate from narrative
memory; prefer credential references. Gitignore does not prevent agent reads or provider transmission.

Only the managed AGENTS block has a 2 KiB framework cap; existing organization guidance is untouched.
Index/ledger budgets and topic splitting keep startup context small. No duplicated TODO/active-tasks/
recent-changes system. Check without mutating or truncating data:

```sh
python3 .ctx/local/framework/scripts/check-context.py /path/to/project
```

## Development checks

```sh
python3 scripts/validate.py
python3 -B -m unittest discover -s tests
node --test tests/sidebar.test.mjs
```

See [getting started](docs/getting-started.md), [scope and deployment](docs/deployment-guide.md),
[skills](docs/skills-guide.md), [migration](docs/migration-flow.md), and [changelog](CHANGELOG.md).

## Ticket sidebar

Title and Context stay native at the top; the plugin appends a focus card: Current activity,
muted Checkpoint, and Blocked only when needed. No green partial-progress Done or Next section.
Short new ticket IDs are secondary to the readable title. Existing IDs remain valid.
The native footer already shows path:branch, so it is not duplicated.
After creating/resuming a ticket, the agent calls `opencode_gen_select_ticket` with its ID and
visibility. Selection lives in ignored `.ctx/local/sessions/<sessionID>.json`; each session has
its own selection. Only that ticket is read. No automatic private-ticket scan or model requests.
The mounted card refreshes every five seconds. Toggle the sidebar with the configured OpenCode
sidebar shortcut (default leader then b). Start from the project root for ticket selection.
