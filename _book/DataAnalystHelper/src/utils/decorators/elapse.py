#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 15:09
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : elapse.py
# @Software: PyCharm


import time
from src.config import public_config


def elapse(dingding=True, des="", subject="inform"):
    """定义装饰器用于查询SQL时打印报错信息并推送到钉钉"""

    def wrapper(func):
        def app(*args, **kwargs):

            try:
                startTime = time.time()
                rst = func(*args, **kwargs)
                endTime = time.time()
                time_eclipse = round((endTime - startTime), 2)
                print(f"{des}time is {time_eclipse} s")

                if dingding:
                    from src.utils.inforobot import dingdingrobot
                    dingdingrobot(f"{des + public_config.cur_time}执行成功耗时:{time_eclipse}", subject=subject)
                return rst

            except Exception as e:

                raise

        return app

    return wrapper
