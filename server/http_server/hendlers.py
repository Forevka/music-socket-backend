from loguru import logger
from aiohttp import web
from db_worker import DBWorker
import json


class Hendlers:
    def __init__(self):
        self.db = DBWorker()

    async def hendler_add_new_user(self, request):
        data = await request.json()
        logger.info(data['data'])
        res = self.db.add_new_user(data['data']['login'], data['data']['password'])
        if res:
            return web.Response(text=json.dumps({"try": True, "userID": res}))
        return web.Response(text=json.dumps({"try": False}))

    async def hendler_return_id(self, request):
        data = await request.json()
        logger.info(data['data'])
        res = self.db.return_id(data['data']['login'])
        if res:
            return web.Response(text=json.dumps({"try": True, "userID": res}))
        return web.Response(text=json.dumps({"try": False}))

    async def hendler_authentication(self, request):
        data = await request.json()
        logger.info(data['data'])
        res = self.db.authentication(data['data']['login'], data['data']['password'])
        if res:
            return web.Response(text=json.dumps({"try": True, "userID": res}))
        return web.Response(text=json.dumps({"try": False}))
