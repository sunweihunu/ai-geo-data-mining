# SVM_R1.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 4.3 KB · 代码 47 行 · 运行输出 5

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_R1.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/SVM_V1/SVM_R1.mlx" download>下载 SVM_R1.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

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
```

<pre class="mlx-out">Mdl = 
  RegressionSVM
             ResponseName: 'Y'
    CategoricalPredictors: []
        ResponseTransform: 'none'
                    Alpha: [75x1 double]
                     Bias: 57.3958
         KernelParameters: [1x1 struct]
          NumObservations: 94
           BoxConstraints: [94x1 double]
          ConvergenceInfo: [1x1 struct]
          IsSupportVector: [94x1 logical]
                   Solver: 'SMO'

  Properties, Methods</pre>

```matlab
% Mdl 是经过训练的 RegressionSVM 模型。
% Mdl is a trained RegressionSVM model.

% 检查模型是否收敛。
% Check the model for convergence.

Mdl.ConvergenceInfo.Converged
```

<pre class="mlx-out">ans = logical
   0</pre>

```matlab
% 0 indicates that the model did not converge.
% 0 表示模型没有收敛。

% 使用标准化数据重新训练模型。
% Retrain the model using standardized data.

MdlStd = fitrsvm(X,Y,'Standardize',true)
```

<pre class="mlx-out">MdlStd = 
  RegressionSVM
             ResponseName: 'Y'
    CategoricalPredictors: []
        ResponseTransform: 'none'
                    Alpha: [77x1 double]
                     Bias: 22.9131
         KernelParameters: [1x1 struct]
                       Mu: [109.3441 2.9625e+03]
                    Sigma: [45.3545 805.9668]
          NumObservations: 94
           BoxConstraints: [94x1 double]
          ConvergenceInfo: [1x1 struct]
          IsSupportVector: [94x1 logical]
                   Solver: 'SMO'

  Properties, Methods</pre>

```matlab
% 检查模型是否收敛。
% Check the model for convergence.

MdlStd.ConvergenceInfo.Converged
```

<pre class="mlx-out">ans = logical
   1</pre>

```matlab
% 1 表示模型确实收敛了。
% 1 indicates that the model did converge.

% 计算新模型的重新代入（样本内）均方误差。
% Compute the resubstitution (in-sample) mean-squared error for the new model.


lStd = resubLoss(MdlStd)
```

<pre class="mlx-out">lStd = 16.8551</pre>

```matlab
% lStd = 17.0256
```
