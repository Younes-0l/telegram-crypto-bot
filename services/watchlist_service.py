class WatchlistService:
    def __init__(self, watchlist_repo, price_service):
        self.watchlist_repo = watchlist_repo
        self.price_service = price_service

    async def add_coin(self, user_id: int, symbol: str) -> bool:
        return await self.watchlist_repo.add(user_id, symbol)

    async def remove_coin(self, user_id: int, symbol: str) -> None:
        await self.watchlist_repo.remove(user_id, symbol)

    async def get_watchlist_with_prices(self, user_id: int) -> list[dict]:
        entries = await self.watchlist_repo.get_all(user_id)
        result = []
        for entry in entries:
            price_data = await self.price_service.get_price(entry.symbol, entry.vs_currency)
            result.append({
                "symbol": entry.symbol,
                "vs_currency": entry.vs_currency,
                "price": price_data["price"] if price_data else None,
            })
        return result