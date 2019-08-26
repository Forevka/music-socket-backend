from loguru import logger
from aiohttp import web

from ..DBdriver.db_worker import DBWorker
from ..utils import encode, decode
from ..middlewares import register_with_cors
import smtplib, ssl
from ..utils import settings
import random

class HandlersWithoutAuth():
    def __init__(self):
        self.recovery_list = dict()
        self.db = DBWorker()


    async def add_new_user(self, request):
        data = await request.json()
        logger.info(data)
        res = self.db.add_new_user(data['login'], data['password'], data['email'] )
        if res:
            response = encode(res)
            token = response.decode("utf-8")
            return web.json_response({'status': "ok", 'token': token})
        return web.json_response({'message': '???'}, status=406)


    async def login_user(self, request):
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
        data = await request.json()
        logger.info(data['id'])
        res = self.db.get_channel(data['id'])
        logger.info(res)
        if res:
            return web.json_response({'channel': res})
        return web.json_response({'message': 'Cant find this channel'}, status=406)


    async def get_fullchannels(self, request):
        res = self.db.get_fullchannels()
        logger.info(res)
        if res:
            return web.json_response({'channels': res})
        return web.json_response({'message': '???'}, status=406)

    async def recovery_password_sending(self, request):
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
        data = await request.json()
        if self.recovery_list[data['email']] == data['key']:
            new_pass = random.randint(10000000, 99999999)
            self.db.update_password(new_pass, data['email'])
            return web.json_response({'temporary_password': new_pass})
        return web.json_response({'message': "invalid key"})

    @staticmethod
    def register(app):
        this_handler = HandlersWithoutAuth()
        register_with_cors(app, 'POST', '/add_new_user', this_handler.add_new_user)
        register_with_cors(app, 'POST', '/authentication', this_handler.login_user)
        register_with_cors(app, 'POST', '/get_channel', this_handler.get_channel)
        register_with_cors(app, 'POST', '/get_fullchannels', this_handler.get_fullchannels)
        register_with_cors(app, 'POST', '/recovery_password_check', this_handler.recovery_password_check)
        register_with_cors(app, 'POST', '/recovery_password_sending', this_handler.recovery_password_sending)
