import json
import logging

from support_triage.core.config import settings
from support_triage.core.logging import configure_logging
from support_triage.db.sql import SessionLocal, create_tables
from support_triage.messaging.rabbitmq import consume
from support_triage.services.tickets import process_ticket


LOGGER = logging.getLogger(__name__)


def on_message(channel, method, properties, body: bytes) -> None:
    del properties
    session = SessionLocal()
    try:
        message = json.loads(body.decode("utf-8"))
        process_ticket(int(message["ticket_id"]), session)
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception:
        LOGGER.exception("Worker failed to process message: %s", body)
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    finally:
        session.close()


def main() -> None:
    configure_logging()
    create_tables()
    LOGGER.info("Worker listening on queue %s", settings.ticket_queue)
    consume(on_message)


if __name__ == "__main__":
    main()
