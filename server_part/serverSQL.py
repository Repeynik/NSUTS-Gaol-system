
from psycopg2 import pool
import threading

# вариация для быстрого переключения между серверами
variant = 2

# Настройки базы данных Алёны
DB_HOST_1 = '37.193.252.134'
DB_NAME_1 = 'NSUTS'
DB_USER_1 = 'postgres'
DB_PASSWORD_1 = 'strongPassword123'
# Моя
DB_HOST_2 = '127.0.0.1'
DB_NAME_2 = 'NSUTS'
DB_USER_2 = 'postgres'
DB_PASSWORD_2 = '123'

#TODO  будет прикольно добавить динамические пулы
connection_pool : pool.SimpleConnectionPool
if variant == 1:
    connection_pool = pool.SimpleConnectionPool(
        1, 
        20, 
        host=DB_HOST_1,
        database=DB_NAME_1,
        user=DB_USER_1,
        password=DB_PASSWORD_1
    )
elif variant == 2:
    connection_pool = pool.SimpleConnectionPool(
        1, 
        20, 
        host=DB_HOST_2,
        database=DB_NAME_2,
        user=DB_USER_2,
        password=DB_PASSWORD_2
    )

# Блокировка для доступа к базе данных. Мы же в потоке лол
db_lock = threading.Lock()

def get_one_task_for_testing():
    with db_lock:
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM QUEUE WHERE is_timeout IS NULL LIMIT 1;")
            task = cursor.fetchone()
            return task
        except Exception as e:
            print(f"Ошибка при подключении к базе данных: {e}")
        finally:
            cursor.close()
            connection_pool.putconn(connection)
       
def get_all_timeout_tasks_for_retesting():
    with db_lock:
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM QUEUE WHERE is_timeout = True ;")
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
            cursor.execute("INSERT INTO Solutions (sol_id, user_id, competition_id, task_id, sol_blob, verdict) VALUES (%s, %s, %s, %s, %s, %s);", (sol_id, 1, 1, 1, b"dead\nbeef", verdict))
            connection.commit()
            print(f"Создана запись для решения Sol_ID {sol_id} с вердиктом: {verdict}")
        except Exception as e:
            print(f"Ошибка при вставке вердикта: {e}")
        finally:
            cursor.close()
            connection_pool.putconn(connection)
            
def insert_task_for_testing(sol_id, user_id, competition_id, task_id, sol_blob):
    with db_lock:
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO QUEUE (sol_id, user_id, competition_id, task_id, sol_blob, is_timeout) VALUES (%s, %s, %s, %s, %s, NULL);", (sol_id, user_id, competition_id, task_id, sol_blob))
            connection.commit()
            print(f"Создана запись для теста Sol_ID {sol_id}")
        except Exception as e:
            print(f"Ошибка при вставке в очередь: {e}")
        finally:
            cursor.close()
            connection_pool.putconn(connection)


def set_timeout(sol_id):
    with db_lock:
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE QUEUE SET is_timeout = True WHERE sol_id = %s;", (sol_id, ))
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
            cursor.execute("DELETE FROM QUEUE WHERE sol_id = %s;", (sol_id,))
            connection.commit()
            print(f"Задача с sol_id {sol_id} успешно удалена из очереди.")
        except Exception as e:
            print(f"Ошибка при удалении задачи: {e}")
        finally:
            cursor.close()
            connection_pool.putconn(connection)

def delete_all_queue():
    with db_lock:
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM QUEUE;")
            connection.commit()
            print(f"Очередь очищена.")
        except Exception as e:
            print(f"Ошибка при удалении очереди: {e}")
        finally:
            cursor.close()
            connection_pool.putconn(connection)

def delete_all_solutions():
    with db_lock:
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM SOLUTIONS;")
            connection.commit()
            print(f"Таблица решений очищена.")
        except Exception as e:
            print(f"Ошибка при удалении таблицы решений: {e}")
        finally:
            cursor.close()
            connection_pool.putconn(connection)