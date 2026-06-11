import json
from collections.abc import Callable

import pika

from support_triage.core.config import settings


def _connection() -> pika.BlockingConnection:
    return pika.BlockingConnection(pika.URLParameters(settings.rabbitmq_url))


def declare_queue(channel: pika.channel.Channel) -> None:
    channel.queue_declare(queue=settings.ticket_queue, durable=True)


def publish_ticket(ticket_id: int) -> None:
    connection = _connection()
    try:
        channel = connection.channel()
        declare_queue(channel)
        channel.basic_publish(
            exchange="",
            routing_key=settings.ticket_queue,
            body=json.dumps({"ticket_id": ticket_id}).encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2),
        )
    finally:
        connection.close()


def consume(callback: Callable) -> None:
    connection = _connection()
    channel = connection.channel()
    declare_queue(channel)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=settings.ticket_queue, on_message_callback=callback)
    channel.start_consuming()
