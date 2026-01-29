from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import WorkerSettings, get_settings
from backend.app.embeddings.interfaces import EmbeddingClient
from backend.app.models.autonomous_action import AutonomousAction
from backend.app.models.learning_cycle import LearningCycle
from backend.app.services.metrics_service import MetricsService
from backend.app.services.reprocess_service import ReprocessService
from backend.app.services.synthetic_qa_service import SyntheticQAService


class LearningService:
    def __init__(self, settings: WorkerSettings | None = None) -> None:
        self.settings = settings or get_settings().worker

    async def start_cycle(self, session: AsyncSession) -> LearningCycle:
        cycle = LearningCycle(status="running")
        session.add(cycle)
        await session.flush()
        return cycle

    async def complete_cycle(self, session: AsyncSession, cycle: LearningCycle, status: str) -> None:
        cycle.status = status
        await MetricsService.update_after_cycle(session, self.settings.quality_threshold)

    async def plan_actions(self, session: AsyncSession, quality_threshold: float) -> list[AutonomousAction]:
        actions: List[AutonomousAction] = []
        weak_stmt = select(AutonomousAction).where(
            AutonomousAction.action_type == "reprocess_weak_chunks",
            AutonomousAction.status.in_(["pending", "running"]),
            AutonomousAction.is_deleted.is_(False),
        )
        weak_existing = await session.execute(weak_stmt)
        if weak_existing.scalars().first() is None:
            action = AutonomousAction(action_type="reprocess_weak_chunks", status="pending")
            session.add(action)
            actions.append(action)
        qa_stmt = select(AutonomousAction).where(
            AutonomousAction.action_type == "generate_synthetic_qa",
            AutonomousAction.status.in_(["pending", "running"]),
            AutonomousAction.is_deleted.is_(False),
        )
        qa_existing = await session.execute(qa_stmt)
        if qa_existing.scalars().first() is None:
            action = AutonomousAction(action_type="generate_synthetic_qa", status="pending")
            session.add(action)
            actions.append(action)
        return actions

    async def execute_action(
        self,
        session: AsyncSession,
        action: AutonomousAction,
        embedder: EmbeddingClient,
    ) -> None:
        if action.action_type == "reprocess_weak_chunks":
            await ReprocessService.reprocess_weak_chunks(
                session,
                embedder=embedder,
                quality_threshold=self.settings.quality_threshold,
            )
            action.status = "completed"
        elif action.action_type == "generate_synthetic_qa":
            await SyntheticQAService.generate_for_failed_queries(
                session,
                embedder=embedder,
                quality_threshold=self.settings.quality_threshold,
            )
            action.status = "completed"
        else:
            action.status = "failed"
            action.error_message = f"Unknown action_type {action.action_type}"

