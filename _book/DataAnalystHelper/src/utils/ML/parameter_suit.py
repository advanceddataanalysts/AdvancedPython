#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/9 15:48
# @Author  : along
# @Email   : yanglong_yan@163.com
# @File    : parameter_suit.py
# @Software: PyCharm


import numpy as np
from sklearn.metrics import recall_score, make_scorer, precision_score, f1_score

##################### 网格调参相关 start###########################################

parameter_score_precision = make_scorer(precision_score, pos_label=1)

parameter_score_recall = make_scorer(recall_score, pos_label=1)

parameter_score_f1 = make_scorer(f1_score, pos_label=1)

# RF parameters
###使用这些方法时要调整的主要参数是n_estimators 和max_features。
###前者是森林里的树木数量。越大越好，而且计算时间越长。
###此外，请注意，超过关键数量的树木，结果将停止显着改善。
###后者是分割节点时要考虑的特征的随机子集的大小。
###偏差减小越大，偏差越大。
###经验良好的默认值max_features=n_features 用于回归问题，max_features=sqrt(n_features)分类任务（n_features数据中的功能数量在哪里）。
###通常max_depth=None 结合min_samples_split=1（即，完全开发树木）时，会获得良好的效果。
###请记住，这些值通常不是最佳的，并且可能导致使用大量RAM的模型。应始终交叉验证最佳参数值。
###bootstrap=True另外，请注意，在随机林中，默认使用引导样本（ ），而外部树的默认策略是使用整个数据集（bootstrap=False）。
###当使用引导抽样时，可以在左边或外面的样本上估算泛化精度。
###这可以通过设置启用oob_score=True。当使用引导抽样时，可以在左边或外面的样本上估算泛化精度。
###这可以通过设置启用。当使用引导抽样时，可以在左边或外面的样本上估算泛化精度。这可以通过设置启用。'''
parameter_rfc = {"n_estimators": [10, 50, 100],
                 "max_features": range(3, 20),
                 "criterion": "gini",
                 "max_depth": range(3, 12),
                 "min_samples_split": range(5, 10),
                 "min_samples_leaf": range(5, 12),
                 "class_weight": [{1: w} for w in np.linspace(1.5, 2, 5)],
                 "oob_score": True,
                 }

# SVM parameters
###SVM在sklearn库中主要三个参数
###- kernel（核函数linear、RBF, 'sigmoid'）
###- C（ C是惩罚系数，即对误差的宽容度。c越高，说明越不能容忍出现误差,容易过拟合。C越小，容易欠拟合。C过大或过小，泛化能力变差）
###- gamma（ gamma是选择RBF函数作为kernel后，该函数自带的一个参数。隐含地决定了数据映射到新的特征空间后的分布，gamma越大，支持向量越少，gamma值越小，支持向量越多。
# 支持向量的个数影响训练与预测的速度。）
###不适合过大数据量，噪声很多的数据
parameter_svm = {"C": np.linspace(0.1, 20, 4),
                 "kernel": ['RBF'],
                 "gamma": np.linspace(0, 1, 3),
                 "class_weight": [{1: i} for i in np.linspace(1, 10, 4)],
                 }

# GBDT parameters
###n_estimators: 也就是弱学习器的最大迭代次数，或者说最大的弱学习器的个数。一般来说n_estimators太小，容易欠拟合，n_estimators太大，又容易过拟合，一般选择一个适中的数值。默认是100。在实际调参的过程中，我们常常将n_estimators和下面介绍的参数learning_rate一起考虑。
###learning_rate: 即每个弱学习器的权重缩减系数νν，也称作步长，在原理篇的正则化章节我们也讲到了，加上了正则化项，我们的强学习器的迭代公式为fk(x)=fk−1(x)+νhk(x)fk(x)=fk−1(x)+νhk(x)。νν的取值范围为0<ν≤10<ν≤1。对于同样的训练集拟合效果，较小的νν意味着我们需要更多的弱学习器的迭代次数。通常我们用步长和迭代最大次数一起来决定算法的拟合效果。所以这两个参数n_estimators和learning_rate要一起调参。一般来说，可以从一个小一点的νν开始调参，默认是1。
###subsample: 即我们在原理篇的正则化章节讲到的子采样，取值为(0,1]。注意这里的子采样和随机森林不一样，随机森林使用的是放回抽样，而这里是不放回抽样。如果取值为1，则全部样本都使用，等于没有使用子采样。如果取值小于1，则只有一部分样本会去做GBDT的决策树拟合。选择小于1的比例可以减少方差，即防止过拟合，但是会增加样本拟合的偏差，因此取值不能太低。推荐在[0.5, 0.8]之间，默认是1.0，即不使用子采样。
###init: 即我们的初始化的时候的弱学习器，拟合对应原理篇里面的f0(x)f0(x)，如果不输入，则用训练集样本来做样本集的初始化分类回归预测。否则用init参数提供的学习器做初始化分类回归预测。一般用在我们对数据有先验知识，或者之前做过一些拟合的时候，如果没有的话就不用管这个参数了。
###loss: 即我们GBDT算法中的损失函数。分类模型和回归模型的损失函数是不一样的。
###对于分类模型，有对数似然损失函数"deviance"和指数损失函数"exponential"两者输入选择。默认是对数似然损失函数"deviance"。在原理篇中对这些分类损失函数有详细的介绍。一般来说，推荐使用默认的"deviance"。它对二元分离和多元分类各自都有比较好的优化。而指数损失函数等于把我们带到了Adaboost算法。
###对于回归模型，有均方差"ls", 绝对损失"lad", Huber损失"huber"和分位数损失“quantile”。默认是均方差"ls"。一般来说，如果数据的噪音点不多，用默认的均方差"ls"比较好。如果是噪音点较多，则推荐用抗噪音的损失函数"huber"。而如果我们需要对训练集进行分段预测的时候，则采用“quantile”。
###alpha:这个参数只有GradientBoostingRegressor有，当我们使用Huber损失"huber"和分位数损失“quantile”时，需要指定分位数的值。默认是0.9，如果噪音点较多，可以适当降低这个分位数的值。
parameters_gbdt = {"loss": ["deviance"],
                   "learning_rate": [0.001, 0.01, 0.03, 0.1, 0.3, 0.5, 1.0],
                   "learning_rate": [0.15, 0.1],
                   "n_estimators": range(20, 25),
                   "subsample": [0.3, 0.5, 0.8, 1.0],
                   "criterion": ["friedman_mse", "mse"],
                   "max_features": range(3, 5),
                   "max_depth": range(3, 5),
                   "min_samples_split": range(2, 10),
                   "min_samples_leaf": range(1, 10),
                   "min_weight_fraction_leaf": [0.0],
                   "warm_start": [True],
                   "min_impurity_decrease": [None],
                   "max_leaf_nodes": [None],
                   }

###################### 网格调参相关 end ############################################


##################### 预处理参数相关 start###########################################

parameters_StandardScaler = {"StandardScaler": {"copy": True, "with_mean": True, "with_std": True}}

parameters_MinMaxScaler = {"MinMaxScaler": {"feature_range": (0, 1), "copy": True}}

parameters_normalize = {"normalize": {"copy": True, "norm": "l2"}}

###################### 预处理参数相关 end ############################################
