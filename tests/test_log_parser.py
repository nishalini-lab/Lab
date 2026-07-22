import os
import sys
import tempfile
import unittest
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from log_parsing.parser import (
    filter_by_date_range,
    filter_by_level,
    parse_file,
    parse_line,
    summarize,
)

SAMPLE_LOG = """\
2026-07-22 10:15:32 ERROR Database connection failed
2026-07-22 10:15:40 INFO Retrying connection
2026-07-22 10:16:01 INFO Connection restored
2026-07-22 10:20:00 WARNING High memory usage
not a valid log line
"""


class TestParseLine(unittest.TestCase):
    def test_parses_valid_line(self):
        entry = parse_line("2026-07-22 10:15:32 ERROR Database connection failed")
        self.assertEqual(entry["level"], "ERROR")
        self.assertEqual(entry["message"], "Database connection failed")
        self.assertEqual(entry["timestamp"], datetime(2026, 7, 22, 10, 15, 32))

    def test_returns_none_for_invalid_line(self):
        self.assertIsNone(parse_line("this is not a log line"))


class TestParseFile(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False)
        self.tmp.write(SAMPLE_LOG)
        self.tmp.close()

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_skips_unparseable_lines(self):
        entries = parse_file(self.tmp.name)
        self.assertEqual(len(entries), 4)

    def test_filter_by_level(self):
        entries = parse_file(self.tmp.name)
        info_entries = filter_by_level(entries, "info")
        self.assertEqual(len(info_entries), 2)

    def test_filter_by_date_range(self):
        entries = parse_file(self.tmp.name)
        filtered = filter_by_date_range(entries, start=datetime(2026, 7, 22, 10, 16, 0))
        self.assertEqual(len(filtered), 2)

    def test_summarize(self):
        entries = parse_file(self.tmp.name)
        counts = summarize(entries)
        self.assertEqual(counts["INFO"], 2)
        self.assertEqual(counts["ERROR"], 1)
        self.assertEqual(counts["WARNING"], 1)


if __name__ == "__main__":
    unittest.main()
