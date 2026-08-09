from tabdeal.spot import Spot
from handlers.settings import TABDEAL_API_KEY, TABDEAL_SECURITY_KEY
import asyncio
import json
import logging


logger = logging.getLogger(__name__)
class PriceService:
    CACHE_TTL_SECONDS = 20
    MAX_RETRIES = 2
    RETRY_DELAY = 1.5

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
            logger.error(f"Redis GET timed out (outer guard)")
        except Exception as e:
            logger.error(f"Redis read error: {e}")
        return None

    async def _set_cache(self, key: str, value: dict):
        try:
            await asyncio.wait_for(
                self.redis.set(key, json.dumps(value), ex=self.CACHE_TTL_SECONDS),
                timeout=1.5
            )
        except asyncio.TimeoutError:
            logger.error(f"Redis SET timed out (outer guard)")
        except Exception as e:
            logger.error(f"Redis write error: {e}")

    async def _fetch_from_api(self, symbol: str, vs_currency: str) -> dict | None:
        tabdeal_symbol = f"{symbol.upper()}{vs_currency.upper()}"

        def _make_request():
            client = Spot(TABDEAL_API_KEY, TABDEAL_SECURITY_KEY)
            return client.trades(symbol=tabdeal_symbol, limit=1)

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                trades = await asyncio.to_thread(_make_request)
                if not trades:
                    return None
                return {"price": float(trades[0]["price"])}
            except Exception as e:
                logger.error(f"Attempt {attempt}/{self.MAX_RETRIES} failed for {tabdeal_symbol}: {e}")
                if attempt < self.MAX_RETRIES:
                    await asyncio.sleep(self.RETRY_DELAY)
                else:
                    return None