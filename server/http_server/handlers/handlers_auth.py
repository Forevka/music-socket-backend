from loguru import logger
from aiohttp import web

from DBdriver.db_worker import DBWorker
from ..utils import encode, decode
from ..middlewares import register_with_cors
from functools import wraps


def is_role(role_list):
    def wrap(func):
        @wraps(func)
        async def wrapped(self, request):
            token = request.headers.get('token')
            decoded = decode(token)
            logger.info(decoded['role'])
            if decoded['role'] in role_list:
                return await func(self ,request)
            else:
               return web.Response(status = 403)
        return wrapped
    return wrap



class HandlersAuth:
    def __init__(self):
        self.db = DBWorker()


    async def get_user(self, request):
        """
        tags:
        - User
        summary: Get user
        description: Get user by login.
        operationId: examples.api.api.createUser
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: User login
          required: true
          schema:
            type: object
            properties:
              login:
                type: string
        responses:
          "200":
            description: Successful operation return user object
          "406":
            description: Can`t find this user
        """
        data = await request.json()
        logger.info(data['login'])
        res = self.db.get_user(data['login'])
        logger.info(res)
        if res:
            return web.json_response(res)
        return web.json_response({'message': 'Can`t find this user'}, status=406)


    async def get_me(self, request):
        """
        tags:
        - User
        summary: Get me
        description: Get user object you logged with.
        operationId: examples.api.api.createUser
        produces:
        - application/json
        responses:
          "200":
            description: Successful operation return user object
        """
        token = request.headers.get('token')
        decoded = decode(token)

        return web.json_response(decoded)

    @is_role([2])
    async def ban_user(self, request):
        """
        tags:
        - Ban user
        summary: Ban user
        description: This method baned specific user.
        operationId: examples.api.api.createUser
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: Channel object
          required: true
          schema:
            type: object
            properties:
              name:
                type: string
        responses:
          "200":
            description: Successful operation return user object
        """
        data = await request.json()
        logger.info(data)
        token = request.headers.get('token')
        decoded = decode(token)
        self.db.delete_user(data['name'])
        return web.json_response({'message': "user was baned"}, status=200)


    @staticmethod
    def register(app):
        this_handler = HandlersAuth()
        register_with_cors(app, 'POST', '/ban_user', this_handler.ban_user)
        register_with_cors(app, 'POST', '/get_me', this_handler.get_me)
        register_with_cors(app, 'POST', '/get_user',  this_handler.get_user)
