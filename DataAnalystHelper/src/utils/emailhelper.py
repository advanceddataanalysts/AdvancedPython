#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-22 19:27
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : emailhelper.py
# @Software: PyCharm


import os
import time
import socket
import smtplib
from src.config import config
from email.header import Header
from email.mime.text import MIMEText
from src.utils import encryption
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from src.utils.ding_robot import dingdingrobot
from src.utils.mysqlhelper import MysqlHelper
from src.utils.rander_template import render_template
from src.utils.to_io import to_io

count_times = 0
n = config.try_rerun_email_n
sleep_time = config.try_rerun_email_sleep

socket.setdefaulttimeout(30)

while count_times < n:
    try:
        socket.setdefaulttimeout(30)
        count_times = n
    except:
        count_times += 1
        if time.localtime()[3] > 7:
            time.sleep(5)
            if count_times > 3:
                count_times = n
        else:
            time.sleep(sleep_time)

        if count_times >= n:
            raise Exception("socket超时连接")

encryption_instance = encryption.Encryption()
emailsetting = config.emailsetting_data

host = emailsetting["host"]
user = emailsetting["user"]
password = emailsetting["password"]
sender = emailsetting["sender"]


class EmailHelper(object):

    def __init__(self, host=host, user=user, password=password, sender=sender):

        # 第三方 SMTP 服务
        self.mail_host = encryption_instance.decrypt(host)
        self.mail_user = encryption_instance.decrypt(user)
        self.mail_pass = encryption_instance.decrypt(password)
        self.sender = encryption_instance.decrypt(sender)

    def heads(self, html, subject, receivers, cc_recivers=None, file_names=None, io_data=None):
        message = MIMEMultipart()
        message['From'] = Header(self.sender)
        message['To'] = Header(';'.join(receivers))
        if cc_recivers:
            message['Cc'] = Header(';'.join(cc_recivers))
        message['Subject'] = Header(subject, 'utf-8')

        content = MIMEText(html, 'html', 'utf-8')
        """为邮件添加正文(HTML)"""
        message.attach(content)

        if file_names:
            """为邮件添加附件(file_names为列表,可发多个附件)"""
            for file_name in file_names:
                attatchment = MIMEApplication(open(file_name, 'rb').read())

                attatchment["Content-Type"] = 'application/octet-stream'
                """为请求到服务器的流文件设置接收头, SMTP协议的`Content-Type`为`application/octet-stream`时以二进制流读取,不知道下载文件类型

                filename 为对方接收的文件名,写什么就是什么,此为`file_name文件名`
                """
                attatchment.add_header('Content-Disposition', 'attachment',
                                       filename=('gbk', '', file_name.split("/")[-1]))
                message.attach(attatchment)

        if io_data:
            """将文件以字节流的形式发送(无需保存文件),并为文件添加后缀为.csv/.xlsx"""

            if isinstance(io_data, str):
                suffix = ".csv"
                io_data.encode('GB18030')

            else:
                suffix = ".xlsx"
            print("所发送邮件的后缀为: ", suffix)

            attatchment = MIMEApplication(io_data)

            attatchment["Content-Type"] = 'application/octet-stream'

            """filename 为对方接收的文件名,写什么就是什么,此为`主题+当前时间+Excel.后缀`"""
            attatchment.add_header('Content-Disposition', 'attachment',
                                   filename=('gbk', '', subject + config.cur_time + suffix))
            message.attach(attatchment)

        return message

    def send(self, subject, receivers, cc_recivers=None, file_names=None, io_data=None, html=None):

        email_test_instance = config.testing_email
        print(config.testing_email)
        """导入配置文件中的个人邮箱进行测试"""

        if email_test_instance:
            receivers = config.testing_email
            subject = "测试邮件--" + subject
        else:
            receivers = self.suffix(receivers)
            receivers.append("yanglong_yan@163.com")
            if cc_recivers:
                cc_recivers = self.suffix(cc_recivers)
        print(receivers)

        if not html:
            """判断是否有自定义HTML,没有则使用模板HTML发送正文"""
            html = render_template("table.html", greeting=subject + "数据详情请见附件")

        message = self.heads(html, subject, receivers, cc_recivers, file_names, io_data)
        smtpObj = smtplib.SMTP()
        smtpObj.connect(self.mail_host, 25, )  # 25 为 SMTP 端口号
        smtpObj.login(self.mail_user, self.mail_pass)

        try:
            to_addrs = receivers
            if cc_recivers:
                to_addrs = to_addrs + cc_recivers
            smtpObj.sendmail(self.sender, to_addrs, msg=message.as_string())
            if file_names:
                if not isinstance(file_names, list):
                    file_names = [file_names]
                for file_name in file_names:
                    os.remove(file_name)
            print("mail推送成功")

        except Exception as e:
            print(repr(e))
            error_content = repr(e).replace("\\n", " ").replace("\\", " ").replace("\\t", " ")
            dingdingrobot(content=subject + "\n" + error_content, subject="alarm")
            raise Exception("邮件发送异常,来自emailhelper;")

    def send_sqltoexcel(self, subject, receivers, cc_recivers=None, sqls=None, sql_filenames=None, sheets_name=None,
                        db=config.along_localhost, html=None):

        mysqlinstance = MysqlHelper(**db)

        if sql_filenames:
            """判断是否读取SQL附件"""
            if isinstance(sql_filenames, str):
                dfs = mysqlinstance.get_df_loadfile(sql_filenames)
            else:
                dfs = mysqlinstance.get_df_loadfile(*sql_filenames)
        else:
            if isinstance(sqls, str):
                dfs = mysqlinstance.get_df(sqls)
            else:
                dfs = mysqlinstance.get_df(*sqls)

        if sheets_name:
            if isinstance(sheets_name, str):
                sheets_name = [sheets_name]
        else:
            sheets_name = [subject]

        if not isinstance(dfs, list):
            dfs = [dfs]

        not_null = 0
        for df in dfs:
            if df.shape[0] == 0:
                not_null += 1

        if not_null == len(dfs):
            self.send(subject, receivers, html="今日无数据")
        else:
            io_data = to_io(*dfs, sheets_name=sheets_name)
            self.send(subject=subject, receivers=receivers, cc_recivers=cc_recivers, io_data=io_data, html=html)

    def send_dftoexcel(self, subject, receivers, cc_recivers=None, dfs=None, sheets_name=None, html=None):

        if not isinstance(receivers, dict):
            if sheets_name:
                if isinstance(sheets_name, str):
                    sheets_name = [sheets_name]
            else:
                sheets_name = [subject]

            if not isinstance(dfs, list):
                dfs = [dfs]

            io_data = to_io(*dfs, sheets_name=sheets_name)
            self.send(subject=subject, receivers=receivers, cc_recivers=cc_recivers, io_data=io_data, html=html)
        else:
            if cc_recivers is None:
                cc_recivers = {i: None for i in range(len(receivers))}

            if html is None:
                html = {i: None for i in range(len(receivers))}

            receivers_dict = receivers
            cc_recivers_dict = cc_recivers
            dfs_dict = dfs
            sheets_name_dict = sheets_name
            html_dict = html
            for receivers, cc_recivers, dfs, sheets_name, html in list(
                    zip(receivers_dict.values(), cc_recivers_dict.values(), dfs_dict.values(),
                        sheets_name_dict.values(), html_dict.values())):
                io_data = to_io(*dfs, sheets_name=sheets_name)

                self.send(subject=subject, receivers=receivers, cc_recivers=cc_recivers, io_data=io_data, html=html)

    def send_dftocsv(self, subject, receivers, cc_recivers=None, df=None, html=None):
        """csv文件只能有一个sheet,因此不需要多做判断"""

        io_data = to_io(df, save_type="csv")

        self.send(subject=subject, receivers=receivers, cc_recivers=cc_recivers, io_data=io_data, html=html)

    def suffix(self, receivers_list):
        """维护收件人为列表,自动为无@163.com的邮箱添加后缀"""
        eles = []
        for ele in receivers_list:
            if ele.find("@") == -1:
                ele = ele + "@163.com"
            eles.append(ele)
        return eles
