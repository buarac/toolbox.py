#!/usr/bin/env python3
"""
🧰 The Python Toolbox

Central entry point for managing and running utility scripts.

Commands:
    list    : List available scripts
    run     : Run a specific script
    new     : Create a new script

Example:
    python3 toolbox.py list
    python3 toolbox.py run file_cleaner --directory ./tmp
    python3 toolbox.py new my_awesome_tool
"""
import argparse
import importlib.metadata
import logging
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

SCRIPTS_DIR = Path(__file__).parent / "scripts"


def get_scripts() -> Dict[str, Path]:
    """Scan scripts directory for executable python scripts."""
    scripts = {}
    if not SCRIPTS_DIR.exists():
        logging.warning("⚠️ Scripts directory not found.")
        return scripts

    # Looking for .py files inside subdirectories of scripts/
    # Assumption: scripts/tool_name/tool_name.py OR scripts/tool_name/main.py
    # Also support simple scripts/tool_name.py

    # Strategy: Recursive scan for .py files, excluding __init__.py
    for path in SCRIPTS_DIR.rglob("*.py"):
        if path.name == "__init__.py":
            continue

        # Identifier is the stem (filename without extension)
        # If there are duplicates, we might have an issue, but let's keep it simple for now.
        # Prefer "resizer" from scripts/image_resizer/resizer.py

        # To make it cleaner for the user, let's map the tool name to the file.
        # We can use the parent folder name if the file is main.py or matches folder name?
        # Let's simple use the filename stem for now.
        scripts[path.stem] = path

    return scripts


