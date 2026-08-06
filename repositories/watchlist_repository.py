from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from database.models import Watchlist
from database.database import get_session


class WatchlistRepository:

    async def add(self, user_id: int, symbol: str, vs_currency: str = "IRT") -> bool:
        with get_session() as session:
            entry = Watchlist(user_id=user_id, symbol=symbol.upper(), vs_currency=vs_currency.upper())
            session.add(entry)
            try:
                session.commit()
                return True
            except IntegrityError:
                session.rollback()
                return False

    async def remove(self, user_id: int, symbol: str, vs_currency: str = "IRT") -> None:
        with get_session() as session:
            stmt = delete(Watchlist).where(
                Watchlist.user_id == user_id,
                Watchlist.symbol == symbol.upper(),
                Watchlist.vs_currency == vs_currency.upper(),
            )
            session.execute(stmt)
            session.commit()

    async def get_all(self, user_id: int) -> list[Watchlist]:
        with get_session() as session:
            stmt = select(Watchlist).where(Watchlist.user_id == user_id)
            result = session.execute(stmt)
            return result.scalars().all()