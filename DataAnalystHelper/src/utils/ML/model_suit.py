#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/9 15:48
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : model_suit.py
# @Software: PyCharm

import os
import re
import io
import json
import prettytable
import pandas as pd
from src.utils import hflog
from src.utils.ML import plot_suit
from sklearn.externals import joblib
from src.config import public_config
from src.utils.ding_robot import dingdingrobot
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, roc_curve, auc


class model_suit(object):

    def __init__(self, dingding=True, log=True, img_saved=True):

        self.dingding = dingding
        self.log = log
        self.img_saved = img_saved
        self.cur_time = public_config.cur_time

    def model_train(self, X_train, y_train, model, method={}):

        model_name = str(model).split("(")[0]
        if method != {}:
            model = self.model_gscv(X_train, y_train, model, method)
        else:
            model.fit(X_train, y_train)
        self.model_save(model, filename=model_name + "_" + self.cur_time)

        if self.dingding:
            dingdingrobot(content="当前时间" + self.cur_time)
            dingdingrobot(model_name + "\n" + re.sub(r'\s+', "", str(model)))
        if self.log:
            data = {}
            data["update"] = self.cur_time
            data["model"] = re.sub(r'\s+', "", str(model))
            json_str = json.dumps(data)
            hflog.info(json_str)
        pred_y = model.predict(X_train)
        self.model_evaluate(y_train, pred_y, des=model_name + "_" + "train")

        return model

    def model_gscv(self, X_train, y_train, model, method={}):
        grid_obj = GridSearchCV(model, **method)
        grid_obj.fit(X_train, y_train)
        print('The parameters of the best model are: ')
        print(grid_obj.best_params_)
        model = grid_obj.best_estimator_
        return model

    def model_test(self, model, X_test, y_test):
        try:
            model_name = str(model).split("(")[0]
        except Exception as e:
            model_name = str(model)
        pred_y = model.predict(X_test)

        self.model_evaluate(y_test, pred_y, des=model_name + "_" + "test")

    def model_evaluate(self, y, pred_y, des="train"):
        try:
            p, n = y.value_counts()
            print("{0}正负样本比:{1}:{2}".format(des, n, p))
        except Exception as e:
            pass

        """获得混淆矩阵"""
        conf_m = confusion_matrix(y, pred_y)
        conf_m_df = pd.DataFrame(conf_m, columns=["pred_0", "pred_1"], index=["true_0", "true_1"]).reset_index()
        plot_suit.plot_matrix(conf_m_df.set_index(["index"]), title="{0}_confusion_matrix".format(des))
        confusion_matrix_table = self.pretty_tabel(conf_m_df)
        print('{0}-confusion matrix'.format(des))
        print(confusion_matrix_table)
        if self.dingding:
            dingdingrobot(des + "\n" + "正负样本比:{0}:{1}\n".format(n, p) + str(confusion_matrix_table))

        """分类指标的文本报告"""
        rpt = classification_report(y, pred_y).replace("avg / total", "avg/total")
        rpt_df = pd.read_csv(io.StringIO(rpt.replace("avg / total", "avg/total")), sep="\s+").round(
            {"precision": 2, "recall": 2, "f1-score": 2, "support": 2})
        plot_suit.plot_matrix(rpt_df, title="{0}_report".format(des))
        print('{0}-classification_report'.format(des))
        print(rpt)
        if self.dingding:
            dingdingrobot(des + "\n" + rpt)

        fpr, tpr, _ = roc_curve(y, pred_y)
        roc_auc = auc(fpr, tpr)
        plot_suit.plot_roc_curve(fpr, tpr, roc_auc, title="{0}_roc".format(des))

        """日志记录"""
        if self.log:
            data = {}
            data["update"] = self.cur_time
            data["confusion_matrix"] = conf_m_df.to_dict(orient='split')
            data["report"] = rpt_df.to_dict(orient='split')
            json_str = json.dumps(data)
            hflog.info(json_str)

    @classmethod
    def pretty_tabel(cls, df):
        confusion_matrix_table = prettytable.PrettyTable()  # 创建表格实例
        confusion_matrix_table.field_names = [""] + df.columns.tolist()[1:]
        for row in range(df.shape[0]):
            confusion_matrix_table.add_row(df.values[row])  # 增加第一行数据
        return confusion_matrix_table

    def model_predict_proba(cls, model, X, y, threshold=0.6):

        proba = pd.DataFrame(model.predict_proba(X)).add_prefix('proba_')
        X = X.reset_index(drop=True)
        y = y.reset_index(drop=True)
        df_proba = pd.concat([X, y, proba], axis=1)
        df_proba = df_proba[df_proba["proba_1"] >= threshold]

        return df_proba

    @classmethod
    def model_save(cls, model, filename):
        model_saved_dir = os.path.join('model_saved/{0}'.format(public_config.cur_time))
        try:
            if not os.path.exists(model_saved_dir):
                os.makedirs(model_saved_dir)
        except Exception as e:
            print(str(e))
        joblib.dump(model, './{0}/{1}.model'.format(model_saved_dir, filename))

    @classmethod
    def model_load(cls, filename):
        model = joblib.load('{}'.format(filename))
        return model
