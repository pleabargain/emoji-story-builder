"""
Test script to verify logger functionality.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.logger import get_logger

def test_logging():
    """Test various logging levels and verify log file creation."""
    logger = get_logger()
    
    print("\nTesting logger functionality...")
    
    # Test each log level
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    
    try:
        # Simulate an error
        raise ValueError("Test error for logging")
    except Exception as e:
        logger.error(f"This is an error message: {str(e)}")
    
    # Verify log file exists
    log_file = 'logs/error.log'
    if os.path.exists(log_file):
        print(f"\nLog file created successfully at: {log_file}")
        print("Recent log contents:")
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                # Read last few lines
                lines = f.readlines()
                for line in lines[-5:]:  # Show last 5 lines
                    print(line.strip())
        except Exception as e:
            print(f"Error reading log file: {str(e)}")
    else:
        print(f"\nError: Log file not found at: {log_file}")

if __name__ == "__main__":
    test_logging()
