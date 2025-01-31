"""
Data storage implementation for the Emoji Story Builder.
Handles JSON operations with atomic writes and ISO 8601 timestamps.
"""

import json
import os
from datetime import datetime
import shutil
from typing import Dict, List, Optional, Any
from uuid import uuid4

try:
    from filelock import FileLock
except ImportError:
    print("Error: 'filelock' package not installed. Please run: pip install -r requirements.txt")
    raise

from src.logger import get_logger

# Ensure required directories exist
os.makedirs('logs', exist_ok=True)
os.makedirs('data', exist_ok=True)

logger = get_logger()

class DataStore:
    def __init__(self, data_dir: str = "data"):
        """Initialize the data store with the specified data directory."""
        try:
            self.data_dir = data_dir
            self.data_file = os.path.join(data_dir, "sessions.json")
            self.lock_file = f"{self.data_file}.lock"
            
            # Ensure data directory exists
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                logger.info(f"Created data directory: {data_dir}")
            
            # Initialize data file if it doesn't exist
            if not os.path.exists(self.data_file):
                self._initialize_data_file()
                
        except Exception as e:
            logger.error(f"Failed to initialize DataStore: {str(e)}")
            raise

    def _initialize_data_file(self) -> None:
        """Create the initial data file structure."""
        try:
            with FileLock(self.lock_file):
                initial_data = {
                    "sessions": []
                }
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(initial_data, f, indent=2)
                logger.info(f"Initialized data file: {self.data_file}")
        except Exception as e:
            logger.error(f"Failed to initialize data file: {str(e)}")
            raise

    def _read_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Read the current data from the JSON file."""
        try:
            with FileLock(self.lock_file):
                if not os.path.exists(self.data_file):
                    logger.warning("Data file not found, creating new one")
                    self._initialize_data_file()
                
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info("Successfully read data file")
                    return data
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in data file: {str(e)}")
            # Backup corrupted file
            backup_file = f"{self.data_file}.backup"
            shutil.copy2(self.data_file, backup_file)
            logger.info(f"Backed up corrupted file to: {backup_file}")
            # Create new data file
            self._initialize_data_file()
            return {"sessions": []}
        except Exception as e:
            logger.error(f"Failed to read data: {str(e)}")
            raise

    def _write_data(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        """Write data to the JSON file atomically."""
        temp_file = f"{self.data_file}.tmp"
        try:
            with FileLock(self.lock_file):
                # Write to temporary file first
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                
                # Rename temporary file to actual file (atomic operation)
                os.replace(temp_file, self.data_file)
                logger.info("Successfully wrote data to file")
        except Exception as e:
            logger.error(f"Failed to write data: {str(e)}")
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    logger.info("Cleaned up temporary file")
                except Exception as cleanup_error:
                    logger.error(f"Failed to clean up temporary file: {str(cleanup_error)}")
            raise

    def save_session(self, emojis: List[str], notes: str, session_id: Optional[str] = None) -> str:
        """
        Save a new session with emojis and notes.
        
        Args:
            emojis: List of emojis used in the session
            notes: User's notes for the session
            session_id: Optional session ID (will be generated if not provided)
            
        Returns:
            session_id: The ID of the saved session
        """
        try:
            if session_id is None:
                session_id = str(uuid4())

            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            
            new_session = {
                "session_id": session_id,
                "timestamp": timestamp,
                "emojis": emojis,
                "notes": notes
            }
            
            data = self._read_data()
            data["sessions"].append(new_session)
            self._write_data(data)
            
            logger.info(f"Session saved successfully: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to save session: {str(e)}")
            raise

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific session by ID."""
        try:
            data = self._read_data()
            for session in data["sessions"]:
                if session["session_id"] == session_id:
                    logger.info(f"Retrieved session: {session_id}")
                    return session
            logger.warning(f"Session not found: {session_id}")
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve session {session_id}: {str(e)}")
            raise

    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Retrieve all sessions."""
        try:
            data = self._read_data()
            sessions = data["sessions"]
            logger.info(f"Retrieved {len(sessions)} sessions")
            return sessions
        except Exception as e:
            logger.error(f"Failed to retrieve all sessions: {str(e)}")
            raise

# Example usage:
if __name__ == "__main__":
    data_store = DataStore()
    try:
        session_id = data_store.save_session(
            emojis=["😊", "🌟", "🎉"],
            notes="Test session"
        )
        print(f"Saved session: {session_id}")
        
        session = data_store.get_session(session_id)
        print(f"Retrieved session: {session}")
    except Exception as e:
        logger.error(f"Example usage failed: {str(e)}")
