# System Patterns

## Architecture Overview

### Design Patterns
1. **Singleton Pattern**
   - Used in Logger implementation
   - Ensures single point of logging across application
   - Maintains consistent log format and handling

2. **Repository Pattern**
   - Applied to JSON data storage
   - Centralizes data access logic
   - Handles atomic file operations

3. **Service Pattern**
   - Emoji Manager service for emoji operations
   - Screen Calculator service for layout optimization
   - Session Manager service for state tracking

## Key Technical Decisions

### 1. Data Storage
- **Decision**: Single JSON file for all sessions
- **Rationale**: 
  * Simplifies data management
  * Easier backup and version control
  * Reduces file system complexity
- **Implementation**:
  * Atomic write operations
  * File locking for concurrent access
  * Regular backups (if implemented)

### 2. Error Logging
- **Decision**: Append-only log file with rotation
- **Rationale**:
  * Preserves error history
  * Prevents data loss
  * Enables long-term tracking
- **Implementation**:
  * ISO 8601 timestamps
  * Detailed stack traces
  * Context preservation

### 3. UI Framework
- **Decision**: Streamlit
- **Rationale**:
  * Rapid development
  * Built-in responsive design
  * Python-native implementation
  * Simple state management
- **Implementation**:
  * Component-based layout
  * Session state handling
  * Dynamic rendering

### 4. Emoji Management
- **Decision**: Session-based uniqueness tracking
- **Rationale**:
  * Prevents repetition
  * Maintains user engagement
  * Simplifies state management
- **Implementation**:
  * Set-based tracking
  * Session-scoped storage
  * Efficient lookup

## Code Organization

### Directory Structure
```
src/
├── app.py              # Entry point
├── emoji_manager.py    # Emoji operations
├── data_store.py       # Data persistence
├── logger.py           # Error logging
└── utils/             # Shared utilities
```

### Module Responsibilities
1. **app.py**
   - UI layout and rendering
   - Event handling
   - State management

2. **emoji_manager.py**
   - Random emoji generation
   - Uniqueness checking
   - Size calculations

3. **data_store.py**
   - JSON file operations
   - Data structure maintenance
   - Atomic updates

4. **logger.py**
   - Error capturing
   - Log rotation
   - Format standardization

## Best Practices

### Error Handling
```python
try:
    # Operation
    pass
except Exception as e:
    logger.error(f"[Operation Name] {str(e)}", exc_info=True)
    # Handle error appropriately
```

### Data Operations
```python
def save_session(data):
    try:
        with FileLock("sessions.json.lock"):
            # Atomic write operation
            pass
    except Exception as e:
        logger.error("[Data Store] Save failed", exc_info=True)
        raise
```

### UI Components
```python
def render_emoji_section():
    try:
        st.container()
        # Render emojis with calculated size
    except Exception as e:
        logger.error("[UI] Render failed", exc_info=True)
        st.error("Display error occurred")
