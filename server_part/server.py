import asyncio
import websockets
import serverSQL
import sys
import os
import json


# Питон свихнулся и не видит пакеты, при нормальной работе эти строчки удалить
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server_part.task_generating import tasks_generating

testing_machines = {}

async def handle_client(websocket, path):
    print(f"Подключено к {websocket.remote_address}")
    testing_machines.update(websocket.remote_address, 0)
    
    async def poll_testing():
        try:
            message = await asyncio.wait_for(websocket.recv(), timeout=10)
            data = json.loads(message)
            if "sol_id" in data and "status" in data:
                return data["sol_id"]
            return None
            
        except asyncio.TimeoutError:
            print("Таймаут ожидания статуса")
            if testing_machines.get(websocket.remote_address) == 3:
                
                print(f"Соединение с {websocket.remote_address} закрыто")
                await serverSQL.reset_task_testing_flag(sol_id)
                return
            else:
                testing_machines.update(websocket.remote_address, testing_machines.get(websocket.remote_address) + 1)
        except websockets.ConnectionClosed:
            print(f"Соединение с {websocket.remote_address} закрыто")
            await serverSQL.reset_task_testing_flag(sol_id)
            return
        

    async def poll_status(sol_id):
        while True:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=10)
                data = json.loads(message)
                if "status" in data:
                    status = data["status"]
                    print(f"Получен статус: {status}")
                elif "verdict" in data:
                    verdict = data["verdict"]
                    print(f"Получен вердикт: {verdict}")
                    return verdict
            except asyncio.TimeoutError:
                print("Таймаут ожидания статуса")
                if testing_machines.get(websocket.remote_address) == 3:
                    
                    print(f"Соединение с {websocket.remote_address} закрыто")
                    await serverSQL.reset_task_testing_flag(sol_id)
                    return
                else:
                    testing_machines.update(websocket.remote_address, testing_machines.get(websocket.remote_address) + 1)
            except websockets.ConnectionClosed:
                print(f"Соединение с {websocket.remote_address} закрыто")
                testing_machines.update(websocket.remote_address, 0)
                await serverSQL.reset_task_testing_flag(sol_id)
                return

    async def handle_verdict(verdict, sol_id, retest=False):
        if verdict == "Accepted":
            await serverSQL.insert_solution_verdict(sol_id, verdict)
            await serverSQL.delete_task_from_queue(sol_id)
            print(f"Задача Sol_ID: {sol_id} успешно протестирована. Вердикт: {verdict}")
        elif verdict == "Timeout":
            if retest == False:
                await serverSQL.set_verdict(sol_id)
                print(f"Задача Sol_ID: {sol_id} отправлена на перетестирование. Вердикт: {verdict}")
            else:
                await serverSQL.insert_solution_verdict(sol_id, verdict)
                await serverSQL.delete_task_from_queue(sol_id)
                print(f"Задача Task_ID: {sol_id} не принята. Вердикт: {verdict}")
        else:
            await serverSQL.insert_solution_verdict(sol_id, verdict)
            await serverSQL.delete_task_from_queue(sol_id)
            print(f"Задача Task_ID: {sol_id} не принята. Вердикт: {verdict}")

    try:
        while True:
            # Проверяем задачи на ретест
            
            testing_sol_id = await poll_testing()
            if testing_sol_id:
                verdict = await poll_status(testing_sol_id)
                if verdict:
                    await handle_verdict(verdict, testing_sol_id, True)
                    testing_machines.update(websocket.remote_address, 0)
            else:        
                tasks_to_retest = await serverSQL.get_all_timeout_tasks_for_retesting()

                if tasks_to_retest:
                    for task in tasks_to_retest:
                        sol_id, user_id, competition_id, task_id, blob, is_testing, verdict = task
                        blob_str = blob.decode('utf-8') if isinstance(blob, bytes) else blob
                        data_to_send = {
                            "sol_id": sol_id,
                            "user_id": user_id,
                            "competition_id": competition_id,
                            "task_id": task_id,
                            "blob": blob_str
                        }
                        await websocket.send(json.dumps(data_to_send))

                        # Запускаем параллельные задачи для опроса статуса и обработки вердикта
                        verdict = await poll_status(sol_id)
                        if verdict:
                            await handle_verdict(verdict, sol_id, True)
                            testing_machines.update(websocket.remote_address, 0)

                else:
                    # Если нет задач на ретест, получаем обычную задачу для тестирования
                    task = await serverSQL.get_one_task_for_testing()
                    if task:
                        sol_id, user_id, competition_id, task_id, blob, is_testing, verdict = task
                        blob_str = blob.decode('utf-8') if isinstance(blob, bytes) else blob
                        data_to_send = {
                            "sol_id": sol_id,
                            "user_id": user_id,
                            "competition_id": competition_id,
                            "task_id": task_id,
                            "blob": blob_str
                        }
                        await websocket.send(json.dumps(data_to_send))

                        # Запускаем параллельные задачи для опроса статуса и обработки вердикта
                        verdict = await poll_status(sol_id)
                        if verdict:
                            await handle_verdict(verdict, sol_id)
                            testing_machines.update(websocket.remote_address, 0)
                    else:
                        print('Нет доступных задач для тестирования.')
                        await asyncio.sleep(1)  # Ждем немного перед повторной проверкой

    except websockets.ConnectionClosed:
        print(f"Соединение с {websocket.remote_address} закрыто")
        testing_machines.update(websocket.remote_address, 0)
        # Сбрасываем флаг is_testing для всех задач, которые были в процессе тестирования
        if task:
            sol_id = task[0]
            await serverSQL.reset_task_testing_flag(sol_id)
        for task in tasks_to_retest:
            sol_id = task[0]
            await serverSQL.reset_task_testing_flag(sol_id)

async def start_server():
    await serverSQL.create_pool()
    # Заглушка для создания задач, заменить при первой потребности
    await tasks_generating(300)

    async with websockets.serve(handle_client, '0.0.0.0', 65432):
        print(f"Сервер запущен и слушает на порту 65432...")
        await asyncio.Future()  # Бесконечный цикл для поддержания сервера




if __name__ == "__main__":
    asyncio.run(start_server())
