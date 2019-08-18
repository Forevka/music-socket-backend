import asyncio
from aiohttp import web
from loguru import logger
from handlers import Handlers
import aiohttp_cors
import jwt


def decode(token):
    return jwt.decode(token, 'onal', algorithms=['HS256'])

@web.middleware
async def check_token(request, handler):
    token = request.headers.get("token")
    try:
        decoded = decode(token)
        logger.info(decoded)
        return await handler(decoded, request)
    except:
        logger.debug("invalid token - {}".format(token))
        return web.StreamResponse(status=401, reason=None, headers = {'Access-Control-Allow-Origin': "*",
                    'test': '123',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'})


def register_route(app, path, method, handler):
    resource = cors.add(app.router.add_resource(path))
    cors.add(
        resource.add_route(method, handler), {
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*"
            )
        })


if __name__ == '__main__':
    app = web.Application()
    app2 = web.Application(middlewares=[check_token])

    hndl = Handlers()
    cors = aiohttp_cors.setup(app)


    register_route(app, '/add_new_user', 'POST', hndl.hendler_add_new_user)
    register_route(app, '/authentication', 'POST', hndl.hendler_authentication)

    register_route(app2, '/get_user', 'POST', hndl.hendler_get_user)
    app.add_subapp('/methods/', app2)


    web.run_app(app, host= "localhost", port=443)
