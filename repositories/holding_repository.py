from sqlalchemy import select, delete
from database.models import Holding
from database.database import get_session
import asyncio


class HoldingRepository:

    async def upsert(self, user_id: int, symbol: str, vs_currency: str,
                      amount: float, avg_buy_price: float):
        def _upsert():
            with get_session() as session:
                stmt = select(Holding).where(
                    Holding.user_id == user_id,
                    Holding.symbol == symbol.upper(),
                    Holding.vs_currency == vs_currency.upper(),
                )
                existing = session.execute(stmt).scalar_one_or_none()

                if existing:
                    existing.amount = amount
                    existing.avg_buy_price = avg_buy_price
                else:
                    holding = Holding(
                        user_id=user_id, symbol=symbol.upper(), vs_currency=vs_currency.upper(),
                        amount=amount, avg_buy_price=avg_buy_price
                    )
                    session.add(holding)

                session.commit()
        await asyncio.to_thread(_upsert)

    async def get_all_for_user(self, user_id: int) -> list[Holding]:
        def _query():
            with get_session() as session:
                stmt = select(Holding).where(Holding.user_id == user_id)
                return session.execute(stmt).scalars().all()
        return await asyncio.to_thread(_query)

    async def delete(self, symbol: str, user_id: int):
        def _delete():
            with get_session() as session:
                stmt = delete(Holding).where(
                    Holding.symbol == symbol.upper(), Holding.user_id == user_id
                )
                session.execute(stmt)
                session.commit()
        await asyncio.to_thread(_delete)