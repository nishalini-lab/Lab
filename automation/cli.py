"""Unified CLI entry point for automation utilities."""
import argparse
import sys
from automation.backup import create_backup
from automation.file_organizer import organize


def main():
    parser = argparse.ArgumentParser(description="Automation utilities")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # backup command
    backup_parser = subparsers.add_parser("backup", help="Create a timestamped zip backup")
    backup_parser.add_argument("source", help="Directory to back up")
    backup_parser.add_argument("destination", help="Directory to store the archive in")
    
    # file-organizer command
    organizer_parser = subparsers.add_parser("organize", help="Sort files by extension")
    organizer_parser.add_argument("directory", help="Directory to organize")
    organizer_parser.add_argument("--dry-run", action="store_true", help="Show what would move without moving")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    if args.command == "backup":
        archive_path = create_backup(args.source, args.destination)
        print(f"Backup created: {archive_path}")
    elif args.command == "organize":
        moves = organize(args.directory, dry_run=args.dry_run)
        for src, dest in moves:
            prefix = "[dry-run] " if args.dry_run else ""
            print(f"{prefix}{src} -> {dest}")
        print(f"\n{len(moves)} file(s) {'would be moved' if args.dry_run else 'moved'}.")


if __name__ == "__main__":
    main()
