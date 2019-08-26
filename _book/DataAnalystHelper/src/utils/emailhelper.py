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
import zipfile
from email.header import Header
from src.utils.encryption import Encryption
from src.utils.to_io import to_io
from email.mime.text import MIMEText
from src.utils.try_rerun import try_rerun
from src.config import config, public_config
from src.utils.mysqlhelper import MysqlHelper
from src.utils.ding_robot import dingdingrobot
from email.mime.multipart import MIMEMultipart
from src.utils.stringhelper import StringHelper
from email.mime.application import MIMEApplication
from src.utils.rander_template import render_template

n = config.try_rerun_email_n
sleep_time = config.try_rerun_email_sleep

socket.setdefaulttimeout(300)

encryption_instance = Encryption()
emailsetting = config.emailsetting_data

host = emailsetting["host"]
user = emailsetting["user"]
password = emailsetting["password"]
sender = emailsetting["sender"]


class EmailHelper(object):
    def __init__(self, host=host, user=user, password=password):
        """第三方 SMTP 服务"""
        self.mail_host = encryption_instance.decrypt(host)
        self.mail_user = encryption_instance.decrypt(user)
        self.mail_pass = encryption_instance.decrypt(password)

    @try_rerun(dingding=True, n=n, sleep_time=sleep_time)
    def send(self, message):
        smtpObj = smtplib.SMTP()
        """25 为 SMTP 端口号"""
        smtpObj.connect(self.mail_host, 25)
        smtpObj.login(self.mail_user, self.mail_pass)
        smtpObj.sendmail(message.sender, message.send_to, msg=message.as_string())
        smtpObj.quit()
        print("mail推送成功")


class EmailMessage(object):

    def __init__(self, subject='', receivers=None, cc_receivers=None, html=None, sqls=None, sql_filenames=None,
                 dfs=None, filename=None, book_name=None, sheets_name=None, db=config.along_localhost, save_type="xlsx"):

        self.sender = encryption_instance.decrypt(sender)

        self.subject = subject
        self.receivers = StringHelper.to_list(receivers)
        self.cc_receivers = StringHelper.to_list(cc_receivers)
        self.html = html
        if not self.html:
            """判断是否有自定义HTML,没有则使用模板HTML发送正文"""
            self.html = render_template("table.html", greeting=self.subject + "数据详情请见附件")

        self.dfs = StringHelper.to_list(dfs)
        self.sqls = StringHelper.to_list(sqls)
        self.sql_filenames = StringHelper.to_list(sql_filenames)
        self.db = db
        self.filename = StringHelper.to_list(filename)
        if book_name:
            self.book_name = book_name
        else:
            self.book_name = self.subject
        self.sheets_name = StringHelper.to_list(sheets_name)
        self.save_type = save_type

        self.msg = self._message()

    @property
    def send_to(self):

        __send_to = list(set(self.receivers) | set(self.cc_receivers or ()))

        """验证收件人是否有效的处理逻辑"""
        # from src.config import public_config
        # email_test_instance = public_config.email_test
        # if not email_test_instance:
        #     pass
        return __send_to

    def as_string(self):
        return self.msg.as_string()

    def _message(self):

        """判断是否测试环境"""
        self.is_test()

        message = MIMEMultipart()
        message["From"] = Header(self.sender)
        message["To"] = Header(";".join(self.receivers))
        if self.cc_receivers:
            message["Cc"] = Header(";".join(self.cc_receivers))
        message["Subject"] = Header(self.subject, "utf-8")

        content = MIMEText(self.html, "html", "utf-8")
        """为邮件添加正文(HTML)"""
        message.attach(content)

        if len(self.dfs + self.sqls + self.sql_filenames) > 0:
            att = Attachment(sqls=self.sqls, sql_filenames=self.sql_filenames, dfs=self.dfs,
                             filename=self.filename,
                             book_name=self.book_name, sheets_name=self.sheets_name,
                             db=self.db,
                             save_type=self.save_type)
            message.attach(att._attachment())

        return message

    def add_attachment(self, **kwargs):
        if not kwargs["book_name"]:
            kwargs["book_name"] = self.subject
        att = Attachment(**kwargs)
        self.msg.attach(att._attachment())

    def is_test(self):

        from src.config import public_config
        email_test_instance = public_config.email_test
        print("是否测试：{0}".format(public_config.email_test))

        """导入配置文件中的个人邮箱进行测试"""
        if email_test_instance:
            self.receivers = config.testing_email
            self.cc_receivers = []
            self.subject = "测试邮件--" + self.subject
        else:
            self.receivers.append("yanglong_yan@163.com")

        print("emailhelper.send收件人:")
        print(self.receivers)


class Attachment(object):

    def __init__(self, sqls=None, sql_filenames=None, dfs=None, filename=None, book_name=None, sheets_name=None,
                 db=config.along_localhost, save_type="xlsx"):

        if (dfs or sqls or sql_filenames) is not None:
            if dfs:
                self.dfs = StringHelper.to_list(dfs)
            else:
                self.sqls = StringHelper.to_list(sqls)
                self.sql_filenames = StringHelper.to_list(sql_filenames)
                self.db = db
                self.dfs = StringHelper.to_list(self.load_df())

        self.filename = StringHelper.to_list(filename)
        self.book_name = book_name
        self.sheets_name = StringHelper.to_list(sheets_name)
        if not self.sheets_name:
            self.sheets_name = ["data"]
        self.save_type = save_type

    def _attachment(self):

        if self.save_type != "zip":
            io_data = to_io(*self.dfs, sheets_name=self.sheets_name, save_type=self.save_type)

            """将文件以字节流的形式发送(无需保存文件),并为文件添加后缀为.csv/.xlsx"""
            if isinstance(io_data, str):
                suffix = ".csv"
                self.io_data.encode("GB18030")
            else:
                suffix = ".xlsx"
            print("所发送邮件的后缀为: ", suffix)

            file_name = self.book_name + public_config.cur_time + suffix

        else:

            from ML import data_suit

            if len(self.dfs) == 1:
                xl_fileabstractname = data_suit.data_save_csv(df=self.dfs[0], csv_name=self.book_name)
            else:
                xl_fileabstractname = data_suit.data_save_excel(dfs=self.dfs, book_name=self.book_name,
                                                                sheets_name=self.sheets_name)

            xl_file_basename = os.path.basename(xl_fileabstractname)
            father_path = os.path.abspath(os.path.dirname(xl_fileabstractname))
            zip_fileabstractname = xl_fileabstractname.replace("xlsx", "zip").replace("csv", "zip")
            with zipfile.ZipFile(zip_fileabstractname, "w", zipfile.zlib.DEFLATED) as zf:
                zf.write(xl_fileabstractname, xl_file_basename)
            with open(zip_fileabstractname, "rb") as f:
                io_data = f.read()
            file_name = os.path.basename(zip_fileabstractname)

            """删除创建的文件和路径"""
            os.remove(xl_fileabstractname)
            os.remove(zip_fileabstractname)
            os.rmdir(father_path)

        attatchment = MIMEApplication(io_data)
        attatchment["Content-Type"] = "application/octet-stream"
        attatchment.add_header("Content-Disposition", "attachment", filename=("gbk", "", file_name))

        return attatchment

    def load_df(self):

        mysqlinstance = MysqlHelper(**self.db)

        if self.sql_filenames:
            """判断是否读取SQL附件"""
            dfs = mysqlinstance.get_df_loadfile(*self.sql_filenames)
        else:
            dfs = mysqlinstance.get_df(*self.sqls)

        return dfs


if __name__ == '__main__':
    pass