def parse_requirements(req_path: Path) -> List[str]:
    """Parse requirements.txt to get package names."""
    requirements = []
    if not req_path.exists():
        return requirements

    with open(req_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Simple regex to extract package name (ignores version specifiers for checking)
            # Matches "package_name" or "package-name" at start of line
            match = re.match(r"^([a-zA-Z0-9_\-]+)", line)
            if match:
                requirements.append(match.group(1))
    return requirements


def check_dependencies(script_path: Path) -> List[str]:
    """Check if dependencies for a script are installed."""
    req_path = script_path.parent / "requirements.txt"
    missing = []

    if req_path.exists():
        required_packages = parse_requirements(req_path)
        for pkg in required_packages:
            try:
                # Map common package names to their import names if needed
                # For now, rely on standard metadata names
                importlib.metadata.distribution(pkg)
            except importlib.metadata.PackageNotFoundError:
                missing.append(pkg)

    return missing


def install_dependencies(script_path: Path) -> bool:
    """Install dependencies for a script using pip."""
    req_path = script_path.parent / "requirements.txt"
    if not req_path.exists():
        logging.info("✨ No dependencies to install.")
        return True

    logging.info(f"📦 Installing dependencies from {req_path.name}...")
    try:
        # Capture output to check for specific errors
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(req_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        logging.info(result.stdout)
        logging.info("✅ Dependencies installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"💥 Failed to install dependencies (Exit code {e.returncode})")
        logging.error(e.stderr)

        if "externally-managed-environment" in e.stderr:
            logging.warning(
                "\n💡 HINT: You are trying to install packages in a system-managed Python environment."
            )
            logging.warning(
                "   Please create and activate a virtual environment first:"
            )
            logging.warning("   python3 -m venv .venv")
            logging.warning("   source .venv/bin/activate")
            logging.warning(f"   python3 toolbox.py install {script_path.stem}")

        return False


def command_list(args):
    """List available scripts with descriptions."""
    scripts = get_scripts()
    if not scripts:
        logging.info("📭 No scripts found in the toolbox.")
        return

    logging.info(f"🧰 Found {len(scripts)} tools in your toolbox:")
    logging.info("-" * 60)
    logging.info(f"{'TOOL':<20} | {'DESCRIPTION'}")
    logging.info("-" * 60)

    for name, path in sorted(scripts.items()):
        description = None
        try:
            with open(path, "r", encoding="utf-8") as f:
                # Naive docstring extraction: read lines until we find a docstring
                lines = f.readlines()
                docstring_lines = []
                in_docstring = False

                for line in lines:
                    stripped = line.strip()
                    if not in_docstring:
                        if stripped.startswith('"""') or stripped.startswith("'''"):
                            in_docstring = True
                            # Handle one-line docstrings: """Description"""
                            content = stripped.strip("\"'")
                            if content:
                                description = content
                                break
                    else:
                        # Inside docstring
                        if stripped.endswith('"""') or stripped.endswith("'''"):
                            # End of docstring
                            content = stripped.strip("\"'")
                            if content:
                                docstring_lines.append(content)
                            break
                        docstring_lines.append(stripped)

                if not description and docstring_lines:
                    # Join first non-empty lines or just take the first one
                    description = next((line for line in docstring_lines if line), None)

        except Exception:
            pass

        if not description:
            description = "No description available."

        logging.info(f"🔧 {name:<17} : {description}")
    logging.info("-" * 60)


def command_run(args):
    """Run a specific script."""
    scripts = get_scripts()
    script_name = args.script

    if script_name not in scripts:
        logging.error(f"❌ Script '{script_name}' not found.")
        command_list(None)
        sys.exit(1)

    script_path = scripts[script_name]
    logging.info(f"🚀 Launching {script_name}...")

    # Check dependencies before running
    missing_deps = check_dependencies(script_path)
    if missing_deps:
        logging.warning(f"⚠️  Missing dependencies: {', '.join(missing_deps)}")
        logging.info("💡 You can install them by running:")
        logging.info(f"   python3 toolbox.py install {script_name}")

        # Interactive prompt?
        # For CLI automation, let's keep it simple: warn and proceed (might crash)
        # OR prompt user if interactive.
        if sys.stdin.isatty():
            response = input("❓ Attempt to install them now? [y/N] ").lower()
            if response == "y":
                if not install_dependencies(script_path):
                    logging.error("❌ Installation failed. Aborting.")
                    sys.exit(1)
            else:
                logging.warning("⚠️  Proceeding without dependencies. Script may crash.")
        else:
            logging.warning("⚠️  Non-interactive mode: Running anyway.")

    # Construct command: python3 [script_path] [legacy_args]
    cmd = [sys.executable, str(script_path)] + args.script_args

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"💥 Script failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        logging.info("\n🛑 Execution interrupted.")
        sys.exit(130)


def command_new(args):
    """Create a new script from template."""
    name = args.name
    target_dir = SCRIPTS_DIR / name
    target_file = target_dir / f"{name}.py"

    if target_file.exists():
        logging.error(f"❌ Script '{name}' already exists at {target_file}")
        sys.exit(1)

    logging.info(f"🔨 Scaffolding new tool: {name}")

    target_dir.mkdir(parents=True, exist_ok=True)

    template = f'''#!/usr/bin/env python3
"""
{name} Tool

[Description of what the tool does]

Arguments:
    --arg1: Description

Example:
    python3 scripts/{name}/{name}.py --arg1 value
"""
import sys
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

def setup_args():
    parser = argparse.ArgumentParser(description="{name} Tool")
    parser.add_argument("--arg1", help="Example argument")
    return parser.parse_args()

def main():
    args = setup_args()
    logging.info("🚀 Starting {name}...")
    
    # Your logic here
    if args.arg1:
        logging.info(f"ℹ️  Argument received: {{args.arg1}}")

    logging.info("✅ Done.")

if __name__ == "__main__":
    main()
'''

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(template)

    # Make executable
    target_file.chmod(0o755)

    logging.info(f"✅ Created: {target_file}")
    logging.info(f"👉 Run it with: python3 {target_file}")
    logging.info(f"👉 Or via toolbox: python3 toolbox.py run {name}")


def command_install(args):
    """Install dependencies for a specific script."""
    scripts = get_scripts()
    script_name = args.script

    if script_name not in scripts:
        logging.error(f"❌ Script '{script_name}' not found.")
        sys.exit(1)

    script_path = scripts[script_name]
    install_dependencies(script_path)


def command_check(args):
    """Run linting and formatting checks."""
    logging.info("🕵️  Running code quality checks...")

    # 1. Formatting (Black)
    logging.info("\n🖤 Checking formatting (black)...")
    black_args = [sys.executable, "-m", "black", "."]
    if not args.fix:
        black_args.append("--check")

    try:
        subprocess.run(black_args, check=True)
        logging.info("✅ Formatting: OK")
    except subprocess.CalledProcessError:
        logging.error("❌ Formatting: Issues found.")
        if not args.fix:
            logging.info("💡 Run 'toolbox.py check --fix' to auto-format.")

    # 2. Linting (Ruff)
    logging.info("\n🐶 Checking linting (ruff)...")
    ruff_args = [sys.executable, "-m", "ruff", "check", "."]
    if args.fix:
        ruff_args.append("--fix")

    try:
        subprocess.run(ruff_args, check=True)
        logging.info("✅ Linting: OK")
    except subprocess.CalledProcessError:
        logging.error("❌ Linting: Issues found.")


def main():
    parser = argparse.ArgumentParser(description="Python Toolbox CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # List command
    subparsers.add_parser("list", help="List available scripts")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a script")
    run_parser.add_argument("script", help="Name of the script to run")
    run_parser.add_argument(
        "script_args", nargs=argparse.REMAINDER, help="Arguments for the script"
    )

    # New command
    new_parser = subparsers.add_parser("new", help="Create a new script")
    new_parser.add_argument("name", help="Name of the new tool")

    # Install command
    install_parser = subparsers.add_parser(
        "install", help="Install dependencies for a tool"
    )
    install_parser.add_argument("script", help="Name of the tool")

    # Check command
    check_parser = subparsers.add_parser(
        "check", help="Run quality checks (linting & formatting)"
    )
    check_parser.add_argument("--fix", action="store_true", help="Auto-fix issues")

    args = parser.parse_args()

    if args.command == "list":
        command_list(args)
    elif args.command == "run":
        command_run(args)
    elif args.command == "new":
        command_new(args)
    elif args.command == "install":
        command_install(args)
    elif args.command == "check":
        command_check(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
