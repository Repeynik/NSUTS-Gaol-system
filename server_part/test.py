import threading
from serverSQL import get_one_task_for_testing, get_all_timeout_tasks_for_retesting, insert_solution_verdict, set_timeout, delete_task_from_queue, insert_task_for_testing

def test_insert_task_for_testing(sol_id, user_id, competition_id, task_id, sol_blob):
    insert_task_for_testing(sol_id, user_id, competition_id, task_id, sol_blob)

def test_get_one_task_for_testing():
    task = get_one_task_for_testing()
    print(f"Полученная задача: {task}")

def test_get_all_timeout_tasks_for_retesting():
    tasks_to_retest = get_all_timeout_tasks_for_retesting()
    print(f"Задачи для повторного тестирования: {tasks_to_retest}")

def test_insert_solution_verdict(sol_id, verdict):
    insert_solution_verdict(sol_id, verdict)

def test_set_timeout(sol_id):
    set_timeout(sol_id)

def test_delete_task_from_queue(sol_id):
    delete_task_from_queue(sol_id)

threads = []

threads.append(threading.Thread(target=test_insert_task_for_testing, args=(17, 1, 1, 1, b'dead\nbeef')))
threads.append(threading.Thread(target=test_get_one_task_for_testing))
threads.append(threading.Thread(target=test_set_timeout, args=(17, )))
threads.append(threading.Thread(target=test_insert_task_for_testing, args=(42, 1, 1, 1, b'dead\nbeef'))) 
threads.append(threading.Thread(target=test_set_timeout, args=(42, )))
threads.append(threading.Thread(target=test_insert_task_for_testing, args=(101, 1, 1, 1, b'dead\nbeef'))) 
threads.append(threading.Thread(target=test_get_all_timeout_tasks_for_retesting))
threads.append(threading.Thread(target=test_insert_solution_verdict, args=(6, 'Accepted')))
threads.append(threading.Thread(target=test_delete_task_from_queue, args=(1,)))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
