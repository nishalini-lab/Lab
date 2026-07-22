"""Organize files in a directory into subfolders grouped by file extension."""
import argparse
import shutil
from pathlib import Path


def organize(target_dir, dry_run=False):
    target = Path(target_dir)
    moves = []
    for item in target.iterdir():
        if item.is_dir():
            continue
        extension = item.suffix.lstrip(".").lower() or "no_extension"
        dest_dir = target / extension
        dest_path = dest_dir / item.name
        moves.append((item, dest_path))
        if not dry_run:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_path))
    return moves


def main():
    parser = argparse.ArgumentParser(description="Sort files into subfolders by extension")
    parser.add_argument("directory", help="Directory to organize")
    parser.add_argument("--dry-run", action="store_true", help="Show what would move without moving anything")
    args = parser.parse_args()

    moves = organize(args.directory, dry_run=args.dry_run)
    for src, dest in moves:
        prefix = "[dry-run] " if args.dry_run else ""
        print(f"{prefix}{src} -> {dest}")
    print(f"\n{len(moves)} file(s) {'would be moved' if args.dry_run else 'moved'}.")


if __name__ == "__main__":
    main()
