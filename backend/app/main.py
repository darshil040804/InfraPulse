from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import alerts, dashboard, devices, health, logs, metrics
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.database import Base, SessionLocal, engine
from app.services.kafka_consumer import KafkaConsumerWorker
from app.services.seed import seed_alert_rules

configure_logging()
settings = get_settings()
kafka_worker = KafkaConsumerWorker()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_alert_rules(db)
    if settings.enable_kafka_consumer:
        kafka_worker.start()
    yield
    kafka_worker.stop()


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(dashboard.router)
app.include_router(devices.router)
app.include_router(metrics.router)
app.include_router(alerts.router)
app.include_router(logs.router)
