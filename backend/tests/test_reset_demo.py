from sqlalchemy import func, select

from app.db.models import Alert, AlertRule, Device, LogEvent, Metric
from app.scripts.reset_demo import reset_demo_data


def test_reset_demo_data_creates_repeatable_snapshot(db_session) -> None:
    counts = reset_demo_data(db_session)

    assert counts == {"devices": 5, "metrics": 120, "alerts": 5, "logs": 5}
    assert db_session.scalar(select(func.count(Device.id))) == 5
    assert db_session.scalar(select(func.count(Metric.id))) == 120
    assert db_session.scalar(select(func.count(Alert.id))) == 5
    assert db_session.scalar(select(func.count(LogEvent.id))) == 5
    assert db_session.scalar(select(func.count(AlertRule.id))) >= 5
    assert db_session.scalar(select(func.count(Alert.id)).where(Alert.status == "active")) == 4
