import asyncio

async def say_hello():
    """Print Hello after 1 second asynchronously and together with an async coroutine."""
    await asyncio.sleep(5)
    print("Hello Mohamad!")

async def main():
    await asyncio.gather(say_hello(), say_hello())


asyncio.run(main())

