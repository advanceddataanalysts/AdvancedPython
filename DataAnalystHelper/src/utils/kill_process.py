#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-21 17:19
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : kill_process.py
# @Software: PyCharm


import os
import signal
import psutil
import datetime
import pandas as pd
from tabulate import tabulate

from src.utils.ding_robot import dingdingrobot


def get_pids():
    pids = psutil.pids()

    ps_pids = []
    ps_cwd = []
    ps_exe = []
    ps_create_time = []
    for pid in pids:
        try:
            p = psutil.Process(pid)
            ps_pid = p.ppid()
            cwd = p.cwd()
            exe = p.exe()
            create_time = p.create_time()

        except Exception as e:
            ps_pid = 'null'
            cwd = 'null'
            exe = 'null'
            create_time = 'null'
        finally:

            ps_pids.append(ps_pid)
            ps_cwd.append(cwd)
            ps_exe.append(exe)
            ps_create_time.append(create_time)

    dic = {'ps_pids': ps_pids, 'ps_cwd': ps_cwd, 'ps_exe': ps_exe, 'ps_create_time': ps_create_time}
    df = pd.DataFrame(dic)
    df = df[df['ps_exe'].apply(lambda x: 'python' in x)].reset_index(drop=True)
    df['ps_create_time'] = df['ps_create_time'].apply(lambda x: datetime.datetime.fromtimestamp(x).strftime("%H%M"))

    df['local_time'] = datetime.datetime.now().strftime("%H%M")
    df['second_shift'] = df['local_time'].astype(int) - df['ps_create_time'].astype(int)
    # 将进程时间过长(超过四小时小于八小时)的进程筛选出来
    df = df[(df['second_shift'] > 60 * 4) & (df['second_shift'] < 60 * 8)]

    return df


def kill_main():
    df = get_pids()
    kill_pids = tuple(df['ps_pids'])
    print(df)
    if kill_pids:
        kill_data = tabulate(df.values, headers=df.columns, tablefmt="simple")
        dingdingrobot(subject="test", title='进程监测', content=kill_data)
        """
        杀死进程
        """
        # for i in kill_pids:
        #     os.kill(i, signal.SIGKILL)


if __name__ == '__main__':
    kill_main()
