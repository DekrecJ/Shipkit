import json,unittest
from pathlib import Path
class Skills(unittest.TestCase):
 def test_manifests(self):
  root=Path(__file__).resolve().parents[1]/'shipkit'/'assets'/'skills'; skills=list(root.glob('*/SKILL.md')); self.assertEqual(len(skills),7)
  for s in skills:
   m=json.loads((s.parent/'manifest.json').read_text()); self.assertEqual(m['protocol'],'shipkit-skill-v1'); self.assertEqual(m['name'],s.parent.name)
if __name__=='__main__': unittest.main()
