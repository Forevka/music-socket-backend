from loguru import logger
from aiohttp import web
from db_worker import DBWorker

class Hendlers:
    def __init__(self):
        self.db = DBWorker()

    async def hendler_add_new_user(self, request):
        data = await request.json()
        logger.info(data['data'])
        res = self.db.add_new_user(data['data']['login'], data['data']['password'])
        logger.info(str(res))
        return web.Response(text=str(res))

    async def hendler_return_id(self, request):
        data = await request.json()
        logger.info(data['data'])
        res = self.db.return_id(data['data']['login'])
        return web.Response(text=str(res))

    async def hendler_check_availability_login(self, request):
        data = await request.json()
        logger.info(data['data'])
        res = self.db.check_availability_login(data['data']['login'])
        return web.Response(text=str(res))

    async def hendler_authentication(self, request):
        data = await request.json()
        logger.info(data['data'])
        res = self.db.authentication(data['data']['login'], data['data']['password'])
        return web.Response(text=str(res))
