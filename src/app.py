"""
Main Streamlit application for the Emoji Story Builder.
Provides UI for emoji display, note taking, and session management.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import requests

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
    from src.ollama_client import OllamaClient
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
        return EmojiManager(), DataStore(), OllamaClient()
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
        if 'generated_story' not in st.session_state:
            st.session_state.generated_story = ""
        if 'browser_logs' not in st.session_state:
            st.session_state.browser_logs = []
        if 'last_log_index' not in st.session_state:
            st.session_state.last_log_index = 0
    except Exception as e:
        logger.error(f"Failed to initialize session state: {str(e)}")
        st.error("Failed to initialize session state. Please refresh the page.")
        raise

def render_emoji_section(emoji_manager: EmojiManager):
    """Render the emoji display section using responsive Streamlit columns."""
    try:
        if st.session_state.current_emojis:
            # Create a responsive grid using st.columns
            # We use 5 columns for a good distribution on most screens
            num_emojis = len(st.session_state.current_emojis)
            cols_per_row = 5
            
            # Use custom CSS for the emoji styling
            st.markdown("""
                <style>
                .emoji-container {
                    font-size: 4rem;
                    text-align: center;
                    padding: 10px;
                    transition: transform 0.2s;
                }
                .emoji-container:hover {
                    transform: scale(1.2);
                }
                </style>
            """, unsafe_allow_html=True)

            # Display emojis in a grid
            for i in range(0, num_emojis, cols_per_row):
                batch = st.session_state.current_emojis[i:i + cols_per_row]
                cols = st.columns(cols_per_row)
                for idx, emoji_char in enumerate(batch):
                    with cols[idx]:
                        st.markdown(
                            f"<div class='emoji-container'>{emoji_char}</div>",
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

def browser_log(tag, data):
    """Log data to the browser's developer console via session state collector."""
    if 'browser_logs' not in st.session_state:
        st.session_state.browser_logs = []
    
    st.session_state.browser_logs.append({
        "timestamp": datetime.now().isoformat(),
        "tag": tag,
        "payload": data
    })

def flush_browser_logs():
    """Flush pending browser logs in a single batch to reduce console noise."""
    import json
    import streamlit.components.v1 as components
    
    if 'browser_logs' not in st.session_state or 'last_log_index' not in st.session_state:
        return
        
    pending_logs = st.session_state.browser_logs[st.session_state.last_log_index:]
    if not pending_logs:
        return
        
    log_js = "".join([f"console.log({json.dumps(log)});" for log in pending_logs])
    components.html(
        f"<script>{log_js}</script>",
        height=0,
        width=0
    )
    st.session_state.last_log_index = len(st.session_state.browser_logs)

def render_mermaid(code: str) -> None:
    """Render a mermaid diagram using a custom HTML component."""
    import streamlit.components.v1 as components
    
    # Strip whitespace to prevent rendering issues
    # Note: We do not escape HTML here because it breaks Mermaid syntax (e.g. --> becomes -&gt;)
    clean_code = code.strip()
    
    components.html(
        f"""
        <pre class="mermaid">
            {clean_code}
        </pre>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true, theme: 'dark', securityLevel: 'loose' }});
        </script>
        """,
        height=500,
        scrolling=True
    )

def markdown_with_mermaid(markdown_text: str) -> None:
    """Render markdown text with support for Mermaid diagrams."""
    parts = markdown_text.split("```mermaid")
    
    # Render the first part (regular markdown)
    if parts[0].strip():
        st.markdown(parts[0])
    
    # Iterate over the remaining parts
    for part in parts[1:]:
        # Split into the diagram code and the rest of the markdown
        if "```" in part:
            mermaid_code, rest = part.split("```", 1)
            render_mermaid(mermaid_code)
            if rest.strip():
                st.markdown(rest)
        else:
            # Fallback if text parsing fails
            st.markdown("```mermaid" + part)

