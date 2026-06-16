from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.db.database import Base, SessionLocal, engine
from app.db.models import Alert, AlertRule, Device, LogEvent, Metric
from app.services.seed import seed_alert_rules

DEMO_DEVICES = [
    {
        "hostname": "router-east-01",
        "device_type": "router",
        "ip_address": "10.10.1.1",
        "location": "us-east",
        "status": "warning",
        "cpu_base": 72,
        "memory_base": 66,
        "latency_base": 122,
        "packet_loss_base": 2.2,
    },
    {
        "hostname": "switch-core-01",
        "device_type": "switch",
        "ip_address": "10.10.1.10",
        "location": "core-dc",
        "status": "healthy",
        "cpu_base": 41,
        "memory_base": 58,
        "latency_base": 42,
        "packet_loss_base": 0.4,
    },
    {
        "hostname": "firewall-edge-01",
        "device_type": "firewall",
        "ip_address": "10.10.1.254",
        "location": "edge",
        "status": "critical",
        "cpu_base": 88,
        "memory_base": 74,
        "latency_base": 236,
        "packet_loss_base": 6.1,
    },
    {
        "hostname": "linux-app-01",
        "device_type": "linux-server",
        "ip_address": "10.10.2.20",
        "location": "app-tier",
        "status": "healthy",
        "cpu_base": 54,
        "memory_base": 63,
        "latency_base": 71,
        "packet_loss_base": 0.9,
    },
    {
        "hostname": "service-api-01",
        "device_type": "service",
        "ip_address": "10.10.3.15",
        "location": "services",
        "status": "warning",
        "cpu_base": 68,
        "memory_base": 91,
        "latency_base": 164,
        "packet_loss_base": 1.6,
    },
]


def metric_status(cpu_usage: float, memory_usage: float, latency_ms: float, packet_loss: float) -> str:
    if cpu_usage >= 95 or latency_ms >= 300 or packet_loss >= 10:
        return "critical"
    if cpu_usage >= 85 or memory_usage >= 90 or latency_ms >= 200 or packet_loss >= 5:
        return "warning"
    return "healthy"


def reset_demo_data(db: Session, base_time: datetime | None = None) -> dict[str, int]:
    Base.metadata.create_all(bind=engine)
    base_time = base_time or datetime.now(timezone.utc).replace(microsecond=0)

    for model in (LogEvent, Alert, Metric, Device, AlertRule):
        db.query(model).delete(synchronize_session=False)
    db.commit()
    seed_alert_rules(db)

    devices: dict[str, Device] = {}
    for spec in DEMO_DEVICES:
        device = Device(
            hostname=spec["hostname"],
            device_type=spec["device_type"],
            ip_address=spec["ip_address"],
            location=spec["location"],
            status=spec["status"],
            last_seen=base_time,
            created_at=base_time - timedelta(days=7),
        )
        db.add(device)
        devices[device.hostname] = device
    db.flush()

    for index in range(24):
        timestamp = base_time - timedelta(minutes=(23 - index) * 2)
        wave = ((index % 6) - 2) * 2.8
        for spec in DEMO_DEVICES:
            device = devices[spec["hostname"]]
            cpu_usage = min(99.0, max(5.0, float(spec["cpu_base"]) + wave))
            memory_usage = min(99.0, max(5.0, float(spec["memory_base"]) + ((index % 4) * 1.7)))
            latency_ms = max(1.0, float(spec["latency_base"]) + ((index % 5) * 8.5))
            packet_loss = max(0.0, float(spec["packet_loss_base"]) + ((index % 3) * 0.35))
            status = metric_status(cpu_usage, memory_usage, latency_ms, packet_loss)
            if index == 23:
                status = str(spec["status"])
                device.status = status
                device.last_seen = timestamp

            db.add(
                Metric(
                    device_id=device.id,
                    cpu_usage=round(cpu_usage, 2),
                    memory_usage=round(memory_usage, 2),
                    disk_usage=round(48 + ((index + device.id) % 10) * 3.1, 2),
                    latency_ms=round(latency_ms, 2),
                    packet_loss=round(packet_loss, 2),
                    bytes_in=620_000 + (index * 38_000) + (device.id * 17_000),
                    bytes_out=510_000 + (index * 31_000) + (device.id * 14_000),
                    status=status,
                    timestamp=timestamp,
                )
            )

    demo_alerts = [
        ("firewall-edge-01", "critical", "packet_loss", "Packet loss above 6 percent on firewall-edge-01", "active", 18),
        ("firewall-edge-01", "warning", "latency_ms", "Latency above 200 ms on firewall-edge-01", "active", 16),
        ("service-api-01", "warning", "memory_usage", "Memory usage above 90 percent on service-api-01", "active", 12),
        ("router-east-01", "warning", "cpu_usage", "CPU usage trending above normal on router-east-01", "active", 9),
        ("linux-app-01", "warning", "disk_usage", "Disk usage spike resolved on linux-app-01", "resolved", 44),
    ]
    for hostname, severity, alert_type, message, status, minutes_ago in demo_alerts:
        created_at = base_time - timedelta(minutes=minutes_ago)
        db.add(
            Alert(
                device_id=devices[hostname].id,
                severity=severity,
                alert_type=alert_type,
                message=message,
                status=status,
                rule_signature=f"demo:{alert_type}:{severity}",
                created_at=created_at,
                resolved_at=base_time - timedelta(minutes=6) if status == "resolved" else None,
            )
        )

    demo_logs = [
        ("fastapi-backend", "INFO", "Dashboard summary generated from PostgreSQL telemetry", None, 5),
        ("telemetry-generator", "INFO", "Published SNMP-style metrics for switch-core-01", "switch-core-01", 8),
        ("fastapi-backend", "WARNING", "High latency alert evaluated for firewall-edge-01", "firewall-edge-01", 12),
        ("telemetry-generator", "WARNING", "Service memory pressure simulated for service-api-01", "service-api-01", 14),
        ("fastapi-backend", "INFO", "Alert rule seed completed", None, 20),
    ]
    for service, level, message, hostname, minutes_ago in demo_logs:
        db.add(
            LogEvent(
                service=service,
                level=level,
                message=message,
                device_id=devices[hostname].id if hostname else None,
                timestamp=base_time - timedelta(minutes=minutes_ago),
            )
        )

    db.commit()
    return {
        "devices": len(DEMO_DEVICES),
        "metrics": len(DEMO_DEVICES) * 24,
        "alerts": len(demo_alerts),
        "logs": len(demo_logs),
    }


def main() -> None:
    with SessionLocal() as db:
        counts = reset_demo_data(db)
    print(
        "Demo data reset: "
        f"{counts['devices']} devices, "
        f"{counts['metrics']} metrics, "
        f"{counts['alerts']} alerts, "
        f"{counts['logs']} logs."
    )


if __name__ == "__main__":
    main()
