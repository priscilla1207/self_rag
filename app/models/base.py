from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, JSON, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class MetadataMixin:
    metadata_json: Mapped[dict | None] = mapped_column(JSON, default=None)


class IntPKMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

