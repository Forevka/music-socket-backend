import asyncio
import datetime
import random
import json
import websockets
import time
from uuid import uuid4
from typing import Any, List, Dict
from loguru import logger

from dispatcher import Dispatcher, Websocket
from dispatcher.filters.builtin import EventTypeFilter
from dispatcher.types import WebsocketEvent
from dispatcher.types import Channel, ChannelPool, User, UserPool, Roles


s = Websocket()
dp = Dispatcher(s)
Dispatcher.set_current(dp)


@dp.event_handler(EventTypeFilter('Login'))
async def echo(event: WebsocketEvent, data):
    if event.body['username'] == "admin" and event.body['password'] == "admin":
        event.user().set_role(Roles.Admin)
        await event.answer({"status": "ok"})
        return True
    event.user().set_role(Roles.Guest)
    await event.answer({"status": "bad"})


@dp.event_handler(EventTypeFilter('Ping'))
async def echo(event: WebsocketEvent, data):
    await event.answer()
    return True

@dp.event_handler(EventTypeFilter('GetInfo'))
async def echo(event: WebsocketEvent, data):
    await event.answer(event.user().to_dict())
    return True

@dp.event_handler(EventTypeFilter('GetChannels'))
async def echo(event: WebsocketEvent, data):
    await event.answer(ChannelPool.get_instance().to_dict())
    return True

@dp.event_handler()
async def echo(event: WebsocketEvent, data):
    await event.answer('idk what you whant')
    return True




if __name__ == "__main__":
    s.ch_pool.add_channel(name = 'Default Channel')
    s.ch_pool.channel_list()

    asyncio.get_event_loop().run_until_complete(s.start_server("127.0.0.1", 5678))
    asyncio.get_event_loop().run_forever()
