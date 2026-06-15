import json
import logging
import threading
from typing import Any

from confluent_kafka import Consumer, KafkaException

from app.core.config import get_settings
from app.db.database import SessionLocal
from app.services.telemetry_service import store_log_event, upsert_metric_event

logger = logging.getLogger(__name__)


class KafkaConsumerWorker:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._consumer: Consumer | None = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run, name="kafka-consumer", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._consumer:
            self._consumer.close()

    def _run(self) -> None:
        config = {
            "bootstrap.servers": self.settings.kafka_bootstrap_servers,
            "group.id": "infrapulse-backend",
            "auto.offset.reset": "earliest",
        }
        self._consumer = Consumer(config)

        try:
            self._consumer.subscribe(self.settings.topics)
            logger.info("Kafka consumer subscribed", extra={"topics": self.settings.topics})
            while not self._stop_event.is_set():
                message = self._consumer.poll(1.0)
                if message is None:
                    continue
                if message.error():
                    logger.warning("Kafka consumer error: %s", message.error())
                    continue
                self._handle_message(message.topic(), message.value())
        except KafkaException:
            logger.exception("Kafka consumer failed")
        finally:
            if self._consumer:
                self._consumer.close()

    def _handle_message(self, topic: str, raw_value: bytes) -> None:
        try:
            payload: dict[str, Any] = json.loads(raw_value.decode("utf-8"))
        except json.JSONDecodeError:
            logger.warning("Skipping invalid Kafka JSON", extra={"topic": topic})
            return

        with SessionLocal() as db:
            if topic == "application-logs":
                store_log_event(db, payload)
            else:
                upsert_metric_event(db, payload)
