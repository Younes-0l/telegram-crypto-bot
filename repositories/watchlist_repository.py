# repositories/watchlist_repository.py
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from database.models import Watchlist


class WatchlistRepository:
    def __init__(self, session):
        self.session = session

    async def add(self, user_id: int, symbol: str, vs_currency: str = "IRT") -> bool:
        entry = Watchlist(user_id=user_id, symbol=symbol.upper(), vs_currency=vs_currency.upper())
        self.session.add(entry)
        try:
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            return False

    async def remove(self, user_id: int, symbol: str, vs_currency: str = "IRT") -> None:
        stmt = delete(Watchlist).where(
            Watchlist.user_id == user_id,
            Watchlist.symbol == symbol.upper(),
            Watchlist.vs_currency == vs_currency.upper(),
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_all(self, user_id: int) -> list[Watchlist]:
        stmt = select(Watchlist).where(Watchlist.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()