import tempfile
import unittest
from pathlib import Path

from monitor import analyse_log, write_report


class LogMonitorTests(unittest.TestCase):
    def test_analyse_log_counts_levels(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "app.log"
            log_path.write_text(
                "INFO started\nWARNING slow\nERROR failed\n",
                encoding="utf-8",
            )

            counts, lines = analyse_log(log_path)

            self.assertEqual(counts["INFO"], 1)
            self.assertEqual(counts["WARNING"], 1)
            self.assertEqual(counts["ERROR"], 1)
            self.assertEqual(len(lines), 3)

    def test_report_is_created(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "reports" / "report.txt"
            log_path = Path(temp_dir) / "app.log"
            counts = {"ERROR": 1, "WARNING": 0, "INFO": 2}

            write_report(report_path, log_path, counts, ["1: ERROR: failed"])

            self.assertTrue(report_path.is_file())
            self.assertIn("ERROR:   1", report_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
