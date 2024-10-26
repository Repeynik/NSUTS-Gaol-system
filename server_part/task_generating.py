import random
import serverSQL
import asyncio

from drop import server_prepare

async def generate_random_string(sol_id):
  letters = b'abcdefghijklmnopqrstuvwxyz'
  random_letters = bytes(random.choices(letters, k=2))
  return random_letters + b'o'*(sol_id%3) + random_letters

async def tasks_generating(num_of_tests):
    # server_prepare необходим для очищения всех очередей, когда сильно забьем таблицу. Использовать когда
    # возникают серьезные изменения или если слишком много мусора.
    await server_prepare()

    last_id = await serverSQL.get_last_id()
    tasks = []

    for sol_id in range(last_id + 1, last_id + num_of_tests + 1):
        new_line = await generate_random_string(sol_id)
        task = asyncio.create_task(serverSQL.insert_task_for_testing(sol_id, 1, 1, 1, new_line))
        tasks.append(task)

    await asyncio.gather(*tasks)
