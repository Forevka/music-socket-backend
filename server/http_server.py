import asyncio
from aiohttp import web
from loguru import logger
from http_server.DBdriver import DBWorker
from http_server.handlers import HandlersWithoutAuth, HandlersAuth, HandlersForAdmin
from http_server.middlewares import register_with_cors, add_cors, check_token

from aiohttp_swagger import *

"""
EXAMPLE
security = {
    "api_key": {
      "type": "apiKey",
      "name": "api_key",
      "in": "header"
    },
    "petstore_auth": {
      "type": "oauth2",
      "flow": "implicit",
      "authorizationUrl": "http://localhost/authentication",
      "scopes": {
        "write_pets": "modify pets in your account",
        "read_pets": "read your pets"
      }
    }
  }
EXAMPLE
"""

if __name__ == '__main__':
    security = {
        "api_key": {
          "type": "apiKey",
          "description": "Login user",
          "name": "token",
          "authorizationUrl": "http://localhost/authentication",
          "in": "header"
        }
      }


    app = web.Application(middlewares=[add_cors])
    app2 = web.Application(middlewares=[check_token])
    app3 = web.Application()

    HandlersWithoutAuth.register(app)
    HandlersAuth.register(app2)
    HandlersForAdmin.register(app3)

    app.add_subapp('/methods/', app2)
    app.add_subapp('/foradmins/', app3)

    setup_swagger(app,
                description = "API for our Radio server",
                title="Radio API",
                security_definitions=security)
    web.run_app(app, host= "localhost", port=443)
