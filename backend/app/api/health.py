from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.common import HealthResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check API and database health",
    description="Runs a lightweight database query and returns the current API health status.",
)
def health(db: Session = Depends(get_db)) -> HealthResponse:
    db.execute(text("select 1"))
    return HealthResponse(
        status="ok",
        database="ok",
        service="infrapulse-api",
        timestamp=datetime.now(timezone.utc),
    )
