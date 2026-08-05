from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Watchlist(Base):
    __tablename__ = "watchlist"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False,
    )

    symbol: Mapped[str] = mapped_column(String(10), nullable=False)

    vs_currency: Mapped[str] = mapped_column(String(10), nullable=False, default="IRT")
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint("user_id", "symbol", "vs_currency", name="uq_user_symbol_currency"),
    )