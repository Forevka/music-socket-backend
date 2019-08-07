from loguru import logger
from aiohttp import web
from db_worker import DBWorker
import json
import jwt

class Handlers:
    def __init__(self):
        self.db = DBWorker()


    def encryption(self, login, password, role):
        encoded = jwt.encode({'login': login, 'password': password, 'role': role}, 'onal', algorithm='HS256')
        logger.info(encoded)
        return encoded



    async def hendler_add_new_user(self, request):
        data = await request.json()
        logger.info(data['data'])
        res = self.db.add_new_user(data['data']['login'], data['data']['password'])
        if res:
            response = encryption(data['data']['login'], data['data']['password'], "guest")
            return web.json_response({'status': "ok", 'token': str(response)})
        return web.json_response({'status': "not_ok"})

    async def hendler_get_user(self, d, request):
        logger.info(d)
        res = self.db.get_user(d['login'])
        if res:
            return web.json_response({'status': 'ok', 'user': res})
        return False

    async def hendler_authentication(self, request):
        data = await request.json()
        logger.info(data['data'])
        res = self.db.authentication(data['data']['login'], data['data']['password'])
        logger.info(res)
        if res:
            response = self.encryption(data['data']['login'], data['data']['password'], res[2])
            token = response.decode("utf-8")
            return web.json_response({'status': "ok", 'token': token})
        return False
