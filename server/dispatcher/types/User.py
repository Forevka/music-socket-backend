from typing import Any, List, Dict
from loguru import logger
import json

from ..utils import ContextInstanceMixin
from . import ChannelPool

class User(ContextInstanceMixin):
    id: int
    on_channel_id: int
    socket: Any

    def __init__(self, id, websocket, on_channel_id = 0):
        self.id = id
        self.websocket = websocket
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

    def get_info(self):
        my_channel = self.get_channel()
        return ResponsePacket(my_channel.song_id, my_channel.current_song_time,
                                my_channel.id, self.socket)

    def answer(self, body):
        self.websocket.send(json.dumps(body))

    def __str__(self):
        return f"User ID {self.id} on channel {self.on_channel_id}"
