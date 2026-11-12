# Incident runbook — simulated service outage

This runbook covers the included educational sample service, **not** a production system.

## Symptoms and severity

- Monitor returns DOWN after retries, HTTP 503 or connection error.
- User-facing `/healthz` unavailable means health check is failing; classify as a sample P2 incident for practice only.

## Reproduce

1. `docker compose up -d --build`
2. `python3 scripts/check_service.py` → UP
3. `DEMO_FAIL_MODE=1 docker compose up -d --force-recreate` → restart with a simulated failure
4. `python3 scripts/check_service.py` → DOWN (exit code 2)
5. `docker compose ps`, `docker compose logs --tail=100` → inspect container state/logs
6. `DEMO_FAIL_MODE=0 docker compose up -d --force-recreate` → restore
7. `python3 scripts/check_service.py` → UP
8. `python3 scripts/summarize_checks.py` → report availability and incident groups

## Notes to record personally

- Timestamp and symptom; affected path; status code
- Likely cause (configured failure mode in demo); log evidence
- Recovery action and verification command
- One prevention improvement you'd make

Never present the simulated incident as a customer outage or real production on-call experience.
