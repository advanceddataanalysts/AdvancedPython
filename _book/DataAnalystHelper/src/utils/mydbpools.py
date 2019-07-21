#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-21 16:21
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : mydbpools.py
# @Software: PyCharm

import pymysql
from src.config import config
from DBUtils.PooledDB import PooledDB


class ConnectionPools(object):
    __pool = None

    def __init__(self):
        pass

    def __enter__(self):
        self.conn = self.__get_conn()
        self.cursor = self.conn.cursor()

        return self

    def __get_conn(self, host, port, user, passwd, db, charset):
        if self.__pool is None:
            self.__pool = PooledDB(creator=pymysql, mincached=config.DB_MIN_CACHED, maxcached=config.DB_MAX_CACHED,
                                   maxshared=config.DB_MAX_SHARED, maxconnections=config.DB_MAX_CONNECYIONS,
                                   blocking=config.DB_BLOCKING, maxusage=config.DB_MAX_USAGE,
                                   setsession=config.DB_SET_SESSION, host=host, port=port, user=user, passwd=passwd,
                                   db=db, use_unicode=True, charset=charset)

        return self.__pool.connection()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        释放连接池资源
        """
        self.cursor.close()
        self.conn.close()

    def getconn(self, host, port, user, passwd, db, charset):
        conn = self.__get_conn(host, port, user, passwd, db, charset)

        return conn
