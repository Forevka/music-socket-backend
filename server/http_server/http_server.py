import asyncio
from aiohttp import web
from loguru import logger
from hendlers import Hendlers


if __name__ == '__main__':
    app = web.Application()
    hndl = Hendlers()
    app.router.add_route('PUT',  '/add_new_user', hndl.hendler_add_new_user)
    app.router.add_route('PUT',  '/return_id', hndl.hendler_return_id)
    app.router.add_route('PUT',  '/check_availability_login', hndl.hendler_check_availability_login)
    app.router.add_route('PUT',  '/authentication', hndl.hendler_authentication)
    web.run_app(app, host= "localhost", port=443)
