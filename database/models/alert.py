from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint, Float, Boolean
from sqlalchemy.sql import func
from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class PriceAlert(Base):
    __tablename__ = "price alerts"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False,
    )

    symbol: Mapped[str] = mapped_column(String(10), nullable=False)

    vs_currency: Mapped[str] = mapped_column(String(10), nullable=False, default="IRT")

    target_price: Mapped[float] = mapped_column(Float, nullable=False)

    direction: Mapped[str] = mapped_column(String(10), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    triggered_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)