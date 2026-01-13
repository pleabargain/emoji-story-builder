import requests
import json
import logging


class OllamaClient:
    """Client for interacting with the local Ollama API."""

    def __init__(self, base_url="http://localhost:11434", model="llama3.2"):
        self.base_url = base_url
        self.model = model
        self.logger = logging.getLogger("emoji_builder.ollama")

    def check_status(self):
        """Check if the Ollama server is running and reachable."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                return True, "Ollama Running"
            return False, f"Ollama Error (Status: {response.status_code})"
        except requests.exceptions.RequestException:
            return False, "Ollama Not Detected"
        except Exception as e:
            return False, f"Ollama Error: {str(e)}"

    def get_available_models(self):
        """Fetch the list of available models from Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception as e:
            self.logger.error(f"Failed to fetch available models: {str(e)}")
            return []

    def generate_story(self, emojis, model=None, word_count=150, temperature=1.2):
        """Generate a story from a list of emojis using Ollama."""
        target_model = model or self.model

        # Validate that the model is available before attempting generation
        available_models = self.get_available_models()
        if target_model not in available_models:
            raise ValueError(
                f"Model '{target_model}' is not available. Available models: {available_models}"
            )

        emoji_str = " ".join(emojis)
        prompt = (
            f"Write a creative story with a beginning, middle, and end, inspired by these emojis: {emoji_str}. "
            f"The story should be about {word_count} words long."
        )

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": target_model,
                    "prompt": prompt,
                    "options": {"temperature": temperature},
                },
                timeout=300,
                stream=True,
            )
            response.raise_for_status()

            story = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            story += data["response"]
                    except Exception:
                        continue
            return story.strip()
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(
                    f"Model '{target_model}' not found or Ollama API error. Ensure the model is pulled and try again."
                )
            else:
                raise
        except Exception as e:
            self.logger.error(f"Ollama story generation failed: {str(e)}")
            raise
