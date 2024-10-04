
from psycopg2 import pool
import threading

# Настройки базы данных
DB_HOST = '37.193.252.134'
DB_NAME = 'NSUTS'
DB_USER = 'postgres'
DB_PASSWORD = 'strongPassword123'

#TODO  будет прикольно добавить динамические пулы
connection_pool = pool.SimpleConnectionPool(
    1, 
    20, 
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Блокировка для доступа к базе данных. Мы же в потоке лол
db_lock = threading.Lock()

def get_task_for_testing():
    with db_lock:
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM QUEUE WHERE verdict_first = 'NULL' LIMIT 1;")
            task = cursor.fetchone()
            return task
        except Exception as e:
            print(f"Ошибка при подключении к базе данных: {e}")
        finally:
            cursor.close()
            connection_pool.putconn(connection)
            
def check_queue_and_retest():
    with db_lock:
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM QUEUE WHERE verdict_first = 'TimeLimit' AND verdict_second = 'NULL';")
            tasks_to_retest = cursor.fetchall()
            return tasks_to_retest
        except Exception as e:
            print(f"Ошибка при подключении к базе данных: {e}")
        finally:
            cursor.close()
            connection_pool.putconn(connection)

# TODO добавить данные о пользователе и решенной задаче(сейчас заглушки)
def insert_solution_verdict(sol_id, verdict):
    with db_lock:
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Solutions (Sol_ID, user_id, task_id, sol_path, verdict_final) VALUES (%s, %s, %s, %s, %s);", (sol_id, 1, 1, "", verdict))
            connection.commit()
            print(f"Создана запись для решения Sol_ID {sol_id} с вердиктом: {verdict}")
        except Exception as e:
            print(f"Ошибка при вставке вердикта: {e}")
        finally:
            cursor.close()
            connection_pool.putconn(connection)
            
# TODO Добавить blob
def insert_task_for_testing(sol_id, verdict_first, verdict_second):
    with db_lock:
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO QUEUE (sol_id, verdict_first, verdict_second) VALUES (%s, %s, %s);", (sol_id, verdict_first, verdict_second))
            connection.commit()
            print(f"Создана запись для теста Sol_ID {sol_id}")
        except Exception as e:
            print(f"Ошибка при вставке в очередь: {e}")
        finally:
            cursor.close()
            connection_pool.putconn(connection)


def update_queue(verdict_num, verdict, sol_id):
    with db_lock:
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE QUEUE SET {verdict_num} = %s WHERE sol_id = %s;", (verdict, sol_id))
            connection.commit()
            print(f"Задача sol_id {sol_id} обновлена.")
        except Exception as e:
            print(f"Ошибка при обновлении таблицы QUEUE: {e}")
        finally:
            cursor.close()
            connection_pool.putconn(connection)
            
def delete_task_from_queue(sol_id):
    with db_lock:
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM QUEUE WHERE sol_id = %s", (sol_id,))
            connection.commit()
            print(f"Задача с sol_id {sol_id} успешно удалена из очереди.")
        except Exception as e:
            print(f"Ошибка при удалении задачи: {e}")
        finally:
            cursor.close()
            connection_pool.putconn(connection)
