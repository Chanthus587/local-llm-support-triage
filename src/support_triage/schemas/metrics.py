from pydantic import BaseModel


class MetricsSummary(BaseModel):
    tickets_by_status: dict[str, int]
    predictions_by_category: dict[str, int]
    predictions_by_priority: dict[str, int]
