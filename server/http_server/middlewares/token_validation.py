from aiohttp import web

from loguru import logger
from ..utils import decode

@web.middleware
async def check_token(request, handler):
    token = request.headers.get("token", None)
    if token is None:
        return web.json_response({'message': "provide 'token' headers first"}, status=401)

    try:
        decoded = decode(token)
    except Exception as e:
        logger.debug("invalid token - {} error {}".format(token, e))
        return web.json_response({'message': 'corrupted token'}, status=401)

    return await handler(request)
