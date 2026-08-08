from sqlalchemy import select, update, func, delete
from database.models import PriceAlert
from database.database import get_session
import asyncio


class AlertRepository:

    async def  create(self, user_id: int, symbol: str, vs_currency: str, target_price: float, direction: str):
        def _create():
            with get_session() as session:
                alert = PriceAlert(
                    user_id=user_id, symbol=symbol.upper(), vs_currency=vs_currency.upper(),
                    target_price=target_price, direction=direction
                )
                session.add(alert)
                session.commit()
                return alert.id
        return await asyncio.to_thread(_create)

    async def get_active_for_user(self, user_id: int) -> list[PriceAlert]:
        def _query():
            with get_session() as session:
                stmt = select(PriceAlert).where(
                    PriceAlert.user_id == user_id, PriceAlert.is_active == True
                )
                return session.execute(stmt).scalars().all()
        return await asyncio.to_thread(_query)

    async def get_all_active(self) -> list[PriceAlert]:
        """For Scheduler – All active alerts for all users"""
        def _query():
            with get_session() as session:
                stmt = select(PriceAlert).where(PriceAlert.is_active == True)
                return session.execute(stmt).scalars().all()
        return await asyncio.to_thread(_query)

    async def deactivate(self, alert_id: int):
        def _update():
            with get_session() as session:
                stmt = update(PriceAlert).where(PriceAlert.id == alert_id).values(
                    is_active=False, triggered_at=func.now()
                )
                session.execute(stmt)
                session.commit()
        await asyncio.to_thread(_update)

    async def delete(self, alert_id: int, user_id: int):
        def _delete():
            with get_session() as session:
                stmt = delete(PriceAlert).where(
                    PriceAlert.id == alert_id, PriceAlert.user_id == user_id
                )
                session.execute(stmt)
                session.commit()
        await asyncio.to_thread(_delete)