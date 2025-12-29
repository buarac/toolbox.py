# 🧠 Application Context

## 🏗️ Architecture
- **Modular Design**: Scripts are isolated in `scripts/`, sharing common utilities from `core/`.
- **Dependency Management**: Hybrid. Global `requirements.txt` for dev tools, per-script `requirements.txt` for individual tools.
- **Portability**: Code must use `pathlib` for paths and handle OS differences (macOS/Linux).

## 🔄 Current State
- **Phase**: Maintenance & New Features
- **Status**: Lot 6 (Web Scraper) complete. Toolbox has 7 active tools.



- **Core Components**:
    - `toolbox.py`: Central CLI (list, run, new).
    - `core/system_check.py`: Validates environment.
    - `scripts/`:
        - `image_resizer/`: JPEG batch processing.
        - `file_cleaner/`: File cleanup (depth control, dry-run).
        - `git_health/`: Git repository audit.
        - `disk_usage/`: Directory size calculator.
        - `weather_forecast/`: Weather forecast and HTML report.
        - `web_scraper/`: Gentle site scraper (Scan -> Scrape).

## 📅 Next Steps
- **CI/CD**: Add linter integration to toolbox (check code quality).
- **Cross-platform**: Verify path handling on Windows/Linux.
