import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.embeddings.providers import get_embedding_client
from backend.app.models import Query, SyntheticQA
from backend.app.services.synthetic_qa_service import SyntheticQAService


@pytest.mark.asyncio
async def test_synthetic_qa_filters_low_quality(db_session: AsyncSession) -> None:
    low_q = Query(question="q1", answer="a1", success=False, confidence=0.1)
    high_q = Query(question="q2", answer="a2", success=False, confidence=0.9)
    db_session.add_all([low_q, high_q])
    await db_session.commit()
    embedder = get_embedding_client()
    await SyntheticQAService.generate_for_failed_queries(
        session=db_session,
        embedder=embedder,
        quality_threshold=0.5,
    )
    await db_session.commit()
    result = await db_session.execute(select(SyntheticQA))
    qas = list(result.scalars().all())
    assert len(qas) == 1
    assert qas[0].question == "q2"

