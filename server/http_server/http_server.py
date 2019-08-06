import asyncio
from aiohttp import web
from loguru import logger
from hendlers import Hendlers
import jwt

def decode(token):
    return jwt.decode(token, 'onal', algorithms=['HS256'])


def encryption(login, password):
    encoded = jwt.encode({'username': login, 'password': password}, 'onal', algorithm='HS256')
    logger.info(encoded)
    return encoded

@web.middleware
async def middle(request, handler):
    data = await request.json()
    if data['data']['password'] and await handler(request):
        logger.info("doshlo")
        return encryption(data['data']['password'], data['data']['login'])
    user_token = request.headers.get("token")
    logger.info(user_token)
    if user_token:
        response = handler(*decode(user_token))
        logger.info(response)
        return response
    return web.json_response({'status': "unautheticated user"})


if __name__ == '__main__':
    app = web.Application(middlewares=[middle])
    hndl = Hendlers()
    app.router.add_route('GET',  '/add_new_user', hndl.hendler_add_new_user)
    app.router.add_route('GET',  '/return_id', hndl.hendler_return_id)
    app.router.add_route('GET',  '/authentication', hndl.hendler_authentication)
    web.run_app(app, host= "localhost", port=443)
