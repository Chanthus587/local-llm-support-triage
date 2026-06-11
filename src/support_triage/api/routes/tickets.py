from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from support_triage.db.models import Ticket
from support_triage.db.sql import get_session
from support_triage.schemas.tickets import TicketCreate, TicketCreated, TicketRead
from support_triage.services import tickets as ticket_service


router = APIRouter()


@router.post("", response_model=TicketCreated, status_code=202)
def create_ticket(payload: TicketCreate, session: Session = Depends(get_session)) -> TicketCreated:
    ticket = ticket_service.create_ticket(payload, session)
    return TicketCreated(ticket_id=ticket.id, status=ticket.status)


@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: int, session: Session = Depends(get_session)) -> Ticket:
    ticket = ticket_service.get_ticket(ticket_id, session)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.get("", response_model=list[TicketRead])
def list_tickets(session: Session = Depends(get_session)) -> list[Ticket]:
    return ticket_service.list_recent_tickets(session)
