#!/usr/bin/env python3
"""Summarize a local check log and produce a reproducible incident overview."""
import argparse
import json
from pathlib import Path


def summarize(events):
    if not events:
        return {"checks": 0, "up": 0, "down": 0, "availability_percent": None, "incidents": 0}
    ups = sum(item['outcome'] == 'UP' for item in events)
    incidents, prev_down = 0, False
    for item in events:
        current_down = item['outcome'] == 'DOWN'
        if current_down and not prev_down:
            incidents += 1
        prev_down = current_down
    return {"checks": len(events), "up": ups, "down": len(events) - ups,
            "availability_percent": round(100 * ups / len(events), 2), "incidents": incidents}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', default='logs/checks.jsonl')
    args = parser.parse_args()
    p = Path(args.file)
    if not p.exists():
        print('No checks recorded yet.')
        return
    events = [json.loads(line) for line in p.read_text().splitlines() if line.strip()]
    print(json.dumps(summarize(events), indent=2))

if __name__ == '__main__': main()
