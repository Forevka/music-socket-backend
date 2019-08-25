from aiohttp import web

from loguru import logger

@web.middleware
async def add_cors(request, handler):
    if (request.method == 'OPTIONS'):
        logger.debug('cors')
        response = web.Response(status = 204)
        response.headers['Access-Control-Max-Age'] = '600'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'
        return response

    response = await handler(request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'

    return response

async def cors_handler(request):
    return web.Response(status = 204)

def register_with_cors(app, method, path, handler, cors_handler = cors_handler):
    app.router.add_route('OPTIONS',  path, cors_handler)
    app.router.add_route(method,  path, handler)
