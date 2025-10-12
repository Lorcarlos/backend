import random


def uniqueTokenGenerator(existsTokens):
    while True:
        token = str(random.randint(0, 999999)).zfill(6)
        if token not in existsTokens:
            return token