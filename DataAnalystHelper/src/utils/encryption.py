#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-21 15:29
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : encryption.py
# @Software: PyCharm


import base64
from src.config import config
from Crypto.Cipher import AES


class Encryption(object):

    def __init__(self, ):
        self.key = config.SECRET_KEY
        self.aes = AES.new(self.add_to_16(self.key), AES.MODE_ECB)

    def encrypt(self, text):
        encrypted_text = str(base64.encodebytes(self.aes.encrypt(self.add_to_16(text))), encoding='utf8').replace(
            '\n', '')

        return encrypted_text

    def decrypt(self, encrypted_text):
        text_decrypted = str(
            self.aes.decrypt(base64.decodebytes(bytes(encrypted_text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))

        return text_decrypted

    @staticmethod
    def add_to_16(text):
        while len(text) % 16 != 0:
            text += '\0'
        return str.encode(text)
