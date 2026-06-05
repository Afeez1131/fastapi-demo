import orjson
import redis.asyncio as aioredis

from app.config import settings

redis_client: aioredis.Redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_cached(key: str):
    data = await redis_client.get(key)
    if data:
        return orjson.loads(data)
    return None


async def set_cached(key: str, value, ttl: int = settings.CACHE_TTL):
    await redis_client.set(key, orjson.dumps(value), ex=ttl)


async def invalidate(key: str):
    await redis_client.delete(key)
