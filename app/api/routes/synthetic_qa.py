from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.schemas import LearningRunResponse, SyntheticQARead
from backend.app.core.config import get_settings
from backend.app.db.session import get_session
from backend.app.embeddings.providers import get_embedding_client
from backend.app.models.synthetic_qa import SyntheticQA
from backend.app.services.synthetic_qa_service import SyntheticQAService


router = APIRouter()


@router.post("/run", response_model=LearningRunResponse)
async def generate_synthetic_qa(session: AsyncSession = Depends(get_session)) -> LearningRunResponse:
    settings = get_settings().worker
    embedder = get_embedding_client()
    async with session.begin():
        await SyntheticQAService.generate_for_failed_queries(
            session=session,
            embedder=embedder,
            quality_threshold=settings.quality_threshold,
        )
    return LearningRunResponse(status="completed")


@router.get("", response_model=List[SyntheticQARead])
async def list_synthetic_qa(session: AsyncSession = Depends(get_session)) -> list[SyntheticQARead]:
    result = await session.execute(SyntheticQA.__table__.select())
    rows = result.fetchall()
    items: list[SyntheticQARead] = []
    for row in rows:
        qa = SyntheticQA(
            id=row.id,
            question=row.question,
            answer=row.answer,
            topic=row.topic,
            qa_type=row.qa_type,
            embedding=row.embedding,
            quality_score=row.quality_score,
            source_query_id=row.source_query_id,
        )
        items.append(SyntheticQARead.model_validate(qa))
    return items

