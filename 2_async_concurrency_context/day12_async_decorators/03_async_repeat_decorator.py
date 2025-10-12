import asyncio
import functools


def repeat(n):
    """Repeat async function n times"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for _ in range(n):
                await func(*args, **kwargs)
        return wrapper
    return decorator


@repeat(3)
async def main():
    print('Hello mate')

asyncio.run(main())