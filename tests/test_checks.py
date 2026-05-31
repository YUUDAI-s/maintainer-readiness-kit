from pathlib import Path
import tempfile
import unittest

from maintainer_readiness.checks import inspect_project


class InspectProjectTests(unittest.TestCase):
    def test_scores_common_maintainer_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_demo.py").write_text("def test_demo():\n    assert True\n", encoding="utf-8")
            (root / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True)
            (root / ".github" / "ISSUE_TEMPLATE" / "bug.yml").write_text("name: Bug\n", encoding="utf-8")
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "ci.yml").write_text("name: CI\n", encoding="utf-8")

            result = inspect_project(root)

        self.assertGreaterEqual(result["score"], 60)
        passed = {item["check_id"] for item in result["checks"] if item["passed"]}
        self.assertIn("readme", passed)
        self.assertIn("license", passed)
        self.assertIn("tests", passed)
        self.assertIn("ci", passed)

    def test_warns_about_high_risk_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".env").write_text("TOKEN=value\n", encoding="utf-8")

            result = inspect_project(root)

        self.assertEqual(result["secret_warnings"][0]["path"], ".env")


if __name__ == "__main__":
    unittest.main()
