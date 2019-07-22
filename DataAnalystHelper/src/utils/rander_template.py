#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-7-22 17:35
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : rander_template.py
# @Software: PyCharm

import os
import jinja2
import pandas as pd

fath_path = os.path.abspath(os.path.join(os.getcwd(), '../'))


def render_template(template_name, **context):
    """使用JinJa2模板渲染引擎渲染发送邮件的正文"""

    if "df" not in context:
        """正文中添加DataFrame"""
        context["df"] = pd.DataFrame()

    TemplateLoader = jinja2.FileSystemLoader(fath_path + '/templates')
    TemplateEnv = jinja2.Environment(loader=TemplateLoader)
    template = TemplateEnv.get_template(template_name)
    return template.render(**context)


if __name__ == '__main__':
    pass
