#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 18:47
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : requestshelper.py
# @Software: PyCharm

import requests
from src.utils.stringhelper import StringHelper


class RequestsHelper(object):

    def __enter__(self):
        print("开始session")
        self.session = requests.session()
        return self

    def __exit__(self, type, value, trace):
        self.session.close()
        print("结束session")

    def session_catch(self, method, url, **kwargs):

        for i in range(10):
            try:
                r = self.session.request(method, url, **kwargs, timeout=10)
                return r
            except Exception as e:
                if i == 0:
                    print("session_catch error execute:")
                    content = repr(e)
                    error_content = StringHelper.error(content)
                    print(error_content)
                elif i == 9:
                    raise


if __name__ == '__main__':
    pass
