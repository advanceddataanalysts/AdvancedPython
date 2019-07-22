#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-22 19:37
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : to_io.py
# @Software: PyCharm

import io
import pandas as pd


def to_io(*args, **kwargs):
    """将Excel文件保存为字节流的方法"""

    if "save_type" not in kwargs:
        kwargs["save_type"] = "xlsx"

    if kwargs["save_type"] == "xlsx":

        output = io.BytesIO()

        writer = pd.ExcelWriter(output)

        for df, sheet_name in zip(args, kwargs["sheets_name"]):

            if type(df.columns) == pd.core.indexes.multi.MultiIndex or type(
                    df.index) == pd.core.indexes.multi.MultiIndex:
                """判断发送的DataFrame是否为多重索引来执行是否忽略index, 多重索引保存到Excel如果忽略索引会使数据可读性极差"""
                df.to_excel(writer, sheet_name, index=True)
            else:
                df.to_excel(writer, sheet_name, index=False)

        writer.save()

    else:
        output = io.StringIO()

        args[0].to_csv(output, header=True, encoding="GB18030")

    data_io = output.getvalue()

    return data_io


if __name__ == '__main__':
    pass
