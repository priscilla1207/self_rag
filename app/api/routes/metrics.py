from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.schemas import MetricRead
from backend.app.db.session import get_session
from backend.app.models.metric import Metric


router = APIRouter()


@router.get("", response_model=List[MetricRead])
async def list_metrics(session: AsyncSession = Depends(get_session)) -> list[MetricRead]:
    stmt = select(Metric).where(Metric.is_deleted.is_(False))
    result = await session.execute(stmt)
    metrics = list(result.scalars().all())
    return [MetricRead.model_validate(m) for m in metrics]

