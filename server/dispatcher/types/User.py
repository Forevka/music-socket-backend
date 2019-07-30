from typing import Any, List, Dict
from loguru import logger
import time
import json

from . import WebsocketEvent
from ..utils import ContextInstanceMixin
from . import ChannelPool

class User(ContextInstanceMixin):
    id: int
    on_channel_id: int
    socket: Any

    def __init__(self, id, websocket, on_channel_id = 0):
        from . import Roles

        self.id = id
        self.websocket = websocket
        self.role = Roles.Guest
        self.move_to_channel(on_channel_id)

    def move_to_channel(self, channel_id):
        old_channel = ChannelPool.get_instance().channel_id(channel_id)
        if old_channel:
            old_channel.unregister_user(self)
        self.on_channel_id = channel_id
        new_channel = ChannelPool.get_instance().channel_id(channel_id)
        new_channel.register_user(self)

    def get_channel(self):
        return ChannelPool.get_instance().channel_id(self.on_channel_id)

    def to_dict(self):
        return {
                "user": self.id,
                "channel": self.on_channel_id,
                "role": self.role.name
        }

    def set_role(self, role):
        self.role = role

    def get_role(self):
        return self.role

    def response_dict(self):
        return {
                    "event": WebsocketEvent.get_current().event,
                    "timestamp": time.time(),
                    "body": {},
                }

    async def answer(self, body = ''):
        response = self.response_dict()
        response.update({"body": body})

        await self.websocket.send(json.dumps(response))

    def __str__(self):
        return str(self.to_dict())
