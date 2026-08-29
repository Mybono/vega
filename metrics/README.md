# Metrics

Download and traffic history for this repository, collected daily by
[`.github/workflows/metrics.yml`](../.github/workflows/metrics.yml).

## Why snapshots

The GitHub API reports release downloads as a **cumulative counter with no
history** — it answers "how many in total since this release was published",
never "how many last week". The traffic API does return daily buckets, but
discards them after 14 days. So both are snapshotted on a schedule, and rates
are reconstructed by diffing.

This means history starts the day collection was switched on. Downloads that
happened before the first snapshot are not recoverable and are reported
separately, as a cumulative baseline.

## Files

| File | Contents |
| :--- | :--- |
| `downloads.csv` | One row per snapshot per release asset: cumulative `download_count`. Append-only. |
| `traffic.csv` | One row per calendar day: views and clones. Upserted, so the partial current day is corrected on the next run. |

## Reading the numbers

```bash
./metrics/report.py                        # daily, last 30 days
./metrics/report.py --by month --last 12   # monthly, last year
./metrics/report.py --by year
./metrics/report.py --by week --detail     # weekly, broken down per asset
./metrics/report.py --asset '*.dmg'        # headline column for another artifact
```

`download_count` counts **file downloads, not installs** — bots, mirrors, CI
runs and repeat downloads by one person all land in it. Treat it as a demand
signal with an unknown multiplier, not as a user count.

## Running it by hand

```bash
./metrics/snapshot.sh   # needs gh, jq, and push access for the traffic half
```

The traffic API requires push access; if the token lacks it, that half is
skipped with a warning and the download snapshot still succeeds.
