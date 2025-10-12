import asyncio
import random


sem = asyncio.Semaphore(2)

async def fetch_data(n):
    async with sem:
        delay = random.uniform(0.5, 3)
        print(f'Fetching data #{n} ...')
        await asyncio.sleep(delay)
        print(f'Fetched data #{n} in {delay:.2f}s')

async def main():
    tasks = [fetch_data(i) for i in range(1, 11)]
    await asyncio.gather(*tasks)

asyncio.run(main())