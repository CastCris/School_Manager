from cryptography.hazmat.primitives.ciphers.aead import AESGCM
# from begin.globals import MASTER_KEY

import base64
import os

MASTER_KEY = AESGCM.generate_key(bit_length=256)

##
def dek_encrypt(dek:bytes, key:bytes=MASTER_KEY)->str:
    aesgcm = AESGCM(key)

    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, dek, None)
    print('cipher: ', ciphertext)

    return base64.b64encode(nonce + ciphertext).decode()

def dek_decrypt(dek:str, key:bytes=MASTER_KEY)->bytes:
    aesgcm = AESGCM(key)
    data = base64.b64decode(dek)

    nonce = data[:12]
    ciphertext = data[12:]

    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    return plaintext


def clm_encrypt(value:str, dek:bytes)->str:
    aesgcm = AESGCM(dek)
    value = value.encode()

    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, value, None)

    return base64.b64encode(nonce + ciphertext).decode()

def clm_decrypt(value:str, dek:bytes)->str:
    aesgcm = AESGCM(dek)
    data = base64.b64decode(value)

    nonce = data[:12]
    ciphertext = data[12:]

    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    return plaintext.decode()


"""
dek = AESGCM.generate_key(bit_length=256)
# print(base64.b64encode(dek).decode())
print(dek)

dek_wrap = dek_encrypt(dek)
print(dek_wrap)

dek_unwrap = dek_decrypt(dek_wrap)
print(dek_unwrap)
print()

##
value = '1234'
value_encrypt = clm_encrypt(value, dek)
value_decrypt = clm_decrypt(value_encrypt, dek)

print(value_encrypt)
print(value_decrypt)
"""
