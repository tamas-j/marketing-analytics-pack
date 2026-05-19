#!/usr/bin/env python3
"""Quick CSV profiler for Marketing Analytics Pack readiness checks.

Uses only the Python standard library. It is intentionally lightweight: enough
to inspect grain, missingness, duplicate keys, and date-like columns before a
skill recommends a workflow.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
from collections import Counter, defaultdict
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Profile a CSV for marketing analytics readiness.")
    parser.add_argument("csv_path")
    parser.add_argument("--grain-key", action="append", default=[], help="Column(s) that define the expected grain")
    parser.add_argument("--max-rows", type=int, default=200000, help="Rows to scan before stopping")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.csv_path)
    if not path.exists():
        print(f"File not found: {path}")
        return 2

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        dialect = csv.Sniffer().sniff(sample) if sample else csv.excel
        reader = csv.DictReader(handle, dialect=dialect)
        fields = reader.fieldnames or []
        stats = {field: {"missing": 0, "non_missing": 0, "examples": Counter()} for field in fields}
        date_hits = Counter()
        grain_counts: Counter[tuple[str, ...]] = Counter()
        rows = 0

        for row in reader:
            rows += 1
            for field in fields:
                value = (row.get(field) or "").strip()
                if value == "":
                    stats[field]["missing"] += 1
                else:
                    stats[field]["non_missing"] += 1
                    if len(stats[field]["examples"]) < 8:
                        stats[field]["examples"][value] += 1
                    if _looks_like_date(value):
                        date_hits[field] += 1
            if args.grain_key:
                grain_counts[tuple((row.get(k) or "").strip() for k in args.grain_key)] += 1
            if rows >= args.max_rows:
                break

    print(f"# Data Profile: {path}")
    print()
    print(f"- Rows scanned: {rows:,}")
    print(f"- Columns: {len(fields):,}")
    print(f"- Column names: {', '.join(fields)}")
    print()

    print("## Missingness")
    print("| Field | Missing | Missing % | Example values |")
    print("|---|---:|---:|---|")
    for field in fields:
        missing = stats[field]["missing"]
        pct = (missing / rows) if rows else 0
        examples = ", ".join(list(stats[field]["examples"].keys())[:4])
        print(f"| `{field}` | {missing:,} | {pct:.1%} | {examples} |")
    print()

    print("## Date-Like Columns")
    found_dates = False
    for field, count in date_hits.most_common():
        if rows and count / rows >= 0.6:
            print(f"- `{field}` parses like a date in {count:,} rows ({count / rows:.1%}).")
            found_dates = True
    if not found_dates:
        print("- No strong date-like columns found in the scanned rows.")
    print()

    if args.grain_key:
        duplicate_keys = sum(1 for count in grain_counts.values() if count > 1)
        duplicate_rows = sum(count - 1 for count in grain_counts.values() if count > 1)
        print("## Grain Key Check")
        print(f"- Grain key: {', '.join(args.grain_key)}")
        print(f"- Distinct keys: {len(grain_counts):,}")
        print(f"- Keys with duplicates: {duplicate_keys:,}")
        print(f"- Extra rows beyond one per key: {duplicate_rows:,}")
        if duplicate_keys:
            examples = [key for key, count in grain_counts.items() if count > 1][:5]
            print(f"- Duplicate examples: {examples}")
    return 0


def _looks_like_date(value: str) -> bool:
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            dt.datetime.strptime(value[:19], fmt)
            return True
        except ValueError:
            continue
    return False


if __name__ == "__main__":
    raise SystemExit(main())
