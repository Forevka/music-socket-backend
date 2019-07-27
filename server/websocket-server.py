import asyncio
import datetime
import random
import json
import websockets
from uuid import uuid4
from typing import Any, List, Dict
from loguru import logger

from dispatcher import Dispatcher
from dispatcher.filters.builtin import EventTypeFilter
from dispatcher.types import WebsocketEvent
from dispatcher.types import Channel, ChannelPool, User, UserPool

class ResponsePacket:
    song_id: int
    current_time_play: int
    channel_id: int

    def __init__(self, song_id, current_time_play, channel_id, user_websocket):
        self.user_websocket = user_websocket
        self.song_id = song_id
        self.current_time_play = current_time_play
        self.channel_id = channel_id

    def __str__(self):
        user = UserPool.get_instance().get_user_by_socket(self.user_websocket)
        return f"Packet from {user}\nSong: {self.song_id} Time: {self.current_time_play} Channel: {self.channel_id}"

    def to_dict(self):
        return {"song_id": self.song_id, "current_time_play": self.current_time_play, "channel_id": self.channel_id}

    async def send_to_user(self):
        await self.user_websocket.send(json.dumps(self.to_dict()))


class Websocket:

    @property
    def dispatcher(self) -> Dispatcher:
        return Dispatcher.get_current()

    async def register(self, websocket):
        user = UserPool.get_instance().add_user(websocket)
        logger.info(f"new user {user}")
        return user


    async def unregister(self, websocket):
        UserPool.get_instance().delete_user(websocket)
        print("left user "+str(websocket))


    async def process_update(self, websocket, path):
        user = await self.register(websocket)
        #websocket.send('13')
        try:
            while True:
                request = await websocket.recv()
                data = {}

                User.set_current(UserPool.get_instance().get_user_by_socket(websocket))
                Channel.set_current(User.get_current().get_channel())

                logger.debug(f"current user {User.get_current()}")
                logger.debug(f"current channel {Channel.get_current()}")

                try:
                    data = json.loads(request)
                except:
                    websocket.send(json.loads({"status": "can`t parse your payload"}))
                    continue

                try:
                    #parse an update
                    request_object = self.dispatcher.parse_request(data)
                    #ViberReqestObject.set_current(request_object)
                except TypeError as e:
                    logger.exception(f"Failed to parse input message: {data} with error: {e}")

                else:
                    #notify all handlers
                    logger.debug(f"Received {request_object}")
                    try:
                        await self.dispatcher.feed_request(request_object)
                    except Exception as e:
                        logger.exception(f"Cause exception while process {request_object}: {e}")
                #user_info = user.get_info()
                #await websocket.send(user_info)
                #print(user_info)
                #print(f"Sended to user {user}")
                #await user_info.send_to_user()
        except Exception as e:
            logger.info(f"user disconected with {e}")
        finally:
            await self.unregister(websocket)

s = Websocket()
dp = Dispatcher(s)
Dispatcher.set_current(dp)

@dp.event_handler(EventTypeFilter('Ping'))
async def echo(event: WebsocketEvent, data):
    logger.info(event)
    logger.info('hello from ping')
    return True

ch_pool = ChannelPool()
ch_pool.add_channel(name = 'Default Channel')
ch_pool.channel_list()

start_server = websockets.serve(s.process_update, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
