import asyncio
import websockets
import json
import time
from loguru import logger
from enum import Enum, auto

class AutoName(Enum):
     def _generate_next_value_(name, start, count, last_values):
          return name

class PossibleEvents(Enum):
    Ping = auto()
    GetInfo = auto()
    GetChannels = auto()
    GetUnknown = auto()
    Login = auto()
    MoveToChannel = auto()


def create_request(event, body = '1'):
    logger.info({"event": event.name, "body": body, "timestamp": time.time()})
    return json.dumps({"event": event.name, "body": body, "timestamp": time.time()})

async def hello():
    uri = "ws://localhost:5678"
    my_channel = {}
    async with websockets.connect(uri) as websocket:
        await websocket.send(create_request(PossibleEvents.Login, {"username": "admin", "password": "admid"}))
        await websocket.send(create_request(PossibleEvents.GetChannels))
        print(f"> waiting for info from server")
        me = await websocket.recv()
        print(f"> you logged as {me}")
        while True:
            events_list = '\n'.join([f"{n + 1} - {i.name}" for n, i in enumerate(list(PossibleEvents))])
            r = input(f"What to send\n{events_list}\n>")
            if r == 6:
                l = input("Please input channel id")
                await websocket.send(create_request(list(PossibleEvents)[int(r) - 1], int(l)))
            await websocket.send(create_request(list(PossibleEvents)[int(r) - 1]))
            server_sent = await websocket.recv()
            print(f"> Server sent {server_sent}")
            #await asyncio.sleep(1)

asyncio.get_event_loop().run_until_complete(hello())
