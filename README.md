# 📝 note — CLI Note Tool for Linux

A simple command-line note-taking tool for Linux, storing notes in a local SQLite database.

## Requirements
- Python 3.x (no external dependencies)

## Installation
```bash
git clone git@github.com:Dr00pyd00/note_tool_linux.git
sudo mv note_tool_linux/notes_rapide.py /usr/bin/note
sudo chmod 755 /usr/bin/note
```

## Usage
```bash
# Add a note
note "my note here"

# Show all notes
note

# Zoom on a specific note
note -z <id>

# Delete a note by id
note -d <id>

# Reset all notes
note --reset

# Save command output as a note
note "$(ip a)"
```

## Database location
Notes are stored in `~/.local/share/note/note.db` — automatically created on first launch.

## Built with
- Python 3 standard library
- sqlite3
- argparse
- pathlib
