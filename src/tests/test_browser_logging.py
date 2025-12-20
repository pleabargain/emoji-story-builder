import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

class TestBrowserLogging(unittest.TestCase):
    @patch('streamlit.components.v1.html')
    def test_browser_log_unified(self, mock_html):
        """Verify that browser_log collects and flush_browser_logs signals."""
        import streamlit as st
        from src.app import browser_log, flush_browser_logs, init_session_state
        
        # Initialize session state for test
        init_session_state()
        st.session_state.browser_logs = []
        st.session_state.last_log_index = 0
        
        test_tag = "TEST_TAG"
        test_data = {"key": "value"}
        
        print(f"\n[Test] Verifying unified browser logging...")
        print("      - Rationale: Ensure logs are collected and sent in a single batch to reduce noise.")
        
        # 1. Test collection
        browser_log(test_tag, test_data)
        self.assertEqual(len(st.session_state.browser_logs), 1)
        self.assertFalse(mock_html.called) # Should not be called yet
        
        # 2. Test flushing
        flush_browser_logs()
        self.assertTrue(mock_html.called)
        
        # Verify the content contains the log data
        args, kwargs = mock_html.call_args
        html_content = args[0]
        self.assertIn("<script>console.log(", html_content)
        self.assertIn(test_tag, html_content)
        
        # 3. Verify index update
        self.assertEqual(st.session_state.last_log_index, 1)
        
        # 4. Verify second flush is empty if no new logs
        mock_html.reset_mock()
        flush_browser_logs()
        self.assertFalse(mock_html.called)

if __name__ == '__main__':
    unittest.main()
