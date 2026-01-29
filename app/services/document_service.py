from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.chunk import Chunk
from backend.app.models.document import Document


class DocumentService:
    @staticmethod
    def _split_into_chunks(text: str, max_chars: int = 800) -> list[str]:
        parts: list[str] = []
        start = 0
        while start < len(text):
            end = min(len(text), start + max_chars)
            parts.append(text[start:end])
            start = end
        return parts or [text]

    @staticmethod
    async def create_document(
        session: AsyncSession,
        title: str,
        content: str,
        source: Optional[str],
        metadata: Optional[dict[str, Any]],
    ) -> Document:
        document = Document(title=title, content=content, source=source, metadata_json=metadata)
        session.add(document)
        await session.flush()
        for chunk_text in DocumentService._split_into_chunks(content):
            chunk = Chunk(
                document_id=document.id,
                content=chunk_text,
                status="pending",
            )
            session.add(chunk)
        return document

