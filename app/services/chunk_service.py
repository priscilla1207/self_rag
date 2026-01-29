from collections.abc import Sequence
from typing import Iterable, List

import numpy as np
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.embeddings.interfaces import EmbeddingClient
from backend.app.models.chunk import Chunk


class ChunkService:
    @staticmethod
    async def get_chunks_by_ids(session: AsyncSession, ids: Iterable[int]) -> list[Chunk]:
        stmt = select(Chunk).where(Chunk.id.in_(list(ids)), Chunk.is_deleted.is_(False))
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def top_k_chunks(
        session: AsyncSession,
        embedder: EmbeddingClient,
        question: str,
        k: int,
    ) -> list[Chunk]:
        stmt = select(Chunk).where(
            Chunk.embedding.is_not(None),
            Chunk.is_deleted.is_(False),
        )
        result = await session.execute(stmt)
        chunks: Sequence[Chunk] = list(result.scalars().all())
        if not chunks:
            return []
        q_vec = np.array(await embedder.embed_text(question), dtype=np.float32)
        mat = np.array([c.embedding for c in chunks if c.embedding is not None], dtype=np.float32)
        if mat.size == 0:
            return []
        scores = mat @ q_vec
        indices = np.argsort(-scores)[:k]
        selected: List[Chunk] = []
        for idx in indices:
            selected.append(chunks[int(idx)])
        return selected

