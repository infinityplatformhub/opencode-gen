# Getting started

Run this from the target project, then `/opencode-gen-init` in its OpenCode workspace:

```sh
curl -fsSL https://raw.githubusercontent.com/infinityplatformhub/opencode-gen/master/install.sh | sh
```

Installation is project-only and requires Python 3, curl, and tar. No checkout or GitHub login
is needed. To specify a target, use `| sh -s -- /path/to/project`. The bootstrap ticket
remains open until setup is actually verified.

Confirm ticket prefix, shared/private default, conversation language, and commit mode. Existing
project instructions win over generated preferences when stricter. The entrypoint reads `.ctx/`
explicitly; it does not automatically import arbitrary files.

For ordinary work, describe the task normally. The required ticket skill resumes or creates a
ticket before investigation or implementation. Use `/opencode-gen-ticket` to explicitly resume,
checkpoint, or close work. Research and memory are task-triggered, never preloaded wholesale.

Verify in a fresh session that the agent reads the workflow, creates/resumes a ticket before
substantive tools, and avoids private files unless needed. Test another unrelated project to
ensure it has no framework commands/skills. Nested workspaces must resolve `.ctx/` from the
project's managed AGENTS.md, not create context beneath the current working directory.
