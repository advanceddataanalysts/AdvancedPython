#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 17:37
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : check_update_time.py
# @Software: PyCharm


from functools import wraps
from src.config import config
from src.utils.stringhelper import StringHelper


def check_update_time(dingding=True, tb_name="", days=0, subject="test", db=config.along_localhost):
    """该装饰器用来检查指定days对应是否有数据更新, 如有更新则删除重新执行"""
    if "." in tb_name:
        tb_name = tb_name.split(".py")[0]

    def app(call_func):
        @wraps(call_func)
        def wrapper(*args, **kwargs):
            try:
                from src.utils.mysqlhelper import MysqlHelper
                from src.utils.ding_robot import dingdingrobot
                sql = """
                select update_time from {0} where update_time > date_sub(CURDATE(),interval {1} day) limit 1;
                """
                sql = sql.format(tb_name, days)
                mysqlinstance = MysqlHelper(**db)
                print("********检查表:{}是否已经更新********".format(tb_name))
                print(sql)
                df = mysqlinstance.get_df(sql)

            except Exception as e:
                print("check_update_time error execute:")
                content = repr(e)
                error_content = StringHelper.error(content)
                print(error_content)
                dingdingrobot(content="check_update_time表达式不正确", subject=subject)
                raise Exception("check_update_time表达式不正确;")

            if df.shape[0] == 0:
                res = call_func(*args, **kwargs)
                return res
            else:
                if dingding:
                    dingdingrobot(content=StringHelper.error(f"表名{tb_name},当日数据已经存在，将自动删除当日数据，重新执行"),
                                  subject=subject)

                sql = """
                delete from {0} where update_time > date_sub(CURDATE(),interval {1} day);
                """

                sql = sql.format(tb_name, days)
                mysqlinstance.execute(sql)

                res = call_func(*args, **kwargs)
                return res

        return wrapper

    return app


if __name__ == '__main__':
    pass
