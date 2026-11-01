# SVM_R6.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 20.8 KB · 代码 21 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_R6.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/SVM_V1/SVM_R6.mlx" download>下载 SVM_R6.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**优化 SVM 回归**

此示例展示了如何使用 fitrsvm 自动优化超参数。 该示例使用 carsmall 数据。

## 脚本内容

```matlab
% 优化 SVM 回归
% 此示例展示了如何使用 fitrsvm 自动优化超参数。
% 该示例使用 carsmall 数据。
% 加载 carsmall 数据集。
% Optimize SVM Regression
% This example shows how to optimize hyperparameters automatically using fitrsvm.
% The example uses the carsmall data.
% Load the carsmall data set.
clear
load carsmall
```

## 指定马力和重量作为预测变量 (X)，指定 MPG 作为响应变量 (Y)。

Specify Horsepower and Weight as the predictor variables (X) and MPG as the response variable (Y).

```matlab
X = [Horsepower Weight];
Y = MPG;
```

## 通过使用自动超参数优化，找到将五倍交叉验证损失最小化的超参数。

为了重现性，设置随机种子并使用“预期改进加”采集功能。 Find hyperparameters that minimize five-fold cross-validation loss by using automatic hyperparameter optimization. For reproducibility, set the random seed and use the 'expected-improvement-plus' acquisition function.

```matlab
rng default
Mdl = fitrsvm(X,Y,'OptimizeHyperparameters','auto',...
    'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName',...
    'expected-improvement-plus'))

% 优化搜索了 BoxConstraint、KernelScale 和 Epsilon。
% 输出是具有最小估计交叉验证损失的回归。
% The optimization searched over BoxConstraint, KernelScale, and Epsilon.
% The output is the regression with the minimum estimated cross-validation loss.
```
