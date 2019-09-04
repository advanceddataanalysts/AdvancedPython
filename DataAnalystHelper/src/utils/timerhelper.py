#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 20:06
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : timerhelper.py
# @Software: PyCharm


import os
import re
import time
import pandas as pd
from datetime import datetime, timedelta
from src.config import config, public_config
from src.utils.mysqlhelper import MysqlHelper
from src.utils.ding_robot import dingdingrobot
from src.utils.stringhelper import StringHelper
from src.utils.verify_crontab import get_next_time

public_config.email_test = False
file_path = os.path.dirname(os.path.realpath(__file__))
mysqlinstance_dmart_dmart = MysqlHelper(**config.dmart_dmart)

tdy = datetime.now().strftime('%Y-%m-%d')
tomorrow = (datetime.now() - timedelta(days=-1)).strftime('%Y-%m-%d')


class TimerHelper(object):
    def __init__(self):

        self.next_run_time = tomorrow
        self.guandata_uuid_list = []
        self.num = 0
        self.level = 1

    def load_df(self, id):

        """
        以任务id查询dmart.ipreject库获取任务基本信息
        :param id: 任务id或者任务的文件名
        :return: 返回任务基本信息的df
        """

        print("开始获取脚本参数——————————————————————————：")
        print(id)

        sql = """
        select 
            id,
            crontab,
            crontab_desc,
            is_delete,
            author,
            author_email,
            syn_task,
            sub_task,
            file_basename,
            model,
            case when id != 339 then guandata_uuid end guandata_uuid,
            ifnull(next_run_time,str_to_date('1970-01-01 00:00:00','%Y-%m-%d %H:%i:%s')) next_run_time
        from 
            iproject.will_timer_task
        where {0}
    """

        if re.search(r"\D", str(id)) is None:

            sql = sql.format("id = {0}".format(id))

        else:

            sql = sql.format("file_basename = '{0}'".format(id))

        df = mysqlinstance_dmart_dmart.get_df(sql)

        return df

    def run(self, id, only=False):

        """
        加载数据，执行任务
        :param id: 传入任务id或者任务文件名
        :param only: 是否调用并行任务或者子任务
        :return:
        """

        print(f"----****----****----****开始执行任务id：{id};****----****----****----")

        df = self.load_df(id)

        if df["is_delete"][0] == 0:

            run_status = self.start(
                df["model"][0], df["file_basename"][0], df["crontab"][0], df["guandata_uuid"][0],
                df["next_run_time"][0])

            if not only:
                syn_task_str = self.string_clean(df["syn_task"][0])
                if syn_task_str:
                    self.check_appendix_task(syn_task_str)

                sub_task_str = self.string_clean(df["sub_task"][0])
                if run_status == 1:
                    if sub_task_str:
                        self.check_appendix_task(sub_task_str)

        else:
            dingdingrobot(content=df["file_basename"][0] + "\n已经假删除；", subject="test")

    def check_appendix_task(self, task_str):

        """
        检查是否有并行或者子任务存在
        :param task_str: 并行或者子任务描述
        :return:
        """

        task_list = task_str.split(",")

        for sub_id in task_list:
            self.num += 1
            self.run(sub_id)
            self.num -= 1

    def start(self, model, file_basename, crontab, guandata_uuid_str, next_run_time):

        """
        调度脚本
        :param model: 任务的模块归属，目前有任务迁移模块，邮件模块，和通知模块
        :param file_basename: 文件名
        :param crontab: 定时器
        :param guandata_uuid_str: 观远id集合
        :param next_run_time: 脚本下次执行时间
        :return: 返回任务执行的结果状态
        """

        import runpy

        startTime = time.time()
        try:
            # 开始执行脚本
            runpy.run_path(
                file_path.replace("utils", "") + "/" + model + "/" + file_basename + ".py", run_name="__main__")

            guandata_uuid_str = self.string_clean(guandata_uuid_str)
            if guandata_uuid_str:
                guandata_uuid_list = guandata_uuid_str.split(",")
                self.guandata_uuid_list.extend(guandata_uuid_list)
            run_status = 1

        except Exception as e:
            print('timerhelper error execute:')
            content = repr(e)
            error_content = StringHelper.str_cut(content)
            print(error_content)

            dingdingrobot(content=f'{file_basename} \n运行失败：{error_content}', subject="test")
            run_status = 0

        endTime = time.time()
        time_eclipse = round((endTime - startTime), 2)

        startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime))
        endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endTime))

        if crontab:
            self.next_run_time = get_next_time(crontab)

        self.maintain_job_check(crontab, file_basename, startTime, endTime, time_eclipse, run_status, next_run_time)

        return run_status

    def maintain_job_check(self, crontab, file_basename, startTime, endTime, time_eclipse, run_status, next_run_time):

        """
        维护任务的反馈结果

        :param crontab:
        :param file_basename:
        :param startTime: 脚本开始执行时间
        :param endTime: 脚本结束执行时间
        :param time_eclipse: 脚本执行耗时
        :param run_status: 脚本的执行结果状态
        :param next_run_time: 脚本下次执行时间
        :return:
        """

        is_update = self.check_update_time(file_basename)

        if run_status == 1:
            if (
                    (not is_update)
                    or (is_update and (not crontab) and (next_run_time < tdy))
                    or (is_update and crontab and self.next_run_time != next_run_time)
                    or (file_basename == "will_check_timer_job")):
                print("刷新下次启动时间——————————————————————————：")
                sql = f"""
                update iproject.will_timer_task set next_run_time = '{self.next_run_time}', start_time = time('{startTime}'),elapse = '{time_eclipse}' where file_basename = '{file_basename}';
                """
                print(sql)

                self.sql_execute(sql)

        print("增加运行状况和用时——————————————————————————：")
        sql = f"""
        insert into iproject.will_timer_task_check (file_basename,start_time,end_time,elapse,run_status) VALUES('{file_basename}','{startTime}','{endTime}',{time_eclipse},{run_status})
        """

        self.sql_execute(sql)

    @staticmethod
    def sql_clean(sql):
        sql = sql.replace('"', "'").replace("'None'", "null")
        return sql

    @staticmethod
    def string_clean(content):
        if content:
            content = content.replace("，", "").strip()
        return content

    def sql_execute(self, sql):

        sql = self.sql_clean(sql)

        mysqlinstance_dmart_dmart.execute(sql)

    @staticmethod
    def check_update_time(file_basename):

        """
        检查脚本当日是否已经执行
        :param file_basename: 传入文件名
        :return: 返回True or False
        """
        print("检查脚本当日是否已经执行check_update_time")
        sql = """
        select  
            *
        from 
            iproject.will_timer_task
        where file_basename = '{0}' and update_time > current_date()
        """

        sql = sql.format(file_basename)

        df = mysqlinstance_dmart_dmart.get_df(sql)

        if df.shape[0] > 0:
            return True
        else:
            return False

    def parse_taks_level(self, df):

        df = df[(df["syn_task"].notnull()) | (df["sub_task"].notnull())]

        if df.shape[0] == 0:
            return pd.DataFrame()

        else:

            syn_tb = pd.DataFrame()
            sub_tb = pd.DataFrame()
            tb = pd.DataFrame()

            for i, x in df.iterrows():

                if x["syn_task"]:
                    sql = f"""
                        select 
                            id,
                            crontab,
                            crontab_desc,
                            is_delete,
                            syn_task,
                            sub_task
                        from 
                            iproject.will_timer_task
                        where id in ({x["syn_task"]})
                        """

                    syn_task = mysqlinstance_dmart_dmart.get_df(sql)
                    syn_tb = pd.concat([syn_tb, syn_task], axis=0)

                if x["sub_task"]:
                    sql = f"""
                        select 
                            id,
                            crontab,
                            crontab_desc,
                            is_delete,
                            syn_task,
                            sub_task
                        from 
                            iproject.will_timer_task
                        where id in ({x["sub_task"]})
                        """

                    sub_task = mysqlinstance_dmart_dmart.get_df(sql)
                    sub_tb = pd.concat([sub_tb, sub_task], axis=0)

            if syn_tb.shape[0] > 0:
                syn_tb["level"] = self.level
                syn_tb = syn_tb[["id", "crontab", "crontab_desc", "is_delete", "sub_task", "syn_task", "level"]]

            if sub_tb.shape[0] > 0:
                self.level = self.level + 1
                sub_tb["level"] = self.level
                sub_tb = sub_tb[["id", "crontab", "crontab_desc", "is_delete", "sub_task", "syn_task", "level"]]

            tb = pd.concat([syn_tb, sub_tb], axis=0)

            return self.parse_taks_level(tb).append(tb)

    def get_pid(self, df):

        pass


if __name__ == "__main__":
    # 参数可以传入int类型的id  /  str的 file_basename
    TimerHelper().run(1, only=False)
