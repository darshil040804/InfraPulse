# InfraPulse Architecture

InfraPulse is built around a local event pipeline:

1. `telemetry-generator` creates synthetic infrastructure events.
2. Events are published to Kafka-compatible topics.
3. The FastAPI backend runs a Kafka consumer during application startup.
4. Incoming telemetry is validated, stored in PostgreSQL, and evaluated by the alert engine.
5. The React dashboard reads aggregated and device-level data from FastAPI.

## Runtime Services

| Service | Role |
| --- | --- |
| frontend | Vite React dashboard |
| backend | FastAPI API and Kafka consumer |
| postgres | Durable relational store for devices, metrics, alerts, and rules |
| kafka | Local Kafka-compatible event streaming layer, implemented with Redpanda for reliable local pulls |
| telemetry-generator | Synthetic producer for infrastructure telemetry |

## Data Model

- `devices`: inventory and current status.
- `metrics`: time-series telemetry samples.
- `alerts`: active and resolved alert records.
- `alert_rules`: configurable threshold rules.
- `logs`: recent structured application and telemetry log events for dashboard display.

## Alerting

Default rules are seeded on backend startup:

- CPU over 85 percent: warning
- CPU over 95 percent: critical
- Memory over 90 percent: warning
- Packet loss over 5 percent: warning
- Latency over 200 ms: warning

Rules are evaluated against each incoming metric event. Duplicate active alerts for the same device, metric, threshold, and severity are suppressed.
