#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets

USERS = set()

async def register(websocket):
    USERS.add(websocket)
    print("new user "+str(websocket))


async def unregister(websocket):
    USERS.remove(websocket)
    print("left user "+str(websocket))

async def time(websocket, path):
    await register(websocket)
    try:
        while True:
            now = datetime.datetime.utcnow().isoformat() + "Z"
            sleep_for = 1
            await websocket.send(now)
            print("Sended time to user " + str(websocket) + " and sleep for " + str(sleep_for) + "seconds")
            await asyncio.sleep(sleep_for)
    except websockets.exceptions.ConnectionClosedError:
        print("user disconected")
    finally:
        await unregister(websocket)

start_server = websockets.serve(time, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
