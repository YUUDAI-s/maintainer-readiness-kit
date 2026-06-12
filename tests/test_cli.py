from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from maintainer_readiness.cli import main, readiness_exit_code


class CliTests(unittest.TestCase):
    def test_version_flag_prints_package_version(self):
        stdout = StringIO()

        with self.assertRaises(SystemExit) as raised:
            with redirect_stdout(stdout):
                main(["--version"])

        self.assertEqual(raised.exception.code, 0)
        self.assertIn("maintainer-readiness 0.6.1", stdout.getvalue())

    def test_inspect_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            output = root / "report.md"

            with redirect_stdout(StringIO()):
                exit_code = main(["inspect", str(root), "--output", str(output), "--root-label", "demo"])

            self.assertEqual(exit_code, 0)
            report = output.read_text(encoding="utf-8")
            self.assertIn("Maintainer Readiness Report", report)
            self.assertIn("`demo`", report)

    def test_init_json_reports_written_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["init", tmp, "--json"])

            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "CONTRIBUTING.md").exists())
            self.assertIn('"templates"', stdout.getvalue())

    def test_fail_under_returns_nonzero_when_score_is_low(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")

            with redirect_stdout(StringIO()):
                exit_code = main(["inspect", str(root), "--fail-under", "90"])

            self.assertEqual(exit_code, 1)

    def test_inspect_writes_sarif_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            sarif = root / "readiness.sarif"

            with redirect_stdout(StringIO()):
                exit_code = main(["inspect", str(root), "--sarif", str(sarif), "--root-label", "demo"])

            self.assertEqual(exit_code, 0)
            report = sarif.read_text(encoding="utf-8")
            self.assertIn('"version": "2.1.0"', report)
            self.assertIn("maintainer-readiness.license", report)

    def test_inspect_writes_badge_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            badge = root / "badge.json"

            with redirect_stdout(StringIO()):
                exit_code = main(["inspect", str(root), "--badge-json", str(badge)])

            self.assertEqual(exit_code, 0)
            payload = json.loads(badge.read_text(encoding="utf-8"))
            self.assertEqual(payload["schemaVersion"], 1)
            self.assertEqual(payload["label"], "maintainer readiness")
            self.assertIn("%", payload["message"])

    def test_rejects_invalid_stale_days(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                main(["inspect", tmp, "--stale-days", "0"])

    def test_readiness_exit_code_accepts_passing_threshold(self):
        result = {"percent": 100.0}

        self.assertEqual(readiness_exit_code(result, 90), 0)
        self.assertEqual(readiness_exit_code(result, None), 0)


if __name__ == "__main__":
    unittest.main()
