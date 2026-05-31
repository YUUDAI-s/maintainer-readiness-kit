from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from maintainer_readiness.cli import main


class CliTests(unittest.TestCase):
    def test_inspect_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            output = root / "report.md"

            with redirect_stdout(StringIO()):
                exit_code = main(["inspect", str(root), "--output", str(output)])

            self.assertEqual(exit_code, 0)
            self.assertIn("Maintainer Readiness Report", output.read_text(encoding="utf-8"))

    def test_init_json_reports_written_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["init", tmp, "--json"])

            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "CONTRIBUTING.md").exists())
            self.assertIn('"templates"', stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
