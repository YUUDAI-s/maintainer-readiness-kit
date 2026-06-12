from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from maintainer_readiness.badge import render_badge


class BadgeTests(unittest.TestCase):
    def test_render_badge_colors_by_score(self):
        self.assertEqual(render_badge({"percent": 95})["color"], "brightgreen")
        self.assertEqual(render_badge({"percent": 75})["color"], "yellow")
        self.assertEqual(render_badge({"percent": 30})["color"], "red")


if __name__ == "__main__":
    unittest.main()
