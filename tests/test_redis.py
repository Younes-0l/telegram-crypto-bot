import asyncio
from database.redis_client import redis_client

async def test():
    await redis_client.set("test_key", "hello", ex=10)
    value = await redis_client.get("test_key")
    print(f"Redis says: {value}")

asyncio.run(test())