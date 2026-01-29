from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.schemas import TopicsResponse
from backend.app.db.session import get_session
from backend.app.services.knowledge_service import KnowledgeService


router = APIRouter()


@router.get("", response_model=TopicsResponse)
async def suggest_topics(session: AsyncSession = Depends(get_session)) -> TopicsResponse:
    topics = await KnowledgeService.suggest_new_topics(session)
    return TopicsResponse(topics=topics)

