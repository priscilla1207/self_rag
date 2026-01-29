from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.schemas import DocumentCreate, DocumentRead
from backend.app.db.session import get_session
from backend.app.services import DocumentService


router = APIRouter()


@router.post(
    "",
    response_model=DocumentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_document(
    payload: DocumentCreate,
    session: AsyncSession = Depends(get_session),
) -> DocumentRead:
    document = await DocumentService.create_document(
        session=session,
        title=payload.title,
        content=payload.content,
        source=payload.source,
        metadata=payload.metadata,
    )
    await session.commit()
    return DocumentRead.model_validate(document)

