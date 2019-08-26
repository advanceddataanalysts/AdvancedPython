#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 18:48
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : sql_format.py
# @Software: PyCharm

# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 19:29
# @Author  : Will
# @Email   : 864311352@qq.com
# @File    : sql_format.py
# @Software: PyCharm

import re
import math
import sqlparse


def clean_sql(sql):
    sql = re.sub(r"\s+", " ", sql).strip()
    return sql


def in_format(content):
    for ele in re.finditer(r'(\sin\s*\()(\s*.*,)*(\s*.*\))', content, flags=re.IGNORECASE):

        if ele.group().find("from") == -1:
            content = content.replace(ele.group(), re.sub(r"[\n\t]", "", ele.group()))

    return content


def rank_format(sql):
    sql = re.sub(r"\(\),\s*over", "() over", sql, flags=re.IGNORECASE)

    return sql


def extract_format(sql):
    for ele in re.finditer(r"EXTRACT\(.*\s*from", sql, flags=re.IGNORECASE):
        sql = sql.replace(ele.group(), re.sub(r"[\n\t]", "", ele.group()).replace("from", " from"))

    return sql


def case_format(content):
    left_n = 0
    right_n = 0
    content_len = len(content)
    start_pos = content.find("case")

    for n in range(start_pos, content_len):
        if content[n:n + 4] == "case":
            left_n += 1
        if content[n:n + 3] == "end":
            right_n -= 1
        if (left_n > 0) and (left_n + right_n == 0):
            case_end = content[start_pos:n + 3]

            case_end_f = sqlparse.format(case_end, reindent=True, indent_tabs=True, keyword_case='lower')

            content = content.replace(case_end, case_end_f)

            left_n = 0
            right_n = 0
            start_pos = n + 3
            content = content.replace(content[n + 3:], case_format(content[n + 3:]))

    return content


def select_from_split(sql):
    select_n = 0
    from_n = 0
    sql_len = len(sql)
    start_pos = sql.find("select")
    for n in range(start_pos, sql_len):

        if sql[n:n + 6] == "select" or sql[n:n + 7] == "EXTRACT":
            select_n += 1
        if sql[n:n + 4] == "from":
            from_n -= 1
        if (select_n > 0) and (select_n + from_n == 0):
            select = sql[:start_pos + 6]
            body = sql[start_pos + 6:n]
            tail = sql[n:]

            sql = sql.replace(body, '\n' + body_format(body))
            sql = sql.replace(tail, tail_format(tail))

            return sql
    else:

        return sql


def add_tab(lines):
    lines_format = []

    for row, line in enumerate(lines.split("\n")):

        if line.find("\t") < 4:

            if line.count("\t") == 3:
                line = line.replace("\t\t\t", "\t", 1)
            elif line.count("\t") == 2:
                line = line.replace("\t\t", "\t", 1)
            elif line.count("\t") == 1:
                line = line
            else:
                n = math.floor((line.count("\t")) / 4)

                if n < 3:
                    line = "\t" * (n + 1) + line.strip()
                elif n == 3:
                    line = "\t" * (3) + line.strip()
                else:

                    line = "\t" * (n - 2) + line.replace("\t\t\t\t", "", n)

        else:
            line = "\t" + line
        lines_format.append(line)

    if len(lines.split("\n")) == 1:
        lines = "\n".join(lines_format)
    else:
        lines = "\n" + "\n".join(lines_format)
    return lines


def body_format(body):
    body = "\t" + body.lstrip()

    body = case_format(body)

    body = add_tab(body)

    return body + "\n"


def tail_format(tail):
    contents = []

    for row, line in enumerate(tail.split("\n")):

        if line.count("\t") > 1:
            n = math.ceil((line.count("\t")) / 2)

            line = line.replace("\t", "", n)

        contents.append(line)

    tail = "\n".join(contents)

    return tail


def brackets_format(sql):
    for ele in re.finditer(r"^ \)", sql, re.M):
        sql = sql.replace(ele.group(), "\t)")

    return sql


def to_format(lines):
    lines = sqlparse.format(lines, reindent=True, indent_tabs=True, keyword_case='lower')

    sql = select_from_split(lines)
    sql = in_format(sql)
    sql = rank_format(sql)
    sql = extract_format(sql)
    sql = brackets_format(sql)

    return sql


if __name__ == '__main__':
    lines = '''
    select * from subject 
    '''

    print(to_format(lines))
