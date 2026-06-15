from datetime import datetime

from app.schemas.common import OrmModel


class MetricRead(OrmModel):
    id: int
    device_id: int
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    latency_ms: float
    packet_loss: float
    bytes_in: int
    bytes_out: int
    status: str
    timestamp: datetime
