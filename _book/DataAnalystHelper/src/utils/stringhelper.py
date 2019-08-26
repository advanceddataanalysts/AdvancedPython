#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 14:28
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : stringhelper.py
# @Software: PyCharm


import os
import sys
import prettytable


class StringHelper(object):

    @classmethod
    def str_cut(cls, my_str):
        """字符串截取"""
        my_str = cls.str_norm(my_str)

        if len(my_str) > 600:
            my_str = my_str[:300] + '……' + my_str[-300:]

        return my_str

    @classmethod
    def to_list(cls, obj):
        if isinstance(obj, type(None)):
            obj = []
        if not isinstance(obj, list):
            obj = [obj]
        return obj

    @classmethod
    def str_norm(cls, my_str):
        my_str = my_str.replace("\\n", " ").replace("\\t", " ").replace("\\", " ")
        return my_str

    @classmethod
    def error(cls, my_str):
        my_str = cls.str_cut(my_str)
        """获取文件路径和函数名"""
        filename = sys.argv[0][sys.argv[0].rfind(os.sep) + 1:].split('.py')[0].split('/')[-1]
        my_str = "报错信息：\n{0}\n执行脚本：{1}".format(my_str, filename)
        return my_str

    @classmethod
    def pretty_tabel(cls, df):
        """创建表格实例"""
        confusion_matrix_table = prettytable.PrettyTable()
        confusion_matrix_table.field_names = [""] + df.columns.tolist()[1:]
        for row in range(df.shape[0]):
            """增加第一行数据"""
            confusion_matrix_table.add_row(df.values[row])
        return confusion_matrix_table

    @classmethod
    def get_alarm_suffix(cls, ):
        from src.utils.get_source import get_source
        mac, ip, somebody = get_source()
        if somebody == 'unknown':
            suffix = "\n--来自数据分析组\nmac: {0}\nip: {1}\nSomebody: {2}".format(mac, ip, somebody)
        else:
            suffix = "\n--来自数据分析组\nSomebody: {0}".format(somebody)
        return suffix

    @classmethod
    def sql_error_check(cls, my_str):

        if my_str.find("DatabaseError") != -1:
            """判断presto语法错误"""
            if my_str.find("java") != -1 and my_str.find("lineNumber") != -1:
                return True
            """判断mysql语法错误"""
            if my_str.find("error") != -1 or my_str.find("Unknown column") != -1 or my_str.find("exist") != -1:
                return True
        else:
            return False


if __name__ == '__main__':
    pass
