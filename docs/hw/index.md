# 小作业习题（总览）

本板块是《人工智能与地理数据挖掘》课程配套的 **MATLAB 小作业习题集**，覆盖课程主要教学方法：
降维、聚类分析、线性模型（判别分析）、k 最近邻、决策树、支持向量机与神经网络。
全部习题同步发布在 [MATLAB Grader 在线自动评分平台](https://grader.mathworks.com/courses/145451-21)，
由系统自动运行、自动判分，本页提供题目的完整描述与起始代码模板，便于预习与离线练习。

## 如何完成作业

1. **在线完成（推荐）**：通过课程邀请加入 MATLAB Grader 课程"数据挖掘21自地"，在对应作业下打开题目，
   直接在网页的 MATLAB 环境中作答并提交，系统立即给出每个测试项的通过情况与百分比分数。
2. **离线练习**：在本地 MATLAB 中新建脚本，把每页给出的"学生模板"粘贴进去，补全代码；
   数据集均为 MATLAB 自带（`fisheriris`、`carsmall`、`ionosphere`、`bodyfat_dataset`），无需下载。

## 评分说明

- 每道题由若干**自动测试**组成，采用加权评分并向学生显示百分比分数；
- 测试检查题目要求输出的**变量**（如 `newid`、`Train_accuracy`、`rmse_valid` 等）的取值是否与参考答案一致，
  以及是否按要求调用了指定建模函数（如 `fitcknn`、`fitrtree`、`fitcsvm`、`fitnet`、`pca`、`fitcdiscr`）；
- 请严格按题目要求设置随机种子、数据划分方式与变量名——它们都参与判分。

## 题目列表

| 作业 | 主题 | 对应章节 | 数据集 | 核心函数 |
|---|---|---|---|---|
| [小作业1](hw06-pca.md) | 降维（PCA） | 第 05 章 | fisheriris | `pca` |
| [小作业2](hw01-clustering.md) | 聚类分析 | 第 04 章 | fisheriris | `kmeans` |
| [小作业3](hw07-lda.md) | 线性模型（判别分析） | 第 06 章 | fisheriris | `fitcdiscr` |
| [小作业4](hw02-knn.md) | k 最近邻 | 第 07 章 | carsmall | `fitcknn` |
| [小作业5](hw03-cart.md) | 决策树（CART 回归） | 第 08 章 | carsmall | `fitrtree` |
| [小作业6](hw04-svm.md) | 支持向量机 | 第 10 章 | ionosphere | `fitcsvm` |
| [小作业7](hw05-ann.md) | 神经网络 | 第 09 章 | bodyfat_dataset | `fitnet`、`trainlm` |

!!! note "参考答案在哪？"
    参考答案、评分细节与解题工作流由教师掌握，不在本站公布。做完作业后请对照课堂讲评。
