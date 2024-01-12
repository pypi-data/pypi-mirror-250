"""
pip install pycryptodome==3.14.1
"""
from Crypto.Cipher import AES
import base64


class KAES(object):
    def __init__(self, key: str, cont: str):
        """
        AES加解密
        :param key: 固定秘钥
        :param cont: 需要解密的字符串
        """
        self.key = key
        self.src = cont

    def encrypt(self):
        aes = AES.new(str.encode(self.key), AES.MODE_ECB)
        encode_pwd = str.encode(self.src.rjust(16, '@'))
        encrypt_str = str(base64.encodebytes(aes.encrypt(encode_pwd)), encoding='utf-8')
        return encrypt_str

    def decrypt(self):
        aes = AES.new(str.encode(self.key), AES.MODE_ECB)
        decrypt_str = (aes.decrypt(base64.decodebytes(self.src.encode(encoding='utf-8'))).
                       decode().replace('@', ''))
        return decrypt_str


if __name__ == '__main__':
    pass
