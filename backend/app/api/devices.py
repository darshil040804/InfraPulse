from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Alert, Device, LogEvent, Metric
from app.schemas.device import DeviceDetail, DeviceRead, DeviceWithLatestMetric

router = APIRouter(prefix="/api/devices", tags=["devices"])


@router.get(
    "",
    response_model=list[DeviceWithLatestMetric],
    summary="List monitored devices",
    description="Returns every monitored device with its latest metric sample for table and status-card views.",
)
def list_devices(db: Session = Depends(get_db)) -> list[DeviceWithLatestMetric]:
    devices = db.scalars(select(Device).order_by(Device.hostname)).all()
    response: list[DeviceWithLatestMetric] = []
    for device in devices:
        latest = db.scalar(select(Metric).where(Metric.device_id == device.id).order_by(desc(Metric.timestamp)).limit(1))
        item = DeviceWithLatestMetric.model_validate(device)
        item.latest_metric = latest
        response.append(item)
    return response


@router.get(
    "/{device_id}",
    response_model=DeviceDetail,
    summary="Get device detail",
    description="Returns inventory metadata, recent metrics, recent alerts, and recent logs for a single device hostname.",
)
def get_device(device_id: str, db: Session = Depends(get_db)) -> DeviceDetail:
    device = db.scalar(select(Device).where(Device.hostname == device_id))
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    recent_metrics = db.scalars(
        select(Metric).where(Metric.device_id == device.id).order_by(desc(Metric.timestamp)).limit(100)
    ).all()
    recent_alerts = db.scalars(
        select(Alert).where(Alert.device_id == device.id).order_by(desc(Alert.created_at)).limit(25)
    ).all()
    recent_logs = db.scalars(
        select(LogEvent).where(LogEvent.device_id == device.id).order_by(desc(LogEvent.timestamp)).limit(25)
    ).all()

    return DeviceDetail(
        device=DeviceRead.model_validate(device),
        latest_metric=recent_metrics[0] if recent_metrics else None,
        recent_metrics=list(reversed(recent_metrics)),
        recent_alerts=recent_alerts,
        recent_logs=recent_logs,
    )
