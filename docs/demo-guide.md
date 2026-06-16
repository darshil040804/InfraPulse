# InfraPulse Demo Guide

This guide is the short path for recording or presenting the local demo.

## 1. Start The Stack

```powershell
.\scripts\start.ps1
```

Wait until `backend`, `frontend`, `postgres`, `kafka`, and `telemetry-generator` are running.

## 2. Reset Stable Demo Data

```powershell
.\scripts\reset-demo.ps1
```

This seeds deterministic data and stops the telemetry generator. The dashboard will stop changing while you take screenshots.

## 3. Walk Through The Product

- Start at `http://localhost:3000`.
- Show the overview cards, charts, device snapshot, and alerts.
- Open the Devices page and drill into one device.
- Resolve one alert on the Alerts page.
- Show structured events on the Logs page.
- Open `http://localhost:8000/docs` and execute `GET /api/dashboard/summary`.

## 4. Resume Live Telemetry

```powershell
docker compose up -d telemetry-generator
```

Refresh the dashboard after a few seconds to show live data changing again.

## 5. Stop The Stack

```powershell
.\scripts\stop.ps1
```
