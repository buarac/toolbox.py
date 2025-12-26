#!/usr/bin/env python3
"""
File Cleaner Tool

Deletes files in a directory that are older than a specified number of days.
Uses creation time (st_birthtime) on macOS.

Arguments:
    --directory, -d: Target directory
    --days: Age threshold in days (default: 7)
    --dry-run: List eligible files without deleting
    --force: Delete without confirmation prompt

Example:
    python3 scripts/file_cleaner/cleaner.py --directory ./tmp --days 30 --dry-run
"""
import argparse
import logging
import os
import sys
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%H:%M:%S"
)


def setup_args():
    parser = argparse.ArgumentParser(description="Delete files older than N days.")
    parser.add_argument(
        "--directory", "-d", type=Path, required=True, help="Target directory"
    )
    parser.add_argument(
        "--days", type=int, default=7, help="Age threshold in days (default: 7)"
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=1,
        help="Recursion depth (1=current dir only, default: 1)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="List files without deleting"
    )
    parser.add_argument(
        "--force", action="store_true", help="Delete without confirmation prompt"
    )
    return parser.parse_args()


def get_file_age_days(file_path: Path) -> float:
    """Return file age in days based on creation time (birthtime on macOS)."""
    try:
        stat = file_path.stat()
        # On macOS, st_birthtime is usually available. Fallback to st_mtime on Linux if needed.
        if hasattr(stat, "st_birthtime"):
            creation_time = stat.st_birthtime
        else:
            # Fallback for Linux/other filesystems where birthtime might not be standard
            creation_time = stat.st_mtime

        age_seconds = time.time() - creation_time
        return age_seconds / (24 * 3600)
    except Exception as e:
        logging.warning(f"⚠️ Could not get stats for {file_path}: {e}")
        return 0


def main():
    args = setup_args()

    if not args.directory.exists():
        logging.error(f"❌ Directory not found: {args.directory}")
        sys.exit(1)

    threshold_days = args.days
    max_depth = args.depth
    logging.info(
        f"🔎 Scanning {args.directory} (Depth: {max_depth}) for files older than {threshold_days} days..."
    )

    eligible_files = []

    # Scan files using os.walk to control depth
    logging.info(f"📂 Scanning files in {args.directory}...")

    base_depth = len(str(args.directory).rstrip(os.sep).split(os.sep))

    for root, dirs, files in os.walk(args.directory):
        # Calculate current depth
        current_depth = len(root.split(os.sep)) - base_depth + 1

        # Stop recursing if depth exceeded
        if current_depth > max_depth:
            dirs[:] = []  # Prevent os.walk from going deeper
            continue

        for filename in files:
            if filename.startswith("."):
                continue

            file_path = Path(root) / filename

            # Additional check to ensuring we are not exceeding depth processing files in the current root
            # (Logic above handles dirs, but files are in current root)
            if current_depth > max_depth:
                continue

            age = get_file_age_days(file_path)

            # Use relative path for cleaner output
            try:
                display_path = file_path.relative_to(args.directory)
            except ValueError:
                display_path = file_path.name

            if age >= threshold_days:
                logging.info(f"  🗑️  [DELETE] {display_path} (Age: {age:.1f} days)")
                eligible_files.append((file_path, age))
            else:
                logging.info(f"  🛡️   [KEEP]   {display_path} (Age: {age:.1f} days)")

    if not eligible_files:
        logging.info("✅ No eligible files found for deletion.")
        sys.exit(0)

    # Summary
    logging.info(f"📦 Found {len(eligible_files)} files eligible for deletion.")

    # Action logic
    if args.dry_run:
        logging.info("🚧 Dry-run enabled. No files were deleted.")
        sys.exit(0)

    if not args.force:
        response = input(f"\n❓ Delete these {len(eligible_files)} files? [y/N] ")
        if response.lower() != "y":
            logging.info("🛑 Operation cancelled.")
            sys.exit(0)

    # Delete files
    logging.info("🚀 Starting deletion...")
    deleted_count = 0
    for file_to_del, _ in eligible_files:
        try:
            file_to_del.unlink()
            logging.info(f"🗑️ Deleted: {file_to_del.name}")
            deleted_count += 1
        except Exception as e:
            logging.error(f"❌ Failed to delete {file_to_del.name}: {e}")

    logging.info(f"🎉 Cleanup complete. {deleted_count} files removed.")


if __name__ == "__main__":
    main()
