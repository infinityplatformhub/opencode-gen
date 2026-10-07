---
name: opencode-gen-memory
description: Recall, verify, update, or retire reusable project knowledge while separating shared facts from local confidential memory
---

# Memory procedure

Establish or resume a ticket first. Follow `.ctx/rules/workflow.md`. Search the relevant index
and topic; read only the facts needed for the task. Shared knowledge lives in `.ctx/memory/`;
local knowledge in `.ctx/local/memory/` or `.ctx/local/environment.md`. Never preload local files.

For a reusable fact, record scope, concise fact, source/ticket, and last verification date.
Mark uncertainty explicitly; unverified hypotheses normally remain research, not learned rules.
Correct or retire stale facts, preserving useful provenance rather than appending contradictions.
Keep one topic document and a short index link. Split at 12 KiB; do not duplicate architecture
documentation or grow AGENTS.md. Do not promote every task outcome into memory.

Hostnames, private endpoints, local paths, confidential findings, and credential references
remain local. Raw secrets, if required, live separately in local/secrets/ and are never loaded
automatically. Gitignore is not a permission boundary. Preserve private visibility when learning
from research or closing tickets; shared promotion requires explicit consent.
