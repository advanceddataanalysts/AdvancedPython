#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 20:06
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : app.py
# @Software: PyCharm

import sys
import warnings
from src.utils.timerhelper import TimerHelper

warnings.filterwarnings("ignore")

if __name__ == '__main__':
    id = sys.argv[1]
    app = TimerHelper()
    app.run(id)
