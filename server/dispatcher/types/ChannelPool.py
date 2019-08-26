from typing import Any, List, Dict
from loguru import logger
from . import Channel

class ChannelPool:
    instance: 'ChannelPool' = None
    channel_dict: Dict[int, 'Channel']

    def __init__(self):
        ChannelPool.instance = self
        self.channel_dict = {}


    def channel_id(self, id):
        return self.channel_dict.get(id)


    def add_channel(self, id, name = None):
        logger.debug(f'new channel {id}')
        ch = self.channel_dict.get(id)
        if ch is None:
            ch = Channel(id, name)
            self.channel_dict[id] = ch

        return ch


    def channel_list(self):
        for i in self.channel_dict.values():
            logger.info(i)


    def to_dict(self):
        return [i.to_dict() for i in self.channel_dict.values()]


    @staticmethod
    def get_instance():
        if ChannelPool.instance == None:
            return ChannelPool()
        return ChannelPool.instance
