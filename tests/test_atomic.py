import tempfile,unittest
from pathlib import Path
from shipkit.utils.filesystem import write_json_atomic,recover_json
class AtomicTests(unittest.TestCase):
 def test_backup_and_recovery(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'state.json'; write_json_atomic(p,{'v':1}); write_json_atomic(p,{'v':2}); self.assertTrue(Path(str(p)+'.bak').exists()); p.write_text('{broken'); data,recovered=recover_json(p); self.assertTrue(recovered); self.assertEqual(data['v'],1)
if __name__=='__main__': unittest.main()
