from fastapi import APIRouter

from support_triage.api.routes import health, metrics, tickets


api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
