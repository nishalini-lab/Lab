import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from diagnostics.system_check import check_cpu_count, check_disk_usage


class TestSystemCheck(unittest.TestCase):
    def test_check_disk_usage_returns_expected_keys(self):
        result = check_disk_usage("/")
        for key in ("total_gb", "used_gb", "free_gb", "free_percent", "ok"):
            self.assertIn(key, result)
        self.assertGreater(result["total_gb"], 0)

    def test_check_cpu_count(self):
        result = check_cpu_count()
        self.assertGreaterEqual(result["cpu_count"], 1)


if __name__ == "__main__":
    unittest.main()
