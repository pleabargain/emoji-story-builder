"""
Main Streamlit application for the Emoji Story Builder.
Provides UI for emoji display, note taking, and session management.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure src directory is in Python path for absolute imports
src_dir = str(Path(__file__).parent.parent)
if src_dir not in sys.path:
    sys.path.append(src_dir)

# Initialize logging before any imports
try:
    from src.logger import get_logger
    logger = get_logger()
except Exception as e:
    print(f"Failed to initialize logger: {str(e)}", file=sys.stderr)
    sys.exit(1)

# Import dependencies with error logging
try:
    import streamlit as st
except ImportError as e:
    logger.error(f"Failed to import streamlit: {str(e)}")
    print("Error: 'streamlit' package not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)

try:
    from src.emoji_manager import EmojiManager
    from src.data_store import DataStore
except ImportError as e:
    logger.error(f"Failed to import application modules: {str(e)}")
    print(f"Error: Failed to import required modules: {str(e)}")
    sys.exit(1)

# Ensure required directories exist
os.makedirs('logs', exist_ok=True)
os.makedirs('data', exist_ok=True)

logger = get_logger()

# Initialize services
@st.cache_resource
def init_services():
    """Initialize application services."""
    try:
        return EmojiManager(), DataStore()
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")
        st.error("Failed to initialize application services. Please check the logs and ensure all dependencies are installed.")
        raise

def init_session_state():
    """Initialize session state variables."""
    try:
        if 'current_emojis' not in st.session_state:
            st.session_state.current_emojis = []
        if 'notes' not in st.session_state:
            st.session_state.notes = ""
    except Exception as e:
        logger.error(f"Failed to initialize session state: {str(e)}")
        st.error("Failed to initialize session state. Please refresh the page.")
        raise

def render_emoji_section(emoji_manager: EmojiManager):
    """Render the emoji display section."""
    try:
        # Get screen dimensions from Streamlit's current layout
        screen_width = 800  # Default width
        screen_height = 600  # Default height
        
        if st.session_state.current_emojis:
            # Calculate layout for current emojis
            layout = emoji_manager.get_emoji_layout(
                st.session_state.current_emojis,
                screen_width,
                screen_height
            )
            
            # Display emojis in a grid
            cols = st.columns(min(len(layout), 3))
            for idx, item in enumerate(layout):
                col_idx = idx % 3
                with cols[col_idx]:
                    st.markdown(
                        f"<div style='font-size: {item['size'][0]}px; text-align: center;'>{item['emoji']}</div>",
                        unsafe_allow_html=True
                    )
        else:
            st.info("Generate some emojis to get started!")
            
    except Exception as e:
        logger.error(f"Failed to render emoji section: {str(e)}")
        st.error("Failed to display emojis. Please try again.")

def save_current_session(data_store: DataStore):
    """Save the current session to storage."""
    try:
        if st.session_state.current_emojis:
            data_store.save_session(
                emojis=st.session_state.current_emojis,
                notes=st.session_state.notes
            )
            logger.info("Session saved successfully")
    except Exception as e:
        logger.error(f"Failed to save session: {str(e)}")
        st.error("Failed to save session. Please try again.")

def main():
    """Main application entry point."""
    try:
        st.title("Emoji Story Builder")
        
        # Initialize services and session state
        try:
            emoji_manager, data_store = init_services()
            init_session_state()
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            st.error("Failed to initialize application. Please ensure all dependencies are installed.")
            return

        # Create tabs
        main_tab, history_tab, readme_tab = st.tabs(["Story Builder", "History", "Documentation"])

        # Main tab content
        with main_tab:
        
            # Emoji count selector
            emoji_count = st.number_input(
                "Number of Emojis",
                min_value=1,
                max_value=10,
                value=3
            )
        
            # Control buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Generate New Emojis"):
                    try:
                        st.session_state.current_emojis = emoji_manager.get_random_emojis(emoji_count)
                        save_current_session(data_store)
                    except Exception as e:
                        logger.error(f"Failed to generate emojis: {str(e)}")
                        st.error("Failed to generate emojis. Please try again.")
                
            with col2:
                if st.button("Clear Results"):
                    try:
                        st.session_state.current_emojis = []
                        st.session_state.notes = ""
                        emoji_manager.reset_session()
                        logger.info("Session cleared")
                    except Exception as e:
                        logger.error(f"Failed to clear session: {str(e)}")
                        st.error("Failed to clear results. Please try again.")
            
            # Render emoji section
            render_emoji_section(emoji_manager)
            
            # Notes section
            try:
                st.text_area(
                    "Your Story",
                    key="notes",
                    height=200,
                    placeholder="Write your story here...",
                    on_change=lambda: save_current_session(data_store)
                )
            except Exception as e:
                logger.error(f"Failed to render notes section: {str(e)}")
                st.error("Failed to display notes section. Please refresh the page.")
            
            # Display session history
            if st.checkbox("Show Session History"):
                try:
                    sessions = data_store.get_all_sessions()
                    for session in sessions:
                        with st.expander(f"Session from {session['timestamp']}"):
                            st.write("Emojis: " + " ".join(session["emojis"]))
                            st.write("Notes:", session["notes"])
                except Exception as e:
                    logger.error(f"Failed to display session history: {str(e)}")
                    st.error("Failed to load session history.")

        # Readme tab content
        with readme_tab:
            try:
                with open('readme.md', 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                st.markdown(readme_content)
            except Exception as e:
                logger.error(f"Failed to load readme: {str(e)}")
                st.error("Failed to load documentation. Please check if readme.md exists.")

        # History tab content
        with history_tab:
            try:
                with open('data/sessions.json', 'r', encoding='utf-8') as f:
                    sessions_json = f.read()
                st.code(sessions_json, language='json')
            except Exception as e:
                logger.error(f"Failed to load sessions history: {str(e)}")
                st.error("Failed to load sessions history. Please check if sessions.json exists.")
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An error occurred. Please refresh the page and try again.")

if __name__ == "__main__":
    main()
