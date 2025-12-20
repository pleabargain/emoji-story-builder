import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.emoji_manager import EmojiManager
from src.data_store import DataStore

class TestAppLogic(unittest.TestCase):
    def test_emoji_manager_unique_random(self):
        print("\n[Test] Verifying EmojiManager uniqueness and count...")
        print("      - Rationale: Emojis must be unique in each generation to provide a good creative prompt.")
        manager = EmojiManager()
        emojis1 = manager.get_random_emojis(5)
        self.assertEqual(len(emojis1), 5)
        # Check uniqueness in current call
        self.assertEqual(len(set(emojis1)), 5)

    def test_data_store_init(self):
        print("\n[Test] Verifying DataStore initialization...")
        print("      - Rationale: Ensure the persistence layer is ready to handle session data.")
        # We should use a temp path here in real scenario, but for now just check it loads
        store = DataStore()
        self.assertIsNotNone(store)

    def test_app_has_main(self):
        print("\n[Test] Verifying structural integrity (main function existence)...")
        print("      - Rationale: Prevents accidental deletion of the application entry point.")
        import src.app as app
        self.assertTrue(hasattr(app, 'main'), "src/app.py is missing the 'main' function!")
        self.assertTrue(callable(app.main), "src/app.py 'main' is not a callable function!")

if __name__ == '__main__':
    unittest.main()
