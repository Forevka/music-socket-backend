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
    logger.info(request.headers)
    token = request.headers.get("token", None)
    logger.info(token)
    if token is None:
        return web.json_response({'message': "provide 'token' headers first"}, status=401)
    try:
        decoded = decode(token)
        logger.info(decoded)
        logger.info(request)
        response = await handler(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        logger.debug("invalid token - {} error {}".format(token, e))
        return web.json_response({'message': 'need authenticate first'}, status=401)

@web.middleware
async def add_cors(request, handler):
    logger.info(request)
    if (request.method == 'OPTIONS'):
        response = web.Response(status=200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        logger.info(response.headers)
        return response
    response = await handler(request)

    logger.info(response.headers)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    logger.info(response.headers)
    return response

def register_route(app, path, method, handler):
    resource = cors.add(app.router.add_resource(path))
    cors.add(
        resource.add_route(method, handler), {
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                allow_headers="*"
            )
        })

async def cors_handler(request):
    logger.info(request)
    return web.json_response()

def register_with_cors(app, method, path, handler, cors_handler = cors_handler):
    app.router.add_route('OPTIONS',  path, cors_handler)
    app.router.add_route(method,  path, handler)

if __name__ == '__main__':
    app = web.Application(middlewares=[add_cors])
    app2 = web.Application(middlewares=[check_token])

    hndl = Handlers()
    register_with_cors(app, 'POST', '/add_new_user', hndl.hendler_add_new_user)
    register_with_cors(app, 'POST', '/authentication', hndl.hendler_authentication)
    register_with_cors(app, 'POST', '/get_channel', hndl.hendler_get_channel)
    register_with_cors(app, 'POST', '/get_fullchannels', hndl.hendler_get_fullchannels)
    register_with_cors(app, 'POST', '/authentication', hndl.hendler_authentication)

    register_with_cors(app2, 'POST', '/get_me', hndl.hendler_get_me)
    register_with_cors(app2, 'POST', '/get_user',  hndl.hendler_get_user)

    app.add_subapp('/methods/', app2)
    web.run_app(app, host= "localhost", port=443)
