"""Read-only shared-context budget and tracked-private-data checks."""
from pathlib import Path
import subprocess
import sys


def check(root):
    root = root.resolve()
    issues = []
    files = {root / ".ctx/index.md": 2048, root / ".ctx/rules/workflow.md": 8192}
    for folder in ("tickets", "research", "memory"):
        for path in (root / ".ctx" / folder).rglob("*.md"):
            files[path] = 8192 if path.name == "index.md" or "archive" in path.parts else 12288
    for path, budget in files.items():
        if not path.exists():
            continue
        if root not in path.resolve().parents:
            issues.append(f"{path.relative_to(root)}: external symlink")
        elif path.stat().st_size > budget:
            issues.append(f"{path.relative_to(root)}: exceeds {budget} bytes; archive/split without losing content")
    agents = root / "AGENTS.md"
    if agents.exists():
        text = agents.read_text()
        start, end = "<!-- opencode-gen:start -->", "<!-- opencode-gen:end -->"
        if text.count(start) != 1 or text.count(end) != 1 or text.index(end) < text.index(start):
            issues.append("AGENTS.md: invalid managed block")
        elif len(text[text.index(start):text.index(end) + len(end)].encode()) > 2048:
            issues.append("AGENTS.md: managed block exceeds 2048 bytes")
    try:
        result = subprocess.run(["git", "-C", str(root), "ls-files", "--", ".ctx/local"],
                                capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            issues.append("Private .ctx/local files are tracked by Git; review without exposing their contents")
    except FileNotFoundError:
        pass
    return issues


if __name__ == "__main__":
    issues = check(Path(sys.argv[1] if len(sys.argv) > 1 else "."))
    print("\n".join(issues) if issues else "Context checks passed")
    sys.exit(bool(issues))
