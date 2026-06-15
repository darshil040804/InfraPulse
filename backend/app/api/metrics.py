from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Device, Metric
from app.schemas.metric import MetricRead

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get(
    "/recent",
    response_model=list[MetricRead],
    summary="Get recent metrics",
    description="Returns recent telemetry samples across all devices, sorted newest first.",
)
def recent_metrics(limit: int = Query(default=100, ge=1, le=500), db: Session = Depends(get_db)) -> list[Metric]:
    return db.scalars(select(Metric).order_by(desc(Metric.timestamp)).limit(limit)).all()


@router.get(
    "/{device_id}",
    response_model=list[MetricRead],
    summary="Get metrics for one device",
    description="Returns recent telemetry samples for a single device hostname, ordered oldest to newest for charting.",
)
def device_metrics(
    device_id: str,
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[Metric]:
    device = db.scalar(select(Device).where(Device.hostname == device_id))
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    metrics = db.scalars(select(Metric).where(Metric.device_id == device.id).order_by(desc(Metric.timestamp)).limit(limit)).all()
    return list(reversed(metrics))
