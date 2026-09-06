import tempfile
import unittest
from pathlib import Path
from shipkit.state.manager import initialize
from shipkit.project_setup import scaffold_project

class ProjectSetupTests(unittest.TestCase):
    def test_scaffold(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            initialize(root, "Demo")
            scaffold_project(root, "Demo")
            self.assertTrue((root / "AGENTS.md").exists())
            self.assertTrue((root / ".shipkit" / "ARCHITECTURE.md").exists())
            self.assertIn("Demo", (root / ".shipkit" / "PROJECT.md").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
