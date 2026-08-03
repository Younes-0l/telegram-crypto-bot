import httpx


class CoinGeckoClient:
    BASE_URL = "https://api.coingecko.com/api/v3"

    async def get_price(self, coin_id: str, vs_currency: str = "usd") -> float | None:
        async with httpx.Client() as session:
            params = {"ids": coin_id, "vs_currencies": vs_currency}
            async with session.get(f"{self.BASE_URL}/simple/price", params=params) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                return data.get(coin_id, {}).get(vs_currency)