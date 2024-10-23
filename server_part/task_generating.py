import serverSQL
import asyncio
import sys
import os

from drop import server_prepare

async def tasks_generating(num_of_tests):
    # server_prepare необходим для очищения всех очередей, когда сильно забьем таблицу. Использовать когда
    # возникают серьезные изменения или если слишком много мусора.
    await server_prepare()

    last_id = await serverSQL.get_last_id()
    tasks = []

    for sol_id in range(last_id + 1, last_id + num_of_tests + 1):
        new_line = b'l' + b'o'*(sol_id%3) + b'l'
        task = asyncio.create_task(serverSQL.insert_task_for_testing(sol_id, 1, 1, 1, new_line))
        tasks.append(task)

    await asyncio.gather(*tasks)
