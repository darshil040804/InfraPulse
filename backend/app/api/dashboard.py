from fastapi import APIRouter, Depends
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Alert, Device, Metric
from app.schemas.dashboard import DashboardSummary

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get(
    "/summary",
    response_model=DashboardSummary,
    summary="Get dashboard summary",
    description="Returns aggregate counts and averages used by the InfraPulse overview dashboard.",
)
def summary(db: Session = Depends(get_db)) -> DashboardSummary:
    total_devices = db.scalar(select(func.count(Device.id))) or 0
    status_counts = dict(db.execute(select(Device.status, func.count(Device.id)).group_by(Device.status)).all())
    active_alerts = db.scalar(select(func.count(Alert.id)).where(Alert.status == "active")) or 0
    averages = db.execute(select(func.avg(Metric.cpu_usage), func.avg(Metric.memory_usage))).one()
    traffic = db.execute(select(func.coalesce(func.sum(Metric.bytes_in), 0), func.coalesce(func.sum(Metric.bytes_out), 0))).one()
    last_event = db.scalar(select(Metric.timestamp).order_by(desc(Metric.timestamp)).limit(1))

    return DashboardSummary(
        total_devices=total_devices,
        healthy_devices=status_counts.get("healthy", 0),
        warning_devices=status_counts.get("warning", 0),
        critical_devices=status_counts.get("critical", 0),
        down_devices=status_counts.get("down", 0),
        active_alerts=active_alerts,
        average_cpu_usage=round(float(averages[0] or 0), 2),
        average_memory_usage=round(float(averages[1] or 0), 2),
        bytes_in_total=int(traffic[0] or 0),
        bytes_out_total=int(traffic[1] or 0),
        last_event_received=last_event,
    )
