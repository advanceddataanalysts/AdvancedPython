#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-21 17:21
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : public_config.py
# @Software: PyCharm
import time
from src.config import config

"""
在此放入钉钉token和公用的非敏变量
"""

cur_time = time.strftime("%m-%d-%H-%M-%S", time.localtime())

email_test = True
"""
用config 中的 environ 字段来区分线上与本地环境
线上环境任务失败和重跑为 循环执行120次,每次间隔10分钟
本地环境任务失败和重跑为 一次,无间隔
"""
if config.environ == 'test':
    ding_token = {
        "test": "https://oapi.dingtalk.com/robot/send?"
                "access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}

if config.environ == 'develop':
    ding_token = {
        "test": "https://oapi.dingtalk.com/robot/send?"
                "access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
