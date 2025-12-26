# 🐍 Python Automation Toolbox

A structured, portable (macOS & Ubuntu) ecosystem for Python utility scripts.

## 🚀 Features
- **Central CLI**: `toolbox.py` to manage and run all tools.
- **Modular Tools**:
    - `image_resizer`: Batch resize/compress images.
    - `file_cleaner`: Auto-delete old files with safety checks.
    - `git_health`: Quick audit of git repo status.
- **Dependency Management**:
    - Automatic dependency check before launch.
    - `install` command to setup environment.
    - Per-script `requirements.txt`.

## 🛠️ Usage

### General
Use the `toolbox.py` CLI to discover and run tools:
```bash
./toolbox.py list             # List all available tools
./toolbox.py new [name]       # Create a new tool
./toolbox.py install [tool]   # Install dependencies for a tool
./toolbox.py run [tool_name]  # Run a specific tool (auto-checks deps)

```

### Examples
**File Cleaner**:
```bash
./toolbox.py run cleaner -- --directory ~/Downloads --days 30 --dry-run
```

**Git Health**:
```bash
./toolbox.py run git_health
```

**Disk Usage**:
```bash
./toolbox.py run usage -- --path ~/Projects --depth 2
```

## 📂 Structure
- `toolbox.py`: Entry point.
- `scripts/`: Utility scripts.
- `core/`: Shared utilities.
- `docs/`: Documentation.
