import asyncio
from aiohttp import web
from loguru import logger
from hendlers import Hendlers
import jwt



def encryption(login, password):
    encoded = jwt.encode({'login': login, 'password': password}, 'onal', algorithm='HS256')
    logger.info(encoded)
    return encoded

@web.middleware
async def check_token(request, handler):
    token = request.headers.get("token")
    if token:
        return await handler(token)
    return web.json_response({'status': "unautheticated user"})


if __name__ == '__main__':
    app = web.Application()
    hndl = Hendlers()
    app2 = web.Application(middlewares=[check_token])
    app.router.add_route('GET',  '/add_new_user', hndl.hendler_add_new_user)
    app2.router.add_route('GET',  '/get_user', hndl.hendler_get_user)
    app.router.add_route('GET',  '/authentication', hndl.hendler_authentication)
    app.add_subapp('/methods/', app2)
    web.run_app(app, host= "localhost", port=443)
