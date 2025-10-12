import asyncio
import aiohttp

urls = [f"https://httpbin.org/delay/{i}" for i in range(1, 6)]

sem = asyncio.Semaphore(2)

async def fetch(url):
    async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(f'Fetched {url}')
                return await response.text()


async def main():
    tasks = [fetch(url) for url in urls]
    await asyncio.gather(*tasks)

asyncio.run(main())