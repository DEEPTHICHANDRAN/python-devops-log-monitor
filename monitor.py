#!/usr/bin/env python3
"""A small DevOps log monitor for application log files."""

import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path
import sys

LOG_LEVELS = ("ERROR", "WARNING", "INFO")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scan an application log and create a monitoring report."
    )
    parser.add_argument(
        "--log-file", default="logs/application.log",
        help="Path to the application log file."
    )
    parser.add_argument(
        "--report-file", default="reports/monitoring_report.txt",
        help="Where to write the monitoring report."
    )
    parser.add_argument(
        "--error-threshold", type=int, default=0,
        help="Exit with status 1 when ERROR count is greater than this value."
    )
    return parser.parse_args()


def analyse_log(log_path):
    """Count log levels and retain matching lines."""
    counts = Counter()
    matching_lines = []

    with log_path.open("r", encoding="utf-8") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            for level in LOG_LEVELS:
                if level in line:
                    counts[level] += 1
                    matching_lines.append(
                        f"{line_number}: {level}: {line.strip()}"
                    )
                    break

    return counts, matching_lines


def write_report(report_path, log_path, counts, matching_lines):
    """Write a timestamped summary and matching log entries."""
    report_path.parent.mkdir(parents=True, exist_ok=True)

    total = sum(counts[level] for level in LOG_LEVELS)
    report_lines = [
        "PYTHON DEVOPS LOG MONITORING REPORT",
        "=" * 38,
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Log file: {log_path}",
        "",
        "SUMMARY",
        f"ERROR:   {counts['ERROR']}",
        f"WARNING: {counts['WARNING']}",
        f"INFO:    {counts['INFO']}",
        f"Matched entries: {total}",
        "",
        "MATCHING LOG ENTRIES",
        "-" * 38,
        *(matching_lines or ["No matching log entries found."]),
    ]

    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")


def main():
    args = parse_args()
    log_path = Path(args.log_file)
    report_path = Path(args.report_file)

    if args.error_threshold < 0:
        print("ERROR: --error-threshold cannot be negative.", file=sys.stderr)
        return 2

    if not log_path.is_file():
        print(f"ERROR: Log file not found: {log_path}", file=sys.stderr)
        return 2

    try:
        counts, matching_lines = analyse_log(log_path)
        write_report(report_path, log_path, counts, matching_lines)
    except OSError as exc:
        print(f"ERROR: Could not process files: {exc}", file=sys.stderr)
        return 2

    print(f"Log analysis complete. Report written to: {report_path}")
    print(
        f"ERROR={counts['ERROR']} "
        f"WARNING={counts['WARNING']} INFO={counts['INFO']}"
    )

    if counts["ERROR"] > args.error_threshold:
        print("STATUS: FAILED - error threshold exceeded.")
        return 1

    print("STATUS: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
