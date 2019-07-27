from typing import Any, List, Dict
from loguru import logger

class UserPool:
    instance: 'UserPool' = None
    user_dict: Dict[Any, 'User']

    def __init__(self):
        UserPool.instance = self
        self.user_dict = {}

    @staticmethod
    def get_instance():
        if UserPool.instance == None:
            return UserPool()
        return UserPool.instance

    def add_user(self, user_websocket):
        from . import User

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
