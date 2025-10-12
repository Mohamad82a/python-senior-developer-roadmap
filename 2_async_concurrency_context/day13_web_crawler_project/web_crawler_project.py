import asyncio
import aiohttp
from bs4 import BeautifulSoup

urls = ["https://httpbin.org/html", "https://example.com", "https://httpbin.org/get"]
sem = asyncio.Semaphore(3)

async def fetch(url):
    async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")
                title = soup.title.string if soup.title else 'No title'
                print(f'{url} -> {title}')
                return text

async def main():
    tasks = [fetch(url) for url in urls]
    await asyncio.gather(*tasks)

asyncio.run(main())


