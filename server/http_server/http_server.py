import asyncio
from aiohttp import web
from loguru import logger
from handlers import Handlers
import jwt


def decode(token):
    logger.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return jwt.decode(token, 'onal', algorithms=['HS256'])

@web.middleware
async def check_token(request, handler):
    token = request.headers.get("token")
    try:
        logger.info("###############################")
        decoded = decode(token)
        logger.info(decoded)
        return await handler(decoded, request)
    except:
        logger.debug("invalid token - {}".format(token))
    finally:
        return web.json_response({'status': "unautheticated user"})


if __name__ == '__main__':
    app = web.Application()
    hndl = Handlers()
    app2 = web.Application(middlewares=[check_token])
    app.router.add_route('GET',  '/add_new_user', hndl.hendler_add_new_user)
    app2.router.add_route('GET',  '/get_user', hndl.hendler_get_user)
    app.router.add_route('GET',  '/authentication', hndl.hendler_authentication)
    app.add_subapp('/methods/', app2)
    web.run_app(app, host= "localhost", port=443)
