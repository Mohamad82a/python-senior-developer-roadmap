# Simple connection to Redis async and get/set cache


import os
import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def get_cached_user(user_id: int):
    key = f'user:{user_id}'
    data = await redis_client.get(key)
    return data


async def set_cached_user(user_id: int, value: str, expire: int = 60):
    key = f'user:{user_id}'
    await redis_client.set(key, value, ex=expire)


async def invalidate_user_cache(user_id: int):
    key = f'user:{user_id}'
    await redis_client.delete(key)

