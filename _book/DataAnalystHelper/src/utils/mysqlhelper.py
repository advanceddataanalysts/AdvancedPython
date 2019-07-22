#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-21 15:55
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : mysqlhelper.py
# @Software: PyCharm

import re
import os
import sys
import time
import threading
import pymysql
import pandas as pd
import multiprocessing
from math import ceil
from queue import Queue
from src.config import config
from src.utils import encryption
from src.utils.ding_robot import dingdingrobot
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

    def insertmany_bydf(self, df, tb, if_exists="append", n=6):
        """数据插入数据库的封装方法用于`处理空值&打印过程信息&打印插入信息`"""

        startTime = time.time()

        filename = sys.argv[0][sys.argv[0].rfind(os.sep) + 1:].split('.py')[0].split('/')[-1]

        df = df.where(pd.notnull(df), "None").replace("nan", "None")
        df = df.astype("str")
        sql = '''insert into {0} ({1}) values ({2});'''
        sql = sql.format(tb, ",".join(df.columns), ("%s," * len(df.columns))[:-1])
        count_times = 0

        while count_times < n:
            try:

                conn = self.getconn()
                cursor = conn.cursor()

                if if_exists == "replace":
                    delete_rows = cursor.execute("delete from {0}".format(tb))
                elif if_exists == "replace-truncate":
                    delete_rows = cursor.execute("truncate {0}".format(tb))
                else:
                    delete_rows = 0
                para = [tuple([None if y == "None" else y for y in x]) for x in df.values]
                insert_rows = cursor.executemany(sql, para)
                conn.commit()

                print("   insert数据行数:{0}".format(insert_rows))
                print("数据库insert成功")

                endTime = time.time()
                time_eclipse = round((endTime - startTime), 2)

                count_times = n

            except Exception as e:

                count_times += 1
                conn.rollback()
                conn.commit()
                time.sleep(10)

                if count_times >= n:
                    error_content = repr(e).replace("\\n", " ").replace("\\", " ").replace("\\t", " ")
                    if len(error_content) > 400:
                        error_content = error_content[:200] + '……' + error_content[-200:]
                    print("分割线start--------我分割我分割----------分割线start")
                    print(repr(e).replace("\\n", " ").replace("\\", " ").replace("\\t", " "))

                    dingdingrobot(content="脚本:" + filename + "\n" + error_content, subject='test')
                    print("分割线end--------我分割我分割----------分割线end")

                    raise Exception("数据插入失败")

            finally:

                self.close(conn, cursor)

    def insertmany_bydf_thread(self, big_df, tb, if_exists="append", pools=True):

        self.pools = pools
        self.dbinstance = ConnectionPools()

        if if_exists == "replace":
            self.execute(sql="truncate {0}".format(tb))

        q = Queue(maxsize=15)  # 设定最大队列数和线程数

        nrows = big_df.shape[0]
        cut = 50000
        nceil = ceil(nrows / 50000)

        for i in range(nceil):
            t = threading.Thread(target=self.insertmany_bydf,
                                 args=(big_df[cut * i:cut * (i + 1)], tb, "append",))
            q.put(t)
            if q.full() or i == nceil - 1:
                thread_list = []
                while q.empty() == False:
                    t = q.get()
                    thread_list.append(t)
                    t.start()
                for t in thread_list:
                    t.join()

    def updatemany_bydf(self, df, sql, batch=False, multip=False, processes=4):
        df = df.where(pd.notnull(df), "None")
        df = df.astype("str")

        if not multip:

            conn = self.getconn()
            cursor = conn.cursor()
            try:
                sql = sql
                para = [[None if y == "None" else y for y in x] for x in df.values]

                if not batch:
                    rows = cursor.executemany(sql, para)
                    print("   update数据行数:{0}".format(rows))
                    print("数据库update完成")
                else:
                    nrows = df.shape[0]
                    nceil = ceil(nrows / 100) + 1

                    for i in range(nceil):
                        if 100 * (i + 1) < nrows:
                            rows = cursor.executemany(sql, para[100 * i:100 * (i + 1)])
                        else:
                            rows = cursor.executemany(sql, para[100 * i:100 * (i + 1)])
                        print("   update数据行数[{0}]:{1}".format(i, rows))
                        print("数据库update完成")

            except Exception as e:
                print("start分割线----------------------------分割线start")
                print(para)
                print(repr(e).replace("\\n", " ").replace("\\", " ").replace("\\t", " "))
                conn.rollback()
                print("end分割线----------------------------分割线end")
            conn.commit()
            self.close(conn, cursor)
        else:
            self.pools = True
            if self.pools:
                self.dbinstance = ConnectionPools()
            processes = processes
            interval = 100
            cut = df.shape[0] // interval + 1

            p = multiprocessing.Pool(processes=processes)

            for i in range(cut):
                tep = df[interval * i:interval * (i + 1)].reset_index(drop=True)
                if tep.shape[0] > 0:
                    print(i)
                    p.apply_async(self.updatemany_bydf(tep, sql, multip=False))
                else:
                    break
            p.close()
            p.join()

    def execute(self, sql, params=None, index=0):

        startTime = time.time()
        filename = sys.argv[0][sys.argv[0].rfind(os.sep) + 1:].split('.py')[0].split('/')[-1]

        conn = self.getconn()
        cursor = conn.cursor()
        sql = self.sql_clean(sql)
        try:
            rows = cursor.execute(sql)
            conn.commit()
            if re.search('(delete)|(truncate)|(drop)', sql, flags=re.I):
                print("   execute[{0}]删除表行数:{1}".format(index, rows))
                endTime = time.time()
                time_eclipse = round((endTime - startTime), 2)
                # hflog.info({"filename": filename, "sql": sql, "rows": rows, "time_eclipse": time_eclipse})
            elif re.search('create', sql, flags=re.I):
                print("   execute[{0}]创建表成功".format(index))
            elif re.search('update', sql, flags=re.I):
                print("   execute[{0}]更新表行数:{1}".format(index, rows))
            else:
                print("   execute[{0}]数据行数:{1}".format(index, rows))
            print("sql语句执行成功")
            self.close(conn, cursor)
        except Exception as e:
            print("start分割线----------------------------分割线start")
            print("   execute[{0}]语句:\n{1}".format(index, sql))
            print(repr(e).replace("\\n", " ").replace("\\", " ").replace("\\t", " "))
            conn.rollback()
            print("end分割线----------------------------分割线end")
            conn.commit()
            self.close(conn, cursor)
            raise Exception("数据execute失败")

    def execute_sqls(self, sql, params=None):
        sqllist = sql.split(";")
        for index, sql in enumerate(sqllist):
            if sql.strip():
                sql = self.sql_clean(sql)
                self.execute(sql, index=index)

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

    @staticmethod
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

    @staticmethod
    def sql_clean(self, sql):

        sql = re.sub('\,\s*\)', ')', sql)
        sql = re.sub('\.0,', ',', sql)

        sql = sql.replace(", nan", "").replace("nan, ", "").replace("None, ", "").replace(", None", "")

        return sql
