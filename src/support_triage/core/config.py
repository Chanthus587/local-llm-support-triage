import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv() -> None:
        return None


load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "local-llm-support-triage")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://triage:triage@localhost:5432/triage",
    )
    mongo_url: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    mongo_database: str = os.getenv("MONGO_DATABASE", "support_triage")
    rabbitmq_url: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    ticket_queue: str = os.getenv("TICKET_QUEUE", "ticket.triage")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
