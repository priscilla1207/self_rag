from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.schemas import LearningRunResponse
from backend.app.db.session import get_session
from backend.app.api.routes.reprocess import reprocess_weak_chunks


router = APIRouter()


@router.post("", response_model=LearningRunResponse)
async def auto_reprocess(session: AsyncSession = Depends(get_session)) -> LearningRunResponse:
    return await reprocess_weak_chunks(session)

