from loguru import logger
from aiohttp import web

from ..DBdriver.db_worker import DBWorker
from ..utils import encode, decode
from ..middlewares import register_with_cors


def a_decorator_passing_arguments(function_to_decorate):
        def a_wrapper_accepting_arguments(self, request):
            logger.info("asdadadasdasdsadsadasdasd")
            token = request.headers.get('token')
            decoded = decode(token)
            if decoded['role']== 1:
                return function_to_decorate(self, request)
            return web.json_response({'message': 'your role not currently'}, status=406)
        return a_wrapper_accepting_arguments

class HandlersForAdmin:
    def __init__(self):
        self.db = DBWorker()


    @a_decorator_passing_arguments
    async def ban_user(self, request):
        """
        tags:
        - Ban user
        summary: Ban user
        description: This method baned specific user.
        operationId: examples.api.api.createUser
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: Channel object
          required: true
          schema:
            type: object
            properties:
              name:
                type: string
        responses:
          "200":
            description: Successful operation return user object
        """
        data = await request.json()
        logger.info(data)
        token = request.headers.get('token')
        decoded = decode(token)
        self.db.ban_user(name)
        return web.json_response({'message': "user was baned"}, status=200)




    @staticmethod
    def register(app):
        this_handler = HandlersForAdmin()
        register_with_cors(app, 'POST', '/ban_user', this_handler.ban_user)
