#!/usr/bin/env python3
"""
System check script to verify environment compatibility.
Checks:
- Python version >= 3.12
- OS is macOS or Linux (Ubuntu)
"""
import logging
import platform
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def check_python_version():
    """Check if Python version is 3.12 or higher."""
    required_version = (3, 12)
    current_version = sys.version_info[:2]

    if current_version < required_version:
        logging.error(
            f"❌ Python version {required_version[0]}.{required_version[1]}+ required. Found {sys.version.split()[0]}"
        )
        return False

    logging.info(f"✅ Python version check passed: {sys.version.split()[0]}")
    return True


def check_os():
    """Check if OS is supported (Darwin/macOS or Linux)."""
    system = platform.system()
    supported_systems = ["Darwin", "Linux"]

    if system not in supported_systems:
        logging.error(
            f"❌ OS '{system}' not supported. Supported OS: {supported_systems}"
        )
        return False

    logging.info(f"✅ OS check passed: {system}")
    return True


def main():
    """Run all system checks."""
    logging.info("🚀 Starting system compatibility check...")

    python_ok = check_python_version()
    os_ok = check_os()

    if python_ok and os_ok:
        logging.info("🎉 System check passed. Toolbox is ready to run.")
        sys.exit(0)
    else:
        logging.error("💀 System check failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
