from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.schemas import LearningRunResponse
from backend.app.core.config import get_settings
from backend.app.db.session import get_session
from backend.app.embeddings.providers import get_embedding_client
from backend.app.services.reprocess_service import ReprocessService


router = APIRouter()


@router.post("", response_model=LearningRunResponse)
async def reprocess_weak_chunks(session: AsyncSession = Depends(get_session)) -> LearningRunResponse:
    settings = get_settings().worker
    embedder = get_embedding_client()
    async with session.begin():
        await ReprocessService.reprocess_weak_chunks(
            session=session,
            embedder=embedder,
            quality_threshold=settings.quality_threshold,
        )
    return LearningRunResponse(status="completed")

