import asyncio
import datetime
import random
import json
import websockets
import time
from uuid import uuid4
from typing import Any, List, Dict
from loguru import logger

from dispatcher import Dispatcher
from dispatcher.filters.builtin import EventTypeFilter
from dispatcher.types import WebsocketEvent
from dispatcher.types import Channel, ChannelPool, User, UserPool

class Websocket:
    def __init__(self):
        self.ch_pool = ChannelPool()
        self.user_pool = UserPool()

    @property
    def dispatcher(self) -> Dispatcher:
        return Dispatcher.get_current()

    async def register(self, websocket):
        user = UserPool.get_instance().add_user(websocket)
        logger.info(f"new user {user}")
        #await websocket.send(json.dumps(
        #                        {"event": "Logged",
        #                            "timestamp": time.time(),
        #                            "body": user.to_dict()
        #                        })
        #                    )
        return user


    async def unregister(self, websocket):
        UserPool.get_instance().delete_user(websocket)
        print("left user "+str(websocket))


    async def process_update(self, websocket, path):
        user = await self.register(websocket)
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
                    request_object = self.dispatcher.parse_request(data)
                    WebsocketEvent.set_current(request_object)
                except TypeError as e:
                    logger.exception(f"Failed to parse input message: {data} with error: {e}")
                else:
                    #notify all handlers
                    logger.debug(f"Received {request_object}")
                    try:
                        await self.dispatcher.feed_request(request_object)
                    except Exception as e:
                        logger.exception(f"Cause exception while process {request_object}: {e}")
        except Exception as e:
            logger.info(f"user disconected with {e}")
        finally:
            await self.unregister(websocket)

    async def start_server(self, path, port):
        await websockets.serve(self.process_update, path, port)
