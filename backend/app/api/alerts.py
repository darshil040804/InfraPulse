from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Alert, AlertRule
from app.schemas.alert import AlertRead, AlertRuleCreate, AlertRuleRead

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertRead])
def list_alerts(
    severity: str | None = None,
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[Alert]:
    query = select(Alert)
    if severity:
        query = query.where(Alert.severity == severity)
    if status:
        query = query.where(Alert.status == status)
    return db.scalars(query.order_by(desc(Alert.created_at)).limit(200)).all()


@router.post("/rules", response_model=AlertRuleRead, status_code=201)
def create_rule(rule: AlertRuleCreate, db: Session = Depends(get_db)) -> AlertRule:
    db_rule = AlertRule(**rule.model_dump())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


@router.patch("/{alert_id}/resolve", response_model=AlertRead)
def resolve_alert(alert_id: int, db: Session = Depends(get_db)) -> Alert:
    alert = db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = "resolved"
    alert.resolved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(alert)
    return alert
