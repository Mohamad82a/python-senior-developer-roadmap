import asyncio
import aiohttp


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def main():
    html = await fetch("https://httpbin.org/get")
    print(html[:100], '...')


asyncio.run(main())



