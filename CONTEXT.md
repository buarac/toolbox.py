# 🧠 Application Context

## 🏗️ Architecture
- **Modular Design**: Scripts are isolated in `scripts/`, sharing common utilities from `core/`.
- **Dependency Management**: Single `requirements.txt` at root.
- **Portability**: Code must use `pathlib` for paths and handle OS differences (macOS/Linux).

## 🔄 Current State
- **Phase**: Sprint 0 - COMPLETE
- **Status**: Feature "File Cleaner" completed.
- **Core Components**:
    - `core/system_check.py`: Validates environment.
    - `.cursorrules`: Project rules.
    - `scripts/image_resizer/`: JPEG batch processing tool.
    - `scripts/file_cleaner/`: File cleanup utility.

## 📅 Next Steps
- Complete Sprint 0 validation.
- Begin Lot 1: `toolbox.py` CLI development.
