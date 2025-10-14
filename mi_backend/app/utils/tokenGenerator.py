import random
from ..models.token.token import Token


def uniqueTokenGenerator():
    while True:
        token = str(random.randint(0, 999999)).zfill(6)
        exists = Token.query.filter(Token.token == token).first()
        if not exists:
            return token
