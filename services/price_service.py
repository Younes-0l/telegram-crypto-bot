from tabdeal.spot import Spot
from handlers.settings import TABDEAL_API_KEY, TABDEAL_SECURITY_KEY


class PriceService:
    def __init__(self):
        self.client = Spot(TABDEAL_API_KEY, TABDEAL_SECURITY_KEY)

    def get_price(self, symbol: str, vs_currency: str = "IRT") -> float | None:
        symbol_info = self.client.trades(symbol=f"{symbol}_{vs_currency}", limit=1)[0]
        if symbol_info is not None:
            price = symbol_info.get("price")
            context = {
                "price": price,
            }
            return context
        
        else:
            return