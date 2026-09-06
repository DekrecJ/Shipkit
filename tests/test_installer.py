import os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from shipkit.installer import codex
class Installer(unittest.TestCase):
 def test_codex_layout(self):
  with tempfile.TemporaryDirectory() as d:
   home=Path(d); env={'HOME':d,'CODEX_HOME':str(home/'.codex'),'SHIPKIT_SKILLS_HOME':str(home/'.agents/skills')}
   with patch.dict(os.environ,env,clear=False), patch('pathlib.Path.home',return_value=home):
    r=codex.install(); self.assertEqual(len(r['skills']),7); self.assertTrue((home/'.codex/AGENTS.md').exists()); self.assertTrue((home/'.shipkit/library/specs/scoring-v1.json').exists())
if __name__=='__main__': unittest.main()
