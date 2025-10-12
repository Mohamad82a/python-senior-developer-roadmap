import asyncio


async def compute_square(n):
    await asyncio.sleep(2)
    return n * n

async def main():
    results = await asyncio.gather(*(compute_square(i) for i in range(5)))
    print(results)
    print(len(results))

asyncio.run(main())