from typing import Optional

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, IntPKMixin, MetadataMixin, SoftDeleteMixin, TimestampMixin


class Document(Base, IntPKMixin, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = "documents"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    chunks: Mapped[list["Chunk"]] = relationship(
        "Chunk", back_populates="document", cascade="all, delete-orphan"
    )


from backend.app.models.chunk import Chunk  # noqa: E402

