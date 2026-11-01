# cart_exp03.mlx

「决策树（CART）」目录 · 对应书稿 **第08章 决策树** · 14.6 KB · 代码 31 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DecisionTree_v2/cart_exp03.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DecisionTree_v2/cart_exp03.mlx" download>下载 cart_exp03.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**Cross Validate a Regression Tree**

This example shows how to examine the resubstitution and cross-validation accuracy of a regression tree for predicting mileage based on the carsmall data. Load the carsmall data set.

## 脚本内容

```matlab
% Cross Validate a Regression Tree
% This example shows how to examine the resubstitution and cross-validation accuracy of a regression tree for predicting mileage based on the carsmall data.
% Load the carsmall data set.
% Consider acceleration, displacement, horsepower, and weight as predictors of MPG.
%  Step 1： 导入原始数据
load carsmall
X = [Acceleration Displacement Horsepower Weight];

%  Step 2： 训练回归树模型
% Grow a regression tree using all of the observations.
rtree = fitrtree(X,MPG);

%  Step 3： 预测回归树模型
MPG_pre=predict(rtree,X);

%  Step 4： 真实和预测值的散点图
plot(MPG,MPG_pre,'ro')

%  Step 5： 计算训练集的性能指数：均方误差（误差平方的均值）
% Compute the in-sample error.
resuberror = resubLoss(rtree)
% The resubstitution loss for a regression tree is the mean-squared error.
% The resulting value indicates that a typical predictive error for the tree is about the square root of 4.7, or a bit over 2.

%  Step 5： 计算交叉检验的性能指数：
% Estimate the cross-validation MSE.
rng 'default';
cvrtree = crossval(rtree);
cvloss = kfoldLoss(cvrtree)
% The cross-validated loss is almost 25, meaning a typical predictive error
% for the tree on new data is about 5. This demonstrates that cross-validated loss is usually higher than simple resubstitution loss.
```
