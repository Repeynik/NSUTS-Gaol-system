import threading
from server_part.serverSQL import delete_all_queue, delete_all_solutions

def server_prepare():
    threads = []

    threads.append(threading.Thread(target=delete_all_solutions))
    threads.append(threading.Thread(target=delete_all_queue))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
        