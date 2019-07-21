#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-21 17:08
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : along_test.py
# @Software: PyCharm


from src.utils import mysqlhelper
from src.config import config

mysqlinstance_localhost = mysqlhelper.MysqlHelper(**config.along_localhost)

sql = '''
select * 
from  subject 
'''

data = mysqlinstance_localhost.get_df(sql)

print(data)