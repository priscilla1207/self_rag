from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.schemas import LearningRunResponse
from backend.app.core.config import get_settings
from backend.app.db.session import get_session
from backend.app.embeddings.providers import get_embedding_client
from backend.app.services.learning_service import LearningService


router = APIRouter()


@router.post("", response_model=LearningRunResponse)
async def run_learning_cycle(session: AsyncSession = Depends(get_session)) -> LearningRunResponse:
    settings = get_settings().worker
    service = LearningService(settings=settings)
    embedder = get_embedding_client()
    async with session.begin():
        cycle = await service.start_cycle(session)
        await service.plan_actions(session, quality_threshold=settings.quality_threshold)
        await service.complete_cycle(session, cycle, status="completed")
    return LearningRunResponse(status="completed")

