import unittest
from pathlib import Path


class SkillBundleTests(unittest.TestCase):
    def test_all_skills_have_frontmatter(self):
        root = Path(__file__).resolve().parents[1] / "shipkit" / "assets" / "skills"
        skills = list(root.glob("*/SKILL.md"))
        self.assertGreaterEqual(len(skills), 7)
        for skill in skills:
            text = skill.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), skill)
            frontmatter = text.split("---", 2)[1]
            self.assertIn("name:", frontmatter, skill)
            self.assertIn("description:", frontmatter, skill)


if __name__ == "__main__":
    unittest.main()
