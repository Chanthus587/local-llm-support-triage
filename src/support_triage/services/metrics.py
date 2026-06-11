from sqlalchemy import func
from sqlalchemy.orm import Session

from support_triage.db.models import Prediction, Ticket
from support_triage.schemas.metrics import MetricsSummary


def get_metrics_summary(session: Session) -> MetricsSummary:
    status_counts = dict(session.query(Ticket.status, func.count(Ticket.id)).group_by(Ticket.status).all())
    category_counts: dict[str, int] = {}
    priority_counts: dict[str, int] = {}

    rows = (
        session.query(Prediction.category, Prediction.priority, func.count(Prediction.id))
        .group_by(Prediction.category, Prediction.priority)
        .all()
    )
    for category, priority, count in rows:
        category_counts[category] = category_counts.get(category, 0) + count
        priority_counts[priority] = priority_counts.get(priority, 0) + count

    return MetricsSummary(
        tickets_by_status=status_counts,
        predictions_by_category=category_counts,
        predictions_by_priority=priority_counts,
    )
