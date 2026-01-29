from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.embeddings.interfaces import EmbeddingClient
from backend.app.models.query import Query
from backend.app.services.chunk_service import ChunkService
from backend.app.services.reasoning_service import ReasoningService


class QueryService:
    @staticmethod
    async def ask_question(
        session: AsyncSession,
        embedder: EmbeddingClient,
        question: str,
        metadata: Optional[dict[str, Any]] = None,
        top_k: int = 5,
    ) -> Query:
        query = Query(question=question, success=False, metadata_json=metadata)
        session.add(query)
        await session.flush()
        chunks = await ChunkService.top_k_chunks(session, embedder, question, top_k)
        if not chunks:
            query.failure_mode = "no_chunks"
            return query
        contexts = [c.content for c in chunks]
        answer, confidence, entropy = await ReasoningService.answer(question, contexts)
        query.answer = answer
        query.success = True
        query.confidence = confidence
        query.entropy = entropy
        return query

