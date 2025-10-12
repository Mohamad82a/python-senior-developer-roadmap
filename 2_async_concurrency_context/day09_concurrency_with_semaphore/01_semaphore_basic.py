import asyncio

sem = asyncio.Semaphore(2)

async def task_worker(n):
    async with sem:
        print(f'Task #{n} started')
        await asyncio.sleep(3)
        print(f'Task #{n} finished')


async def main():
    await asyncio.gather(*(task_worker(i) for i in range(1, 6)))

asyncio.run(main())

