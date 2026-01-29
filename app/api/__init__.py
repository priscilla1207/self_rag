from fastapi import APIRouter, FastAPI

from backend.app.api.routes import (
    autonomous,
    chunks,
    documents,
    knowledge,
    learning,
    metrics,
    queries,
    reprocess,
    synthetic_qa,
    auto_reprocess,
)
from backend.app.core.config import get_settings


def init_api(app: FastAPI) -> None:
    settings = get_settings()
    api_router = APIRouter(prefix=settings.api_prefix)
    api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
    api_router.include_router(queries.router, prefix="/queries", tags=["queries"])
    api_router.include_router(learning.router, prefix="/learning", tags=["learning"])
    api_router.include_router(reprocess.router, prefix="/reprocess", tags=["reprocess"])
    api_router.include_router(
        auto_reprocess.router,
        prefix="/auto-reprocess",
        tags=["reprocess"],
    )
    api_router.include_router(synthetic_qa.router, prefix="/synthetic-qa", tags=["synthetic_qa"])
    api_router.include_router(autonomous.router, prefix="/autonomous", tags=["autonomous"])
    api_router.include_router(chunks.router, prefix="/chunks", tags=["chunks"])
    api_router.include_router(knowledge.router, prefix="/knowledge-expansion", tags=["knowledge"])
    api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
    app.include_router(api_router)
