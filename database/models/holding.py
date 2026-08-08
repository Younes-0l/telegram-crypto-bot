from sqlalchemy.sql import func
from ..database import Base
from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Holding(Base):
    __tablename__ = "holdings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False,
    )

    symbol: Mapped[str] = mapped_column(String(10), nullable=False)

    vs_currency: Mapped[str] = mapped_column(String(10), nullable=False, default="IRT")

    amount: Mapped[float] = mapped_column(Float, nullable=False)

    avg_buy_price: Mapped[float] = mapped_column(Float, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "symbol", "vs_currency", name="uq_user_holding"),
    )