#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-21 15:07
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : config.py
# @Software: PyCharm

testing_email = ["yanglong_yan@163.com"]

environ = 'test'

if environ == 'develop':

    try_rerun_n = 3
    try_rerun_sleep = 5

    try_rerun_mysql_n = 120
    try_rerun_mysql_sleep = 600

    try_rerun_prosto_n = 120
    try_rerun_prosto_sleep = 900

    try_rerun_email_n = 1080
    try_rerun_email_sleep = 10

    depend_on_check_n = 120
    depend_on_check_sleep = 900

elif environ == 'test':

    try_rerun_n = 1
    try_rerun_sleep = 5

    try_rerun_mysql_n = 1
    try_rerun_mysql_sleep = 5

    try_rerun_prosto_n = 1
    try_rerun_prosto_sleep = 5

    try_rerun_email_n = 1
    try_rerun_email_sleep = 5

    depend_on_check_n = 1
    depend_on_check_sleep = 5

"""数据库连接"""
along_localhost = {"host": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                   "port": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                   "user": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                   "passwd": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                   "db": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}

dmart_dmart = {"host": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
               "port": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
               "user": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
               "passwd": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
               "db": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}

hive_prosto = {"host": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
               "port": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}

"""邮件服务器"""
emailsetting_data = {"host": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                     "user": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                     "password": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                     "sender": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}

SECRET_KEY = '123456'

# 数据库连接编码
DB_CHARSET = "utf8"

# mincached : 启动时开启的闲置连接数量(缺省值 0 以为着开始时不创建连接)
DB_MIN_CACHED = 10

# maxcached : 连接池中允许的闲置的最多连接数量(缺省值 0 代表不闲置连接池大小)
DB_MAX_CACHED = 10

# maxshared : 共享连接数允许的最大数量(缺省值 0 代表所有连接都是专用的)如果达到了最大数量,被请求为共享的连接将会被共享使用
DB_MAX_SHARED = 10

# maxconnecyions : 创建连接池的最大数量(缺省值 0 代表不限制)
DB_MAX_CONNECYIONS = 20

# blocking : 设置在连接池达到最大数量时的行为(缺省值 0 或 False 代表返回一个错误<toMany......>; 其他代表阻塞直到连接数减少,连接被分配)
DB_BLOCKING = False

# maxusage : 单个连接的最大允许复用次数(缺省值 0 或 False 代表不限制的复用).当达到最大数时,连接会自动重新连接(关闭和重新打开)
DB_MAX_USAGE = 3

# setsession : 一个可选的SQL命令列表用于准备每个会话，如["set datestyle to german", ...]
DB_SET_SESSION = None
