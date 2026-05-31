from pathlib import Path
import tempfile
import unittest

from maintainer_readiness.templates import write_templates


class TemplateTests(unittest.TestCase):
    def test_writes_templates_without_overwriting_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            existing = root / "SECURITY.md"
            existing.write_text("keep me\n", encoding="utf-8")

            result = write_templates(root)

            self.assertEqual(existing.read_text(encoding="utf-8"), "keep me\n")
            statuses = {item["path"]: item["status"] for item in result}
            self.assertEqual(statuses["SECURITY.md"], "skipped")
            self.assertEqual(statuses["CONTRIBUTING.md"], "written")


if __name__ == "__main__":
    unittest.main()
