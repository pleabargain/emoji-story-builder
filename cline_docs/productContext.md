# Product Context

## Purpose
The Emoji Story Builder exists to facilitate creative storytelling and communication through emojis. It helps people express themselves and talk about random topics in a fun, visual way by providing randomly generated emoji combinations that can spark conversations or storytelling sessions.

## Problems Solved
1. **Creative Block**: By providing random emojis, the application helps overcome initial creative blocks in starting conversations or stories.
2. **Visual Expression**: Enables users to complement their written notes with visual elements (emojis) that can convey emotion and context.
3. **Session Persistence**: Maintains a history of all interactions with proper timestamps, allowing users to track their storytelling journey.
4. **Screen Optimization**: Automatically calculates and adjusts emoji sizes to ensure optimal visibility regardless of the number of emojis displayed.

## How It Works

### Core Functionality
1. **Emoji Generation**
   - Users specify desired number of emojis (1-10)
   - System ensures no emoji repeats within the same session
   - Emojis are sized dynamically to fit the screen

2. **Note Taking**
   - Users can add detailed notes alongside their emoji combinations
   - Notes are preserved with ISO-formatted timestamps
   - All data is stored in a centralized JSON file

3. **Session Management**
   - Clear button to reset current session
   - Generate new random emojis without losing previous entries
   - All interactions are logged with proper timestamps

### Data Management
- Single JSON file stores all sessions
- Each entry includes:
  * ISO 8601 timestamp
  * Selected emojis
  * User notes
  * Unique session identifier

### Error Handling
- Comprehensive error logging system
- Logs are appended, never overwritten
- All functions include proper error handling
- Errors are logged with timestamps and full context

## Success Criteria
1. Users can easily generate random emoji combinations
2. Emojis are properly sized and visible
3. Notes are successfully saved and retrieved
4. Session history is maintained accurately
5. Error logging captures all issues without data loss
