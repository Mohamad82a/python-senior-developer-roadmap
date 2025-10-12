import asyncio


async def delayed_print(msg, delay):
    """Prints messages asynchronously with different priority"""
    await asyncio.sleep(delay)
    print(msg)

async def main():
    tasks = [delayed_print('Hey', 1), delayed_print('How are you?', 3)]
    await asyncio.gather(*tasks)

asyncio.run(main())








