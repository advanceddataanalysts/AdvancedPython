#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 17:45
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : depend_on_check.py
# @Software: PyCharm

from functools import wraps
from src.config import config
from src.utils.try_rerun import try_rerun
from src.utils.ding_robot import dingdingrobot
from src.utils.stringhelper import StringHelper


def depend_on_check(dingding=True, tb_name="", days=0, subject="test", db=config.along_localhost, col="update_time",
                    conditions="", engine="mysql", format="%Y%m%d", ):
    """该装饰器用于监测使用的表在指定days是否有更新,若没有则不跳过执行阶段"""

    def app(call_func):
        global count_times
        count_times = 0

        @try_rerun(dingding=True, n=config.depend_on_check_n, sleep_time=config.depend_on_check_sleep)
        @wraps(call_func)
        def wrapper(*args, **kwargs):
            try:
                if engine == "mysql":
                    from src.utils.mysqlhelper import MysqlHelper
                    sql = """
                     select {1} from {0} where {1} >= date_sub(CURDATE(),interval {2} day) {3} limit 1;
                     """
                    sql = sql.format(tb_name, col, days, conditions)
                    sqlinstance = MysqlHelper(**db)
                if engine == "presto":
                    sql = """
                    select {1} from {0} where {1} >= date_format(date_add('day',{2},current_date),'{3}') {4} limit 1 """
                    sql = sql.format(tb_name, col, days, format, conditions)
                    from src.utils.prostohelper import prestohelper

                    sqlinstance = prestohelper(**config.hive_prosto)
                print("********检查表:{}是否已经更新********".format(tb_name))
                print(sql)
                df = sqlinstance.get_df(sql)

            except Exception as e:
                print("depend_on_check error execute:")
                content = repr(e)
                error_content = StringHelper.error(content)
                print(error_content)

                dingdingrobot(content=StringHelper.error(f"表{tb_name},depend_on_check表达式不正确"), subject=subject)

                raise Exception("depend_on_check表达式不正确")

            if df.shape[0] > 0:

                try:
                    res = call_func(*args, **kwargs)
                    return res
                except Exception as e:

                    print('depend_on_check error execute:')
                    content = repr(e)
                    error_content = StringHelper.error(content)
                    print(error_content)

                    raise
            else:
                global count_times
                print(f"depend_on_check第{count_times + 1}次")

                if dingding and count_times == 0:
                    dingdingrobot(content=StringHelper.error(f"依赖表{tb_name},当日无数据"), subject=subject)
                    count_times += 1

                raise Exception("依赖表未存在,来自depend_on_check")

        return wrapper

    return app


if __name__ == '__main__':
    pass
