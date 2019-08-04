from loguru import logger
from aiohttp import web
from db_worker import DBWorker

class Hendlers:
    def __init__(self):
        self.db = DBWorker()

    async def hendler_get(self, request):
        data = await request.json()
        logger.info(data)
        logger.info(data['data'])
        if data['action'] == "add_new_user":
            res = self.db.add_new_user(data['data']['login'], data['data']['password'])
        elif data['action'] == "check_availability_login":
            res = self.db.check_availability_login(data['data']['login'])
        elif data['action'] == "return_id":
            res = self.db.return_id(data['data']['login'])
        elif data['action'] == "authentication":
            res = self.db.authentication(data['data']['login'], data['data']['password'])
        else:
            logger.error("unknown action")
        logger.info(str(res))
        return web.Response(text=str(res))
