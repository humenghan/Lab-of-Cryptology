
from Crypto.Cipher import DES3
import base64
import binascii

def create_key(key):
    if len(key) >= 16:
        tmp = key[0:15]
        key =tmp + ' '
    else:
        while len(key) < 16:
            key += " "
    return key.encode()


def add_ei(data):
    tmp = data + '\0' * (8 - (len(data) % 8))
    return tmp

class _3DES():
    def __init__(self,key):
        self.key = create_key(key)
        self.mode = DES3.MODE_ECB


    def encrypt(self, code):
        msg = code + '\0' * (8 - (len(code) % 8))
        msg = msg.encode('utf-8')
        cryptor = DES3.new(self.key, self.mode)
        encode = cryptor.encrypt(msg)
        return base64.encodebytes(encode)

    def decrypt(self, encode):
        cryptor = DES3.new(self.key, self.mode)
        return ((cryptor.decrypt(base64.decodebytes(encode)).decode('utf-8')).rstrip('\0'))


code = "abcdefg123 4567"
key = '123456'
my = _3DES(key)
enc = my.encrypt(code)
c = my.decrypt(enc)
print(code,'\n',enc,'\n',c)
print("十六进制密文：",binascii.b2a_hex(enc).swapcase())


