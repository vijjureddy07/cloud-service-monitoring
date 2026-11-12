#!/usr/bin/env python3
"""Perform health checks with timeouts/retries and emit a JSONL event.

Exit 0 for healthy, 2 for unhealthy. No third-party dependencies.
"""
import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def probe(url, timeout=3):
    start = time.monotonic()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            status = response.status
            payload = json.loads(response.read().decode('utf-8'))
        okay = status == 200 and payload.get('status') == 'ok'
        reason = 'healthy' if okay else f'Unexpected status or payload: {status}'
    except urllib.error.HTTPError as error:
        okay, status, reason = False, error.code, f'HTTP {error.code}'
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as error:
        okay, status, reason = False, None, type(error).__name__
    return {"ok": okay, "status_code": status, "reason": reason, "latency_ms": round((time.monotonic() - start) * 1000, 1)}


def run_checks(url, attempts=3, delay=1, timeout=3, sleep=time.sleep, probe_func=probe):
    if attempts < 1: raise ValueError('attempts must be positive')
    attempts_made = []
    for number in range(attempts):
        result = probe_func(url, timeout=timeout)
        attempts_made.append(result)
        if result['ok']: break
        if number < attempts - 1: sleep(delay)
    final = attempts_made[-1]
    return {"timestamp": datetime.now(timezone.utc).isoformat(), "url": url,
            "outcome": "UP" if final['ok'] else "DOWN", "attempts": len(attempts_made),
            "status_code": final['status_code'], "latency_ms": final['latency_ms'], "reason": final['reason']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:8090/healthz')
    parser.add_argument('--attempts', type=int, default=3)
    parser.add_argument('--delay', type=float, default=1.0)
    parser.add_argument('--timeout', type=float, default=3.0)
    parser.add_argument('--output', default='logs/checks.jsonl')
    args = parser.parse_args()
    event = run_checks(args.url, args.attempts, args.delay, args.timeout)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(event) + '\n')
    print(json.dumps(event, indent=2))
    raise SystemExit(0 if event['outcome'] == 'UP' else 2)

if __name__ == '__main__': main()
