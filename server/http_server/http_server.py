import asyncio
from aiohttp import web
from loguru import logger
from hendlers import Hendlers
import jwt

def decode(token):


def encryption(login, password):
    encoded = jwt.encode({'login': login, 'password': password}, 'onal', algorithm='HS256')
    logger.info(encoded)
    return encoded

@web.middleware
async def create_token(request, handler):
    if handler(request):
        response = encryption(data['data']['login'], data['data']['password'])
        return web.json_response({'status': "unautheticated user", 'token': response})
    return web.json_response({'status': "unautheticated user"})


if __name__ == '__main__':
    app = web.Application(middlewares=[create_token])
    hndl = Hendlers()
    app2 = web.Application()
    app.router.add_route('GET',  '/add_new_user', hndl.hendler_add_new_user)
    app2.router.add_route('GET',  '/return_id', hndl.hendler_get_user)
    app.router.add_route('GET',  '/authentication', hndl.hendler_authentication)
    web.run_app(app, host= "localhost", port=443)
