#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 14:13
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : verify_crontab.py
# @Software: PyCharm

import requests
from src.utils.try_rerun import try_rerun
from src.utils.ding_robot import dingdingrobot


@try_rerun(dingding=True, n=10, sleep_time=5)
def get_next_time(crontab):
    url = "http://api.bejson.com/btools/othertools/cron/"
    data = {"crontxt": crontab}

    response = requests.post(url=url, data=data)

    hjson = response.json()

    if hjson["code"] != -1:
        obj_str = hjson['obj']

        return obj_str.split("<br>")[0]
    else:
        if hjson["message"] != "解析失败,请联系管理员":
            import sys
            import os
            filename = sys.argv[0][sys.argv[0].rfind(os.sep) + 1:].split('.py')[0].split('/')[-1]
            dingdingrobot(title='crontab设置失败:', content=f"{filename}:{crontab}", subject="test")
        return None


if __name__ == '__main__':
    get_next_time('00 00 00 * * ? ?')
