"""Daily snapshot of GoatCounter cumulative counts per city.

Appends today's reading to dist/timeseries.json. Run via cron 4× daily;
each run overwrites today's entry (last write wins) but preserves all
prior days so the dashboard can compute daily diffs.

JSON shape:
  [
    {"date": "2026-05-21",
     "total": {"count": 12, "count_unique": 8},
     "cities": {"hk": {"count": 5, "count_unique": 4}, ...}},
    ...
  ]
"""
from __future__ import annotations
import json, sys, urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).parent.parent
SNAPSHOT = REPO_ROOT / "timeseries.json"  # also served as static asset
GC = "https://fengelh.goatcounter.com"
CITIES = [
    {"code": "hk",      "path": "/events/hk/"},
    {"code": "la",      "path": "/events/la/"},
    {"code": "nrw",     "path": "/events/nrw/"},
    {"code": "singa",   "path": "/events/singa/"},
    {"code": "fukuoka", "path": "/events/fukuoka/"},
]


def fetch(url: str) -> dict | None:
    try:
        r = requests.get(url, timeout=15)
        if r.status_code in (200, 404):
            data = r.json()
            return {"count": int(data.get("count", 0) or 0),
                    "count_unique": int(data.get("count_unique", 0) or 0)}
    except Exception as exc:
        print(f"  ! fetch {url}: {exc}", file=sys.stderr)
    return None


def main():
    today = datetime.now(timezone.utc).date().isoformat()
    entry = {"date": today, "snapped_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "total": None, "cities": {}}

    total = fetch(f"{GC}/counter/TOTAL.json")
    if total:
        entry["total"] = total
        print(f"  TOTAL: {total['count']} views / {total['count_unique']} uniq")

    for c in CITIES:
        enc = urllib.parse.quote(c["path"], safe="")
        d = fetch(f"{GC}/counter/{enc}.json")
        if d is None:
            d = {"count": 0, "count_unique": 0}
        entry["cities"][c["code"]] = d
        print(f"  {c['code']:>8}: {d['count']} views / {d['count_unique']} uniq")

    # Load existing, replace today, sort
    if SNAPSHOT.exists():
        try:
            history = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        except Exception:
            history = []
    else:
        history = []
    history = [e for e in history if e.get("date") != today]
    history.append(entry)
    history.sort(key=lambda e: e.get("date", ""))

    SNAPSHOT.write_text(json.dumps(history, indent=2), encoding="utf-8")
    print(f"\n  -> {SNAPSHOT}  ({len(history)} snapshots, {SNAPSHOT.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
