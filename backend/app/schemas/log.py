from datetime import datetime

from app.schemas.common import OrmModel


class LogRead(OrmModel):
    id: int
    service: str
    level: str
    message: str
    device_id: int | None
    timestamp: datetime
