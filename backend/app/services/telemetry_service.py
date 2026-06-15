from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Device, LogEvent, Metric
from app.services.alert_engine import evaluate_metric_alerts


def parse_timestamp(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def status_from_metric(payload: dict[str, Any]) -> str:
    if payload.get("status"):
        return str(payload["status"])
    if payload.get("cpu_usage", 0) >= 95 or payload.get("packet_loss", 0) >= 10:
        return "critical"
    if payload.get("cpu_usage", 0) >= 85 or payload.get("memory_usage", 0) >= 90 or payload.get("packet_loss", 0) >= 5:
        return "warning"
    return "healthy"


def upsert_metric_event(db: Session, payload: dict[str, Any]) -> Metric:
    hostname = str(payload["device_id"])
    timestamp = parse_timestamp(payload.get("timestamp"))
    status = status_from_metric(payload)

    device = db.scalar(select(Device).where(Device.hostname == hostname))
    if not device:
        device = Device(
            hostname=hostname,
            device_type=str(payload.get("device_type", "unknown")),
            ip_address=str(payload.get("ip_address", "0.0.0.0")),
            location=str(payload.get("location", "unknown")),
            status=status,
            last_seen=timestamp,
        )
        db.add(device)
        db.flush()
    else:
        device.device_type = str(payload.get("device_type", device.device_type))
        device.ip_address = str(payload.get("ip_address", device.ip_address))
        device.location = str(payload.get("location", device.location))
        device.status = status
        device.last_seen = timestamp

    metric = Metric(
        device_id=device.id,
        cpu_usage=float(payload.get("cpu_usage", 0)),
        memory_usage=float(payload.get("memory_usage", 0)),
        disk_usage=float(payload.get("disk_usage", 0)),
        latency_ms=float(payload.get("latency_ms", 0)),
        packet_loss=float(payload.get("packet_loss", 0)),
        bytes_in=int(payload.get("bytes_in", 0)),
        bytes_out=int(payload.get("bytes_out", 0)),
        status=status,
        timestamp=timestamp,
    )
    db.add(metric)
    db.flush()

    created_alerts = evaluate_metric_alerts(db, device, metric)
    log_level = "WARNING" if created_alerts or status in {"warning", "critical"} else "INFO"
    db.add(
        LogEvent(
            service="fastapi-backend",
            level=log_level,
            message=f"Processed telemetry for {hostname} with status {status}",
            device_id=device.id,
            timestamp=timestamp,
        )
    )
    db.commit()
    db.refresh(metric)
    return metric


def store_log_event(db: Session, payload: dict[str, Any]) -> LogEvent:
    hostname = payload.get("device_id")
    device = db.scalar(select(Device).where(Device.hostname == hostname)) if hostname else None
    log = LogEvent(
        service=str(payload.get("service", "telemetry-generator")),
        level=str(payload.get("level", "INFO")),
        message=str(payload.get("message", "Telemetry event")),
        device_id=device.id if device else None,
        timestamp=parse_timestamp(payload.get("timestamp")),
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
