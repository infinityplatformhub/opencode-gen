"""Project-local installation with owned-file conflict detection."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
from datetime import datetime, timezone
import uuid

START = "<!-- opencode-gen:start -->"
END = "<!-- opencode-gen:end -->"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def merge_agents(text, block):
    if START not in text and END not in text:
        return text.rstrip() + ("\n\n" if text.strip() else "") + block
    if text.count(START) != 1 or text.count(END) != 1 or text.index(END) < text.index(START):
        raise ValueError("Malformed managed AGENTS block; repair before installation")
    return text[:text.index(START)] + block.rstrip() + text[text.index(END) + len(END):]


def install(source, target):
    if source == target or source in target.parents or target in source.parents:
        raise ValueError("Framework and target must be separate, non-nested directories")
    assets = target / ".ctx/local/framework"
    manifest_path = assets / "manifest.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    desired = {}
    for folder in ("commands", "skills"):
        for file in (source / ".opencode" / folder).rglob("*.md"):
            desired[str(file.relative_to(source))] = file.read_bytes()
    for file in (source / "bootstrap/ctx").rglob("*"):
        if not file.is_file():
            continue
        name = ".ctx/" + str(file.relative_to(source / "bootstrap/ctx"))
        # User preferences and data are seeded, never refreshed by installation.
        if name in (".ctx/config.json", ".ctx/index.md") or name.endswith("/index.md"):
            if not (target / name).exists():
                desired[name] = file.read_bytes()
        else:
            desired[name] = file.read_bytes()
    conflicts = []
    for name, data in desired.items():
        path = target / name
        if path.is_symlink():
            conflicts.append(name)
        elif path.exists() and path.read_bytes() != data and previous.get(name) != digest(path.read_bytes()):
            conflicts.append(name)
    if conflicts:
        raise ValueError("Customized/unowned files require a manual merge: " + ", ".join(conflicts))
    agents = target / "AGENTS.md"
    old_agents = agents.read_text() if agents.exists() else ""
    new_agents = merge_agents(old_agents, (source / "bootstrap/AGENTS.md.tmpl").read_text())
    config_path = target / ".ctx/config.json"
    config = json.loads(config_path.read_text() if config_path.exists()
                        else (source / "bootstrap/ctx/config.json").read_text())
    prefix = config.get("ticket_prefix", "T-")
    if not isinstance(prefix, str) or not prefix or any(c in prefix for c in "/\\\n\r"):
        raise ValueError("Invalid ticket prefix")
    if config.get("default_visibility") not in ("shared", "private"):
        raise ValueError("Invalid default_visibility")
    # Prevent writes through project-controlled symlinks outside the target.
    for name in [*desired, "AGENTS.md", ".gitignore", ".ctx/local/framework/manifest.json",
                 ".ctx/local/backups/check", ".ctx/local/tickets/index.md", ".ctx/tickets/index.md"]:
        path = target / name
        if target not in path.resolve().parents:
            raise ValueError(f"External symlink destination: {name}")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    backup = target / ".ctx/local/backups" / (stamp + "-" + uuid.uuid4().hex[:8])
    for name in [*desired, "AGENTS.md", ".gitignore"]:
        path = target / name
        if path.is_file():
            dest = backup / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
    ignore = target / ".gitignore"
    text = ignore.read_text() if ignore.exists() else ""
    if "/.ctx/local/" not in text.splitlines():
        ignore.write_text(text + ("\n" if text and not text.endswith("\n") else "") + "/.ctx/local/\n")
    # Establish a ticket before substantive setup. Ticket ID is unique across sessions.
    ledger = target / ".ctx/tickets/index.md"
    for name, data in desired.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    ticket_id = prefix + stamp + "-" + uuid.uuid4().hex[:8]
    if config.get("default_visibility") == "private":
        ledger = target / ".ctx/local/tickets/index.md"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ticket = ledger.parent / (ticket_id + ".md")
    template = (source / "bootstrap/ticket.md.tmpl").read_text()
    for key, value in {"TICKET_ID": ticket_id, "TITLE": "Initialize or update project workflow",
                       "GOAL": "Install and verify project-local ticket control",
                       "ACCEPTANCE": "Assets installed; preferences and runtime workflow verified"}.items():
        template = template.replace("{{" + key + "}}", value)
    with ticket.open("x") as file:
        file.write(template)
    with ledger.open("a") as file:
        file.write(f"\n- {ticket_id} | open | Initialize or update project workflow\n")
    agents.write_text(new_agents)
    assets.mkdir(parents=True, exist_ok=True)
    # Inactive assets never live under an auto-discovered skills directory.
    for relative in ("bootstrap/ticket.md.tmpl", "scripts/check-context.py"):
        destination = assets / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, destination)
    (assets / "source.json").write_text(json.dumps({"path": None if os.environ.get("OPENCODE_GEN_EPHEMERAL_SOURCE") == "1" else str(source),
        "origin": "git@github.com:infinityplatformhub/opencode-gen.git", "branch": "master"}, indent=2) + "\n")
    # Library remains in the source checkout; activation is opt-in, no per-project cache copy.
    managed = {name: digest(data) for name, data in desired.items()
               if not name.endswith("/index.md") and name != ".ctx/config.json"}
    manifest_path.write_text(json.dumps(managed, indent=2) + "\n")
    print(f"Installed into {target}; bootstrap ticket: {ticket_id}")
    if backup.exists():
        print(f"Backup: {backup}")
    print("Run /opencode-gen-init to confirm preferences and verify the bootstrap ticket.")


if __name__ == "__main__":
    install(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
