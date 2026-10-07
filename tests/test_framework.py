import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


class FrameworkTests(unittest.TestCase):
    def install(self, target, success=True):
        result = subprocess.run(["sh", str(ROOT / "install.sh"), str(target)], capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stderr)
        return result

    def test_repeat_install_preserves_project_and_bounds_context(self):
        with tempfile.TemporaryDirectory(dir="/tmp/opencode") as temp:
            root = Path(temp)
            (root / "AGENTS.md").write_text("# Org rules\nKeep our conventions.\n")
            (root / "opencode.jsonc").write_text('{// custom\n"model":"example/model"}')
            self.install(root)
            self.install(root)
            agents = (root / "AGENTS.md").read_text()
            self.assertEqual(agents.count("<!-- opencode-gen:start -->"), 1)
            self.assertTrue(agents.startswith("# Org rules"))
            self.assertLess(len(agents.encode()), 2048)
            self.assertIn("// custom", (root / "opencode.jsonc").read_text())
            self.assertEqual(len(list((root / ".opencode/skills").rglob("SKILL.md"))), 7)
            self.assertFalse((root / ".opencode/plugins").exists())
            self.assertFalse((root / ".ctx/local/framework/skills-library").exists())
            self.assertEqual((root / ".gitignore").read_text().count("/.ctx/local/"), 1)
            result = subprocess.run(["python3", str(ROOT / "scripts/check-context.py"), str(root)], capture_output=True)
            self.assertEqual(result.returncode, 0)

    def test_custom_rule_conflict_is_not_overwritten(self):
        with tempfile.TemporaryDirectory(dir="/tmp/opencode") as temp:
            root = Path(temp)
            self.install(root)
            rule = root / ".ctx/rules/workflow.md"
            rule.write_text("Organization customization")
            self.install(root, success=False)
            self.assertEqual(rule.read_text(), "Organization customization")

    def test_private_bootstrap_does_not_enter_shared_ledger(self):
        with tempfile.TemporaryDirectory(dir="/tmp/opencode") as temp:
            root = Path(temp)
            (root / ".ctx").mkdir()
            (root / ".ctx/config.json").write_text(json.dumps({"default_visibility": "private", "ticket_prefix": "P-"}))
            self.install(root)
            self.assertNotIn("P-", (root / ".ctx/tickets/index.md").read_text())
            self.assertIn("P-", (root / ".ctx/local/tickets/index.md").read_text())
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            ignored = subprocess.run(["git", "-C", str(root), "check-ignore", ".ctx/local/tickets/index.md"], capture_output=True)
            self.assertEqual(ignored.returncode, 0)

    def test_budget_violation_and_self_install(self):
        self.install(ROOT, success=False)
        with tempfile.TemporaryDirectory(dir="/tmp/opencode") as temp:
            root = Path(temp)
            self.install(root)
            (root / ".ctx/index.md").write_text("x" * 2049)
            result = subprocess.run(["python3", str(ROOT / "scripts/check-context.py"), str(root)], capture_output=True)
            self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
