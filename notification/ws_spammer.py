import asyncio
import websockets
from asyncio import sleep
from ws import people

URI = "ws://localhost:8765"


async def spammer():
    async with websockets.connect(URI) as websocket:
        while True:
            for human in people:
                await websocket.send("You've been hacked!")
            await sleep(0.1)

loop = asyncio.get_event_loop()
loop.run_until_complete(spammer())
