"""
Logger implementation for the Emoji Story Builder.
Implements singleton pattern for centralized logging with ISO 8601 timestamps.
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

# Ensure logs directory exists
try:
    os.makedirs('logs', exist_ok=True)
except Exception as e:
    print(f"Error creating logs directory: {str(e)}")
    raise

class Logger:
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> 'Logger':
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self) -> None:
        """Initialize the logger with proper format and handlers."""
        if self._logger is not None:
            return

        try:
            # Initialize logger
            self._logger = logging.getLogger('emoji_story_builder')
            self._logger.setLevel(logging.DEBUG)

            # Create formatter with ISO 8601 timestamps
            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%dT%H:%M:%S'  # Simplified format to avoid errors
            )

            # File handler with daily rotation
            try:
                file_handler = TimedRotatingFileHandler(
                    'logs/error.log',
                    when='midnight',
                    interval=1,
                    backupCount=30,
                    encoding='utf-8'
                )
                file_handler.setFormatter(formatter)
                file_handler.setLevel(logging.ERROR)
                self._logger.addHandler(file_handler)
            except Exception as e:
                print(f"Error setting up file handler: {str(e)}")
                raise

            # Stream handler for console output
            try:
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(formatter)
                console_handler.setLevel(logging.INFO)
                self._logger.addHandler(console_handler)
            except Exception as e:
                print(f"Error setting up console handler: {str(e)}")
                raise

            # Log initialization success
            self._logger.info("Logger initialized successfully")

        except Exception as e:
            print(f"Error initializing logger: {str(e)}")
            raise

    def _ensure_logger(self) -> None:
        """Ensure logger is initialized."""
        if self._logger is None:
            self._initialize_logger()

    def _log(self, level: int, message: str, exc_info: bool = False) -> None:
        """Internal method to handle logging with proper timestamp conversion."""
        try:
            self._ensure_logger()
            if self._logger is None:
                raise RuntimeError("Logger initialization failed")
            
            # Ensure timestamp is in UTC
            from datetime import timezone
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
            formatted_message = f"{message}"
            
            self._logger.log(level, formatted_message, exc_info=exc_info)
        except Exception as e:
            # If logging fails, print to stderr as last resort
            print(f"Logging failed: {str(e)}", file=sys.stderr)
            if exc_info:
                import traceback
                traceback.print_exc(file=sys.stderr)

    def error(self, message: str, exc_info: bool = True) -> None:
        """Log an error message with stack trace."""
        try:
            self._log(logging.ERROR, message, exc_info)
        except Exception as e:
            print(f"Error logging failed: {str(e)}", file=sys.stderr)
            if exc_info:
                import traceback
                traceback.print_exc(file=sys.stderr)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        try:
            self._log(logging.WARNING, message)
        except Exception as e:
            print(f"Warning logging failed: {str(e)}", file=sys.stderr)

    def info(self, message: str) -> None:
        """Log an info message."""
        try:
            self._log(logging.INFO, message)
        except Exception as e:
            print(f"Info logging failed: {str(e)}", file=sys.stderr)

    def debug(self, message: str) -> None:
        """Log a debug message."""
        try:
            self._log(logging.DEBUG, message)
        except Exception as e:
            print(f"Debug logging failed: {str(e)}", file=sys.stderr)

# Global logger instance
try:
    logger = Logger()
except Exception as e:
    print(f"Failed to create global logger instance: {str(e)}", file=sys.stderr)
    raise

def get_logger() -> Logger:
    """Get the global logger instance."""
    return logger

# Example usage:
if __name__ == '__main__':
    logger = get_logger()
    try:
        raise ValueError("Test error")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
