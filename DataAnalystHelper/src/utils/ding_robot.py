#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-21 17:25
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : ding_robot.py
# @Software: PyCharm


import requests
from src.config import public_config
from src.utils.get_source import get_source


def dingdingrobot(content='', subject='test', title=''):
    suffix = get_alarm_suffix()

    if title:
        content = title + '\n' + content + suffix
    else:
        content = content + suffix

    # text类型
    msg1 = {
        'msgtype': 'text',
        'text': {
            'content': content,
            'title': title
        },
        'at': {
            'atMobiles': [
                '110xxxx0120',  # @某人,传入注册钉钉使用的手机号码
                '999xxxx6969'
            ],
            'isAtAll': False  # @全体
        }
    }

    # link类型
    msg2 = {
        'msgtype': 'link',
        'link': {
            'text': content,
            'title': title,
            'picUrl': '图片地址',
            'messageUrl': '文字地址'
        }
    }

    # markdown类型
    msg3 = {
        'msgtype': 'markdown',
        'markdown': {
            'title': title,
            'text': content
        },
        'at': {
            'atMobiles': [
                '110xxxx0120',  # @某人,传入注册钉钉使用的手机号码
                '999xxxx6969'
            ],
            'isAtAll': False  # @全体
        }
    }

    # 整体跳转ActionCard类型
    msg4 = {
        'actionCard': {
            'title': title,
            'text': content,
            'hideAvatar': '0',
            'btnOrientation': '0',
            'singleTitle': '阅读全文',
            'singleURL': 'https://advanceddataanalysts.github.io/AdvancedPython/'
        },
        'msgtype': 'actionCard'
    }

    url = public_config.ding_token[subject]

    requests.post(url, json=msg1)


def get_alarm_suffix():
    mac, ip, somebody = get_source()
    if somebody == 'unknown':
        suffix = "\n--来自数据分析组\nmac: {0}\nip: {1}\nSomebody: {2}".format(mac, ip, somebody)
    else:
        suffix = "\n--来自数据分析组\nSomebody: {0}".format(somebody)
    return suffix


if __name__ == '__main__':
    pass
