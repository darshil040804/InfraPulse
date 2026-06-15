from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AlertRule


DEFAULT_RULES = [
    ("cpu_usage", ">", 85, "warning"),
    ("cpu_usage", ">", 95, "critical"),
    ("memory_usage", ">", 90, "warning"),
    ("packet_loss", ">", 5, "warning"),
    ("latency_ms", ">", 200, "warning"),
]


def seed_alert_rules(db: Session) -> None:
    existing = db.scalar(select(AlertRule.id).limit(1))
    if existing:
        return

    db.add_all(
        AlertRule(metric_name=metric, operator=operator, threshold=threshold, severity=severity)
        for metric, operator, threshold, severity in DEFAULT_RULES
    )
    db.commit()
