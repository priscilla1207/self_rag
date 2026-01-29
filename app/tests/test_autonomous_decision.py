import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import AutonomousAction
from backend.app.services.learning_service import LearningService


@pytest.mark.asyncio
async def test_autonomous_plans_basic_actions(db_session: AsyncSession) -> None:
    service = LearningService()
    actions = await service.plan_actions(db_session, quality_threshold=0.5)
    await db_session.commit()
    assert len(actions) == 2
    stored = await db_session.execute(select(AutonomousAction))
    rows = list(stored.scalars().all())
    assert sorted(a.action_type for a in rows) == [
        "generate_synthetic_qa",
        "reprocess_weak_chunks",
    ]


@pytest.mark.asyncio
async def test_autonomous_avoids_duplicate_actions(db_session: AsyncSession) -> None:
    existing = AutonomousAction(action_type="reprocess_weak_chunks", status="pending")
    db_session.add(existing)
    await db_session.commit()
    service = LearningService()
    actions = await service.plan_actions(db_session, quality_threshold=0.5)
    await db_session.commit()
    assert len(actions) == 1
    assert actions[0].action_type == "generate_synthetic_qa"

