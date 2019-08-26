#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-21 17:08
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : along_test.py
# @Software: PyCharm

import random
from src.utils.mysqlhelper import MysqlHelper
from src.utils.emailhelper import EmailMessage
from src.utils.prestohelper import PrestoHelper
from src.config import config

mysqlinstance_localhost = MysqlHelper(**config.along_localhost)
prestoinstance = PrestoHelper(**config.hive_prosto)

sql = '''
select *  
from  subject
'''

data = mysqlinstance_localhost.get_df(sql)

print(data)

title = 'test' + str(random.random())
receivers = ["yanglong_yan@163.com"]
message = EmailMessage(subject=title, receivers=receivers, dfs=data, sheets_name=["test"])

# mysqlinstance_localhost.execute(sql)

# mysqlinstance_localhost.insertmany_byengin(data, 'along_subject_copy', if_exists='replace')
