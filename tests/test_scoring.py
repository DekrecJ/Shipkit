import tempfile,unittest
from pathlib import Path
from shipkit.state.manager import initialize
from shipkit.checks.scoring import load_scoring
class Scoring(unittest.TestCase):
 def test_saas_profile(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d); initialize(r,'Demo','saas'); s=load_scoring(r,{'type':'saas'}); self.assertEqual(s['$schema'],'shipkit:scoring-v1'); self.assertEqual(s['thresholds']['ready'],92)
if __name__=='__main__': unittest.main()
