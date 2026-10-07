---
name: opencode-gen-update
description: Update project-local OpenCode Gen assets without replacing tickets, memory, or organization rules
---

# Update

Load `opencode-gen-ticket` and establish an update ticket before substantive work.
Use the supplied checkout path or `.ctx/local/framework/source.json`. Official origin is
`git@github.com:infinityplatformhub/opencode-gen.git`, branch `master` (HTTPS also works).
For a local checkout, inspect its origin and working tree first. Fetch master and fast-forward
only when clean and tracking the official source; never reset or overwrite local changes.
If no persistent checkout is available, run the official one-line installer with the project
path: `curl -fsSL https://raw.githubusercontent.com/infinityplatformhub/opencode-gen/master/install.sh | sh -s -- <project>`.
Quote the actual project path. Check curl/download failures and do not report success without
installer output. No user-managed clone or SSH authentication is needed for this route.
Never pull the target project's origin. For a persistent checkout run `sh <source>/install.sh <project>`.
When using a temporary checkout, clear the recorded local source path after installation and
retain origin/branch so the next update can clone again. Remove only the temporary clone created
by this operation. On network or authentication failure, preserve installed state and report.
The installer preserves data and preferences, backs up managed assets, and refuses conflicts
with customized managed files. Resolve reported conflicts by comparing backup/source/current
versions, preserving organization policy and custom content. Never force broad replacement.

The installer opens a bootstrap verification ticket; link it from the current update ticket
and close both after verification rather than leaving a duplicate open task.
Read the updated workflow and run `python3 .ctx/local/framework/scripts/check-context.py .`. Verify
discovery with the explicit project location. Update the ticket checkpoint and report changes,
backup path, and remaining checks. No global writes or implicit commits.
