import socket
# TODO Заглушка тайм. Потом будут реальные тесты
import time

variation = 1

HOST : str
if variation == 1:
    HOST = '37.193.252.134'
elif variation == 2:
    HOST = '127.0.0.1'
PORT = 65432

def connect():
    while True:
        time.sleep(0.3)
        client_socket = socket.socket()
        client_socket.connect((HOST, PORT))

        # TODO Определить реальные лимити входных данных
        data = client_socket.recv(2**20)
        if data:
            # TODO В будущем тут будут тесты
            time.sleep(2)
            data = bytes(data)
            length = len(data) % 3
            if length == 0:
                client_socket.send(b'Accepted')
            elif length == 1:
                client_socket.send(b'Timeout')
            elif length == 2:
                client_socket.send(b'Wrong Answear')
            client_socket.close()

            print(data)

if __name__ == "__main__":
    connect()


