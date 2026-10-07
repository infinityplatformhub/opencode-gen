# Scope and deployment

Install only into projects that opt in. Never write framework assets under global OpenCode config
or organization parent directories. Projects beneath a common parent must not inherit a framework
entrypoint installed at that parent; test scope explicitly when using nested repositories.

Tracked/shared: bounded AGENTS section, project commands/skills, `.ctx/config.json`, workflow,
shared ticket ledger/documents, retained shared research, and verified shared memory.

Ignored/private: `.ctx/local/` including environment notes, local tickets/research/memory, secrets,
scratch, installation source metadata, and backups. Never preload local indexes; read only what
the task needs. Gitignore does not make a file inaccessible to agents or providers.

Each teammate runs the installer from their own checkout to restore private management assets.
It preserves user data/config, updates hash-owned files, and refuses unowned/customized conflicts.
Backups contain affected existing files rather than recursively copying the entire cache.
Review old backups periodically; do not delete them automatically or retain an unbounded cache.

Private requests use local ticket ledgers. Do not leak their titles or IDs into shared indexes,
commit messages, summaries, or another project's memory. Shared promotion requires explicit consent.
