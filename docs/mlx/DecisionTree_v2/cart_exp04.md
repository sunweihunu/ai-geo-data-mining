# cart_exp04.mlx

「决策树（CART）」目录 · 对应书稿 **第08章 决策树** · 167.8 KB · 代码 29 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DecisionTree_v2/cart_exp04.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DecisionTree_v2/cart_exp04.mlx" download>下载 cart_exp04.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**优化回归树**

使用 fitrtree 自动优化超参数。 Optimize Regression Tree

## 脚本内容

```matlab
% ================ 注释中英文对照，供阅读比较================
% 优化回归树
% 使用 fitrtree 自动优化超参数。
% Optimize Regression Tree
% Optimize hyperparameters automatically using fitrtree.

% Load the carsmall data set.
load carsmall
% 使用重量和马力作为 MPG 的预测指标。
X = [Weight,Horsepower];
Y = MPG;
```

## 训练回归树

```matlab
Md0 = fitrtree(X,Y);
view(Md0,'Mode','graph')
% 计算训练集的损失函数
resubLoss(Md0)  %  5.8158
% 计算训练集的误差平方的均值（均方误差）
Y0_pre=predict(Md0,X);
mean((Y0_pre-Y).^2) % 缺失值没有处理
```

## 通过使用fitrtree的自动超参数优化，

找到将五倍交叉验证损失最小化的超参数。 为了重现性，设置随机种子并使用“预期改进加”采集功能。 Use Weight and Horsepower as predictors for MPG. Find hyperparameters that minimize five-fold cross-validation loss by using automatic hyperparameter optimization. For reproducibility, set the random seed and use the 'expected-improvement-plus' acquisition function.

```matlab
rng default
Md1 = fitrtree(X,Y,'OptimizeHyperparameters','auto',...
    'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName',...
    'expected-improvement-plus'))
view(Md1,'Mode','graph')
resubLoss(Md1) % 12.1673
% 计算训练集的误差平方的均值（均方误差）
Y1_pre=predict(Md1,X);
mean((Y1_pre-Y).^2) % 缺失值没有处理

% 模型结构大大精简了，训练集的性能下降了
```
