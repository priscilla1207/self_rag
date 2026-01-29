from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.chunk import Chunk
from backend.app.models.metric import Metric
from backend.app.models.query import Query


class MetricsService:
    @staticmethod
    async def record_metric(
        session: AsyncSession,
        name: str,
        value: float,
        window: str = "global",
    ) -> Metric:
        metric = Metric(name=name, value=value, window=window)
        session.add(metric)
        return metric

    @staticmethod
    async def latest_metric(
        session: AsyncSession,
        name: str,
        window: str = "global",
    ) -> Optional[Metric]:
        stmt = (
            select(Metric)
            .where(Metric.name == name, Metric.window == window, Metric.is_deleted.is_(False))
            .order_by(Metric.created_at.desc())
            .limit(1)
        )
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def update_after_cycle(session: AsyncSession, quality_threshold: float) -> None:
        weak_chunks_stmt = select(Chunk).where(
            Chunk.quality_score.is_not(None),
            Chunk.quality_score < quality_threshold,
            Chunk.is_deleted.is_(False),
        )
        weak_result = await session.execute(weak_chunks_stmt)
        weak_count = len(list(weak_result.scalars().all()))
        await MetricsService.record_metric(session, "weak_chunk_count", float(weak_count))
        failed_queries_stmt = select(Query).where(
            Query.success.is_(False),
            Query.is_deleted.is_(False),
        )
        failed_result = await session.execute(failed_queries_stmt)
        failed_count = len(list(failed_result.scalars().all()))
        await MetricsService.record_metric(session, "failed_query_count", float(failed_count))

