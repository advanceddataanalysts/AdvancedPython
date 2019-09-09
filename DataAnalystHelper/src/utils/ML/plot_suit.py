#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/9 15:48
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : plot_suit.py
# @Software: PyCharm

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.config import public_config


class plot_suit(object):
    # def __init__(self):
    cur_time = public_config.cur_time

    #### 矩阵并可视化
    @classmethod
    def plot_matrix(cls, df, title="train_confusion_matrix"):
        matrix = df.values
        xticklabels = df.columns.tolist()
        yticklabels = df.index.tolist()
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.matshow(matrix, cmap=plt.cm.Blues, alpha=0.3)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                ax.text(x=j, y=i, s=matrix[i, j], va='center', ha='center')
        plt.title(title)
        ax.set_xticklabels(["x"] + xticklabels)
        ax.set_yticklabels(["y"] + yticklabels)

        # plt.xlabel('predicted label')
        # plt.ylabel('true label')
        cls.img_save(plt, des=title + "_" + cls.cur_time)

        plt.show()

    # ROC曲线
    @classmethod
    def plot_roc_curve(cls, fpr, tpr, roc_auc, title="train_roc"):

        plt.figure(figsize=(5, 5))
        plt.plot(fpr, tpr, color='red', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='blue', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.0])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(title)
        cls.img_save(plt, des=title + "_" + cls.cur_time)
        plt.show()

    # 特征排序
    @classmethod
    def plot_feature_importances(cls, importances, labels, title='feature_importancet', threshold=0.05):

        df = pd.DataFrame(list(zip(labels, importances)), columns=["labels", "improtance"]).sort_values(
            by=["improtance"], ascending=False).round(3)
        df = df[df["improtance"].abs() >= threshold]
        print(df)
        # 可视化特征重要性-依据平均不纯度衰减
        plt.figure(figsize=(5, 5))
        plt.title(title)
        plt.bar(range(len(df["improtance"])), df["improtance"], color='lightblue', align='center')
        plt.xticks(range(len(df["labels"])), df["labels"], rotation=90)
        plt.xlim([-1, len(df["improtance"])])
        plt.tight_layout()
        cls.img_save(plt, des=title + "_" + cls.cur_time)
        plt.show()

    # 离散化占比分布
    @classmethod
    def plot_discretize(cls, df, fcol, lcol=None,
                        method={"cut": {"bins": 9, "right": True, "include_lowest": False},
                                "value_counts": {"normalize": True, "sort": False}},
                        title='discretization', saved=False):

        title = title + "-" + fcol
        if not "cut" in method:
            method["cut"] = {"bins": 9, "right": True}
        if not "value_counts" in method:
            method["value_counts"] = {"normalize": True, "sort": False}

        df_cut = pd.DataFrame(pd.cut(df[fcol], retbins=True, **method["cut"])[0])
        df_distribution = pd.DataFrame(df_cut[fcol].value_counts(**method["value_counts"])).reset_index()
        df_distribution.columns = ["bins", "total"]
        fig = plt.figure(figsize=(5, 5))
        ax1 = fig.add_subplot(111)
        ax1.bar(range(len(df_distribution["total"])), df_distribution["total"], color='bisque', align='center')

        plt.title(title)
        plt.xticks(range(len(df_distribution["total"])), df_distribution["bins"], rotation=60)
        plt.xlim([-1, len(df_distribution["total"])])

        if lcol != None:
            ax2 = ax1.twinx()
            # df_cut = pd.DataFrame(pd.cut(df[fcol], retbins=True, **method["cut"])[0])

            print("step1")

            df[fcol] = df_cut[fcol]

            df_distribution_p = pd.DataFrame(
                df.loc[df[lcol] == 1, fcol].value_counts(**method["value_counts"])).reset_index()
            df_distribution_p.columns = ["bins", "p"]
            df_distribution = pd.merge(df_distribution, df_distribution_p, on="bins", how="inner")

            df_distribution_n = pd.DataFrame(
                df.loc[df[lcol] == 0, fcol].value_counts(**method["value_counts"])).reset_index()
            df_distribution_n.columns = ["bins", "n"]
            df_distribution = pd.merge(df_distribution, df_distribution_n, on="bins", how="inner")

            # print(df_distribution_p.dtypes)
            ax2.plot(range(len(df_distribution["p"])), df_distribution["p"], color='red')

            ax2.plot(range(len(df_distribution["n"])), df_distribution_n["n"], color='green', linestyle='--')

            plt.legend([1, 0], shadow=False, loc="upper right", framealpha=0)
            # print(df_distribution_p.dtypes)
            # df_distribution_p["index"]=df_distribution_p["index"].astype("str")
            # ax2.plot(df_distribution_p["index"], df_distribution_p[fcol])

        plt.tight_layout()

        if saved:
            cls.img_save(plt, des=title + cls.cur_time)
        plt.show()

    # 类别字段占比分布
    @classmethod
    def plot_category_distribute(cls, df, fcol, lcol=None, method={"normalize": True, "sort": False},
                                 title='distribution-', axis=1, legend=None, saved=False, threshold=0.05):

        title = title + fcol
        df_distribution = pd.DataFrame(df[fcol].value_counts(**method)).reset_index().sort_values(by=["index"])

        plt.figure(figsize=(5, 5))

        if lcol == None:
            plt.title(title)
            plt.bar(range(len(df_distribution[fcol])), df_distribution[fcol], color='lightblue', align='center')
            plt.xticks(range(len(df_distribution[fcol])), df_distribution["index"], rotation=90)
            plt.xlim([-1, len(df_distribution[fcol])])
            if legend:
                plt.legend([legend], shadow=False, loc="upper right", framealpha=0)
        else:

            plt.plot(range(len(df_distribution[fcol])), df_distribution[fcol], color='purple', linestyle='--',
                     label="proportion")

            bar_width = 0.35
            df_distribution = df.groupby([fcol, lcol], as_index=False, group_keys=True)[lcol].size()
            df_distribution = df_distribution.unstack(lcol)

            if axis == 1:
                df_distribution = df_distribution.div(df_distribution.sum(axis=1).astype(float), axis=0).reset_index()
            else:
                df_distribution = df_distribution / df_distribution.sum()
                df_distribution = df_distribution.reset_index()

            plt.bar(np.arange(len(df_distribution[fcol])), df_distribution[0], bar_width, color='lightgreen',
                    align='center', label="0")
            plt.bar(np.arange(len(df_distribution[fcol])) + bar_width, df_distribution[1], bar_width,
                    color='lightcoral', align='center', label="1")

            plt.xticks(np.arange(len(df_distribution[fcol])) + bar_width / 2, df_distribution[fcol], rotation=60)

            plt.legend(loc="upper right")

            title = title + "--axis=" + str(axis)

            plt.title(title)

        plt.tight_layout()
        if saved:
            cls.img_save(plt, des=title + "_" + fcol + cls.cur_time)
        plt.show()

    # 定量字段箱体图
    @classmethod
    def plot_box_distribute(cls, df, col, method={}, title='box_distribution', saved=False, threshold=0.05):

        plt.figure(figsize=(5, 5))
        plt.title(title)
        plt.boxplot(df[col], labels=[col], **method)
        # plt.xticks(range(len(df[col])),df[col],rotation=90)
        # plt.xlim([-1,len(df[col])])

        plt.tight_layout()
        if saved:
            cls.img_save(plt, des=title + "_" + col + cls.cur_time)
        plt.show()

    @classmethod
    def img_save(cls, plt, des="untitled"):
        img_saved_dir = os.path.join('img_saved/{0}'.format(cls.cur_time))
        try:
            if not os.path.exists(img_saved_dir):
                os.makedirs(img_saved_dir)
        except Exception as e:
            print(str(e))
        plt.savefig("./{0}/{1}.jpg".format(img_saved_dir, des))
