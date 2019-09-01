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
from DBdriver import MongoDBWorker

s = Websocket()
dp = Dispatcher(s)
Dispatcher.set_current(dp)
mongo = MongoDBWorker('localhost', 27017)

@dp.login_handler()
async def echo(event: WebsocketEvent, data):
    logger.info('login')
    s.ch_pool.add_channel(int(event.body['channelId']))
    user = User.get_current()
    user.avatar = event.body['avatar']
    user.status = event.body['status']

    res = user.move_to_channel(int(event.body['channelId']))
    channel = user.get_channel()

    await user.custom_answer('UserList', channel.user_list_except(user.id))
    message_history = await mongo.get_message_for_channel(channel.id, page = 1)
    logger.debug(message_history)
    await user.custom_answer('MessageListHistory', message_history)

    await channel.to_all_users(user.to_dict())

@dp.change_status_handler()
async def echo(event: WebsocketEvent, data):
    logger.info('status')
    logger.info(event)
    user = User.get_current()
    channel = user.get_channel()
    user.status = event.body['status']
    await channel.to_all_users(user.to_dict())

@dp.message_list_history()
async def echo(event: WebsocketEvent, data):
    logger.info('message list history')
    logger.info(event)
    user = User.get_current()
    channel = user.get_channel()

    message_history = await mongo.get_message_for_channel(channel.id, page = event.body)
    await asyncio.sleep(4)
    await event.answer(message_history)

@dp.chat_message_handler()
async def echo(event: WebsocketEvent, data):
    logger.info('chat')
    logger.info(event)
    await mongo.insert_message(event.body)
    logger.info(event.body)
    channel = User.get_current().get_channel()
    logger.info(channel)
    await channel.to_all_users(event.body)

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


def run_websocket_server():
    s.ch_pool.add_channel(-1, name = 'Trash')
    s.ch_pool.channel_list()

    asyncio.get_event_loop().run_until_complete(s.start_server("0.0.0.0", 5678))
    asyncio.get_event_loop().run_forever()
