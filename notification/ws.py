import asyncio
import websockets

people = {}


async def welcome(websocket: websockets.WebSocketServerProtocol) -> str:
    await websocket.send('Представьтесь!')
    name = await websocket.recv()  # websocket.recv ожидает получения сообщения
    await websocket.send('Чтобы поговорить, напишите "<имя>:<сообщение>". Например: Ира: купи хлеб.')
    await websocket.send('Посмотреть список участников можно командой "?"')
    people[name.strip()] = websocket
    return name


async def receiver(websocket: websockets.WebSocketServerProtocol, path: str) -> None:
    name = await welcome(websocket)
    while True:
        message = (await websocket.recv()).strip()
        if message == '?':
            await websocket.send(', '.join(people.keys()))
            continue
        else:
            to, text = message.split(': ', 1)
            if to in people:
                await people[to].send(f'Сообщение от {name}:{text}')
            else:
                await websocket.send(f'Пользователь {to} не найден')

ws_server = websockets.serve(receiver, "localhost", 8765)

loop = asyncio.get_event_loop()
loop.run_until_complete(ws_server)
loop.run_forever()
