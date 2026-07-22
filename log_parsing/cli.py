import argparse
from datetime import datetime

from log_parsing.parser import filter_by_date_range, filter_by_level, parse_file, summarize


def main():
    parser = argparse.ArgumentParser(description="Parse and summarize application log files")
    parser.add_argument("logfile", help="Path to the log file")
    parser.add_argument("--level", help="Only show entries at this level (e.g. ERROR)")
    parser.add_argument("--since", help="Only show entries at/after this timestamp (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--until", help="Only show entries at/before this timestamp (YYYY-MM-DD HH:MM:SS)")
    args = parser.parse_args()

    entries = parse_file(args.logfile)

    since = datetime.strptime(args.since, "%Y-%m-%d %H:%M:%S") if args.since else None
    until = datetime.strptime(args.until, "%Y-%m-%d %H:%M:%S") if args.until else None
    entries = filter_by_date_range(entries, since, until)

    if args.level:
        entries = filter_by_level(entries, args.level)

    for e in entries:
        print(f"{e['timestamp']} {e['level']:<8} {e['message']}")

    counts = summarize(entries)
    print("\n--- Summary ---")
    for level, count in sorted(counts.items()):
        print(f"{level:<8} {count}")
    print(f"{'TOTAL':<8} {sum(counts.values())}")


if __name__ == "__main__":
    main()
