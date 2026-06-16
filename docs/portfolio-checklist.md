# InfraPulse Portfolio Checklist

Use this checklist after the stack is running and the demo data has been reset.

## Demo Setup

```powershell
.\scripts\start.ps1
.\scripts\reset-demo.ps1
docker compose ps
```

Open:

- Dashboard: http://localhost:3000
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Screenshots To Capture

Save screenshots in `docs/screenshots/` with these names:

- `01-overview-dashboard.png`: overview page with summary cards, charts, device snapshot, and active alerts.
- `02-devices-table.png`: devices page showing router, switch, firewall, Linux server, and service rows.
- `03-device-detail.png`: one unhealthy or warning device detail page with metric charts and recent alerts.
- `04-alerts.png`: alerts page with active and resolved alert examples.
- `05-logs.png`: logs page with structured operational events.
- `06-api-docs.png`: FastAPI docs with `GET /api/dashboard/summary` expanded and a successful response visible.
- `07-docker-compose-ps.png`: terminal output proving all local services are running.
- `08-ci-passing.png`: GitHub Actions page showing backend, frontend, audit, and Compose checks passing.

## Demo Talk Track

1. InfraPulse simulates infrastructure telemetry from routers, switches, firewalls, Linux servers, and services.
2. The telemetry generator publishes Kafka-compatible events into Redpanda.
3. FastAPI consumes events, validates payloads, persists metrics to PostgreSQL, and creates alerts from threshold rules.
4. React presents a dense operations dashboard with health summaries, trends, devices, alerts, logs, and API failure states.
5. Docker Compose runs the complete local platform, and GitHub Actions validates tests, builds, audits, and Compose config on every push.
6. Ansible demonstrates how the same local stack can be managed through repeatable deployment automation.

## Resume Bullets

- Built InfraPulse, a Docker Compose observability platform with React, FastAPI, PostgreSQL, and Kafka-compatible telemetry streaming.
- Implemented simulated infrastructure telemetry for network devices, Linux hosts, and services, with backend ingestion, persistence, alert rules, and structured logs.
- Designed a TypeScript operations dashboard with device health, metric charts, alert resolution, logs, loading states, and API failure handling.
- Added CI checks for backend tests, frontend build, npm audit, and Docker Compose validation using GitHub Actions.
- Created demo reset scripts and Ansible automation to make the project repeatable for portfolio presentations.

## Final Pre-Resume Check

Run:

```powershell
.\scripts\test.ps1
git status --short
git log --oneline -5
```

Before adding the project to your resume, make sure:

- The GitHub repo is public.
- CI is green on `main`.
- `README.md` has the CI badge visible.
- Screenshots are committed or attached in the portfolio writeup.
- No real secrets are present in `.env.example`, docs, or committed files.
