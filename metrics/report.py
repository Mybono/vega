#!/usr/bin/env python3
"""Report download and traffic rates from the snapshots in metrics/*.csv.

GitHub reports release downloads as a cumulative counter with no history, so a
rate is only recoverable by diffing consecutive snapshots. The first snapshot of
an asset is therefore a baseline, not a delta: downloads that happened before
collection started are unknowable and are excluded rather than attributed to the
day collection began.
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

METRICS_DIR = Path(__file__).resolve().parent
DOWNLOADS_CSV = METRICS_DIR / "downloads.csv"
TRAFFIC_CSV = METRICS_DIR / "traffic.csv"

GRANULARITIES = ("day", "week", "month", "year")
INSTALLER_GLOB = "*.pkg"


def bucket_start(day: date, by: str) -> date:
    """Snap a date down to the first day of its bucket."""
    if by == "day":
        return day
    if by == "week":
        return day - timedelta(days=day.weekday())
    if by == "month":
        return day.replace(day=1)
    return day.replace(month=1, day=1)


def next_bucket(start: date, by: str) -> date:
    if by == "day":
        return start + timedelta(days=1)
    if by == "week":
        return start + timedelta(days=7)
    if by == "month":
        return (start.replace(day=28) + timedelta(days=4)).replace(day=1)
    return start.replace(year=start.year + 1)


def bucket_label(start: date, by: str) -> str:
    if by == "day":
        return start.isoformat()
    if by == "week":
        year, week, _ = start.isocalendar()
        return f"{year}-W{week:02d}"
    if by == "month":
        return f"{start.year}-{start.month:02d}"
    return str(start.year)


def read_download_deltas(by: str) -> tuple[dict[date, dict[str, int]], int, int]:
    """Return per-bucket {asset: delta}, the snapshot count, and the asset count."""
    if not DOWNLOADS_CSV.exists():
        sys.exit(f"no snapshots yet: {DOWNLOADS_CSV} does not exist")

    series: dict[tuple[str, str], list[tuple[datetime, int]]] = defaultdict(list)
    timestamps: set[datetime] = set()
    with DOWNLOADS_CSV.open(newline="") as handle:
        for row in csv.DictReader(handle):
            taken = datetime.strptime(row["snapshot_utc"], "%Y-%m-%dT%H:%M:%SZ")
            series[(row["tag"], row["asset"])].append((taken, int(row["download_count"])))
            timestamps.add(taken)

    deltas: dict[date, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for (_tag, asset), points in series.items():
        points.sort()
        for (_prev_at, prev_count), (taken, count) in zip(points, points[1:]):
            # A counter that moved backwards means the asset was replaced or the
            # release re-cut; that is not a negative number of downloads.
            gain = max(0, count - prev_count)
            deltas[bucket_start(taken.date(), by)][asset] += gain

    return deltas, len(timestamps), len(series)


def read_traffic(by: str) -> dict[date, tuple[int, int]]:
    """Return per-bucket (views, clones), summed over the daily buckets."""
    if not TRAFFIC_CSV.exists():
        return {}

    totals: dict[date, list[int]] = defaultdict(lambda: [0, 0])
    with TRAFFIC_CSV.open(newline="") as handle:
        for row in csv.DictReader(handle):
            start = bucket_start(date.fromisoformat(row["date"]), by)
            totals[start][0] += int(row["views"])
            totals[start][1] += int(row["clones"])
    return {start: (views, clones) for start, (views, clones) in totals.items()}


def cumulative_totals() -> list[tuple[str, str, int]]:
    """Latest known cumulative count per asset, newest snapshot wins."""
    latest: dict[tuple[str, str], tuple[str, int]] = {}
    with DOWNLOADS_CSV.open(newline="") as handle:
        for row in csv.DictReader(handle):
            key = (row["tag"], row["asset"])
            if key not in latest or row["snapshot_utc"] >= latest[key][0]:
                latest[key] = (row["snapshot_utc"], int(row["download_count"]))
    return sorted((tag, asset, count) for (tag, asset), (_at, count) in latest.items())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--by", choices=GRANULARITIES, default="day",
                        help="bucket size (default: day)")
    parser.add_argument("--last", type=int, default=30, metavar="N",
                        help="show only the last N buckets (default: 30)")
    parser.add_argument("--asset", default=INSTALLER_GLOB, metavar="GLOB",
                        help=f"glob for the headline column (default: {INSTALLER_GLOB})")
    parser.add_argument("--detail", action="store_true",
                        help="break the totals down per asset")
    args = parser.parse_args()

    deltas, snapshots, assets = read_download_deltas(args.by)
    traffic = read_traffic(args.by)

    if snapshots < 2:
        print(f"Only {snapshots} snapshot so far, so no rate can be derived yet — "
              "a rate needs two points to diff.\n"
              "Cumulative downloads since each release was published:\n")
        for tag, asset, count in cumulative_totals():
            print(f"  {tag:<10} {asset:<40} {count:>6}")
        print(f"\nRun snapshot.sh again tomorrow and this becomes a series.")
        return

    starts = sorted(set(deltas) | set(traffic))
    buckets: list[date] = []
    cursor = starts[0]
    while cursor <= starts[-1]:
        buckets.append(cursor)
        cursor = next_bucket(cursor, args.by)
    buckets = buckets[-args.last:]

    print(f"Downloads by {args.by}, last {len(buckets)} buckets "
          f"({snapshots} snapshots, {assets} assets tracked)\n")
    header = f"{'period':<12}{args.asset:>12}{'all assets':>12}{'views':>8}{'clones':>8}"
    print(header)
    print("-" * len(header))

    totals = [0, 0, 0, 0]
    for start in buckets:
        per_asset = deltas.get(start, {})
        matched = sum(n for asset, n in per_asset.items()
                      if fnmatch.fnmatch(asset, args.asset))
        every = sum(per_asset.values())
        views, clones = traffic.get(start, (0, 0))
        totals = [totals[0] + matched, totals[1] + every,
                  totals[2] + views, totals[3] + clones]
        print(f"{bucket_label(start, args.by):<12}{matched:>12}{every:>12}"
              f"{views:>8}{clones:>8}")
        if args.detail:
            for asset, n in sorted(per_asset.items()):
                if n:
                    print(f"  {asset:<38}{n:>10}")

    print("-" * len(header))
    print(f"{'total':<12}{totals[0]:>12}{totals[1]:>12}{totals[2]:>8}{totals[3]:>8}")

    if not traffic:
        print("\nnote: traffic columns stay zero until snapshot.sh runs with push access")


if __name__ == "__main__":
    main()
