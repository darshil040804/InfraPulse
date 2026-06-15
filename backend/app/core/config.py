from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "InfraPulse API"
    database_url: str = Field(
        default="postgresql+psycopg://infrapulse:infrapulse_password@localhost:5432/infrapulse",
        alias="DATABASE_URL",
    )
    kafka_bootstrap_servers: str = Field(default="localhost:9092", alias="KAFKA_BOOTSTRAP_SERVERS")
    kafka_topics: str = Field(
        default="device-metrics,network-telemetry,service-health,application-logs",
        alias="KAFKA_TOPICS",
    )
    enable_kafka_consumer: bool = Field(default=True, alias="ENABLE_KAFKA_CONSUMER")
    cors_origins: str = Field(default="http://localhost:3000,http://127.0.0.1:3000", alias="CORS_ORIGINS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def topics(self) -> list[str]:
        return [topic.strip() for topic in self.kafka_topics.split(",") if topic.strip()]

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
