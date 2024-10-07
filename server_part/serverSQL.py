
from psycopg2 import pool
import threading

# вариация для быстрого переключения между серверами
variation = 1

DB_HOST : str
DB_NAME : str
DB_USER : str
DB_PASSWORD : str

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

def get_one_task_for_testing():
    with db_lock:
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM QUEUE WHERE is_timeout IS NULL AND is_testing IS False LIMIT 1; ")
            task = cursor.fetchone()
            sol_id = task[0]
            cursor.execute("UPDATE QUEUE SET is_testing = True WHERE sol_id = %s;", (sol_id, ))
            connection.commit()
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
            cursor.execute("SELECT * FROM QUEUE WHERE is_testing IS False AND is_timeout = True ;")
            tasks_to_retest = cursor.fetchall()
            for row in tasks_to_retest:
                sol_id = row[0]
                cursor.execute("UPDATE QUEUE SET is_testing = True WHERE sol_id = %s;", (sol_id, ))
            connection.commit()
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
            cursor.execute("INSERT INTO QUEUE (sol_id, user_id, competition_id, task_id, sol_blob, is_testing, is_timeout) VALUES (%s, %s, %s, %s, %s, False, NULL);", (sol_id, user_id, competition_id, task_id, sol_blob))
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
            cursor.execute("UPDATE QUEUE SET is_testing = False, is_timeout = True WHERE sol_id = %s;", (sol_id, ))
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