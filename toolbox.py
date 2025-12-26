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
import sys
import os
import argparse
import subprocess
import logging
from pathlib import Path
from typing import List, Dict

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

def command_list(args):
    """List available scripts."""
    scripts = get_scripts()
    if not scripts:
        logging.info("📭 No scripts found in the toolbox.")
        return

    logging.info(f"🧰 Found {len(scripts)} tools regarding your request:")
    logging.info("-" * 40)
    for name, path in sorted(scripts.items()):
        # Try to read docstring for description
        description = "No description available."
        try:
            with open(path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line.startswith('"""') or first_line.startswith("'''"):
                    # Basic parsing, might need improvement
                   description = first_line.strip('"\'') 
                # Or check second line if shebang exists
                elif first_line.startswith("#!"):
                     second_line = f.readline().strip()
                     if second_line.startswith('"""') or second_line.startswith("'''"):
                         description = second_line.strip('"\'')
        except Exception:
            pass
            
        logging.info(f"🔧 {name:<20} : {path.relative_to(Path.cwd())}")

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
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(template)
        
    # Make executable
    target_file.chmod(0o755)
    
    logging.info(f"✅ Created: {target_file}")
    logging.info(f"👉 Run it with: python3 {target_file}")
    logging.info(f"👉 Or via toolbox: python3 toolbox.py run {name}")

def main():
    parser = argparse.ArgumentParser(description="Python Toolbox CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List command
    subparsers.add_parser("list", help="List available scripts")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run a script")
    run_parser.add_argument("script", help="Name of the script to run")
    run_parser.add_argument("script_args", nargs=argparse.REMAINDER, help="Arguments for the script")
    
    # New command
    new_parser = subparsers.add_parser("new", help="Create a new script")
    new_parser.add_argument("name", help="Name of the new tool")
    
    args = parser.parse_args()
    
    if args.command == "list":
        command_list(args)
    elif args.command == "run":
        command_run(args)
    elif args.command == "new":
        command_new(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
