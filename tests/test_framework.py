import json
import os
import tarfile
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


class FrameworkTests(unittest.TestCase):
    def test_subagent_session_guard_is_installed_and_bounded(self):
        with tempfile.TemporaryDirectory(dir="/tmp/opencode") as temp:
            root = Path(temp)
            self.install(root)
            text = (root / "AGENTS.md").read_text()
            self.assertIn("When spawning a new subagent, omit sessionID entirely", text)
            self.assertIn("never retry with fabricated IDs", text)
            self.assertLessEqual(len(text.encode()), 2048)

    def test_pipe_install_downloads_and_cleans_temporary_source(self):
        with tempfile.TemporaryDirectory(dir="/tmp/opencode") as temp:
            base = Path(temp)
            archive = base / "source.tar.gz"
            with tarfile.open(archive, "w:gz") as tar:
                for name in ("scripts", "bootstrap", ".opencode"):
                    tar.add(ROOT / name, arcname="opencode-gen-master/" + name)
            commands = base / "bin"
            commands.mkdir()
            curl = commands / "curl"
            curl.write_text('#!/bin/sh\ncp "$TEST_ARCHIVE" "$4"\n')
            curl.chmod(0o755)
            project = base / "project with spaces"
            project.mkdir()
            env = dict(os.environ, PATH=str(commands) + os.pathsep + os.environ["PATH"], TEST_ARCHIVE=str(archive))
            result = subprocess.run(["sh"], input=(ROOT / "install.sh").read_text(),
                                    cwd=project, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            source = json.loads((project / ".ctx/local/framework/source.json").read_text())
            self.assertIsNone(source["path"])
            self.assertEqual(source["branch"], "master")
            self.assertTrue((project / "AGENTS.md").exists())

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
            self.assertTrue((root / ".opencode/plugins/opencode-gen-sidebar/tui.tsx").exists())
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

    def test_language_preferences_survive_reinstall(self):
        for language in ("th", "en", "Japanese"):
            with self.subTest(language=language), tempfile.TemporaryDirectory(dir="/tmp/opencode") as temp:
                root = Path(temp)
                self.install(root)
                config_path = root / ".ctx/config.json"
                config = json.loads(config_path.read_text())
                self.assertIsNone(config["conversation_language"])
                self.assertFalse(config["preferences_confirmed"])
                config.update(conversation_language=language, preferences_confirmed=True, organization_setting="keep")
                config_path.write_text(json.dumps(config))
                self.install(root)
                self.assertEqual(json.loads(config_path.read_text()), config)
                self.assertIn("conversation_language", (root / "AGENTS.md").read_text())

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
