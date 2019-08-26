#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 18:05
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : prestohelper.py
# @Software: PyCharm

import re
import pandas as pd
from pyhive import presto
from src.config import config
from src.utils.try_rerun import try_rerun
from src.utils.encryption import Encryption
from src.utils.decorators.elapse import elapse
from src.utils.ding_robot import dingdingrobot
from src.utils.stringhelper import StringHelper

host = config.hive_prosto["host"]
port = config.hive_prosto['port']

encryption_instance = Encryption()


class PrestoHelper(object):

    def __init__(self, host=host, port=port):
        self.host = encryption_instance.decrypt(host)
        self.port = int(encryption_instance.decrypt(port))

    @elapse(dingding=False, des="(presto)从数据库get数据")
    @try_rerun(dingding=True, n=config.try_rerun_prosto_n, sleep_time=config.try_rerun_prosto_sleep)
    def __get_df(self, sql, index=0, toprint=None, connect_once=True):
        sql = self.sql_clean(sql)
        try:
            if not self.conn.open:
                self.conn = self.getconn()
        except:
            self.conn = self.getconn()
            self.cursor = self.conn.cursor()
        try:
            df = pd.read_sql(sql, self.conn)
            self.to_print(df, index=index, toprint=toprint)
            if not connect_once:
                self.close(self.conn)
        except Exception as e:
            print("(presto)连接异常")
            self.close(self.conn)
            """判断错误如果为sql语法错误的话，跳出循环"""
            content = repr(e)
            error_content = StringHelper.error(content)

            if StringHelper.sql_error_check(content):
                dingdingrobot(content=f"(presto)sql语法不正确\n{error_content}\n路径try_rerun", subject="test")
                raise

        return df

    def get_df(self, *args, toprint=None, connect_once=True):
        dfs = []
        for i, sql in enumerate(args):
            df = self.__get_df(sql, index=i, toprint=toprint, connect_once=connect_once)
            dfs.append(df)
        if connect_once:
            self.close(self.conn, self.cursor)

        return dfs if len(dfs) > 1 else dfs[0]

    def get_df_loadfile(self, *file_names, toprint=None, encoding="utf-8", format=None, connect_once=True):
        sqls = []
        for file_name in file_names:
            print(f"***(presto)开始执行sql文件:{file_name}***")
            with open(f'{file_name}', 'r', encoding=encoding) as f:
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
        return dfs if len(dfs) > 1 else dfs[0]

    def getconn(self):
        conn = presto.connect(host=self.host, port=self.port)
        print("\n(presto)数据库连接成功")
        return conn

    def close(self, conn, cursor=None):
        if cursor is not None:
            cursor.close()
        conn.close()
        print("(presto)数据库连接关闭")

    @staticmethod
    def to_print(df, index=0, toprint=None):
        print(f"(presto)get[{index + 1}]原始数据shape:{df.shape}")
        if toprint:
            if isinstance(toprint, str):
                toprint = [toprint]
            for method in toprint:
                mtd = getattr(df, method)
                if callable(mtd):
                    print(f"(presto)get原始数据{method}:\n{mtd()}")
                else:
                    print(f"(presto)get原始数据{method}:\n{mtd}")

    @staticmethod
    def sql_clean(sql):

        sql = re.sub(r'\,\s*\)', ')', sql)

        return sql
