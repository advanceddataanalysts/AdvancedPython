#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-22 18:09
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : hflog.py
# @Software: PyCharm


import os
import logbook
from logbook import Logger, TimedRotatingFileHandler

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.00"


def user_handler_log_formatter(record, handler):
    log = "{dt}\t{level}\t{filename}\t{func_name}\t{lineno}\t{msg}".format(
        dt=record.time,
        level=record.level_name,
        filename=os.path.split(record.filename)[-1],
        func_name=record.func_name,
        lineno=record.lineno,
        msg=record.message,
    )
    return log


LOG_DIR = os.path.join('logs')
try:
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
except Exception as e:
    print(repr(e))
user_file_handler = TimedRotatingFileHandler(os.path.join(LOG_DIR, '%s.log' % os.path.split(os.getcwd())[-1]),
                                             date_format='%Y%m%d', bubble=True)
user_file_handler.formatter = user_handler_log_formatter

# 用户代码logger日志
hflog = Logger("hflog")


def init_logger():
    logbook.set_datetime_format("local")
    hflog.handlers = []
    hflog.handlers.append(user_file_handler)


init_logger()
