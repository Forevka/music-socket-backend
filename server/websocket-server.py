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

@dp.login_handler()
async def echo(event: WebsocketEvent, data):
    if event.body['username'] == "admin" and event.body['password'] == "admin":
        event.user().set_username(event.body['username'])
        event.user().set_role(Roles.Admin)
        await event.answer(event.user().to_dict())
        return True
    event.user().set_role(Roles.Guest)
    await event.answer(event.user().to_dict())

@dp.chat_message_handler()
async def echo(event: WebsocketEvent, data):
    print(event)

@dp.ping_handler()
async def echo(event: WebsocketEvent, data):
    await event.answer()
    return True

@dp.get_info_handler()
async def echo(event: WebsocketEvent, data):
    await event.answer(event.user().to_dict())
    return True

@dp.get_channel_handler()
async def echo(event: WebsocketEvent, data):
    await event.answer(ChannelPool.get_instance().to_dict())
    return True

@dp.move_to_channel_handler()
async def echo(event: WebsocketEvent, data):
    res = User.get_current().move_to_channel(int(event.body))
    logger.info(User.get_current().get_channel())
    await event.answer({"moved": res})

@dp.unhandled_event()
async def echo(event: WebsocketEvent, data):
    await event.answer('idk what you whant')
    return True


if __name__ == "__main__":
    s.ch_pool.add_channel(name = 'Default Channel')
    s.ch_pool.add_channel(name = 'Rock Channel')
    s.ch_pool.channel_list()

    asyncio.get_event_loop().run_until_complete(s.start_server("127.0.0.1", 5678))
    asyncio.get_event_loop().run_forever()
