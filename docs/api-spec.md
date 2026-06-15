# InfraPulse API Spec

Base URL: `http://localhost:8000`

## Health

`GET /health`

Returns service health and database connectivity.

## Dashboard

`GET /api/dashboard/summary`

Returns device counts, active alert count, average resource usage, network totals, and last event timestamp.

## Devices

`GET /api/devices`

Returns devices with their latest metric.

`GET /api/devices/{device_id}`

Returns one device, latest metric, recent metrics, recent alerts, and recent logs.

## Metrics

`GET /api/metrics/recent?limit=100`

Returns recent metrics across all devices.

`GET /api/metrics/{device_id}?limit=100`

Returns recent metrics for one device.

## Alerts

`GET /api/alerts?severity=warning&status=active`

Returns alerts sorted newest first. Filters are optional.

`POST /api/alerts/rules`

Creates an alert rule.

`PATCH /api/alerts/{alert_id}/resolve`

Marks an alert as resolved.

## Logs

`GET /api/logs/recent?limit=100`

Returns recent structured log events stored by the backend.
