import serverSQL
import threading
import sys
import os

from drop import server_prepare

def tasks_generating(num_of_tests):
    threads = []
    
    # server_prepare необходим для очищения всех очередей, когда сильно забьем таблицу. Использовать когда 
    # возникают серьезные изменения или если слишком много мусора.
    server_prepare()
    
    last_id = serverSQL.get_last_id()
    for sol_id in range(last_id + 1,  last_id + num_of_tests + 1):
        new_line = b'l' + b'o'*(sol_id%3) + b'l'
        thread = threading.Thread(target=serverSQL.insert_task_for_testing, args=(sol_id, 1, 1, 1, new_line))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
        
        
if __name__ == "__main__":
    tasks_generating()