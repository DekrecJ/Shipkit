import tempfile,unittest
from pathlib import Path
from shipkit.state.manager import initialize
from shipkit.project_setup import scaffold_project
class Setup(unittest.TestCase):
 def test_scaffold(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d); initialize(r,'Demo'); scaffold_project(r,'Demo'); self.assertTrue((r/'AGENTS.md').exists()); self.assertTrue((r/'.shipkit/ARCHITECTURE.md').exists())
if __name__=='__main__': unittest.main()
