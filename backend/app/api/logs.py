from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import LogEvent
from app.schemas.log import LogRead

router = APIRouter(prefix="/api/logs", tags=["logs"])


@router.get(
    "/recent",
    response_model=list[LogRead],
    summary="Get recent logs",
    description="Returns recent structured log events captured from backend and telemetry services.",
)
def recent_logs(limit: int = Query(default=100, ge=1, le=500), db: Session = Depends(get_db)) -> list[LogEvent]:
    return db.scalars(select(LogEvent).order_by(desc(LogEvent.timestamp)).limit(limit)).all()
