import asyncio
from aiohttp import web
from loguru import logger
from hendlers import Hendlers


if __name__ == '__main__':
    app = web.Application()
    hndl = Hendlers()
    app.router.add_route('GET',  '/db', hndl.hendler_get)
    web.run_app(app, host= "localhost", port=443)
