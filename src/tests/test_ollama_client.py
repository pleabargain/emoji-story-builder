import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.ollama_client import OllamaClient

class TestOllamaClient(unittest.TestCase):
    def setUp(self):
        self.client = OllamaClient(base_url="http://test:11434")

    @patch('requests.get')
    def test_check_status_success(self, mock_get):
        print("\n[Test] Verifying Ollama status check (Success Case)...")
        print("      - Rationale: Ensure the app correctly identifies when Ollama is online.")
        mock_get.return_value.status_code = 200
        online, msg = self.client.check_status()
        self.assertTrue(online)
        self.assertEqual(msg, "Ollama Running")

    @patch('requests.get')
    def test_check_status_offline(self, mock_get):
        print("\n[Test] Verifying Ollama status check (Offline Case)...")
        print("      - Rationale: Ensure the app handles connection errors gracefully.")
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError()
        online, msg = self.client.check_status()
        self.assertFalse(online)
        self.assertEqual(msg, "Ollama Not Detected")

    @patch('requests.get')
    def test_get_available_models(self, mock_get):
        print("\n[Test] Verifying model enumeration from Ollama API...")
        print("      - Rationale: Ensure the app can fetch and parse the list of locally installed models.")
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "models": [{"name": "llama3.2"}, {"name": "gpt-oss:120b"}]
        }
        models = self.client.get_available_models()
        self.assertIn("llama3.2", models)
        self.assertIn("gpt-oss:120b", models)

    @patch('requests.post')
    def test_generate_story_success(self, mock_post):
        print("\n[Test] Verifying story generation with mocked Ollama response...")
        print("      - Rationale: Ensure the app correctly formats prompts and parses streamed responses.")
        mock_response = MagicMock()
        mock_response.iter_lines.return_value = [b'{"response": "Once "}', b'{"response": "upon "}', b'{"response": "a time."}']
        mock_post.return_value = mock_response
        
        story = self.client.generate_story(["🦁"], word_count=5)
        self.assertEqual(story, "Once upon a time.")

if __name__ == '__main__':
    unittest.main()
