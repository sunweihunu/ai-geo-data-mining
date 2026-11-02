# 小作业7 神经网络：ANN 预测体脂率

**对应章节**：第 09 章 人工神经网络 ｜ **数据集**：MATLAB 自带 `bodyfat_dataset`（252 个样本，13 个自变量）｜ **核心函数**：`fitnet`、`trainlm`

## 题目背景

构建一个前馈神经网络（ANN），通过 13 个身体属性来预测体脂率。数据采用 MATLAB 自带的
`bodyfat_dataset`（252 个样本）。`bodyfatInputs` 包含 13 个自变量：年龄（岁）、重量（磅）、身高（英寸）、
颈围、胸围、腹围、臀围、大腿围、膝围、踝围、上臂（伸展）围、前臂围、腕围（cm）；
`bodyfatTargets` 是体脂率。十三个身体属性作为神经网络的输入（自变量），体脂率作为目标（因变量）。

注意 MATLAB 神经网络工具箱的数据约定：**每列是一个样本**，`X` 为 13×252，`T` 为 1×252。

## 需要完成

按以下要求构建并训练网络，求出训练集、验证集和测试集的 RMSE：

- 网络为双层（即**一个隐藏层**）前馈神经网络，隐含层单元数为 **15**；
- 训练算法为 **`trainlm`**（Levenberg–Marquardt 反向传播）；
- 用 **`setdemorandstream(100)`** 设定随机数种子（网络初始化用它，而不是 `rng`）；
- **顺序划分**数据：前 60% 训练集、接着 20% 验证集、最后 20% 测试集（`divideblock`）；
- **强制网络不显示训练窗口**（`net.trainParam.showWindow = false`），否则可能报错；
- 输出三个实数：`train_rmse`、`valid_rmse`、`test_rmse`。

## 学生模板（起始代码）

```matlab
% 选择和导入数据
clear


% 选择训练算法


%  设置随机种子


% 创建网络

net.trainParam.showWindow = false; %  强制网络不要显示窗口，否则可能报错。

% 顺序划分数据，前60%作为训练集，接着20%作为验证集，最后20%作为测试集


% 训练网络


% 神经网络预测训练集、验证集和测试集



% 计算训练集、验证集和测试集的性能指数RMSE(实数)
train_rmse=
valid_rmse=
test_rmse=
```

## 提交与评分说明

- 本题共 **4 个自动测试**：随机种子初始化与前馈网络函数检查（`setdemorandstream`、`fitnet`）、
  训练集 RMSE、验证集 RMSE、测试集 RMSE，加权评分；
- 系统检查 `train_rmse`、`valid_rmse`、`test_rmse` 的数值是否与参考答案一致。

!!! tip "提示"
    - `[X,T] = bodyfat_dataset` 直接得到输入与目标；
    - `fitnet(hiddenLayerSize, trainFcn)` 创建前馈网络；`net.divideFcn = 'divideblock'` 设置顺序划分，
      配合 `net.divideParam.trainRatio/valRatio/testRatio`；
    - 训练返回 `[net, tr]`，`tr.trainInd / tr.valInd / tr.testInd` 是三个子集的样本下标，
      用 `net(X)` 得到全部预测后按下标切片分别算 RMSE；
    - 神经网络训练对随机初始化敏感：务必先 `setdemorandstream(100)` 再创建网络，
      且顺序不要颠倒，否则结果不可复现。