def main():
    """Main application entry point."""
    print("[Emoji Story Builder] Starting main application...")
    try:
        st.title("Emoji Story Builder")
        print("[Emoji Story Builder] Rendering title...")
        
        # Initialize services and session state
        try:
            print("[Emoji Story Builder] Initializing services...")
            emoji_manager, data_store, ollama_client = init_services()
            print("[Emoji Story Builder] Services initialized.")
            init_session_state()
            print("[Emoji Story Builder] Session state initialized.")
        except Exception as e:
            print(f"[Emoji Story Builder] Initialization failed: {str(e)}")
            logger.error(f"Initialization failed: {str(e)}")
            st.error("Failed to initialize application. Please ensure all dependencies are installed.")
            return

        # Create tabs
        print("[Emoji Story Builder] Creating tabs...")
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

            # --- Story Generation Controls ---
            st.divider()
            
            # Check Ollama Status
            ollama_online, status_msg = ollama_client.check_status()
            if ollama_online:
                st.success(f"🟢 {status_msg}")
            else:
                st.error(f"🔴 {status_msg} - Please start Ollama to enable story generation.")

            # Get available models
            models = []
            selected_model = None
            if ollama_online:
                models = ollama_client.get_available_models()
                if not models:
                    st.warning("No local models found. Use 'ollama pull <modelname>' to download one.")
                else:
                    selected_model = st.selectbox(
                        "Select Ollama Model",
                        options=models,
                        index=0,
                        help="Choose the model to use for story generation."
                    )

            if st.session_state.current_emojis:
                st.markdown("**Generate a Story from these Emojis**")
                word_count = st.slider(
                    "Approximate Story Length (words)",
                    min_value=50,
                    max_value=500,
                    value=150,
                    step=10,
                    help="Target number of words for the generated story."
                )
                temperature = st.slider(
                    "Creativity (Temperature)",
                    min_value=0.1,
                    max_value=1.5,
                    value=1.2,
                    step=0.05,
                    help="Higher values = more creative, lower = more focused."
                )
                
                if st.button("Generate Story from Emojis", disabled=not (ollama_online and selected_model)):
                    try:
                        # Log the request to browser console
                        browser_log("OLLAMA_REQUEST", {
                            "model": selected_model,
                            "emojis": st.session_state.current_emojis,
                            "word_count": word_count,
                            "temperature": temperature
                        })
                        
                        with st.spinner(f"Generating story using {selected_model}..."):
                            story = ollama_client.generate_story(
                                st.session_state.current_emojis,
                                model=selected_model,
                                word_count=word_count,
                                temperature=temperature
                            )
                        
                        # Log the response to browser console
                        browser_log("OLLAMA_RESPONSE", {"story_length": len(story), "story_preview": story[:100] + "..."})
                        
                        st.session_state.generated_story = story
                        st.rerun() # Force a rerun to update the text area immediately
                    except Exception as e:
                        logger.error(f"Failed to generate story: {str(e)}")
                        st.error("Failed to generate story. Please check Ollama server and try again.")
                
                if st.session_state.generated_story:
                    st.text_area(
                        "Generated Story",
                        value=st.session_state.generated_story,
                        height=250,
                        key="generated_story_area"
                    )
            # --- End Story Generation Controls ---

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

            # --- Debug Console ---
            st.divider()
            with st.expander("🛠️ Debug Console", expanded=False):
                st.write("### Application State")
                st.json({
                    "current_emojis": st.session_state.current_emojis,
                    "generated_story_length": len(st.session_state.get('generated_story', '')),
                    "ollama_status": status_msg,
                    "timestamp": datetime.now().isoformat()
                })
                st.write("### Internal Logs")
                # Showing a mock log for now or we could read from logs/error.log
                try:
                    with open('logs/error.log', 'r') as f:
                        log_lines = f.readlines()
                        st.text_area("Recent Logs", value="".join(log_lines[-10:]), height=150)
                except:
                    st.info("No logs found yet.")

        with readme_tab:
            try:
                # readme.md is in the project root
                with open('readme.md', 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                markdown_with_mermaid(readme_content)
            except Exception as e:
                logger.error(f"Failed to load readme: {str(e)}")
                st.error("Failed to load documentation. Please check if readme.md exists.")

        # History tab content
        with history_tab:
            try:
                print("[Emoji Story Builder] Rendering History tab...")
                with open('data/sessions.json', 'r', encoding='utf-8') as f:
                    sessions_json = f.read()
                st.code(sessions_json, language='json')
            except Exception as e:
                print(f"[Emoji Story Builder] History tab error: {str(e)}")
                logger.error(f"Failed to load sessions history: {str(e)}")
                st.error("Failed to load sessions history. Please check if sessions.json exists.")
        
        print("[Emoji Story Builder] Main loop complete.")
        # Flush logs at the end of the run
        flush_browser_logs()
    except Exception as e:
        print(f"[Emoji Story Builder] Critical application error: {str(e)}")
        logger.error(f"Application error: {str(e)}")
        st.error("An error occurred. Please refresh the page and try again.")

if __name__ == "__main__":
    main()
    print("[Emoji Story Builder] Script execution finished.")
    
