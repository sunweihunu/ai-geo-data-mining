# SVM_R1.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 4.3 KB · 代码 47 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_R1.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/SVM_V1/SVM_R1.mlx" download>下载 SVM_R1.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**训练线性支持向量机回归模型**

使用存储在矩阵中的样本数据训练支持向量机 (SVM) 回归模型。 加载 carsmall 数据集。

## 脚本内容

```matlab
% 训练线性支持向量机回归模型
% 使用存储在矩阵中的样本数据训练支持向量机 (SVM) 回归模型。
% 加载 carsmall 数据集。
% Train Linear Support Vector Machine Regression Model
% Train a support vector machine (SVM) regression model using sample data
% stored in matrices.
% Load the carsmall data set.

load carsmall
rng 'default'  % For reproducibility
% 指定马力和重量作为预测变量 (X)，指定 MPG 作为响应变量 (Y)。
% Specify Horsepower and Weight as the predictor variables (X) and
% MPG as the response variable (Y).

X = [Horsepower,Weight];
Y = MPG;
% 训练默认的 SVM 回归模型。
% Train a default SVM regression model.

Mdl = fitrsvm(X,Y)
% Mdl 是经过训练的 RegressionSVM 模型。
% Mdl is a trained RegressionSVM model.

% 检查模型是否收敛。
% Check the model for convergence.

Mdl.ConvergenceInfo.Converged
% 0 indicates that the model did not converge.
% 0 表示模型没有收敛。

% 使用标准化数据重新训练模型。
% Retrain the model using standardized data.

MdlStd = fitrsvm(X,Y,'Standardize',true)
% 检查模型是否收敛。
% Check the model for convergence.

MdlStd.ConvergenceInfo.Converged
% 1 表示模型确实收敛了。
% 1 indicates that the model did converge.

% 计算新模型的重新代入（样本内）均方误差。
% Compute the resubstitution (in-sample) mean-squared error for the new model.


lStd = resubLoss(MdlStd)
% lStd = 17.0256
```
