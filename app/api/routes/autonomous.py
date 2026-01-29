from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.schemas import LearningRunResponse
from backend.app.core.config import get_settings
from backend.app.db.session import get_session
from backend.app.embeddings.providers import get_embedding_client
from backend.app.models.autonomous_action import AutonomousAction
from backend.app.services.learning_service import LearningService


router = APIRouter()


@router.post("", response_model=LearningRunResponse)
async def run_autonomous_cycle(session: AsyncSession = Depends(get_session)) -> LearningRunResponse:
    settings = get_settings().worker
    service = LearningService(settings=settings)
    embedder = get_embedding_client()
    async with session.begin():
        cycle = await service.start_cycle(session)
        await service.plan_actions(session, quality_threshold=settings.quality_threshold)
        stmt = select(AutonomousAction).where(
            AutonomousAction.status == "pending",
            AutonomousAction.is_deleted.is_(False),
        )
        result = await session.execute(stmt)
        actions = list(result.scalars().all())
        for action in actions:
            action.status = "running"
            await service.execute_action(session, action, embedder)
        await service.complete_cycle(session, cycle, status="completed")
    return LearningRunResponse(status="completed")


@router.get("", response_model=List[str])
async def list_autonomous_actions(session: AsyncSession = Depends(get_session)) -> list[str]:
    stmt = select(AutonomousAction).where(AutonomousAction.is_deleted.is_(False))
    result = await session.execute(stmt)
    actions = list(result.scalars().all())
    return [f"{a.id}:{a.action_type}:{a.status}" for a in actions]

