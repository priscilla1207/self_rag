from typing import Optional

from sqlalchemy import Float, ForeignKey, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, IntPKMixin, MetadataMixin, SoftDeleteMixin, TimestampMixin


class SyntheticQA(Base, IntPKMixin, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = "synthetic_qa"

    question: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str] = mapped_column(String, nullable=False)
    topic: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    qa_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    embedding: Mapped[Optional[list[float]]] = mapped_column(JSON, nullable=True)
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    source_query_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("queries.id", ondelete="SET NULL"), nullable=True
    )

    source_query: Mapped[Optional["Query"]] = relationship("Query")


from backend.app.models.query import Query  # noqa: E402
