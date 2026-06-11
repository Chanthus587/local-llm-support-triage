from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from support_triage.db.sql import get_session
from support_triage.schemas.metrics import MetricsSummary
from support_triage.services.metrics import get_metrics_summary


router = APIRouter()


@router.get("/summary", response_model=MetricsSummary)
def metrics_summary(session: Session = Depends(get_session)) -> MetricsSummary:
    return get_metrics_summary(session)
