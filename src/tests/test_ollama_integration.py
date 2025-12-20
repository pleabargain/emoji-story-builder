import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.ollama_client import OllamaClient

class TestOllamaIntegration(unittest.TestCase):
    """
    Live integration test for Ollama.
    NOTE: This test requires a specific model to be installed locally.
    Default: gemma3:4b
    """
    def setUp(self):
        self.client = OllamaClient()
        self.target_model = "gemma3:4b" # HARDCODED: Change this if using a different model

    def test_live_generation(self):
        print(f"\n[Integration Test] Running live prompt to Ollama ({self.target_model})...")
        print("      - Rationale: End-to-end verification of the AI generation pipeline.")
        
        # 1. Check if Ollama is running
        online, msg = self.client.check_status()
        if not online:
            self.skipTest("Ollama is not running. Skipping integration test.")
            
        # 2. Check if the specific model is available
        models = self.client.get_available_models()
        if self.target_model not in models:
            self.skipTest(f"Model '{self.target_model}' not found in Ollama. "
                         f"Available models: {models}. "
                         "Please pull the model or edit test_ollama_integration.py.")

        # 3. Run a very short generation
        test_emojis = ["🍎", "🐍"]
        try:
            story = self.client.generate_story(test_emojis, model=self.target_model, word_count=20)
            self.assertIsNotNone(story)
            self.assertTrue(len(story) > 0)
            print(f"      - Success! Output preview: {story[:50]}...")
        except Exception as e:
            self.fail(f"Live generation failed: {str(e)}")

if __name__ == '__main__':
    unittest.main()
