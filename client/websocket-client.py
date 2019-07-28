import asyncio
import websockets
import json
import time
from enum import Enum, auto

class AutoName(Enum):
     def _generate_next_value_(name, start, count, last_values):
          return name

class PossibleEvents(Enum):
    Ping = auto()
    GetInfo = auto()
    GetChannels = auto()
    GetUnknown = auto()

def create_request(event, body = '1'):
    return json.dumps({"event": event.name, "body": body, "timestamp": time.time()})

async def hello():
    uri = "ws://localhost:5678"
    my_channel = {}
    async with websockets.connect(uri) as websocket:
        print(f"> waiting for info from server")
        me = await websocket.recv()
        print(f"> you logged as {me}")
        while True:
            events_list = '\n'.join([f"{n + 1} - {i.name}" for n, i in enumerate(list(PossibleEvents))])
            r = input(f"What to send\n{events_list}\n>")
            await websocket.send(create_request(list(PossibleEvents)[int(r) - 1]))
            server_sent = await websocket.recv()
            print(f"> Server sent {server_sent}")
            #await asyncio.sleep(1)

asyncio.get_event_loop().run_until_complete(hello())
