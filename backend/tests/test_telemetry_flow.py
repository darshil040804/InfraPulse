from app.db.models import Alert, Device
from app.services.seed import seed_alert_rules
from app.services.telemetry_service import upsert_metric_event


def test_metric_event_creates_device_and_alert(db_session) -> None:
    seed_alert_rules(db_session)
    metric = upsert_metric_event(
        db_session,
        {
            "device_id": "router-east-01",
            "device_type": "router",
            "ip_address": "10.0.0.1",
            "location": "us-east",
            "cpu_usage": 97,
            "memory_usage": 64,
            "disk_usage": 40,
            "latency_ms": 90,
            "packet_loss": 1,
            "bytes_in": 1000,
            "bytes_out": 800,
            "timestamp": "2026-06-15T14:30:00Z",
        },
    )
    assert metric.cpu_usage == 97
    assert db_session.query(Device).count() == 1
    assert db_session.query(Alert).filter_by(status="active").count() >= 1
