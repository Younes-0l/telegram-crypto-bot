from repositories.holding_repository import HoldingRepository
from services.price_service import PriceService


class PortfolioService:
    def __init__(self, holding_repo: HoldingRepository, price_service: PriceService):
        self.holding_repo = holding_repo
        self.price_service = price_service

    async def set_holding(self, user_id: int, symbol: str, amount: float, avg_buy_price: float):
        await self.holding_repo.upsert(user_id, symbol, "IRT", amount, avg_buy_price)

    async def remove_holding(self, user_id: int, symbol: str):
        await self.holding_repo.delete(symbol, user_id)

    async def get_portfolio_summary(self, user_id: int) -> list[dict]:
        holdings = await self.holding_repo.get_all_for_user(user_id)
        summary = []

        for h in holdings:
            price_data = await self.price_service.get_price(h.symbol, h.vs_currency)
            current_price = price_data["price"] if price_data else None

            entry = {
                "symbol": h.symbol,
                "amount": h.amount,
                "avg_buy_price": h.avg_buy_price,
                "current_price": current_price,
            }

            if current_price is not None:
                current_value = h.amount * current_price
                cost_basis = h.amount * h.avg_buy_price
                entry["current_value"] = current_value
                entry["profit"] = current_value - cost_basis
                entry["profit_percent"] = (entry["profit"] / cost_basis * 100) if cost_basis > 0 else 0

            summary.append(entry)

        return summary