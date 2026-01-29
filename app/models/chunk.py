from typing import Optional

from sqlalchemy import Float, ForeignKey, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, IntPKMixin, MetadataMixin, SoftDeleteMixin, TimestampMixin


class Chunk(Base, IntPKMixin, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = "chunks"

    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(String, nullable=False)
    embedding: Mapped[Optional[list[float]]] = mapped_column(JSON, nullable=True)
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)

    document: Mapped["Document"] = relationship("Document", back_populates="chunks")


from backend.app.models.document import Document  # noqa: E402
