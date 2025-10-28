from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import os

##
KEY_MASTER = AESGCM.generate_key(bit_length=256)
KEY_SALT = os.urandom(12)

KEY_ID_CHARS = 'abcdefghijklmnopqrstuvwxyz'
KEY_ID_LEN = 30

##
def crypt_sha256(value:str, salt:bytes=KEY_SALT)->str:
    import hashlib
    import base64

    value_hashed = hashlib.sha256(salt + value.encode()).digest()
    return base64.b64encode(value_hashed).decode()

def id_generate()->str:
    import secrets

    ##
    return ''.join(i for i in secrets.choice(KEY_ID_CHARS))
