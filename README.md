# 🐍 Python Automation Toolbox

A structured, portable (macOS & Ubuntu) ecosystem for Python utility scripts.

## 🚀 Features
- **Central CLI**: `toolbox.py` to manage and run all tools.
- **Modular Tools**:
    - `resizer`: Batch resize/compress images.
    - `cleaner`: Auto-delete old files with safety checks.
    - `git_health`: Quick audit of git repo status.
    - `usage`: Calculate disk usage for directories.
    - `weather`: 7-day weather forecast with rich HTML report.
    - `web_scraper`: Two-step (scan/scrape) site-to-markdown converter.
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
./toolbox.py check            # Run code quality checks (linting/format)


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

**Web Scraper**:
```bash
# Step 1: Scan
./toolbox.py run web_scraper -- --url "https://example.com" --output "docs" --step scan

# Step 2: Scrape
./toolbox.py run web_scraper -- --output "docs" --step scrape
```

## 📂 Structure
- `toolbox.py`: Entry point.
- `scripts/`: Utility scripts.
- `core/`: Shared utilities.
- `docs/`: Documentation.
