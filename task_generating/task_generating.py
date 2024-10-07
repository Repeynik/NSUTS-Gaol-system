import server_part.serverSQL as serverSQL
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task_generating.drop import server_prepare

def tasks_generating(num_of_tests):
    threads = []
    server_prepare()
    
    for sol_id in range(1, num_of_tests + 1):
        thread = threading.Thread(target=serverSQL.insert_task_for_testing, args=(sol_id, 1, 1, 1, b'dead\nbeef'))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
        
        
if __name__ == "__main__":
    tasks_generating()