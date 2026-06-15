from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import OrmModel
from app.schemas.metric import MetricRead


class DeviceRead(OrmModel):
    id: int
    hostname: str
    device_type: str
    ip_address: str
    location: str
    status: str
    last_seen: datetime | None
    created_at: datetime


class DeviceWithLatestMetric(DeviceRead):
    latest_metric: MetricRead | None = None


class DeviceDetail(BaseModel):
    device: DeviceRead
    latest_metric: MetricRead | None
    recent_metrics: list[MetricRead]
    recent_alerts: list["AlertRead"]
    recent_logs: list["LogRead"]


from app.schemas.alert import AlertRead  # noqa: E402
from app.schemas.log import LogRead  # noqa: E402

DeviceDetail.model_rebuild()
