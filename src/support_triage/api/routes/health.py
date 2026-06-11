from fastapi import APIRouter

from support_triage.core.config import settings
from support_triage.schemas.health import HealthRead


router = APIRouter()


@router.get("/health", response_model=HealthRead)
def health() -> HealthRead:
    return HealthRead(status="ok", app=settings.app_name)
