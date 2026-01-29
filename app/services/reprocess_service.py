from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.embeddings.interfaces import EmbeddingClient
from backend.app.models.chunk import Chunk


class ReprocessService:
    @staticmethod
    async def reprocess_weak_chunks(
        session: AsyncSession,
        embedder: EmbeddingClient,
        quality_threshold: float,
    ) -> list[Chunk]:
        stmt = select(Chunk).where(
            Chunk.quality_score.is_not(None),
            Chunk.quality_score < quality_threshold,
            Chunk.is_deleted.is_(False),
        )
        result = await session.execute(stmt)
        weak_chunks = list(result.scalars().all())
        processed: list[Chunk] = []
        for chunk in weak_chunks:
            if chunk.metadata_json and chunk.metadata_json.get("force_fail"):
                raise RuntimeError("Forced failure for testing rollback")
            vector = await embedder.embed_text(chunk.content)
            chunk.embedding = vector
            chunk.quality_score = max(quality_threshold, chunk.quality_score or 0.0)
            chunk.status = "reprocessed"
            processed.append(chunk)
        return processed

