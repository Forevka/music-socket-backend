from typing import Any, List, Dict
from loguru import logger
from uuid import uuid4
import random

from ..utils import ContextInstanceMixin

class Channel(ContextInstanceMixin):
    id: int
    name: str
    users: List['User']
    current_song_time: int
    song_id: int

    def __init__(self, id, name = None, song_id = None):
        self.id = id
        self.song_id = song_id if song_id is not None else random.randint(1, 100)
        self.current_song_time = 0
        self.name = name if name is not None else uuid4()
        self.users = []


    async def to_all_users(self, body):
        for user in self.users:
            await user.answer(body = body)

    async def to_all_users_custom(self, event, body):
        for user in self.users:
            await user.custom_answer(event, body = body)

    def user_list_except(self, except_id):
        return [user.to_dict() for user in self.users if user.id != except_id]

    def add_user_id(self, user_id):
        from . import ChannelPool

        user = ChannelPool.get_instance().get(user_id) #noqa
        if user:
            user.move_to_channel(self.id)

    def register_user(self, user):
        """
            here need to register user on this channel
            when they join channel
        """
        self.users.append(user)

    def unregister_user(self, user):
        """
            uregister user when they leave from this channel
            or when they leave from server
        """
        if user in self.users:
            self.users.remove(user)

    def to_dict(self):
        return {"id": self.id,
                    "name": self.name,
                    "song": self.song_id,
                    "song_time": self.current_song_time,
                    "user_count": len(self.users),
                }

    def __str__(self):
        return f"Channel: Name {self.name} ID {self.id}"
