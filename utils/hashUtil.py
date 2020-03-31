import jwt
from bcrypt import hashpw, gensalt
import time
from hashlib import sha256
import random

#to-do: Move to environment var

CHAR_ENCODING_DEFAULT = "utf-8"
PW_SALT = b'$2b$12$YQQr9sRz.pz/I0aqNhwHTe'
JWT_ALGO = 'HS256'
TOKEN_EXP_INCREMENT = 300000

# END env MOVE

class PasswordManager(object):
    def __init__(self):
        pass

    def hashPassword(self, _pw):
        return hashpw(_pw, PW_SALT)

    def createUserId(self):
        sh2_hash = sha256(str(time.time()).encode("utf-8"))
        sh2_hash.update(str(gensalt()).encode("utf-8"))

        return sh2_hash.hexdigest()


class TokenManager(object):
    def __init__(self):
        pass

    def generateTokenExpiry(self):
        now = int(time.time())
        offset = now + TOKEN_EXP_INCREMENT

        return offset

    def generateWebToken(self, payload={}, decoder=None):
        salt = str(time.time()) + str(random.randint(0,1000) * random.randint(0,1000))
        payload = {"salt": salt}
        encoded_jwt = jwt.encode(payload, PW_SALT.decode(CHAR_ENCODING_DEFAULT), algorithm=JWT_ALGO)

        if decoder:
            return encoded_jwt.decode(decoder)
        else:
            return encoded_jwt

    def generateNewExpiry(self, _expiration = 0):
        if _expiration > 0:
            return int(time.time()) + _expiration
        else:
            return int(time.time()) + TOKEN_EXP_INCREMENT
