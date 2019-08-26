from loguru import logger
from aiohttp import web

from ..DBdriver.db_worker import DBWorker
from ..utils import encode, decode
from ..middlewares import register_with_cors

class HandlersWithoutAuth:
    def __init__(self):
        self.db = DBWorker()


    async def add_new_user(self, request):
        data = await request.json()
        logger.info(data)
        res = self.db.add_new_user(data['login'], data['password'])
        if res:
            response = encode(res)
            token = response.decode("utf-8")
            return web.json_response({'status': "ok", 'token': token})
        return web.json_response({'message': '???'}, status=406)


    async def login_user(self, request):
        data = await request.json()
        logger.info(data)
        res = self.db.authentication(data['login'], data['password'])
        if res:
            response = encode(res)
            logger.info(res)
            token = response.decode("utf-8")
            res['token'] = token
            return web.json_response(res)
        return web.json_response({'message': 'Login or password incorect'}, status=406)


    async def get_channel(self, request):
        data = await request.json()
        logger.info(data['id'])
        res = self.db.get_channel(data['id'])
        logger.info(res)
        if res:
            return web.json_response(res)
        return web.json_response({'message': 'Cant find this channel'}, status=406)


    async def get_channel_list(self, request):
        """
            {"page": 0}
        """
        data = await request.json()
        res = self.db.get_channel_list(data['page'])
        logger.info(res)
        if res:
            return web.json_response(res)
        return web.json_response({'message': '???'}, status=406)

    async def get_all_channel_list(self, request):
        """
            {}
        """
        data = await request.json()
        res = self.db.get_channel_list(0, 999999)
        logger.info(res)
        if res:
            return web.json_response(res)
        return web.json_response({'message': '???'}, status=406)

    async def get_channels_number(self, request):
        """
            {}
        """
        res = self.db.get_channels_number()
        logger.info(res)
        if res:
            return web.json_response(res)
        return web.json_response({'message': '???'}, status=406)


    @staticmethod
    def register(app):
        this_handler = HandlersWithoutAuth()
        register_with_cors(app, 'POST', '/add_new_user', this_handler.add_new_user)
        register_with_cors(app, 'POST', '/authentication', this_handler.login_user)
        register_with_cors(app, 'POST', '/get_channel', this_handler.get_channel)
        register_with_cors(app, 'POST', '/get_channels_list', this_handler.get_channel_list)
        register_with_cors(app, 'POST', '/get_channels_number', this_handler.get_channels_number)
        register_with_cors(app, 'POST', '/get_all_channel_list', this_handler.get_all_channel_list)
