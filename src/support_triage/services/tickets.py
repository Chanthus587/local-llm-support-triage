import logging

from sqlalchemy.orm import Session, joinedload

from support_triage.db.models import Prediction, Ticket
from support_triage.db.mongo import get_raw_ticket_body, store_llm_output, store_raw_ticket
from support_triage.messaging.rabbitmq import publish_ticket
from support_triage.schemas.tickets import TicketCreate
from support_triage.services.triage import triage_ticket


LOGGER = logging.getLogger(__name__)


def create_ticket(payload: TicketCreate, session: Session) -> Ticket:
    ticket = Ticket(
        customer_id=payload.customer_id,
        subject=payload.subject,
        channel=payload.channel,
        status="queued",
    )
    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    store_raw_ticket(ticket.id, payload.body)
    publish_ticket(ticket.id)
    return ticket


def get_ticket(ticket_id: int, session: Session) -> Ticket | None:
    return (
        session.query(Ticket)
        .options(joinedload(Ticket.prediction))
        .filter(Ticket.id == ticket_id)
        .first()
    )


def list_recent_tickets(session: Session, limit: int = 50) -> list[Ticket]:
    return (
        session.query(Ticket)
        .options(joinedload(Ticket.prediction))
        .order_by(Ticket.created_at.desc())
        .limit(limit)
        .all()
    )


def process_ticket(ticket_id: int, session: Session) -> None:
    ticket = session.get(Ticket, ticket_id)
    if ticket is None:
        LOGGER.warning("Ticket %s not found", ticket_id)
        return

    ticket.status = "processing"
    session.commit()

    body = get_raw_ticket_body(ticket_id)
    if not body:
        ticket.status = "failed"
        session.commit()
        LOGGER.error("Ticket %s has no raw body in MongoDB", ticket_id)
        return

    result = triage_ticket(ticket.subject, body)
    store_llm_output(ticket_id, result.as_dict())

    prediction = ticket.prediction or Prediction(ticket_id=ticket.id)
    prediction.category = result.category
    prediction.priority = result.priority
    prediction.sentiment = result.sentiment
    prediction.confidence = result.confidence
    prediction.assigned_team = result.assigned_team
    prediction.summary = result.summary
    prediction.recommended_action = result.recommended_action
    prediction.model_name = result.model_name

    ticket.prediction = prediction
    ticket.status = "triaged"
    session.add(prediction)
    session.commit()
    LOGGER.info("Ticket %s triaged as %s/%s", ticket_id, result.category, result.priority)
