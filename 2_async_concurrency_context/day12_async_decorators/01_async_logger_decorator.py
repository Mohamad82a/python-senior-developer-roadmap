import asyncio
import functools


def async_logger(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        print(f'Start {func.__name__}')
        result = await func(*args, **kwargs)
        print(f'End {func.__name__}')
        return result
    return wrapper


@async_logger
async def say_hello():
    await asyncio.sleep(5)
    print('Hello')

asyncio.run(say_hello())



