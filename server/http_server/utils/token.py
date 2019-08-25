import jwt
from .settings import settings

def decode(token):
    return jwt.decode(token, settings.jwt_key, algorithms=['HS256'])

def encode(user):
    return jwt.encode(user, settings.jwt_key, algorithm='HS256')
