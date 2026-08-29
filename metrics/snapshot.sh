#!/usr/bin/env bash
# Append a snapshot of release download counts and repo traffic to metrics/*.csv.
#
# Release counts are cumulative and carry no history, so the download series is
# reconstructed later by diffing consecutive snapshots (see report.py).
# Traffic buckets are already daily but expire after 14 days, so they are
# upserted: fresh values overwrite stored ones, correcting the partial day.

set -euo pipefail

REPO="${GITHUB_REPOSITORY:-Mybono/vega}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DOWNLOADS="${DIR}/downloads.csv"
TRAFFIC="${DIR}/traffic.csv"
readonly REPO DIR NOW DOWNLOADS TRAFFIC

snapshot_downloads() {
  local rows
  # shellcheck disable=SC2016  # $tag is a jq variable, not a shell one
  rows="$(gh api "repos/${REPO}/releases" --paginate \
    --jq '.[] | .tag_name as $tag | .assets[]? |
          [$tag, .name, .download_count] | @csv')"

  if [[ -z "$rows" ]]; then
    echo "warning: no release assets found for ${REPO}" >&2
    return 0
  fi

  [[ -f "$DOWNLOADS" ]] || echo 'snapshot_utc,tag,asset,download_count' > "$DOWNLOADS"
  while IFS= read -r row; do
    printf '%s,%s\n' "$NOW" "$row" >> "$DOWNLOADS"
  done <<< "$rows"

  echo "downloads: recorded $(wc -l <<< "$rows" | tr -d ' ') asset rows at ${NOW}"
}

# Traffic needs push access. A fine-grained token may lack it, so a failure here
# must not lose the download snapshot that already succeeded.
snapshot_traffic() {
  local views clones merged
  if ! views="$(gh api "repos/${REPO}/traffic/views" 2>/dev/null)" ||
     ! clones="$(gh api "repos/${REPO}/traffic/clones" 2>/dev/null)"; then
    echo "warning: traffic API unavailable (needs push access); skipping" >&2
    return 0
  fi

  [[ -f "$TRAFFIC" ]] || echo 'date,views,views_uniques,clones,clones_uniques' > "$TRAFFIC"

  # Index both series by date, then emit one row per date seen in either.
  merged="$(jq -rn --argjson v "$views" --argjson c "$clones" '
    ( [ $v.views[]?  | {key: (.timestamp[0:10]), value: .} ] | from_entries ) as $vi |
    ( [ $c.clones[]? | {key: (.timestamp[0:10]), value: .} ] | from_entries ) as $ci |
    ( ($vi | keys) + ($ci | keys) | unique )[] |
    [ ., ($vi[.].count // 0), ($vi[.].uniques // 0),
         ($ci[.].count // 0), ($ci[.].uniques // 0) ] | @csv
  ' | tr -d '"')"

  if [[ -z "$merged" ]]; then
    echo "traffic: API returned no daily buckets"
    return 0
  fi

  # Upsert: drop stored rows for the dates we just fetched, then re-add them.
  local refreshed header
  refreshed="$(cut -d, -f1 <<< "$merged" | paste -sd'|' -)"
  header="$(head -n 1 "$TRAFFIC")"
  {
    printf '%s\n' "$header"
    {
      tail -n +2 "$TRAFFIC" | grep -vE "^(${refreshed})," || true
      printf '%s\n' "$merged"
    } | sort -t, -k1,1
  } > "${TRAFFIC}.tmp"
  mv "${TRAFFIC}.tmp" "$TRAFFIC"

  echo "traffic: upserted $(wc -l <<< "$merged" | tr -d ' ') daily rows"
}

snapshot_downloads
snapshot_traffic
