#!/usr/bin/env python3
"""
Git Health Check Tool

Analyzes a Git repository to report:
- Active branch
- Uncommitted changes (dirty state)
- Lists of modified/untracked files
- Local branches

Arguments:
    --path, -p: Path to the git repository (default: current directory)

Example:
    python3 scripts/git_health/git_health.py --path ~/my-project
"""
import sys
import argparse
import logging
from pathlib import Path
try:
    import git
    from git import Repo
except ImportError:
    print("❌ GitPython is required. Please install it: pip install GitPython")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

def setup_args():
    parser = argparse.ArgumentParser(description="Git Health Check Tool")
    parser.add_argument("--path", "-p", type=Path, default=Path.cwd(), help="Path to git repository (default: current dir)")
    return parser.parse_args()

def main():
    args = setup_args()
    repo_path = args.path.resolve()
    
    if not (repo_path / ".git").exists():
        logging.error(f"❌ Not a git repository: {repo_path}")
        sys.exit(1)

    logging.info(f"🔎 Analyzing Git repository at: {repo_path}")
    logging.info("-" * 40)

    try:
        repo = Repo(repo_path)
        
        # 1. Active Branch
        try:
            active_branch = repo.active_branch.name
            logging.info(f"🌿 Active Branch: {active_branch}")
        except TypeError:
             # Detached HEAD
             logging.info(f"🌿 Active Branch: (Detached HEAD) {repo.head.commit.hexsha[:7]}")

        # 2. Local Branches
        branches = [b.name for b in repo.branches]
        logging.info(f"📚 Local Branches: {', '.join(branches)}")
        
        # 3. Status (Clean/Dirty)
        if repo.is_dirty(untracked_files=True):
            logging.info("\n🚧 Repository is DIRTY")
            
            # Modified files
            diff = repo.index.diff(None)
            for file in diff:
                logging.info(f"  📝 Modified: {file.a_path}")
            
            # Staged but not committed
            diff_staged = repo.index.diff("HEAD")
            for file in diff_staged:
                 logging.info(f"  📦 Staged: {file.a_path}")

            # Untracked files
            for file in repo.untracked_files:
                logging.info(f"  ❓ Untracked: {file}")
                
        else:
            logging.info("\n✅ Repository is CLEAN (No uncommitted changes)")

    except Exception as e:
        logging.error(f"❌ Error analyzing repository: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
