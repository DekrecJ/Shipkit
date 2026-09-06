import tempfile,unittest
from pathlib import Path
from shipkit.state.manager import initialize,advance
from shipkit.project_setup import scaffold_project
from shipkit.state.phases import validate_phase
class PhaseTests(unittest.TestCase):
 def test_placeholder_does_not_validate(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); initialize(root,'Demo'); scaffold_project(root,'Demo'); self.assertFalse(validate_phase(root,'discovery')['ok'])
   with self.assertRaises(ValueError): advance(root)
 def test_discovery_can_advance_when_complete(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); initialize(root,'Demo'); scaffold_project(root,'Demo')
   content='# Overview\n'+('A'*80)+'\n# Goals\n'+('B'*40)+'\n# Users\nUsers here.\n# Constraints\nConstraints here.'
   (root/'.shipkit/PROJECT.md').write_text(content,encoding='utf-8')
   state=advance(root); self.assertEqual(state['current_phase'],'requirements')
if __name__=='__main__': unittest.main()
