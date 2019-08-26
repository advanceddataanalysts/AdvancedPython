#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-21 17:25
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : ding_robot.py
# @Software: PyCharm


import requests
from src.config import public_config
from src.utils.stringhelper import StringHelper


def dingdingrobot(content='', subject='test', title=''):
    suffix = StringHelper.get_alarm_suffix()

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


if __name__ == '__main__':
    pass
