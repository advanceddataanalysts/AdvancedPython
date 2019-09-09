#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/9 15:46
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : data_suit.py
# @Software: PyCharm

import os
import re
import json
import numpy as np
import pandas as pd
from src.utils import hflog
from sklearn import preprocessing
from src.utils.ML import model_suit
from src.config import public_config
from src.utils.mysqlhelper import MysqlHelper
from sklearn.model_selection import train_test_split


class data_suit(object):
    cur_time = public_config.cur_time

    @classmethod
    def data_load(cls, sql, data_saved=False):
        try:
            df = MysqlHelper().getdataframe(sql)
            if data_saved:
                cls.data_save(df, des="raw")
        except Exception as e:
            print(repr(e))
        return df

    @classmethod
    def data_transform(cls, df):
        pass

    @classmethod
    def data_split(cls, X, y, method={"test_size": 0.3, "random_state": 3}):

        data = {"update": cls.cur_time, "feature": X.columns.tolist()}
        json_str = json.dumps(data)
        hflog.info(json_str)

        X_train, X_test, y_train, y_test = train_test_split(X, y, **method)

        return X_train, X_test, y_train, y_test

    @classmethod
    def data_dictvectorizer(cls, df):
        df = df.astype("str")
        from sklearn.feature_extraction import DictVectorizer

        vec = DictVectorizer()
        trans_vec = vec.fit_transform(df.to_dict(orient="records")).toarray()
        df_dctvct = pd.DataFrame(trans_vec, columns=vec.get_feature_names())
        return df_dctvct

    @classmethod
    def data_preprocessing(cls, X_train, X_test, method={"StandardScaler": {}}):
        """
        使用l2范式，对特征列进行正则
        X_train = preprocessing.normalize(X_train, norm="l2", axis=0)
        """
        method_name = list(method.keys())[0]
        method_para = list(method.values())[0]

        if method_name == "StandardScaler":

            scaler = preprocessing.StandardScaler(**method_para)

        elif method_name == "MinMaxScaler":

            scaler = preprocessing.MinMaxScaler(**method_para)

        elif method_name == "normalize":

            scaler = preprocessing.Normalizer(**method_para)

        X_train_scaler = scaler.fit_transform(X_train)

        X_test_scaler = scaler.transform(X_test)

        model_suit.model_save(scaler, "{0}-{1}".format(method_name, public_config.cur_time))

        return X_train_scaler, X_test_scaler

    @classmethod
    def my_feature_selection(cls, cur_time, X_train, y_train, method={"SelectKBest": {}}):

        method_name = list(method.keys())[0]
        method_para = list(method.values())[0]

        if method_name == "StandardScaler":
            from sklearn.feature_selection import SelectKBest
            from sklearn.feature_selection import chi2

            data_new = SelectKBest(chi2, k=50).fit_transform(X_train, y_train)

        return X_train

    @classmethod
    def data_pca(
            cls,
            X_train,
            X_test,
            method={
                "n_components": None,
                "copy": True,
                "whiten": False,
                "svd_solver": "auto",
                "tol": 0.0,
                "iterated_power": "auto",
                "random_state": 3,
            },
    ):
        from sklearn.decomposition import PCA

        pca = PCA(**method)
        X_train_pca = pca.fit_transform(X_train)
        X_test_pca = pca.transform(X_test)
        model_suit.model_save(pca, "pca_{0}".format(cls.cur_time))

        return X_train_pca, X_test_pca

    @classmethod
    def data_merges(cls, *dfs, on=None, how="left"):
        if isinstance(on, str):
            on = [on]
        tb = dfs[0]
        tb[on] = tb[on].astype("str")
        for ele in on:
            tb[ele] = tb[ele].apply(lambda x: re.sub("\.0$", "", x))
        for df in dfs[1:]:
            df[on] = df[on].astype("str")
            for ele in on:
                df[ele] = df[ele].apply(lambda x: re.sub("\.0$", "", x))
            tb = pd.merge(tb, df, on=on, how=how)
        return tb

    @classmethod
    def data_value_counts_n(cls, df, col=None, n=1):

        df = df[col].value_counts().reset_index().rename(columns={"index": col, col: "{0}_count".format(col)})

        df = df[df["{0}_count".format(col)] > n]

        return df

    @classmethod
    def data_save_csv(cls, df, csv_name="untitled", method={"index": False, "encoding": "GB18030"}):
        data_saved_dir = os.path.join("data_saved/{0}_{1}".format(csv_name, cls.cur_time))
        try:
            if not os.path.exists(data_saved_dir):
                os.makedirs(data_saved_dir)
        except Exception as e:
            print(repr(e))

        fileabstractname = "./{0}/{1}_{2}.csv".format(data_saved_dir, csv_name, cls.cur_time)
        df = df.replace("\\n", ";", regex=True).replace("\\r", ";", regex=True).reset_index(drop=True)
        df.to_csv(fileabstractname, header=True, **method)

        return fileabstractname

    @classmethod
    def data_save_excel(cls, book_name, sheets_name, dfs):
        data_saved_dir = os.path.join("data_saved/{0}_{1}".format(book_name, cls.cur_time))
        try:
            if not os.path.exists(data_saved_dir):
                os.makedirs(data_saved_dir)
        except Exception as e:
            print(repr(e))

        fileabstractname = "./{0}/{1}_{2}.xlsx".format(data_saved_dir, book_name, cls.cur_time)
        writer = pd.ExcelWriter(fileabstractname)
        if not isinstance(dfs, list):
            dfs = [dfs]

        if isinstance(sheets_name, str):
            sheets_name = [sheets_name]

        for df, sheet_name in zip(dfs, sheets_name):
            if (
                    type(df.columns) == pd.core.indexes.multi.MultiIndex
                    or type(df.index) == pd.core.indexes.multi.MultiIndex
            ):
                df.to_excel(writer, sheet_name, index=True)
            else:
                df.to_excel(writer, sheet_name, index=False)
        writer.save()

        return fileabstractname

    @classmethod
    def to_html(cls, df):
        th = """"""
        for col in df.columns:
            th += "<th>" + col + "</th>"
        html = (
                """
            <table width="50%"; style="table-layout:auto;word-break:break-all;background:#f2f2f2">
            """
                + th
        )
        for i in range(df.shape[0]):
            if i % 2 == 0:
                html += '<tr class="bg">'
            else:
                html += "<tr>"

            for j in range(df.shape[1]):

                val = str((df.iloc[i, j]))
                if val.find("↑") != -1:
                    val = '<td align=center> <font color="red" style="font-weight:bold">' + val + "</font></td>"
                elif val.find("↓") != -1:
                    val = '<td align=center> <font color="green" style="font-weight:bold">' + val + "</font></td>"
                else:
                    val = "<td align=center>" + val + "</td>"
                html += val
            html += "</tr>"
        html += "</table>"

        html = (
                """
            <style>
            span {
                font-size: 19px
            }
            table,table tr , table tr td { border:1px solid #0094ff;} 
            table {border-collapse: collapse;}  
            .bg{background:#CCE8CF} 
            th {border-left: 1px solid #0094ff}
            </style>"""
                + html
        )
        return html

    @classmethod
    def to_html_table(cls, df, caption=None, annotate=None):
        style = """<style>
        /* grid */   
        table.grid {   
            font-family: verdana,arial,sans-serif;  
            font-size:11px;  
            color:#333333;  
            border-width: 1px;  
            border-color: #666666;  
            border-collapse: collapse;
            text-align: center;
            }
        table.grid caption {
            border-width: 1px;  
            padding: 8px;  
            border-style: solid;  
            border-color: #666666;  
            background-color: #dedede;  
            }         
        table.grid th {
            border-width: 1px;  
            padding: 8px;  
            border-style: solid;  
            border-color: #666666;  
            background-color: #dedede;  
            }  
        table.grid td {  
            border-width: 1px;  
            padding: 8px;  
            border-style: solid;  
            border-color: #666666;  
            background-color: #ffffff;
            }  
        /* /grid */
        </style>"""
        th = ""
        for col in df.columns:
            th += "<th>" + col + "</th>"
        if caption:
            caption = "<caption>{0}</caption>".format(caption)
            html = style + "<table class='grid'>" + caption + th
        else:
            html = style + "<table class='grid'>" + th
        for i in range(df.shape[0]):
            html += "<tr>"
            for j in range(df.shape[1]):
                html += """<td> """ + str((df.iloc[i, j])) + """</td>"""
            html += "</tr>"
        html += "</table>"

        if annotate:
            html += "<br>" + "<p style='font-size:8px;'>" + annotate + "</p>"
        return html

    @classmethod
    def re_group_concat(cls, df, unique_col, gp_concat_col):

        if isinstance(unique_col, str):
            unique_col = [unique_col]

        df.loc[df[gp_concat_col].isnull(), gp_concat_col] = ""

        expand = df[gp_concat_col].str.split(",", expand=True).reset_index(drop=True)

        expand = pd.concat([df[unique_col].reset_index(drop=True), expand], axis=1)

        expand = expand.set_index(unique_col).stack().reset_index().rename(columns={0: gp_concat_col})

        col = expand.columns[expand.columns.str.contains("level_")]

        expand = expand.drop(col, axis=1)

        expand.loc[expand[gp_concat_col] == "", gp_concat_col] = np.nan

        return expand

    @classmethod
    def group_concat(cls, df, unique_col, gp_concat_col, separator=","):

        rst = df.groupby([unique_col])[gp_concat_col].apply(lambda x: separator.join(x)).reset_index()

        return rst

    @classmethod
    def get_pid_list(cls, df, id):

        df["id"] = df["id"].astype("int")
        df["pid"] = df["pid"].astype("int")

        tmp_df = df[df["id"] == int(id)]

        if tmp_df.empty or tmp_df["pid"].values[0] is None:
            return pd.DataFrame()
        else:
            return cls.get_pid_list(df, tmp_df["pid"].values[0]).append(tmp_df)

    @classmethod
    def get_pid_expand(cls, df, col, concat=True):

        id_list = df["id"].values

        big_list = []
        for i in id_list:
            pid_list = cls.get_pid_list(df, i)[col].values.tolist()
            big_list.append(pid_list)

        df["pid_list"] = big_list

        df["pid_len"] = df["pid_list"].apply(lambda x: len(x))

        df["pid_list"] = df["pid_list"].apply(lambda x: ",".join([str(i) for i in x]))

        df_expand = df["pid_list"].str.split(",", expand=True)

        for ele in df_expand.columns:
            df_expand = df_expand.rename(columns={ele: cls.number_to_name(ele + 1) + "_level"})

        if concat:
            rst = pd.concat([df, df_expand], axis=1)
            return rst
        else:
            return df_expand

    @classmethod
    def number_to_name(cls, number):

        numbers = {}
        numbers[0] = "zeroth"
        numbers[1] = "first"
        numbers[2] = "second"
        numbers[3] = "third"
        numbers[4] = "fourth"
        numbers[5] = "fifth"
        numbers[6] = "sixth"
        numbers[7] = "seventh"
        numbers[8] = "eighth"
        numbers[9] = "ninth"
        numbers[10] = "tenth"
        numbers[11] = "eleventh"
        numbers[12] = "twelfth"
        numbers[13] = "thirteenth"
        numbers[14] = "fourteenth"

        return numbers[number]
