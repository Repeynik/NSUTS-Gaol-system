import socket
import threading
import serverSQL
import sys
import os
# Питон свихнулся и не видит пакеты, при нормальной работе эти строчки удалить
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

from task_generating.task_generating import tasks_generating

variation = 1

# Настройки сервера
HOST : str
if variation == 1:
    HOST = '0.0.0.0'
elif variation == 2:
    HOST = '127.0.0.1'
PORT = 65432

# TODO Возможно стоит вместо задач на одного клиента смотреть на address ТестМашины и 
# при совпадении с адресом выделенной тестМашины отдавать ей задачи на ретест (сейчас отдаются на любую). 
# Минусы - вообще никакой гибкости, но сделать просто, нужно просто определить любую тест машину.
def handle_client(client_socket, address):
    print(f"Подключено к {address}")
    
    # Сначала проверяем задачи на ретест. Логика такая - тк задачи на ретест будут крутиться на одной машине, 
    # возьмем сразу весь список задач на ретест.
    # Тогда один клиент будет занят только ретестом.
    # Проблема - я хз насолько это правильно, тк мы все время тестирования будем подрублены к клиенту + есть гипотетическая ситуация 
    # когда мы можем занять несколько ТестМашин такими списками.
    tasks_to_retest = serverSQL.get_all_timeout_tasks_for_retesting()

    if tasks_to_retest:
        
        for task in tasks_to_retest:
            #TODO Возможно blob находится на другом месте, исправить если что
            sol_id, user_id, competition_id, task_id, blob, is_testing, is_timeout = task
            print(task)
            # Отправляем blob клиенту
            # TODO sendall не является безопасной функцией те мы не знаем, сколько пакетов отправили в случае ошибки. Но она позволяет
            # отсылать сколько угодно данных, что сильно полезно при отправке большого количества текста. Стоит подумать над заменой 
            # и в целом добавить обработчик ошибок сюда
            client_socket.sendall(bytes(blob))
            
            verdict = client_socket.recv(1024).decode('utf-8')  #Ждем и получаем вердикт
            serverSQL.insert_solution_verdict(sol_id, verdict) # Нам не важно, какой будет вердикт - он уже будет окончательный
            serverSQL.delete_task_from_queue(sol_id)
            if verdict == "Accepted":
                print(f"Задача Sol_ID: {sol_id} успешно перетестирована. Вердикт: {verdict}")
            else:
                print(f"Задача Sol_ID: {sol_id} не принята. Вердикт: {verdict}")
    
    else:
        # Если нет задач на ретест, получаем обычную задачу для тестирования
        task = serverSQL.get_one_task_for_testing()
        print(task)
        if task:
            #TODO Возможно blob находится на другом месте, исправить если что
            sol_id, user_id, competition_id, task_id, blob, is_testing, is_timeout = task = task
            
            # Отправляем blob клиенту
            # TODO sendall не является безопасной функцией те мы не знаем, сколько пакетов отправили в случае ошибки. Но она позволяет
            # отсылать сколько угодно данных, что сильно полезно при отправке большого количества текста. Стоит подумать над заменой 
            # и в целом добавить обработчик ошибок сюда
            client_socket.sendall(bytes(blob))
            client_socket.shutdown(socket.SHUT_WR)  # Закрываем отправку
            
            verdict = client_socket.recv(1024).decode('utf-8')  #Ждем и получаем вердикт
            if verdict == "Accepted":
                serverSQL.insert_solution_verdict(sol_id, verdict)
                serverSQL.delete_task_from_queue(sol_id)
                print(f"Задача Sol_ID: {sol_id} успешно протестирована. Вердикт: {verdict}")
            elif verdict == "Timeout":
                # Обновляем таблицу QUEUE для повторного тестирования
                serverSQL.set_timeout(sol_id)
                print(f"Задача Sol_ID: {sol_id} отправлена на перетестирование. Вердикт: {verdict}")
            else:
                # Не отправляем задачу на повторное тестирование, просто игнорируем
                serverSQL.insert_solution_verdict(sol_id, verdict)
                serverSQL.delete_task_from_queue(sol_id)
                print(f"Задача Task_ID: {sol_id} не принята. Вердикт: {verdict}")
        else:
            print('Нет доступных задач для тестирования.')

    # Закрываем соединение с клиентом
    # TODO Я так и не поняла, нужно ли закрывать соединение с клиентом во время тестирования, вынесла пока здесь. Возможно стоит это изменить.
    # Есть закрытие отправки на клиента выше
    client_socket.close()

def start_server():
    # TODO Заглушка для создания задач, заменить при первой потребности
    tasks_generating(10)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        #М TODO Если сокет занят, то setsockopt переиспользует его
        # Нужно при случае если убить сокет не закрыв его
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Сервер запущен и слушает на порту {PORT}...")

        while True:
            client_socket, address = server_socket.accept()
            # Делаем потоки для каждого соединения
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()

if __name__ == "__main__":
    start_server()
