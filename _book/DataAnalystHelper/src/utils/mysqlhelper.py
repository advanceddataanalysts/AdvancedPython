#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-21 15:55
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : mysqlhelper.py
# @Software: PyCharm

import re
import pymysql
import pandas as pd
from src.config import config
from src.utils import encryption
from src.utils.mydbpools import ConnectionPools

DB = config.along_localhost
host = DB['host']
port = DB['port']
user = DB['user']
passwd = DB['passwd']
db = DB["db"]

encryption_instance = encryption.Encryption()


class MysqlHelper(object):
    def __init__(self, host=host, port=port, user=user, passwd=passwd, db=db, charset="utf8", read_timeout=7200,
                 pools=False):
        self.host = encryption_instance.decrypt(host)
        self.port = int(encryption_instance.decrypt(port))
        self.user = encryption_instance.decrypt(user)
        self.passwd = encryption_instance.decrypt(passwd)
        self.db = encryption_instance.decrypt(db)
        self.charset = charset
        self.read_timeout = read_timeout
        self.pools = pools

        if self.pools:
            self.dbinstance = ConnectionPools()

    def to_print(self, df, index=0, toprint=None):
        print("   get[{0}]原始数据shape:{1}".format(index + 1, df.shape))
        if toprint:
            if isinstance(toprint, str):
                toprint = [toprint]
            for method in toprint:
                mtd = getattr(df, method)
                if callable(mtd):
                    print("   get原始数据{0}:\n{1}".format(method, mtd()))
                else:
                    print("   get原始数据{0}:\n{1}".format(method, mtd))

    def __get_df(self, sql, conn=None, index=0, toprint=None):
        sql = self.sql_clean(sql)
        if not conn:
            conn = self.getconn()
            df = pd.read_sql(sql, conn)
            self.close(conn)
        else:
            df = pd.read_sql(sql, conn)
        self.to_print(df, index=index, toprint=toprint)
        return df

    def get_df(self, *args, connect_once=True, toprint=None):
        dfs = []
        if connect_once:
            conn = self.getconn()
            for i, sql in enumerate(args):
                cursor = conn.cursor()
                set_sql = 'SET SESSION group_concat_max_len = 102400;'
                cursor.execute(set_sql)
                df = self.__get_df(sql, conn=conn, index=i, toprint=toprint)
                dfs.append(df)
            self.close(conn, cursor)
        else:
            for i, sql in enumerate(args):
                df = self.__get_df(sql, index=i, toprint=toprint)
                dfs.append(df)
        return dfs if len(dfs) > 1 else dfs[0]

    def get_df_loadfile(self, *file_names, toprint=None, encoding="utf-8", format=None, connect_once=True):
        sqls = []
        for file_name in file_names:
            print("***开始执行sql文件:{0}***".format(file_name))
            with open('{0}'.format(file_name), 'r', encoding=encoding) as f:
                lines = f.read()
                if format:
                    if not isinstance(format, list):
                        format = [format]
                    lines = lines.format(*format)
                sqllist = lines.split(";\n")
                for sql in sqllist:
                    if sql.strip():
                        sql = self.sql_clean(sql)
                        sqls.append(sql.strip())
        dfs = self.get_df(*sqls, toprint=toprint, connect_once=connect_once)
        if not isinstance(dfs, list):
            dfs = [dfs]
        return dfs if len(dfs) > 1 else dfs[0]

    def getconn(self):
        if self.pools:
            conn = self.dbinstance.getconn(self.host, self.port, self.user, self.passwd, self.db, self.charset)
        else:
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                   read_timeout=self.read_timeout, charset=self.charset)
            print("\n数据库连接成功")
        return conn

    def close(self, conn, cursor=None):

        if cursor is not None:
            cursor.close()
        conn.close()
        if not self.pools:
            print("数据库连接关闭")

    def sql_clean(self, sql):

        sql = re.sub('\,\s*\)', ')', sql)
        sql = re.sub('\.0,', ',', sql)

        sql = sql.replace(", nan", "").replace("nan, ", "").replace("None, ", "").replace(", None", "")

        return sql
