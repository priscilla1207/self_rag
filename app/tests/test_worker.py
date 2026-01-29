import asyncio

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.app.models import AutonomousAction, Chunk, Document, Metric, Query
from backend.app.workers.background import BackgroundWorker


@pytest.mark.asyncio
async def test_worker_rollback_on_failure(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async with session_factory() as session:
        doc = Document(title="doc", content="content", source=None)
        session.add(doc)
        await session.flush()
        weak_chunk = Chunk(
            document_id=doc.id,
            content="weak",
            embedding=[0.1, 0.2, 0.3],
            quality_score=0.1,
            status="pending",
            metadata_json={"force_fail": True},
        )
        session.add(weak_chunk)
        await session.commit()
    worker = BackgroundWorker(session_factory=session_factory)
    with pytest.raises(RuntimeError):
        await worker.run_once()
    async with session_factory() as session:
        chunks_result = await session.execute(select(Chunk))
        chunks = list(chunks_result.scalars().all())
        assert len(chunks) == 1
        assert chunks[0].status == "pending"
        metrics_result = await session.execute(
            select(Metric).where(Metric.name == "worker_failure")
        )
        metrics = list(metrics_result.scalars().all())
        assert len(metrics) == 1


@pytest.mark.asyncio
async def test_worker_cancellation_and_rethrows(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    worker = BackgroundWorker(session_factory=session_factory)
    task = asyncio.create_task(worker.run_forever())
    await asyncio.sleep(0.1)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task


@pytest.mark.asyncio
async def test_metrics_updated_after_cycle(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async with session_factory() as session:
        doc = Document(title="doc", content="content", source=None)
        session.add(doc)
        await session.flush()
        weak_chunk = Chunk(
            document_id=doc.id,
            content="weak",
            embedding=[0.1, 0.2, 0.3],
            quality_score=0.1,
            status="pending",
        )
        strong_chunk = Chunk(
            document_id=doc.id,
            content="strong",
            embedding=[0.4, 0.5, 0.6],
            quality_score=0.9,
            status="pending",
        )
        session.add_all([weak_chunk, strong_chunk])
        failed_query = Query(
            question="q",
            answer=None,
            success=False,
            confidence=0.1,
        )
        session.add(failed_query)
        await session.commit()
    worker = BackgroundWorker(session_factory=session_factory)
    await worker.run_once()
    async with session_factory() as session:
        weak_metric_result = await session.execute(
            select(Metric)
            .where(Metric.name == "weak_chunk_count")
            .order_by(Metric.created_at.desc())
        )
        weak_metric = weak_metric_result.scalars().first()
        assert weak_metric is not None
        assert weak_metric.value >= 0.0
        failed_metric_result = await session.execute(
            select(Metric)
            .where(Metric.name == "failed_query_count")
            .order_by(Metric.created_at.desc())
        )
        failed_metric = failed_metric_result.scalars().first()
        assert failed_metric is not None
        assert failed_metric.value == 1.0
