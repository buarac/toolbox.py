# ✅ Completed Backlog

## Sprint 0: Architecture & Foundations
- Initialized directory structure (`/scripts`, `/core`, `/docs`).
- Created `requirements.txt` & `pyproject.toml`.
- Developed `core/system_check.py` (OS/Python validation).
- Configured `.cursorrules` for agentic workflows.
- Validated environment (Python 3.12+).

## Feature: Image Resizer
- Implemented `scripts/image_resizer/resizer.py`.
- Added `Pillow` dependency.
- Verified batch processing and optimization.

## Refactor: Emoji Logging
- Updated project rules to mandate emojis in logs.
- Refactored `system_check.py` and `resizer.py` outputs.

## Feature: File Cleaner
- Implemented `scripts/file_cleaner/cleaner.py`.
- Features: Age filter (days), Dry-run, Confirmation prompt.
- Verified on macOS (`st_birthtime`).
- **Refactor**: Verbose mode listing all files with 🗑️/🛡️.
- **Fix**: Ignore hidden files (e.g. `.DS_Store`).
- **Feature**: Depth control (`--depth`). Defaults to current directory (1). Recursion is optional.

## Lot 1: The "Toolbox" Core
- **toolbox.py**: Central CLI (`list`, `run`, `new`).
- **Discovery**: Automatically finds scripts in `/scripts`.
- **Scaffolding**: `new` command creates standardized script templates.
- **Micro-UX**: `list` shows descriptions, `./toolbox.py` executable directly.
- **Git Health**: `git_health` tool for quick repo audit (branches, dirty state) using `GitPython`.
- **Disk Usage**: `usage` tool to calculate and display directory sizes (recursive) with depth control.

## Lot 2: Dependency Management
- **Isolation**: Removed script-specific deps from global `requirements.txt`.
- **Local Requirements**: Added `requirements.txt` to `image_resizer` and `git_health`.
- **Auto-Detection**: `toolbox.py` checks dependencies before execution.
- **Install Command**: Added `check-deps` via `toolbox.py install <tool>`.
- **UX**: Helpful error messages with venv instructions for PEP 668 environments.
