from tabdeal.spot import Spot
from handlers.settings import TABDEAL_API_KEY, TABDEAL_SECURITY_KEY
import asyncio
import json


class PriceService:
    CACHE_TTL_SECONDS = 20

    def __init__(self, redis_client):
        self.client = Spot(TABDEAL_API_KEY, TABDEAL_SECURITY_KEY)
        self.redis = redis_client

    def _cache_key(self, symbol: str, vs_currency: str) -> str:
        return f"price:{symbol.upper()}{vs_currency.upper()}"

    async def get_price(self, symbol: str, vs_currency: str = "IRT") -> dict | None:
        cache_key = self._cache_key(symbol, vs_currency)

        cached = await self._get_from_cache(cache_key)
        if cached is not None:
            return cached

        result = await self._fetch_from_api(symbol, vs_currency)

        if result is not None:
            await self._set_cache(cache_key, result)

        return result

    async def _get_from_cache(self, key: str) -> dict | None:
        try:
            cached_value = await asyncio.wait_for(self.redis.get(key), timeout=1.5)
            if cached_value:
                return json.loads(cached_value)
        except asyncio.TimeoutError:
            print(f"Redis GET timed out (outer guard)")
        except Exception as e:
            print(f"Redis read error: {e}")
        return None

    async def _set_cache(self, key: str, value: dict):
        try:
            await asyncio.wait_for(
                self.redis.set(key, json.dumps(value), ex=self.CACHE_TTL_SECONDS),
                timeout=1.5
            )
        except asyncio.TimeoutError:
            print(f"Redis SET timed out (outer guard)")
        except Exception as e:
            print(f"Redis write error: {e}")

    async def _fetch_from_api(self, symbol: str, vs_currency: str) -> dict | None:
        tabdeal_symbol = f"{symbol.upper()}{vs_currency.upper()}"
        try:
            trades = await asyncio.to_thread(
                self.client.trades, symbol=tabdeal_symbol, limit=1
            )
        except Exception as e:
            print(f"Error fetching price for {tabdeal_symbol}: {e}")
            return None

        if not trades:
            return None

        return {"price": float(trades[0]["price"])}