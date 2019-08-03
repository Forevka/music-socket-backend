import asyncio
from aiohttp import web
from loguru import logger
from hendlers import Hendlers
import db_worker

if __name__ == '__main__':
    db = db_worker.DB()
    app = web.Application()
    hndl = Hendlers()
    app.router.add_route('PUT',  '/da', hndl.hendler_put)
    app.router.add_route('GET',  '/da', hndl.hendler_get)
    app.router.add_route('DELETE',  '/da', hndl.hendler_delete)
    web.run_app(app, host= "localhost", port=443)
