import json
import logging
import os
import random
import signal
import time
from datetime import datetime, timezone
from typing import Any

from confluent_kafka import Producer
from pythonjsonlogger import jsonlogger


DEVICES = [
    {"device_id": "router-east-01", "device_type": "router", "ip_address": "10.10.1.1", "location": "us-east"},
    {"device_id": "switch-core-01", "device_type": "switch", "ip_address": "10.10.1.10", "location": "core-dc"},
    {"device_id": "firewall-edge-01", "device_type": "firewall", "ip_address": "10.10.1.254", "location": "edge"},
    {"device_id": "linux-app-01", "device_type": "linux-server", "ip_address": "10.10.2.20", "location": "app-tier"},
    {"device_id": "service-api-01", "device_type": "service", "ip_address": "10.10.3.15", "location": "services"},
]

TOPICS = ["device-metrics", "network-telemetry", "service-health"]
running = True


def configure_logging() -> logging.Logger:
    handler = logging.StreamHandler()
    handler.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    logger = logging.getLogger("telemetry-generator")
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


logger = configure_logging()


def shutdown(_: int, __: Any) -> None:
    global running
    running = False


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return round(max(low, min(high, value)), 2)


def choose_status(cpu: float, memory: float, packet_loss: float, latency: float) -> str:
    if cpu >= 95 or packet_loss >= 10 or latency >= 350:
        return "critical"
    if cpu >= 85 or memory >= 90 or packet_loss >= 5 or latency >= 200:
        return "warning"
    return "healthy"


def make_event(device: dict[str, str]) -> dict[str, Any]:
    stress = random.random()
    cpu = random.gauss(55, 18)
    memory = random.gauss(60, 15)
    packet_loss = abs(random.gauss(1.2, 1.4))
    latency = abs(random.gauss(80, 45))

    if stress > 0.88:
        cpu += random.uniform(25, 45)
        memory += random.uniform(15, 35)
        packet_loss += random.uniform(3, 9)
        latency += random.uniform(100, 280)

    event = {
        **device,
        "cpu_usage": clamp(cpu),
        "memory_usage": clamp(memory),
        "disk_usage": clamp(random.gauss(52, 18)),
        "latency_ms": round(max(1, latency), 2),
        "packet_loss": round(max(0, packet_loss), 2),
        "bytes_in": random.randint(120_000, 2_500_000),
        "bytes_out": random.randint(90_000, 2_100_000),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    event["status"] = choose_status(event["cpu_usage"], event["memory_usage"], event["packet_loss"], event["latency_ms"])
    return event


def delivery_report(error: Any, message: Any) -> None:
    if error is not None:
        logger.warning("Kafka delivery failed: %s", error)
    else:
        logger.info("Published telemetry", extra={"topic": message.topic(), "partition": message.partition()})


def publish_log(producer: Producer, event: dict[str, Any]) -> None:
    payload = {
        "service": "telemetry-generator",
        "level": "WARNING" if event["status"] != "healthy" else "INFO",
        "message": f"{event['device_id']} generated {event['status']} telemetry",
        "device_id": event["device_id"],
        "timestamp": event["timestamp"],
    }
    producer.produce("application-logs", json.dumps(payload).encode("utf-8"), callback=delivery_report)


def main() -> None:
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    interval = float(os.getenv("TELEMETRY_INTERVAL_SECONDS", "2"))
    producer = Producer({"bootstrap.servers": bootstrap_servers})

    logger.info("Telemetry generator started", extra={"bootstrap_servers": bootstrap_servers})
    while running:
        for device in DEVICES:
            event = make_event(device)
            topic = random.choice(TOPICS)
            producer.produce(topic, json.dumps(event).encode("utf-8"), callback=delivery_report)
            publish_log(producer, event)
        producer.poll(0)
        producer.flush(5)
        time.sleep(interval)

    producer.flush(10)
    logger.info("Telemetry generator stopped")


if __name__ == "__main__":
    main()
