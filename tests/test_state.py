import json,tempfile,unittest
from pathlib import Path
from shipkit.state.manager import initialize,load,update_phase,advance
class StateTests(unittest.TestCase):
 def test_schema_and_migration(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d); initialize(r,'Demo'); p,s=load(r); self.assertEqual(s['$schema'],'shipkit:state-v1')
   legacy={'shipkit_version':'0.1.0','project':'Old','current_phase':'discovery','phases':{'discovery':'in_progress'}}; (r/'.shipkit/state.json').write_text(json.dumps(legacy)); _,s=load(r); self.assertEqual(s['$schema'],'shipkit:state-v1')
 def test_invalid_jump_blocked(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d); initialize(r,'Demo')
   with self.assertRaises(ValueError): update_phase(r,'testing')
 def test_force_records_debt(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d); initialize(r,'Demo'); s=update_phase(r,'requirements',force=True); self.assertTrue(s['blockers']); self.assertEqual(s['phases']['discovery'],'blocked')
if __name__=='__main__': unittest.main()
