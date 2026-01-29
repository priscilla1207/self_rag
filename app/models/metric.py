from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base, IntPKMixin, MetadataMixin, SoftDeleteMixin, TimestampMixin


class Metric(Base, IntPKMixin, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = "metrics"

    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    window: Mapped[str] = mapped_column(String(50), default="global", nullable=False)

