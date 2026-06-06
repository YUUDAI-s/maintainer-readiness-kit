from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from maintainer_readiness.github import summarize_open_items


class GitHubSummaryTests(unittest.TestCase):
    def test_summarize_open_items_splits_issues_and_pull_requests(self):
        now = datetime(2026, 6, 6, tzinfo=timezone.utc)
        items = [
            {"updated_at": "2026-05-01T00:00:00Z"},
            {"updated_at": "2026-06-01T00:00:00Z"},
            {"updated_at": "2026-04-01T00:00:00Z", "pull_request": {"url": "https://example.test/pr/1"}},
            {"updated_at": "not-a-date"},
        ]

        summary = summarize_open_items(items, now=now, stale_days=30)

        self.assertEqual(summary["open_issue_items_sampled"], 2)
        self.assertEqual(summary["open_pr_items_sampled"], 1)
        self.assertEqual(summary["stale_issue_items"], 1)
        self.assertEqual(summary["stale_pr_items"], 1)
        self.assertEqual(summary["oldest_open_issue_updated_at"], "2026-05-01T00:00:00Z")
        self.assertEqual(summary["oldest_open_pr_updated_at"], "2026-04-01T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
