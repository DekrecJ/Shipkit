import tempfile
import unittest
from pathlib import Path
from shipkit.state.manager import initialize
from shipkit.project_setup import scaffold_project
from shipkit.checks.runner import run_all


class CheckTests(unittest.TestCase):
    def test_check_returns_score(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            initialize(root, "Demo", "cli_tool")
            scaffold_project(root, "Demo")
            (root / "README.md").write_text(("# Demo\n" * 20), encoding="utf-8")
            (root / ".gitignore").write_text(".env\n", encoding="utf-8")
            (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
            result = run_all(root)
            self.assertIn("score", result)
            self.assertTrue(0 <= result["score"] <= 100)


if __name__ == "__main__":
    unittest.main()
