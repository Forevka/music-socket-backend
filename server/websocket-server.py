import asyncio
import datetime
import random
import json
import websockets
from uuid import uuid4
from typing import Any, List, Dict

class User:
    id: int
    on_channel_id: int
    socket: Any

    def __init__(self, id, socket, on_channel_id = 0):
        self.id = id
        self.socket = socket
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

    def __str__(self):
        return f"User ID {self.id} on channel {self.on_channel_id}"
    

class Channel:
    id: int
    name: str
    users: List[User]
    current_song_time: int
    song_id: int

    def __init__(self, id, name = None, song_id = None):
        self.id = id
        self.song_id = song_id if song_id is not None else random.randint(1, 100)
        self.current_song_time = 0
        self.name = name if name is not None else uuid4()
        self.users = []
    
    def add_user_id(self, user_id):
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

class UserPool:
    instance: 'UserPool' = None
    user_dict: Dict[Any, User]

    def __init__(self):
        UserPool.instance = self
        self.user_dict = {}
    
    @staticmethod
    def get_instance():
        if UserPool.instance == None:
            return UserPool()
        return UserPool.instance
    
    def add_user(self, user_websocket):
        new_user = User(len(self.user_dict), user_websocket)
        self.user_dict[user_websocket] = new_user
        return new_user
    
    def get_user_by_socket(self, sock):
        return self.user_dict.get(sock)
    
    def delete_user(self, user_websocket):
        """
            calling when user leave from server
        """
        del self.user_dict[user_websocket]



class ChannelPool:
    instance: 'ChannelPool' = None
    channel_dict: Dict[int, Channel]

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
        print([f"CH ID {i.id} NAME {i.name}" for i in self.channel_dict.values()])

    @staticmethod
    def get_instance():
        if ChannelPool.instance == None:
            return ChannelPool()
        return ChannelPool.instance

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


#song_file = open("songs\\1.zip", "rb").read()
#song_current_time = 0

async def register(websocket):
    user = UserPool.get_instance().add_user(websocket)
    print(f"new user {user}")
    return user


async def unregister(websocket):
    UserPool.get_instance().delete_user(websocket)
    print("left user "+str(websocket))


async def process(websocket, path):
    user = await register(websocket)
    try:
        async for message in websocket:
            request = await websocket.recv()
            print(request)
            #user_info = user.get_info()
            #await websocket.send(user_info)
            #print(user_info)
            #print(f"Sended to user {user}")
            #await user_info.send_to_user()
    except websockets.exceptions.ConnectionClosedError:
        print("user disconected")
    finally:
        await unregister(websocket)


ch_pool = ChannelPool()
ch_pool.add_channel(name = 'Default Channel')
ch_pool.channel_list()

start_server = websockets.serve(process, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
