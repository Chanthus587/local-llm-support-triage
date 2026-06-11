from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from support_triage.api import api_router
from support_triage.core.logging import configure_logging
from support_triage.db.sql import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    del app
    configure_logging()
    create_tables()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Local LLM Support Triage", version="0.2.0", lifespan=lifespan)
    app.include_router(api_router)
    return app


app = create_app()
