from redis import asyncio as aioredis
from api.config import settings


redis = aioredis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)


async def get_bank_from_redis(bin: str):
    bank = await redis.get(f'{bin}')
    if bank is None:
        bank = 'По номеру карты'
    return bank
