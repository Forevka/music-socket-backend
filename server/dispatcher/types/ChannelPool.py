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

    def add_channel(self, name = None):
        new_channel = Channel(len(self.channel_dict), name = name)
        self.channel_dict[len(self.channel_dict)] = new_channel
        return new_channel

    def channel_list(self):
        for i in self.channel_dict.values():
            logger.info(i)

    @staticmethod
    def get_instance():
        if ChannelPool.instance == None:
            return ChannelPool()
        return ChannelPool.instance
