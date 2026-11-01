# New_ANN_09.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 5.0 KB · 代码 35 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/New_ANN_09.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/ANN/New_ANN_09.mlx" download>下载 New_ANN_09.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**早停法**

提高泛化能力的默认方法称为早停法。该方法自动提供给所有的有监督网络创建函数，包括反向传播网络创建函数，如 feedforwardnet。 在此方法中，可用数据划分为三个子集。第一个子集是训练集，用于计算梯度和更新网络权重及偏置。第二个子集是验证集。在训练过程中会监控基于验证集的误差。验证误差通常在训练的初始阶段减小，训练集误差也是如此。然而，当网络开始过拟合数据时，基于验证集的误差通常开始增大。当验证误差在指定次数的迭代 (net.trainParam.max_fail) 中增加时，训练停止，并返回验证误差最小时的权重和偏置。

## 脚本内容

```matlab
% 早停法
% 提高泛化能力的默认方法称为早停法。该方法自动提供给所有的有监督网络创建函数，包括反向传播网络创建函数，如 feedforwardnet。
%
% 在此方法中，可用数据划分为三个子集。第一个子集是训练集，用于计算梯度和更新网络权重及偏置。第二个子集是验证集。在训练过程中会监控基于验证集的误差。验证误差通常在训练的初始阶段减小，训练集误差也是如此。然而，当网络开始过拟合数据时，基于验证集的误差通常开始增大。当验证误差在指定次数的迭代 (net.trainParam.max_fail) 中增加时，训练停止，并返回验证误差最小时的权重和偏置。
%
% 训练期间不使用测试集误差，但测试集误差用于比较不同模型。在训练过程中绘制测试集误差也很有用。如果测试集误差与验证集误差达到最小值所需的迭代次数显著不同，这可能表示数据集的划分不佳。
%
% 可使用四个函数将数据划分为训练集、验证集和测试集。它们是 dividerand（默认值）、divideblock、divideint 和 divideind。您可以使用以下属性访问或更改网络的划分函数：

net.divideFcn
% 其中每个函数都采用自定义其行为的参数。这些值会被存储，且可以通过以下网络属性进行更改：

net.divideParam
% 索引数据划分 (divideind)
% 创建一个简单的测试问题。对于完整的数据集，以 0.01 的步长生成有 201 个输入点的含噪正弦波，输入点范围为 −1 至 1：

p = [-1:0.01:1];
t = sin(2*pi*p)+0.1*randn(size(p));
% 按索引划分数据，以便将连续样本依次分配给训练集、验证集和测试集：

trainInd = 1:3:201
valInd = 2:3:201;
testInd = 3:3:201;
[trainP,valP,testP] = divideind(p,trainInd,valInd,testInd);
[trainT,valT,testT] = divideind(t,trainInd,valInd,testInd);
```

## 随机数据划分 (dividerand)

您可以随机划分输入数据，以便将 60% 的样本分配给训练集，20% 分配给验证集，20% 分配给测试集，如下所示：

```matlab
[trainP,valP,testP,trainInd,valInd,testInd] = dividerand(p);
% 该函数不仅划分输入数据，还返回索引，以便您可以使用 divideind 相应地划分目标数据：

[trainT,valT,testT] = divideind(t,trainInd,valInd,testInd);
```

## 分块数据划分 (divideblock)

您还可以随机划分输入数据，以便将前 60% 的样本分配给训练集，接下来的 20% 分配给验证集，最后 20% 分配给测试集，如下所示：

```matlab
[trainP,valP,testP,trainInd,valInd,testInd] = divideblock(p);
```

## 使用 divideind 相应地划分目标数据：

```matlab
[trainT,valT,testT] = divideind(t,trainInd,valInd,testInd);
```

## 交错数据划分 (divideint)

划分输入数据的另一种方法是根据百分比将样本循环分配给训练集、验证集和测试集。您可以按照交错方式将 60% 的样本分配给训练集、20% 分配给验证集、20% 分配给测试集，如下所示：

```matlab
[trainP,valP,testP,trainInd,valInd,testInd] = divideint(p);
% 使用 divideind 相应地划分目标数据。

[trainT,valT,testT] = divideind(t,trainInd,valInd,testInd);
```
