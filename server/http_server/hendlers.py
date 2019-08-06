from loguru import logger
from aiohttp import web
from db_worker import DBWorker
import json
import jwt

class Hendlers:
    def __init__(self):
        self.db = DBWorker()


    def decode(token):
        return jwt.decode(token, 'onal', algorithms=['HS256'])

    async def hendler_add_new_user(self, request):
        data = await request.json()
        logger.info(data['data'])
        res = self.db.add_new_user(data['data']['login'], data['data']['password'])
        if res:
            return res
        return False

    async def hendler_get_user(self, request):
        token = request.headers.get("token")
        logger.info(token)
        d = decode(token)
        logger.info(d)
        res = self.db.get_user(d['login'])
        if res:
            return {'status': 'ok', 'user': res}
        return False

    async def hendler_authentication(self, request):
        data = await request.json()
        logger.info(data['data'])
        res = self.db.authentication(data['data']['login'], data['data']['password'])
        if res:
            return res
        return False
