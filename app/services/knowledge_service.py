from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.chunk import Chunk
from backend.app.models.query import Query


class KnowledgeService:
    @staticmethod
    async def suggest_new_topics(session: AsyncSession) -> list[str]:
        failed_stmt = select(Query.question).where(
            Query.success.is_(False),
            Query.is_deleted.is_(False),
        )
        failed_result = await session.execute(failed_stmt)
        failed_questions = [q for q in failed_result.scalars().all()]
        chunk_stmt = select(Chunk.content).where(Chunk.is_deleted.is_(False))
        chunk_result = await session.execute(chunk_stmt)
        chunk_contents = [c for c in chunk_result.scalars().all()]
        topics: List[str] = []
        for q in failed_questions:
            if any(q in c for c in chunk_contents):
                continue
            topics.append(q[:80])
        return topics

