"""Parse plain-text application logs of the form:

    2026-07-22 10:15:32 ERROR Database connection failed
    2026-07-22 10:15:40 INFO  Retrying connection
"""
import re
from collections import Counter
from datetime import datetime

LOG_LINE_RE = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>[A-Z]+)\s+"
    r"(?P<message>.*)$"
)
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_line(line):
    """Return a dict of {timestamp, level, message} or None if the line doesn't match."""
    match = LOG_LINE_RE.match(line.strip())
    if not match:
        return None
    fields = match.groupdict()
    fields["timestamp"] = datetime.strptime(fields["timestamp"], TIMESTAMP_FORMAT)
    return fields


def parse_file(path):
    """Parse a log file, skipping unparseable lines, and return a list of entries."""
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            entry = parse_line(line)
            if entry:
                entries.append(entry)
    return entries


def filter_by_level(entries, level):
    level = level.upper()
    return [e for e in entries if e["level"] == level]


def filter_by_date_range(entries, start=None, end=None):
    result = entries
    if start:
        result = [e for e in result if e["timestamp"] >= start]
    if end:
        result = [e for e in result if e["timestamp"] <= end]
    return result


def summarize(entries):
    """Return a Counter of log level -> occurrence count."""
    return Counter(e["level"] for e in entries)
