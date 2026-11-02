# 小作业5 决策树：采用 CART 预测汽车的 MPG

**对应章节**：第 08 章 决策树 ｜ **数据集**：MATLAB 自带 `carsmall`（100 辆车）｜ **核心函数**：`fitrtree`

## 题目背景

本习题通过 MATLAB 自带的汽车数据集 `carsmall`，熟悉 CART 树算法的基本使用方法。学生需要加载数据集、
选择特征，把数据集划分为训练集（前 80%）和验证集（后 20%），构建 CART **回归**模型预测 MPG（每加仑
英里数），并计算预测性能指数 RMSE。

选定的自变量为 4 个：`Acceleration`、`Cylinders`、`Displacement`、`Horsepower`；
因变量为 `MPG`。

## 需要完成

1. 加载数据，取 4 个特征与 MPG；
2. 按**前 80 个样本为训练集、后 20 个样本为验证集**分割（顺序分割）；
3. 用 `fitrtree` 训练 CART 回归树模型；
4. 分别预测训练集与验证集的 MPG；
5. 计算 RMSE（均方根误差），结果存入 `rmse_train` 与 `rmse_valid`。
   RMSE 可以按定义计算，也可以直接使用 MATLAB 自带函数。

注意事项：

- 注意数据集的分割（顺序分割）；
- 选取 4 个特征；
- 模型训练时可以不用数据清洗；
- **计算 RMSE 时需要数据清洗**（训练集 MPG 中含有缺失值 NaN，直接算 RMSE 会得到 NaN）。

## 学生模板（起始代码）

```matlab
% 导入原始数据
clear


% 将数据划分为训练集和测试集


% 训练回归树模型


% 预测


% 计算性能指数：均方误差（误差平方的均值）
rmse_train =
rmse_valid =
```

## 提交与评分说明

- 本题共 **3 个自动测试**：训练集 RMSE、验证集 RMSE、是否使用了 CART 建模函数 `fitrtree`，
  加权评分；
- 系统检查 `rmse_train`、`rmse_valid` 的数值是否与参考答案一致，以及代码中是否调用了 `fitrtree`。

!!! tip "提示"
    - RMSE = sqrt(mean((预测值 − 真实值).^2))；
    - 训练集 MPG 含 NaN：先 `find(isnan(train_MPG)==0)` 找出非缺失样本，再对这些样本计算 RMSE；
    - 训练集 RMSE 会远小于验证集 RMSE——这是回归树的过拟合现象，课堂会结合最小叶节点数
      （`MinLeafSize`）讨论如何控制树的复杂度。
