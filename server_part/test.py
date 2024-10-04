import threading
from serverSQL import get_task_for_testing, check_queue_and_retest, insert_solution_verdict, update_queue, delete_task_from_queue, insert_task_for_testing

def test_insert_task_for_testing(sol_id, verdict, verdict2):
    insert_task_for_testing(sol_id, verdict, verdict2)

def test_get_task_for_testing():
    task = get_task_for_testing()
    print(f"Полученная задача: {task}")

def test_check_queue_and_retest():
    tasks_to_retest = check_queue_and_retest()
    print(f"Задачи для повторного тестирования: {tasks_to_retest}")

def test_insert_solution_verdict(sol_id, verdict):
    insert_solution_verdict(sol_id, verdict)

def test_update_queue(verdict_num, verdict, sol_id):
    update_queue(verdict_num, verdict, sol_id)

def test_delete_task_from_queue(sol_id):
    delete_task_from_queue(sol_id)

threads = []

threads.append(threading.Thread(target=test_insert_task_for_testing, args=(1, 'TimeLimit', 'NULL')))
threads.append(threading.Thread(target=test_get_task_for_testing))
threads.append(threading.Thread(target=test_check_queue_and_retest))
threads.append(threading.Thread(target=test_insert_solution_verdict, args=(6, 'Accepted')))
threads.append(threading.Thread(target=test_update_queue, args=('verdict_second', 'Accepted', 1)))
threads.append(threading.Thread(target=test_delete_task_from_queue, args=(1,)))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
