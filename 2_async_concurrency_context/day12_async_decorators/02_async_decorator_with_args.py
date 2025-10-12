import asyncio
import functools


def async_logger(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        print(f'Started {func.__name__}')
        result = await func(*args, **kwargs)
        print(f'End {func.__name__}')
        return result
    return wrapper

@async_logger
async def fetch_data(n):
    await asyncio.sleep(n)
    print(f'Fetched data in {n}s')


asyncio.run(fetch_data(3))
