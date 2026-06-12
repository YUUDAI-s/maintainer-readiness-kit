from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from maintainer_readiness.sarif import render_sarif


class SarifTests(unittest.TestCase):
    def test_render_sarif_includes_failed_checks_and_warnings(self):
        result = {
            "root": "/private/path",
            "display_root": "demo",
            "checks": [
                {
                    "check_id": "license",
                    "label": "Open source license is present",
                    "passed": False,
                    "weight": 12,
                    "evidence": "missing",
                    "fix": "Add a recognized open source license.",
                }
            ],
            "secret_warnings": [{"path": ".env", "reason": "high-risk local credential/config filename"}],
        }

        sarif = render_sarif(result)
        run = sarif["runs"][0]

        self.assertEqual(sarif["version"], "2.1.0")
        self.assertEqual(len(run["results"]), 2)
        self.assertEqual(run["results"][0]["ruleId"], "maintainer-readiness.license")
        self.assertEqual(run["results"][1]["level"], "error")


if __name__ == "__main__":
    unittest.main()
