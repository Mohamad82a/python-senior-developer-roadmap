import asyncio
import random

sem = asyncio.Semaphore(2)

async def download_file(name):
    async with sem:
        print(f'Start downloading {name}')
        await asyncio.sleep(random.uniform(5,10))
        print(f'Finish downloading {name}')
        return f'{name} done'

async def main():
    result = await asyncio.gather(*(download_file(f'File #{i}') for i in range(1, 10)))
    print('All downloads:', result)

asyncio.run(main())

