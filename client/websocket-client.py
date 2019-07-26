import asyncio
import websockets

async def hello():
    uri = "ws://localhost:5678"
    async with websockets.connect(uri) as websocket:
        while True:
            body = await websocket.recv()
            print(f"> Server send {body}")

asyncio.get_event_loop().run_until_complete(hello())
