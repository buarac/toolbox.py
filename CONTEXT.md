# 🧠 Application Context

## 🏗️ Architecture
- **Modular Design**: Scripts are isolated in `scripts/`, sharing common utilities from `core/`.
- **Dependency Management**: Single `requirements.txt` at root.
- **Portability**: Code must use `pathlib` for paths and handle OS differences (macOS/Linux).

## 🔄 Current State
- **Phase**: Lot 2 - Dependency Management (Upcoming)
- **Status**: Toolbox Core & Git Health Check implemented.
- **Core Components**:
    - `toolbox.py`: Central CLI (list, run, new).
    - `core/system_check.py`: Validates environment.
    - `scripts/`:
        - `image_resizer/`: JPEG batch processing.
        - `file_cleaner/`: File cleanup (depth control, dry-run).
        - `git_health/`: Git repository audit.
        - `disk_usage/`: Directory size calculator.

## 📅 Next Steps
- Automate dependency management (Lot 2).
- Improve cross-platform path handling.
