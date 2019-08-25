import asyncio
from aiohttp import web
from loguru import logger
from http_server.DBdriver import DBWorker
from http_server.handlers import HandlersWithoutAuth, HandlersAuth
from http_server.middlewares import register_with_cors, add_cors, check_token

if __name__ == '__main__':
    app = web.Application(middlewares=[add_cors])
    app2 = web.Application(middlewares=[check_token])

    HandlersWithoutAuth.register(app)
    HandlersAuth.register(app2)

    app.add_subapp('/methods/', app2)
    web.run_app(app, host= "localhost", port=443)
