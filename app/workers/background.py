import asyncio
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.app.core.config import Settings, WorkerSettings, get_settings
from backend.app.db.session import AsyncSessionLocal
from backend.app.embeddings.interfaces import EmbeddingClient
from backend.app.embeddings.providers import get_embedding_client
from backend.app.models.autonomous_action import AutonomousAction
from backend.app.services.learning_service import LearningService
from backend.app.services.metrics_service import MetricsService


class BackgroundWorker:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] | None = None,
        settings: Settings | None = None,
        embedder: EmbeddingClient | None = None,
    ) -> None:
        self.session_factory = session_factory or AsyncSessionLocal
        self.settings = settings or get_settings()
        self.worker_settings: WorkerSettings = self.settings.worker
        self.embedder = embedder or get_embedding_client()
        self.learning_service = LearningService(settings=self.worker_settings)

    async def run_once(self) -> None:
        async with self.session_factory() as session:
            try:
                await self._run_cycle(session)
            except Exception as exc:
                if session.in_transaction():
                    await session.rollback()
                async with session.begin():
                    await MetricsService.record_metric(session, "worker_failure", 1.0)
                raise exc

    async def _run_cycle(self, session: AsyncSession) -> None:
        async with session.begin():
            cycle = await self.learning_service.start_cycle(session)
            await self.learning_service.plan_actions(
                session, quality_threshold=self.worker_settings.quality_threshold
            )
            stmt = select(AutonomousAction).where(
                AutonomousAction.status == "pending",
                AutonomousAction.is_deleted.is_(False),
            )
            result = await session.execute(stmt)
            actions = list(result.scalars().all())
            for action in actions[: self.worker_settings.max_batch_size]:
                action.status = "running"
                await self.learning_service.execute_action(session, action, self.embedder)
            await self.learning_service.complete_cycle(session, cycle, status="completed")

    async def run_forever(self) -> None:
        try:
            while True:
                await self.run_once()
                await asyncio.sleep(self.worker_settings.poll_interval_seconds)
        except asyncio.CancelledError:
            raise
