# 小作业4 k 最近邻：采用 kNN 构建汽车分类模型

**对应章节**：第 07 章 k最近邻（kNN）模型 ｜ **数据集**：MATLAB 自带 `carsmall`（100 辆车）｜ **核心函数**：`fitcknn`

## 题目背景

本习题通过 MATLAB 自带的汽车数据集 `carsmall`，熟悉 k 最近邻（k-Nearest Neighbors, kNN）算法的基本
使用方法。学生需要加载数据集、预处理数据、选择特征，把数据集划分为训练集（前 70%）和验证集（后 30%），
构建 kNN 分类模型，计算分类精度。

`carsmall` 数据集包含的变量：

```
Name             Size      Bytes  Class
Acceleration    100x1        800  double
Cylinders       100x1        800  double
Displacement    100x1        800  double
Horsepower      100x1        800  double
MPG             100x1        800  double
Mfg             100x13      2600  char
Model           100x33      6600  char
Model_Year      100x1        800  double
Origin          100x7       1400  char
Weight          100x1        800  double
```

其中 `Acceleration`、`Cylinders`、`Displacement`、`Horsepower`、`MPG`、`Weight` 是候选特征（自变量），
`Origin`（汽车产地）是需要预测的类别（因变量）。

## 需要完成

1. 加载数据，选择 **6 个数值特征**作为自变量，`Origin` 作为标签；
2. 按**前 70 个样本为训练集、后 30 个样本为验证集**分割（顺序分割）；
3. 用 `fitcknn` 构建 kNN 分类模型，**最近邻数量 k = 2**；
4. 分别预测训练集与验证集，并计算分类精度（预测类别与实际类别一致的总次数 ÷ 样本数），
   结果存入 `Train_accuracy` 与 `Valid_accuracy`（小数，如 0.8888）。

注意事项：

- 注意数据集的分割（顺序分割，不要随机打乱）；
- 最近邻的数量 k 选取 2；
- 选取 6 个特征；
- 不考虑数据清洗。

## 学生模板（起始代码）

```matlab
%% 加载carsmall数据集

% 选择 6个自变量，Origin 作为标签


%% 将数据划分为训练集和测试集


%%  使用kNN进行分类


% 预测数据的标签


% 计算分类准确率(补全计算公式的代码)
Train_accuracy =
Valid_accuracy =

% 输出结果(Train_accuracy或Valid_accuracy 是个小数（如0.8888）；不修改下列代码)
disp(['训练集分类准确率: ', num2str(Train_accuracy)])
disp(['验证集分类准确率: ', num2str(Valid_accuracy)])
```

## 提交与评分说明

- 本题共 **3 个自动测试**：训练集精度（约 1/3）、验证集精度（约 1/3）、是否使用了 kNN 建模函数
  `fitcknn`（约 1/3），加权评分；
- 系统检查 `Train_accuracy`、`Valid_accuracy` 的数值是否与参考答案一致，以及代码中是否调用了 `fitcknn`。

!!! tip "提示"
    - `Origin` 是 char 元胞数组，比较预测类别与真实类别时统一转成 `string` 再用 `strcmp` 比较较方便；
    - 训练集精度会明显高于验证集精度——想一想是什么原因（提示：顺序分割后验证集的产地分布、
      特征量纲差异、k=2 的平票问题），这正是课堂讨论的好素材。
