import asyncio
import websockets

async def hello():
    uri = "ws://localhost:5678"
    async with websockets.connect(uri) as websocket:
        while True:
            current_time = await websocket.recv()
            print(f"> Server send time {current_time}")

asyncio.get_event_loop().run_until_complete(hello())
