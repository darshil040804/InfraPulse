import operator
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Alert, AlertRule, Device, Metric


OPERATORS = {
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
}


def evaluate_metric_alerts(db: Session, device: Device, metric: Metric) -> list[Alert]:
    rules = db.scalars(select(AlertRule).where(AlertRule.enabled.is_(True))).all()
    created: list[Alert] = []

    for rule in rules:
        value = getattr(metric, rule.metric_name, None)
        comparison = OPERATORS.get(rule.operator)
        if value is None or comparison is None or not comparison(float(value), rule.threshold):
            continue

        signature = f"{rule.metric_name}:{rule.operator}:{rule.threshold}"
        duplicate = db.scalar(
            select(Alert).where(
                Alert.device_id == device.id,
                Alert.alert_type == rule.metric_name,
                Alert.severity == rule.severity,
                Alert.status == "active",
                Alert.rule_signature == signature,
            )
        )
        if duplicate:
            continue

        alert = Alert(
            device_id=device.id,
            severity=rule.severity,
            alert_type=rule.metric_name,
            message=f"{device.hostname} {rule.metric_name} is {value:.1f}, threshold {rule.operator} {rule.threshold:.1f}",
            status="active",
            rule_signature=signature,
            created_at=datetime.now(timezone.utc),
        )
        db.add(alert)
        created.append(alert)

    return created
