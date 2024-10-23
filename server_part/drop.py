import asyncio
from serverSQL import delete_all_queue, delete_all_solutions

async def server_prepare():
    tasks = [
        asyncio.create_task(delete_all_solutions()),
        asyncio.create_task(delete_all_queue())
    ]

    await asyncio.gather(*tasks)

