from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from maintainer_readiness.checks import classify_level, detect_ecosystems, inspect_project


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

    def test_detects_python_ecosystem(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")

            ecosystems = detect_ecosystems(root)

        self.assertEqual(ecosystems[0]["ecosystem"], "python")
        self.assertIn("pyproject.toml", ecosystems[0]["evidence"])

    def test_detects_java_ecosystem(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pom.xml").write_text("<project />\n", encoding="utf-8")

            ecosystems = detect_ecosystems(root)

        self.assertEqual(ecosystems[0]["ecosystem"], "java")
        self.assertIn("pom.xml", ecosystems[0]["evidence"])

    def test_uses_root_label_for_shared_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = inspect_project(tmp, root_label="sample-project")

        self.assertEqual(result["display_root"], "sample-project")

    def test_classifies_readiness_levels(self):
        self.assertEqual(classify_level(95), "ready")
        self.assertEqual(classify_level(75), "nearly-ready")
        self.assertEqual(classify_level(30), "needs-work")

    def test_warns_about_high_risk_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".env").write_text("TOKEN=value\n", encoding="utf-8")

            result = inspect_project(root)

        self.assertEqual(result["secret_warnings"][0]["path"], ".env")


if __name__ == "__main__":
    unittest.main()
