from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import OrmModel


class AlertRead(OrmModel):
    id: int
    device_id: int
    severity: str
    alert_type: str
    message: str
    status: str
    created_at: datetime
    resolved_at: datetime | None


class AlertRuleCreate(BaseModel):
    metric_name: str = Field(min_length=2, max_length=50)
    operator: str = Field(pattern=r"^(>|>=|<|<=|==)$")
    threshold: float
    severity: str = Field(pattern=r"^(info|warning|critical)$")
    enabled: bool = True


class AlertRuleRead(OrmModel):
    id: int
    metric_name: str
    operator: str
    threshold: float
    severity: str
    enabled: bool
    created_at: datetime
