from typing import Iterable, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.embeddings.interfaces import EmbeddingClient
from backend.app.models.query import Query
from backend.app.models.synthetic_qa import SyntheticQA


class SyntheticQAService:
    @staticmethod
    async def generate_for_failed_queries(
        session: AsyncSession,
        embedder: EmbeddingClient,
        quality_threshold: float,
    ) -> list[SyntheticQA]:
        stmt = select(Query).where(
            Query.success.is_(False),
            Query.is_deleted.is_(False),
        )
        result = await session.execute(stmt)
        failed_queries: Iterable[Query] = result.scalars().all()
        created: List[SyntheticQA] = []
        for q in failed_queries:
            if not q.question:
                continue
            vector = await embedder.embed_text(q.question)
            quality = q.confidence or 0.5
            if quality < quality_threshold:
                continue
            qa = SyntheticQA(
                question=q.question,
                answer=q.answer or "",
                topic=None,
                qa_type="failed_query",
                embedding=vector,
                quality_score=quality,
                source_query_id=q.id,
            )
            session.add(qa)
            created.append(qa)
        return created

