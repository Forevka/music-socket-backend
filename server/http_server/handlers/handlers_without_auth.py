from loguru import logger
from aiohttp import web

from DBdriver.db_worker import DBWorker
from ..utils import encode, decode
from ..middlewares import register_with_cors
import smtplib, ssl
from ..utils import settings
import random

class HandlersWithoutAuth():
    def __init__(self):
        self.recovery_list = dict()
        self.db = DBWorker()

    async def ping(self, request):
        """
        ---
        description: This end-point allow to test that service is up.
        tags:
        - Health check
        produces:
        - application/json
        responses:
            "200":
                description: successful operation. Return "pong" text
            "405":
                description: invalid HTTP Method
        """
        return web.json_response({'status': 'pong'})

    async def show_site(self, request):
        return web.Response(text=open("dist/index.html").read(), content_type='text/html')


    async def add_new_user(self, request):
        """
        tags:
        - User
        summary: Create user
        description: Creating a new user.
        operationId: examples.api.api.createUser
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: User object
          required: true
          schema:
            type: object
            properties:
              login:
                type: string
              email:
                type: string
              password:
                type: string
        responses:
          "200":
            description: successful operation
          "406":
            description: can`t create user
        """
        data = await request.json()
        logger.info(data)
        res = self.db.add_new_user(data['login'], data['password'], data['email'] )
        if res:
            response = encode(res)
            token = response.decode("utf-8")
            return web.json_response({'status': "ok", 'token': token})
        return web.json_response({'message': '???'}, status=406)


    async def login_user(self, request):
        """
        tags:
        - User
        summary: Login user
        description: Login user with given credentionals.
        operationId: examples.api.api.createUser
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: Login object
          required: true
          schema:
            type: object
            properties:
              login:
                type: string
              password:
                type: string
        responses:
          "200":
            description: Successful operation
          "406":
            description: Login or password incorect
        """
        data = await request.json()
        logger.info(data)
        res = self.db.authentication(data['login'], data['password'])
        if res:
            response = encode(res)
            logger.info(res)
            token = response.decode("utf-8")
            res['token'] = token
            return web.json_response(res)
        return web.json_response({'message': 'Login or password incorect'}, status=406)


    async def get_channel(self, request):
        """
        tags:
        - Channel
        summary: Get channel
        description: Get information about a specific channel.
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
              id:
                type: integer
        responses:
          "200":
            description: Successful operation
          "406":
            description: Id incorect
        """
        data = await request.json()
        logger.info(data['id'])
        res = self.db.get_channel(data['id'])
        logger.info(res)
        if res:
            return web.json_response(res)
        return web.json_response({'message': 'Cant find this channel'}, status=406)


    async def get_channel_page(self, request):
        """
        tags:
        - Channel
        summary: Get page with channels
        description: Get information about a channels.
        operationId: examples.api.api.createUser
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: Channels object
          required: true
          schema:
            type: object
            properties:
              page:
                type: integer
              amount:
                type: integer
              sort_by:
                type: string
              asc:
                type: boolean
        responses:
          "200":
            description: Successful operation
          "406":
            description: request incorect
        """
        data = await request.json()
        res = self.db.get_channel_list(page = data['page'],
                                        amount = data['amount'],
                                        sort_by = data['sort_by'],
                                        asc = bool(data['asc']))
        logger.info(res)
        if res:
            return web.json_response(res)
        return web.json_response({'message': '???'}, status=406)

    async def recovery_password_sending(self, request):
        """
        tags:
        - Recovery password
        summary: Sending key on email
        description: Sending key on email.
        operationId: examples.api.api.createUser
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: Recovery password object
          required: true
          schema:
            type: object
            properties:
              email:
                type: string
        responses:
          "200":
            description: Successful operation
          "406":
            description: email incorect
        """
        data = await request.json()
        res = self.db.check_email(data['email'])
        if res:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", settings.port_mail, context=context) as server:
                server.login(settings.mail_radio, settings.password_mail)
                key = random.randint(1000, 9999)
                message = "your key -->> {}".format(str(key))
                server.sendmail(settings.mail_radio, data['email'], message)
                self.recovery_list[data['email']] = key
                logger.info(self.recovery_list[data['email']])
                return web.json_response({'message': "message send"})
            return web.json_response({'message': "invalid email"})


    async def recovery_password_check(self, request):
        """
        tags:
        - Recovery password
        summary: Сheck key by email
        description: Сheck key by email.
        operationId: examples.api.api.createUser
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: Recovery password object
          required: true
          schema:
            type: object
            properties:
              email:
                type: string
              key:
                type: integer
        responses:
          "200":
            description: Successful operation
          "406":
            description: key or email incorect
        """
        data = await request.json()
        if self.recovery_list[data['email']] == data['key']:
            new_pass = random.randint(10000000, 99999999)
            self.db.update_password(new_pass, data['email'])
            return web.json_response({'temporary_password': new_pass})
        return web.json_response({'message': "invalid key"})

    @staticmethod
    def register(app):
        this_handler = HandlersWithoutAuth()
        register_with_cors(app, 'POST', '/ping', this_handler.ping)
        register_with_cors(app, 'POST', '/add_new_user', this_handler.add_new_user)
        register_with_cors(app, 'POST', '/authentication', this_handler.login_user)
        register_with_cors(app, 'POST', '/get_channel', this_handler.get_channel)
        register_with_cors(app, 'POST', '/get_channel_page', this_handler.get_channel_page)
        register_with_cors(app, 'POST', '/recovery_password_check', this_handler.recovery_password_check)
        register_with_cors(app, 'POST', '/recovery_password_sending', this_handler.recovery_password_sending)
        app.router.add_route('get', "/", this_handler.show_site)
        app.router.add_static('/static', "dist/static", show_index=True)
