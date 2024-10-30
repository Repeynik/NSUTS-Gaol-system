import asyncio
import websockets
import json
import random

VARIATION = 2
RECONNECT_TIMEOUT = 15  # Тайм-аут в секундах для ожидания переподключения

# URL сервера
# Алены
if VARIATION == 1:
    server_url = 'ws://37.193.252.134:65432'
# Максима (локальный)
if VARIATION == 2:
    server_url = 'ws://127.0.0.1:65432'
    # Максима (прокси) -> Алены
if VARIATION == 3:
    server_url = 'ws://90.189.151.132:1030'

# Хранит задачи, которые находятся в процессе тестирования
pending_tasks = {}


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
    pending_tasks[sol_id] = {"task": task, "client": websocket}
    try:
        # Тестируем задачу
        sol_id, verdict = await test_task(task)

        # Удаляем задачу из pending_tasks после завершения
        pending_tasks.pop(sol_id, None)

        # Отправляем вердикт
        await send_verdict(websocket, sol_id, verdict)
        print(f"Отправлен вердикт для Sol_ID: {sol_id}, Вердикт: {verdict}")

    except websockets.ConnectionClosed:
        print(f"Клиент отключился во время тестирования задачи Sol_ID: {sol_id}")
        await wait_for_reconnect(sol_id)


# ожидание переподключения клиента, который был отключен во время тестирования задачи
async def wait_for_reconnect(sol_id):
    task_info = pending_tasks.get(sol_id)
    if task_info is None:
        return

    try:
        await asyncio.wait_for(task_info["reconnect_event"].wait(), timeout=RECONNECT_TIMEOUT)
        print(f"Клиент переподключился и продолжает задачу Sol_ID: {sol_id}")
    except asyncio.TimeoutError:
        print(f"Клиент не переподключился в разумное время, задача Sol_ID: {sol_id} освобождена для других")
        pending_tasks.pop(sol_id, None)


async def client():
    retry_delay = 1
    max_retries = 3

    for attempt in range(max_retries):
        try:
            async with websockets.connect(server_url) as websocket:
                print(f"Подсоединено к серверу {server_url}")
                await resend_pending_tasks(websocket)
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


# повторная отправка статусов задач клиенту, который переподключился
async def resend_pending_tasks(websocket):
    # Повторно отправляем клиенту его задачи на тестирование, если он переподключился
    client_tasks = {sol_id: info for sol_id, info in pending_tasks.items() if info["client"] == websocket}
    for sol_id, info in client_tasks.items():
        await send_status(websocket, sol_id, "Testing")


if __name__ == "__main__":
    asyncio.run(client())
