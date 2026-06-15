from datetime import datetime

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_devices: int
    healthy_devices: int
    warning_devices: int
    critical_devices: int
    down_devices: int
    active_alerts: int
    average_cpu_usage: float
    average_memory_usage: float
    bytes_in_total: int
    bytes_out_total: int
    last_event_received: datetime | None
