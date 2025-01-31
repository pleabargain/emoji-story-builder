"""
Emoji manager implementation for the Emoji Story Builder.
Handles emoji selection, uniqueness tracking, and size calculations.
"""

import random
from typing import List, Set, Tuple, Dict
import os
from datetime import datetime
from pathlib import Path

from src.logger import get_logger

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

logger = get_logger()

def load_streamlit_emojis() -> Dict[str, str]:
    """Load Streamlit emoji mappings from file."""
    try:
        emoji_dict = {}
        emoji_file = Path(__file__).parent / 'streamlitemojis.txt'
        
        with open(emoji_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    emoji, shortcode = line.strip().split(':')
                    emoji_dict[emoji] = shortcode
                    
        logger.info(f"Loaded {len(emoji_dict)} Streamlit emojis")
        return emoji_dict
    except Exception as e:
        logger.error(f"Failed to load Streamlit emojis: {str(e)}")
        raise

class EmojiManager:
    def __init__(self):
        """Initialize the emoji manager."""
        self.used_emojis: Set[str] = set()
        self.all_emojis = self._load_emojis()
        
    def _load_emojis(self) -> List[str]:
        """Load all available Streamlit emojis."""
        try:
            # Get all emoji characters from Streamlit emoji mappings
            emoji_dict = load_streamlit_emojis()
            emoji_list = list(emoji_dict.keys())
            logger.info(f"Loaded {len(emoji_list)} Streamlit emojis")
            return emoji_list
        except Exception as e:
            logger.error(f"Failed to load emojis: {str(e)}")
            raise

    def reset_session(self) -> None:
        """Reset the session's used emojis tracking."""
        try:
            self.used_emojis.clear()
            logger.info("Session emoji tracking reset")
        except Exception as e:
            logger.error(f"Failed to reset session: {str(e)}")
            raise

    def get_random_emojis(self, count: int) -> List[str]:
        """
        Get a list of random unique emojis.
        
        Args:
            count: Number of emojis to generate (1-10)
            
        Returns:
            List of unique emoji characters
        """
        try:
            # Validate count
            count = max(1, min(10, count))
            
            # Calculate available emojis
            available_emojis = [e for e in self.all_emojis if e not in self.used_emojis]
            
            if len(available_emojis) < count:
                logger.warning("Not enough unique emojis available, resetting tracking")
                self.reset_session()
                available_emojis = self.all_emojis
            
            # Select random emojis
            selected_emojis = random.sample(available_emojis, count)
            
            # Track used emojis
            self.used_emojis.update(selected_emojis)
            
            logger.info(f"Generated {count} random emojis")
            return selected_emojis
            
        except Exception as e:
            logger.error(f"Failed to generate random emojis: {str(e)}")
            raise

    def calculate_emoji_size(self, screen_width: int, screen_height: int, emoji_count: int) -> Tuple[int, int]:
        """
        Calculate the size for each emoji based on screen dimensions and count.
        
        Args:
            screen_width: Width of the screen in pixels
            screen_height: Height of the screen in pixels
            emoji_count: Number of emojis to display
            
        Returns:
            Tuple of (width, height) for each emoji in pixels
        """
        try:
            # Calculate optimal grid layout
            cols = min(emoji_count, 3)  # Max 3 emojis per row
            rows = (emoji_count + cols - 1) // cols
            
            # Calculate maximum possible size
            max_width = (screen_width * 0.9) // cols  # 90% of screen width
            max_height = (screen_height * 0.6) // rows  # 60% of screen height
            
            # Use the smaller dimension to maintain square aspect ratio
            size = min(max_width, max_height)
            
            # Ensure minimum size
            size = max(50, size)  # Minimum 50px
            
            logger.info(f"Calculated emoji size: {size}x{size} pixels")
            return (int(size), int(size))
            
        except Exception as e:
            logger.error(f"Failed to calculate emoji size: {str(e)}")
            raise

    def get_emoji_layout(self, emojis: List[str], screen_width: int, screen_height: int) -> List[dict]:
        """
        Get the layout information for displaying emojis.
        
        Args:
            emojis: List of emojis to display
            screen_width: Width of the screen in pixels
            screen_height: Height of the screen in pixels
            
        Returns:
            List of dicts containing emoji and its display properties
        """
        try:
            size = self.calculate_emoji_size(screen_width, screen_height, len(emojis))
            
            layout = []
            for emoji_char in emojis:
                layout.append({
                    "emoji": emoji_char,
                    "size": size
                })
            
            return layout
            
        except Exception as e:
            logger.error(f"Failed to generate emoji layout: {str(e)}")
            raise

# Example usage:
if __name__ == "__main__":
    manager = EmojiManager()
    try:
        # Generate 5 random emojis
        emojis = manager.get_random_emojis(5)
        print(f"Random emojis: {emojis}")
        
        # Calculate layout for 1920x1080 screen
        layout = manager.get_emoji_layout(emojis, 1920, 1080)
        print(f"Layout: {layout}")
    except Exception as e:
        logger.error(f"Example usage failed: {str(e)}")
