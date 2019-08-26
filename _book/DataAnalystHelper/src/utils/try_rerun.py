#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 14:28
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : try_rerun.py
# @Software: PyCharm

import time
from functools import wraps
from src.config import config
from src.utils.ding_robot import dingdingrobot
from src.utils.stringhelper import StringHelper

n = config.try_rerun_n
sleep_time = config.try_rerun_sleep


def try_rerun(dingding=True, n=n, sleep_time=sleep_time, subject="test"):
    """失败重新执行的装饰器"""

    def try_n_times(call_func):
        @wraps(call_func)
        def wrapper(*args, **kwargs):
            count_times = n
            sleep = sleep_time
            for i in range(count_times):
                try:
                    res = call_func(*args, **kwargs)
                    return res
                except Exception as e:
                    error_n = i + 1
                    """
                    早上七点之后每次休眠时间改成5秒，最大重跑次数为3
                    """
                    if time.localtime()[3] > 7:
                        sleep = 5
                        if i > 3:
                            i = count_times - 1
                    time.sleep(sleep)
                    fun = call_func.__name__

                    print("try_rerun error execute:")
                    content = repr(e)
                    error_content = StringHelper.error(content)
                    print(f"连续{i + 1}次出现异常\n函数名：{fun}\n{error_content}\n路径try_rerun;")

                    """如果为sql语法错误，跳出循环"""
                    if StringHelper.sql_error_check(content):
                        raise Exception("sql语法不正确,路径try_rerun;")
                    if i == count_times - 1:
                        if dingding:
                            dingdingrobot(content=f"连续{error_n}次出现异常\n函数:{fun}\n{error_content}\n路径try_rerun",
                                          subject=subject)
                        raise Exception("连续{}次出现异常,路径try_rerun;".format(error_n))

        return wrapper

    return try_n_times


if __name__ == "__main__":
    pass
