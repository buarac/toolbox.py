# 🐍 Python Automation Toolbox

A structured, portable (macOS & Ubuntu) ecosystem for Python utility scripts.

## 🚀 Features
- Modular architecture (`/scripts`, `/core`)
- Centralized dependency management
- CLI entry point (`toolbox.py` - *Coming Soon*)
- Cross-platform compatibility (macOS/Linux)

## 🛠️ Setup

1. **Prerequisites**
   - Python 3.12+
   - macOS 14+ (Sonoma) or Ubuntu 22.04+

2. **Installation**
   ```bash
   # Clone the repo (if not already done)
   
   # Create virtual environment
   python3 -m venv .venv
   source .venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Verification**
   Run the system check to verify compatibility:
   ```bash
   python3 core/system_check.py
   ```

## 📂 Structure
- `scripts/`: Utility scripts.
    - `image_resizer/`: Batch JPEG resizer & compressor.
- `core/`: Shared utilities and internal logic.
- `docs/`: Documentation.
