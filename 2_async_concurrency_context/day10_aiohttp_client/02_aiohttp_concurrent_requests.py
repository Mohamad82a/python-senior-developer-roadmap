import asyncio
import aiohttp

urls = ["https://httpbin.org/delay/1", "https://httpbin.org/delay/2"]

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    for i, r in enumerate(results):
        print(f'URL #{i} length:', len(r))


asyncio.run(main())