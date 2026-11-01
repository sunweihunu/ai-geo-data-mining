# SVM_R5.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 3.9 KB · 代码 33 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_R5.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/SVM_V1/SVM_R5.mlx" download>下载 SVM_R5.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**手动计算交叉验证损失**

创建交叉验证回归模型时，您可以使用 kfoldLoss 对象函数计算均方误差 (MSE)。 或者，您可以使用 kfoldPredict 预测验证折叠观察的响应并手动计算 MSE。

## 脚本内容

```matlab
% 手动计算交叉验证损失
% 创建交叉验证回归模型时，您可以使用 kfoldLoss 对象函数计算均方误差 (MSE)。
% 或者，您可以使用 kfoldPredict 预测验证折叠观察的响应并手动计算 MSE。
%
% 加载 carsmall 数据集。指定预测变量数据 X 和响应数据 Y。
% Compute Cross-Validation Loss Manually
% When you create a cross-validated regression model,
% you can compute the mean squared error (MSE) by using the kfoldLoss object function.
% Alternatively, you can predict responses for validation-fold observations
% using kfoldPredict and compute the MSE manually.
%
% Load the carsmall data set. Specify the predictor data X and the response data Y.

load carsmall
X = [Cylinders Displacement Horsepower Weight];
Y = MPG;
% 训练交叉验证的回归树模型。默认情况下，软件实施 10 折交叉验证。
% Train a cross-validated regression tree model.
% By default, the software implements 10-fold cross-validation.

rng('default') % For reproducibility
CVMdl = fitrtree(X,Y,'CrossVal','on');
% 使用 kfoldLoss 计算 10 倍交叉验证 MSE。
% Compute the 10-fold cross-validation MSE by using kfoldLoss.

L = kfoldLoss(CVMdl)
% L = 29.4963
% 使用交叉验证的回归模型预测响应 yfit。计算 yfit 和真实响应 CVMdl.Y 之间的均方误差。计算出的 MSE 与 kfoldLoss 返回的损失值相匹配。
% Predict the responses yfit by using the cross-validated regression model. Compute the mean squared error between yfit and the true responses CVMdl.Y. The computed MSE matches the loss value returned by kfoldLoss.

yfit = kfoldPredict(CVMdl);
mse = mean((yfit - CVMdl.Y).^2)
% mse = 29.4963
```
