import asyncio
import aiohttp
import time
import functools
import os


# --- Context Manager ---
class Timer:
    """Context manager to measure total runtime"""
    def __enter__(self):
        self.start = time.time()
        print('Download started ....')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        print(f'All downloads finished in {self.end - self.start:.2f}s')


# --- Async Decorator ---
def logger(func):
    """Async decorator to log start and end of downloads"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        url = args[1]
        print(f"➡️ Starting download: {url}")
        result = await func(*args, **kwargs)
        print(f"✅ Finished download: {url}")
        return result
    return wrapper



# --- Downloader Class ---
class DownloadManager:
    """Async multi-file downloader"""
    def __init__(self, save_dir='downloads', limit=3):
        self.save_dir = save_dir
        self.sem = asyncio.Semaphore(limit)
        os.makedirs(save_dir, exist_ok=True)

    @logger
    async def download(self, url):
        """Download a file asynchronously"""
        async with self.sem:
            filename = os.path.join(self.save_dir, url.split('/')[-1] or 'index.html')
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.read()
                    with open(filename, 'wb') as file:
                        file.write(data)
                    print(f"📁 Saved: {filename}")



# --- Main Runner ---
async def main():
    urls =[
        "https://httpbin.org/image/png",
        "https://httpbin.org/image/jpeg",
        "https://httpbin.org/image/svg",
        "https://httpbin.org/image/webp",
    ]
    downloader = DownloadManager(limit=2)
    tasks = [downloader.download(url) for url in urls]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    with Timer():
        asyncio.run(main())