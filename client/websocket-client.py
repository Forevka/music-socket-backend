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
    GetTime = auto()

def create_request(event, body = '1'):
    return json.dumps({"event": event.name, "body": body, "timestamp": time.time()})

async def hello():
    uri = "ws://localhost:5678"
    async with websockets.connect(uri) as websocket:
        while True:
            print(f"> start")
            await websocket.send(create_request(PossibleEvents.Ping))
            server_sent = await websocket.recv()
            print(f"> Server sent {server_sent}")
            await asyncio.sleep(1)

asyncio.get_event_loop().run_until_complete(hello())
