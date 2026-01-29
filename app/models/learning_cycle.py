from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base, IntPKMixin, MetadataMixin, SoftDeleteMixin, TimestampMixin


class LearningCycle(Base, IntPKMixin, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = "learning_cycles"

    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

