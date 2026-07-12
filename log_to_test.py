#!/usr/bin/env python3
"""Cluster structured failures and generate a safe unittest skeleton."""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


def redact(value):
    return re.sub(r"(?i)(token|password|secret)=\S+", r"\1=[REDACTED]", str(value))


def cluster(logs):
    groups = defaultdict(list)
    for log in logs:
        key = (log.get("exception", "Error"), log.get("operation", "unknown"))
        groups[key].append(log)
    return [{"exception": key[0], "operation": key[1], "count": len(rows), "example": redact(rows[0].get("context", ""))} for key, rows in sorted(groups.items())]


def generate(case):
    name = re.sub(r"\W+", "_", f"{case['operation']}_{case['exception']}").lower()
    return f"def test_{name}(self):\n    # Reproduce {case['exception']} in {case['operation']}\n    with self.assertRaises(Exception):\n        exercise_system_under_test()\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs")
    args = parser.parse_args()
    cases = cluster(json.loads(Path(args.logs).read_text()))
    print(json.dumps({"cases": cases, "tests": [generate(case) for case in cases]}, indent=2))


if __name__ == "__main__":
    main()
