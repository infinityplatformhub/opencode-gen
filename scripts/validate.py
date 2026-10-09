"""Validate framework manifests and native entrypoints without network access."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
index = json.loads((ROOT / "skills-library/_index.json").read_text())
registry = json.loads((ROOT / "skills-library/_registry.json").read_text())
for name, info in registry["skills"].items():
    directory = ROOT / "skills-library/_cache" / name
    assert len(info["files"]) == info["file_count"], name
    assert all((directory / file).is_file() for file in info["files"]), name
for name, profile in index["stack_profiles"].items():
    assert all(skill in index["skills"] for skill in profile["skills"]), name
    assert all((ROOT / "bootstrap/rules/stacks" / rule).is_file() for rule in profile["rules"]), name
for command in (ROOT / ".opencode/commands").glob("*.md"):
    assert command.stem.startswith("opencode-gen-"), command
    skill = ROOT / ".opencode/skills" / command.stem / "SKILL.md"
    assert skill.is_file(), skill
    assert f"name: {command.stem}\n" in skill.read_text(), skill
    assert "$ARGUMENTS" in command.read_text(), command
    hidden = command.stem in {"opencode-gen-init", "opencode-gen-update", "opencode-gen-add-skill", "opencode-gen-sync-skills"}
    assert ("  opencode/autoinvoke: false\n" in skill.read_text()) == hidden, skill
assert (ROOT / "bootstrap/AGENTS.md.tmpl").is_file()
assert not (ROOT / "CLAUDE.md").exists()
assert len((ROOT / "bootstrap/AGENTS.md.tmpl").read_bytes()) <= 2048
assert len((ROOT / "bootstrap/ctx/rules/workflow.md").read_bytes()) <= 8192
assert not list((ROOT / ".opencode/agents").glob("*.md"))
assert not list((ROOT / "bootstrap/plugins").rglob("index.ts"))
print(f"Validated {len(registry['skills'])} cached skills, {len(index['stack_profiles'])} profiles, and native entrypoints")
