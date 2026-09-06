import tempfile,unittest
from shipkit.cli import main
class Cli(unittest.TestCase):
 def test_init_and_status(self):
  with tempfile.TemporaryDirectory() as d:
   self.assertEqual(main(['init','--path',d,'--name','Demo']),0); self.assertEqual(main(['status','--path',d]),0)
if __name__=='__main__': unittest.main()
