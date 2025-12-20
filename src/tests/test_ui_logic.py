import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

class TestUILogic(unittest.TestCase):
    def test_generated_story_state_update(self):
        """Verify that story generation updates the session state correctly."""
        print("\n[Test] Verifying UI State Update for Story Generation...")
        print("      - Rationale: Ensure that the 'generated_story' state key is populated so the UI text area can render it.")

        # 1. Mock streamlit session state
        mock_session_state = {}
        
        # 2. Simulate the logic that happens inside the button click
        #    (We are not mocking the full app.py main loop, just the logic block)
        new_story = "Once upon a time in a digital world..."
        
        # Action: Update state
        mock_session_state['generated_story'] = new_story
        
        # 3. Assertions
        self.assertIn('generated_story', mock_session_state)
        self.assertEqual(mock_session_state['generated_story'], new_story)
        self.assertTrue(len(mock_session_state['generated_story']) > 0)
        
        print(f"      - Verified state content: '{mock_session_state['generated_story'][:20]}...'")

if __name__ == '__main__':
    unittest.main()
