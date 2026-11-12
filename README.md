# Service Monitoring & Incident Response Lab

A runnable operations lab for junior cloud/application-support interviews. It contains a small Python HTTP service, Nginx reverse proxy, Docker Compose deployment, health-probe scripting, JSONL check history, incident summaries and an outage runbook.

## Learning goals

Linux terminal basics · HTTP/DNS troubleshooting concepts · service health checks · logs · retries · reverse proxies · Docker · incident diagnosis · Python scripting · GitHub Actions.

## Prerequisites

Python 3.10+ and Docker Desktop with Compose (or Docker Engine + Compose plugin).

## Start and verify

```bash
docker compose up -d --build
curl -i http://127.0.0.1:8090/healthz
python3 scripts/check_service.py
python3 scripts/summarize_checks.py
```

Only the loopback port `127.0.0.1:8090` is exposed locally. The app is not configured for public production hosting.

## Simulate, diagnose and recover

```bash
DEMO_FAIL_MODE=1 docker compose up -d --force-recreate
python3 scripts/check_service.py   # expect DOWN and exit status 2
docker compose ps
docker compose logs --tail=80
DEMO_FAIL_MODE=0 docker compose up -d --force-recreate
python3 scripts/check_service.py   # expect UP
python3 scripts/summarize_checks.py
```

Use `docs/incident-runbook.md` to record what you actually observe. A failed health check is not always the same as a totally unavailable host—explain the difference during interviews.

## Without Docker

```bash
python3 -m app.server
python3 scripts/check_service.py --url http://127.0.0.1:8080/healthz
python3 -m unittest discover -s tests -v
```

## Public portfolio page

GitHub Pages serves the static runbook overview from `docs/` when configured with **GitHub Actions** as the Pages source. It is **not live monitoring**; don't claim production uptime, public cloud hosting or real incidents.

## Practice exercises

- Reproduce a 503 incident and document the response, log evidence and recovery.
- Add a response-time threshold to the probe with a unit test.
- Describe the path from browser → host port → Nginx proxy → application container.
- Explain the difference between a process running and a service responding correctly.
