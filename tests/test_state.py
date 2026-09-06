import tempfile
import unittest
from pathlib import Path
from shipkit.state.manager import initialize, load, update_phase, update_task

class StateTests(unittest.TestCase):
    def test_initialize_and_phase(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            initialize(root, "Demo")
            project, state = load(root)
            self.assertEqual(project["name"], "Demo")
            self.assertEqual(state["current_phase"], "discovery")
            state = update_phase(root, "requirements")
            self.assertEqual(state["current_phase"], "requirements")
            self.assertEqual(state["phases"]["discovery"], "completed")
            state = update_task(root, "AUTH-001", "in_progress")
            self.assertEqual(state["current_task"], "AUTH-001")
            state = update_task(root, "AUTH-001", "completed")
            self.assertIsNone(state["current_task"])
            self.assertIn("AUTH-001", state["completed_tasks"])

if __name__ == "__main__":
    unittest.main()
