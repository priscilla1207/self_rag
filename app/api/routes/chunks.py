from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.schemas import ChunkRead
from backend.app.db.session import get_session
from backend.app.models.chunk import Chunk


router = APIRouter()


@router.get("", response_model=List[ChunkRead])
async def list_chunks(session: AsyncSession = Depends(get_session)) -> list[ChunkRead]:
    stmt = select(Chunk).where(Chunk.is_deleted.is_(False))
    result = await session.execute(stmt)
    chunks = list(result.scalars().all())
    return [ChunkRead.model_validate(c) for c in chunks]

