"""Create a timestamped zip archive of a directory."""
import argparse
import shutil
from datetime import datetime
from pathlib import Path


def create_backup(source_dir, dest_dir):
    source = Path(source_dir)
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_base = dest / f"{source.name}_{timestamp}"
    archive_path = shutil.make_archive(str(archive_base), "zip", root_dir=source)
    return Path(archive_path)


def main():
    parser = argparse.ArgumentParser(description="Back up a directory into a timestamped zip archive")
    parser.add_argument("source", help="Directory to back up")
    parser.add_argument("destination", help="Directory to store the archive in")
    args = parser.parse_args()

    archive_path = create_backup(args.source, args.destination)
    print(f"Backup created: {archive_path}")


if __name__ == "__main__":
    main()
