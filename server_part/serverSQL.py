import asyncpg
import asyncio

# вариация для быстрого переключения между серверами
variation = 1

DB_HOST: str
DB_NAME: str
DB_USER: str
DB_PASSWORD: str

if variation == 1:
    # Настройки базы данных Алёны
    DB_HOST = '37.193.252.134'
    DB_NAME = 'NSUTS'
    DB_USER = 'postgres'
    DB_PASSWORD = 'strongPassword123'
elif variation == 2:
    # Моя
    DB_HOST = '127.0.0.1'
    DB_NAME = 'NSUTS'
    DB_USER = 'postgres'
    DB_PASSWORD = '123'


# Глобальный пул соединений
pool = None

async def create_pool():
    global pool
    pool = await asyncpg.create_pool(
        min_size=1,
        max_size=20,
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# async def validate_token(client_id, token):
#     async with pool.acquire() as conn:
#         try:
#             query = """
#             SELECT COUNT(*)
#             FROM client_tokens
#             WHERE client_id = $1 AND token = $2
#             """
#             result = await conn.fetchval(query, client_id, token)
#             return result > 0
#         except Exception as e:
#             print(f"Ошибка при проверке токена: {e}")
#             return False

async def get_one_task_for_testing():
    async with pool.acquire() as conn:
        try:
            task = await conn.fetchrow("SELECT * FROM QUEUE WHERE verdict IS NULL AND is_testing IS FALSE LIMIT 1;")
            if task:
                sol_id = task[0]
                await conn.execute("UPDATE QUEUE SET is_testing = TRUE WHERE sol_id = $1;", sol_id)
                return task
            return None
        except Exception as e:
            print(f"Ошибка при получении задачи: {e}")

async def get_all_timeout_tasks_for_retesting():
    async with pool.acquire() as conn:
        try:
            tasks_to_retest = await conn.fetch("SELECT * FROM QUEUE WHERE is_testing IS FALSE AND verdict = 'Timeout';")
            for row in tasks_to_retest:
                sol_id = row[0]
                await conn.execute("UPDATE QUEUE SET is_testing = TRUE WHERE sol_id = $1;", sol_id)
            return tasks_to_retest
        except Exception as e:
            print(f"Ошибка при получении задач для повторного тестирования: {e}")

async def insert_solution_verdict(sol_id, verdict):
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                "INSERT INTO Solutions (sol_id, user_id, competition_id, task_id, sol_blob, verdict) VALUES ($1, $2, $3, $4, $5, $6);",
                sol_id, 1, 1, 1, b"dead\nbeef", verdict
            )
            print(f"Создана запись для решения Sol_ID {sol_id} с вердиктом: {verdict}")
        except Exception as e:
            print(f"Ошибка при вставке вердикта: {e}")

async def insert_task_for_testing(sol_id, user_id, competition_id, task_id, sol_blob):
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                "INSERT INTO QUEUE (sol_id, user_id, competition_id, task_id, sol_blob, is_testing, verdict) VALUES ($1, $2, $3, $4, $5, FALSE, NULL);",
                sol_id, user_id, competition_id, task_id, sol_blob
            )
            print(f"Создана запись для теста Sol_ID {sol_id}")
        except Exception as e:
            print(f"Ошибка при вставке в очередь: {e}")

async def delete_task_from_queue(sol_id):
    async with pool.acquire() as conn:
        try:
            await conn.execute("DELETE FROM QUEUE WHERE sol_id = $1;", sol_id)
            print(f"Задача с sol_id {sol_id} успешно удалена из очереди.")
        except Exception as e:
            print(f"Ошибка при удалении задачи: {e}")

async def set_verdict(sol_id):
    async with pool.acquire() as conn:
        try:
            await conn.execute("UPDATE QUEUE SET is_testing = FALSE, verdict = 'Timeout' WHERE sol_id = $1;", sol_id)
            print(f"Задача sol_id {sol_id} обновлена.")
        except Exception as e:
            print(f"Ошибка при обновлении таблицы QUEUE: {e}")

async def reset_task_testing_flag(sol_id):
    async with pool.acquire() as conn:
        try:
            await conn.execute("UPDATE QUEUE SET is_testing = FALSE WHERE sol_id = $1;", sol_id)
            print(f"Задача sol_id {sol_id} сброшена.")
        except Exception as e:
            print(f"Ошибка при обновлении таблицы QUEUE: {e}")

async def get_last_id():
    async with pool.acquire() as conn:
        try:
            sol_id_1 = await conn.fetchval("SELECT max(sol_id) FROM QUEUE;") or 0
            sol_id_2 = await conn.fetchval("SELECT max(sol_id) FROM SOLUTIONS;") or 0
            return max(sol_id_1, sol_id_2)
        except Exception as e:
            print(f"Ошибка при получении последнего ID: {e}")

async def delete_all_queue():
    async with pool.acquire() as conn:
        try:
            await conn.execute("DELETE FROM QUEUE;")
            print(f"Очередь очищена.")
        except Exception as e:
            print(f"Ошибка при удалении очереди: {e}")

async def delete_all_solutions():
    async with pool.acquire() as conn:
        try:
            await conn.execute("DELETE FROM SOLUTIONS;")
            print(f"Таблица решений очищена.")
        except Exception as e:
            print(f"Ошибка при удалении таблицы решений: {e}")

