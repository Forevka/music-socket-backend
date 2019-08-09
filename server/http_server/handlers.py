from loguru import logger
from aiohttp import web
from db_worker import DBWorker
import json
import jwt

class Handlers:
    def __init__(self):
        self.db = DBWorker()


    def encryption(self, d):
        encoded = jwt.encode(d, 'onal', algorithm='HS256')
        logger.info(encoded)
        return encoded



    async def hendler_add_new_user(self, request):
        data = await request.json()
        logger.info(data)
        res = self.db.add_new_user(data['login'], data['password'])
        if res:
            response = self.encryption(res)
            token = response.decode("utf-8")
            return web.json_response({'status': "ok", 'token': token})
        return web.StreamResponse(status=401, reason=None)

    async def hendler_get_user(self, d, request):
        data = await request.json()
        logger.info(data['login'])
        res = self.db.get_user(data['login'])
        logger.info(res)
        if res:
            return web.json_response({'status': 'ok', 'user': res})
        return web.StreamResponse(status=401, reason=None)

    async def hendler_authentication(self, request):
        data = await request.json()
        logger.info(data)
        res = self.db.authentication(data['login'], data['password'])
        logger.info(res)
        if res:
            response = self.encryption(res)
            logger.info(res)
            token = response.decode("utf-8")
            return web.json_response({'status': "ok", 'token': token})
        return web.StreamResponse(status=401, reason=None)
