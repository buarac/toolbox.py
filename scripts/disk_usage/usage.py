#!/usr/bin/env python3
"""
Disk Usage Tool

Calculates the size of directories.
- Recursive size calculation.
- Human-readable units (KB, MB, GB).
- Configurable recursion depth.

Arguments:
    --path, -p: Target directory (default: current dir)
    --depth, -d: recursion depth (default: 1)

Example:
    python3 scripts/disk_usage/usage.py --path ~/Downloads --depth 2
"""
import sys
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

def setup_args():
    parser = argparse.ArgumentParser(description="Disk Usage Tool")
    parser.add_argument("--path", "-p", type=Path, default=Path.cwd(), help="Target directory (default: current dir)")
    parser.add_argument("--depth", "-d", type=int, default=1, help="Recursion depth (default: 1)")
    return parser.parse_args()

def format_size(size_bytes):
    """Format bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def get_dir_size(path: Path) -> int:
    """Recursively calculate directory size in bytes."""
    total_size = 0
    try:
        if not path.is_dir():
            return path.stat().st_size
            
        for p in path.rglob('*'):
            if p.is_file():
                try:
                    total_size += p.stat().st_size
                except OSError:
                    pass # Ignore permission errors
    except OSError as e:
        # logging.warning(f"⚠️ Error accessing {path}: {e}")
        pass
    return total_size

def scan_directory(path: Path, current_depth: int, max_depth: int):
    """Scan directory printing sizes up to max_depth."""
    # Always print current directory size
    size = get_dir_size(path)
    
    # Indentation based on depth (relative to start) but user asked for simple list maybe?
    # Let's align logically. usage typically lists subdirs.
    
    # Display format: Size Path
    # Using relative path if possible
    try:
        display_path = path.relative_to(Path.cwd())
    except ValueError:
        display_path = path

    logging.info(f"{format_size(size):>10}  {display_path}")

    if current_depth >= max_depth:
        return

    try:
        # Get immediate subdirectories
        # Sort by name for consistency
        subdirs = sorted([p for p in path.iterdir() if p.is_dir()])
        for subdir in subdirs:
             scan_directory(subdir, current_depth + 1, max_depth)
             
    except PermissionError:
        logging.warning(f"🚫 Permission denied: {path}")

def main():
    args = setup_args()
    target_path = args.path.resolve()
    
    if not target_path.exists() or not target_path.is_dir():
        logging.error(f"❌ Invalid directory: {target_path}")
        sys.exit(1)

    logging.info(f"💾 Computing disk usage for: {target_path}")
    logging.info(f"   (Depth: {args.depth})")
    logging.info("-" * 40)
    
    # Special handling: user might expect "du -h --max-depth=1" behavior
    # which shows sizes of subdirectories AND the root itself at the end (or beginning).
    
    # We will implement a recursive printer.
    # Start scan.
    # Note: 'current_depth' logic in my helper matches the traversal.
    # However, 'du --max-depth=1' on '.' lists ./foo, ./bar, and .
    
    # Let's just traverse exactly max_depth levels down.
    
    # Initial call is depth 0.
    scan_directory(target_path, 0, args.depth)
    
    logging.info("-" * 40)
    logging.info("✅ Done.")

if __name__ == "__main__":
    main()
