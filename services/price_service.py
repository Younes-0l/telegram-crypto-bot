from tabdeal.spot import Spot
import json


class PriceService:
    def __init__(self):
        self.client = Spot()

    async def get_price(self, symbol: str, vs_currency: str = "IRT") -> float | None:
        symbol_info = await self.client.exchange_info(symbol=f"{symbol}_{vs_currency}")
        if price is not None:
            price = symbol_info.get("minPrice") + symbol_info.get("maxPrice") / 2
            context = {
                "price": price,
            }
            return context
        else:
            return