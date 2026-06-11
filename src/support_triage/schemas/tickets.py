from datetime import datetime

from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    customer_id: str = Field(..., examples=["cust-102"])
    subject: str = Field(..., min_length=3, examples=["Cannot access billing dashboard"])
    body: str = Field(..., min_length=5)
    channel: str = Field(default="email", examples=["email"])


class TicketCreated(BaseModel):
    ticket_id: int
    status: str


class PredictionRead(BaseModel):
    category: str
    priority: str
    sentiment: str
    confidence: float
    assigned_team: str
    summary: str
    recommended_action: str
    model_name: str

    model_config = {"from_attributes": True}


class TicketRead(BaseModel):
    id: int
    customer_id: str
    subject: str
    channel: str
    status: str
    created_at: datetime
    updated_at: datetime
    prediction: PredictionRead | None = None

    model_config = {"from_attributes": True}
