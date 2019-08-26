#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-21 15:30
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : get_source.py
# @Software: PyCharm

import uuid
import socket


def get_source():
    """获取执行脚本机器的MAC地址"""
    seriers = uuid.UUID(int=uuid.getnode()).hex[-12:]
    mac = ":".join([seriers[e:e + 2] for e in range(0, 11, 2)])

    """获取执行脚本机器的电脑名"""
    # myname = socket.getfqdn(socket.gethostname())

    """获取执行脚本机器的IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    ips = {'10.51.12.65': '闫洋龙', }
    if ip in ips:
        somebody = ips[ip]
    else:
        somebody = 'unknown'
    return mac, ip, somebody


if __name__ == '__main__':
    print(get_source())
