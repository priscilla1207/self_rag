from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.schemas import QueryRead, QueryRequest
from backend.app.db.session import get_session
from backend.app.embeddings.providers import get_embedding_client
from backend.app.services import QueryService


router = APIRouter()


@router.post("", response_model=QueryRead)
async def ask_query(
    payload: QueryRequest,
    session: AsyncSession = Depends(get_session),
) -> QueryRead:
    embedder = get_embedding_client()
    query = await QueryService.ask_question(
        session=session,
        embedder=embedder,
        question=payload.question,
        metadata=payload.metadata,
    )
    await session.commit()
    return QueryRead.model_validate(query)

