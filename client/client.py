import asyncio
import websockets
import json
import random


VARIATION = 2
# URL сервера
# Алены
if VARIATION == 1:
    server_url = 'ws://37.193.252.134:65432'
# Максима
if VARIATION == 2:
    server_url = 'ws://127.0.0.1:65432'

async def test_task(task):
    # Симуляция тестирования задачи
    sol_id = task["sol_id"]
    await asyncio.sleep(random.randint(1, 5))  # Симуляция времени тестирования
    verdict = random.choice(["Accepted", "Wrong Answer", "Timeout", "Runtime Error"])
    return sol_id, verdict

async def send_status(websocket, sol_id, status):
    message = json.dumps({"sol_id": sol_id, "status": status})
    await websocket.send(message)

async def send_verdict(websocket, sol_id, verdict):
    message = json.dumps({"sol_id": sol_id, "verdict": verdict})
    await websocket.send(message)

async def handle_task(websocket, task):
    sol_id = task["sol_id"]
    print(f"Принята на обработку задача Sol_ID: {sol_id}")

    # Отправляем статус "Testing"
    await send_status(websocket, sol_id, "Testing")

    # Тестируем задачу
    sol_id, verdict = await test_task(task)

    # Отправляем вердикт
    await send_verdict(websocket, sol_id, verdict)
    print(f"Отправлен вердикт для Sol_ID: {sol_id}, Вердикт: {verdict}")

async def client():
    retry_delay = 1 
    max_retries = 3

    for attempt in range(max_retries):
        try:
            async with websockets.connect(SERVER_URL) as websocket:
                print(f"Подсоединено к серверу {SERVER_URL}")

                while True:
                    try:
                        message = await websocket.recv()
                        task = json.loads(message)
                        await handle_task(websocket, task)
                    except websockets.ConnectionClosed:
                        print("Соединение с сервером закрыто")
                        print("Ожидайте...")
                        break
                    except Exception as e:
                        print(f"Ошибка следующая: {e}")
                        break

            retry_delay = 1
            break
        except websockets.ConnectionClosed:
            print(f"Не удалось подключиться к серверу. Повторная попытка через {retry_delay} секунд...")
            print("Ожидайте...")
            await asyncio.sleep(retry_delay)
            retry_delay *= 2
        except Exception as e:
            print(f"Ошибка: {e}")
            await asyncio.sleep(retry_delay)
            retry_delay *= 2
        print("Сервер не доступен, клиент отключён")

if __name__ == "__main__":
    asyncio.run(client())

