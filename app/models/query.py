from typing import Optional

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base, IntPKMixin, MetadataMixin, SoftDeleteMixin, TimestampMixin


class Query(Base, IntPKMixin, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = "queries"

    question: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    success: Mapped[bool] = mapped_column(default=True, nullable=False)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    entropy: Mapped[float | None] = mapped_column(Float, nullable=True)
    failure_mode: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

