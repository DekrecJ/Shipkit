import tempfile,unittest
from pathlib import Path
from shipkit.state.manager import initialize
from shipkit.project_setup import scaffold_project
from shipkit.checks.runner import run_all
class Check(unittest.TestCase):
 def test_check_schema(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); initialize(root,'Demo','cli_tool'); scaffold_project(root,'Demo')
   (root/'README.md').write_text(('# Demo\n')*20,encoding='utf-8')
   (root/'pyproject.toml').write_text('[project]\nname="demo"',encoding='utf-8')
   (root/'tests').mkdir(); (root/'tests/test_x.py').write_text('import unittest\nclass T(unittest.TestCase):\n def test_ok(self): self.assertTrue(True)',encoding='utf-8')
   out=run_all(root); self.assertIn(out['status'],{'READY','REVIEW','NOT_READY'}); self.assertEqual(out['scoring_schema'],'shipkit:scoring-v1')
if __name__=='__main__': unittest.main()
