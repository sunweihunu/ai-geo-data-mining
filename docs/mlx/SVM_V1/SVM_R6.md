# SVM_R6.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 20.8 KB · 代码 21 行 · 图窗 1

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_R6.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/SVM_V1/SVM_R6.mlx" download>下载 SVM_R6.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

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
```

<pre class="mlx-out">|===================================================================================================================================|
| Iter | Eval   | Objective:  | Objective   | BestSoFar   | BestSoFar   | BoxConstraint|  KernelScale |      Epsilon |  Standardize |
|      | result | log(1+loss) | runtime     | (observed)  | (estim.)    |              |              |              |              |
|===================================================================================================================================|
|    1 | Best   |      4.1981 |     0.31273 |      4.1981 |      4.1981 |    0.0084663 |       510.98 |     0.016185 |         true |
|    2 | Best   |      2.9429 |     0.20164 |      2.9429 |      3.0186 |       45.353 |      0.47041 |     0.020424 |         true |
|    3 | Accept |      4.1889 |    0.076329 |      2.9429 |       2.943 |    0.0012899 |     0.057544 |       42.794 |         true |
|    4 | Accept |      4.1889 |    0.057331 |      2.9429 |       2.943 |     0.003523 |      0.40964 |       426.64 |        false |
|    5 | Accept |      3.1735 |     0.05058 |      2.9429 |      2.9431 |       551.55 |       84.602 |     0.022522 |         true |
|    6 | Accept |      4.1899 |     0.02877 |      2.9429 |      2.9431 |       11.274 |       695.59 |       1.5383 |         true |
|    7 | Accept |      4.5486 |      4.5846 |      2.9429 |       2.943 |        69.45 |    0.0041907 |     0.014018 |         true |
|    8 | Accept |      4.1889 |    0.035815 |      2.9429 |       2.943 |       87.669 |      0.83548 |       642.06 |         true |
|    9 | Accept |      2.9458 |    0.061772 |      2.9429 |       2.943 |       31.665 |      0.37494 |    0.0097618 |         true |
|   10 | Accept |      2.9456 |    0.041632 |      2.9429 |      2.9431 |        80.56 |      0.62773 |    0.0093135 |         true |
|   11 | Accept |      2.9857 |    0.042189 |      2.9429 |      2.9432 |      0.12861 |      0.60904 |    0.0096602 |         true |
|   12 | Accept |      2.9662 |    0.048453 |      2.9429 |      2.9434 |       388.44 |       21.998 |     0.011121 |         true |
|   13 | Best   |      2.9312 |    0.047702 |      2.9312 |      2.9314 |       812.52 |       23.622 |      0.43745 |         true |
|   14 | Accept |      2.9377 |    0.028808 |      2.9312 |      2.9313 |       802.92 |       5.5384 |     0.080709 |         true |
|   15 | Accept |      2.9537 |    0.026686 |      2.9312 |      2.9319 |       806.71 |       15.925 |     0.079228 |         true |
|   16 | Accept |       2.953 |    0.034276 |      2.9312 |       2.932 |       696.46 |       2.9706 |    0.0098432 |         true |
|   17 | Accept |      4.1889 |    0.029563 |      2.9312 |       2.932 |       947.96 |       36.027 |       101.97 |         true |
|   18 | Best   |      2.9304 |    0.043737 |      2.9304 |      2.9306 |        781.9 |       1.8968 |      0.13036 |         true |
|   19 | Best   |      2.9145 |    0.047557 |      2.9145 |      2.9145 |       890.61 |       6.5493 |      0.57601 |         true |
|   20 | Accept |      4.1779 |    0.028535 |      2.9145 |      2.9143 |    0.0085371 |       4.9203 |      0.49274 |         true |
|===================================================================================================================================|
| Iter | Eval   | Objective:  | Objective   | BestSoFar   | BestSoFar   | BoxConstraint|  KernelScale |      Epsilon |  Standardize |
|      | result | log(1+loss) | runtime     | (observed)  | (estim.)    |              |              |              |              |
|===================================================================================================================================|
|   21 | Accept |      2.9651 |    0.028332 |      2.9145 |      2.9144 |       3.9907 |       2.1347 |    0.0093749 |         true |
|   22 | Accept |      2.9617 |    0.033952 |      2.9145 |      2.9145 |       2.1916 |      0.58222 |    0.0095314 |         true |
|   23 | Accept |      2.9393 |    0.076092 |      2.9145 |      2.9145 |       620.79 |       603.43 |     0.010353 |        false |
|   24 | Accept |      3.9638 |    0.043062 |      2.9145 |      2.9145 |     0.026609 |       974.52 |    0.0094395 |        false |
|   25 | Accept |      3.3724 |      4.4338 |      2.9145 |      2.9145 |       988.78 |       24.099 |    0.0094952 |        false |
|   26 | Accept |      2.9253 |    0.065023 |      2.9145 |      2.9145 |       889.86 |       858.55 |      0.21283 |        false |
|   27 | Accept |      2.9316 |    0.068214 |      2.9145 |      2.9145 |       989.86 |       975.98 |     0.058976 |        false |
|   28 | Accept |      4.1889 |    0.027258 |      2.9145 |      2.9145 |       925.21 |       938.19 |       91.406 |        false |
|   29 | Accept |      2.9413 |     0.37091 |      2.9145 |      2.9145 |       987.54 |       281.98 |     0.096646 |        false |
|   30 | Best   |      2.9031 |    0.051604 |      2.9031 |      2.9032 |       93.995 |       603.79 |     0.099481 |        false |

__________________________________________________________
Optimization completed.
MaxObjectiveEvaluations of 30 reached.
Total function evaluations: 30
Total elapsed time: 24.9715 seconds
Total objective function evaluation time: 11.0269

Best observed feasible point:
    BoxConstraint    KernelScale    Epsilon     Standardize
    _____________    ___________    ________    ___________

       93.995          603.79       0.099481       false   

Observed objective function value = 2.9031
Estimated objective function value = 2.9032
Function evaluation time = 0.051604

Best estimated feasible point (according to models):
    BoxConstraint    KernelScale    Epsilon     Standardize
    _____________    ___________    ________    ___________

       93.995          603.79       0.099481       false   

Estimated objective function value = 2.9032
Estimated function evaluation time = 0.067925</pre>

<img src="../SVM_R6_media/figure_0.png" alt="图窗 1" loading="lazy" />

<pre class="mlx-out">Mdl = 
  RegressionSVM
                         ResponseName: 'Y'
                CategoricalPredictors: []
                    ResponseTransform: 'none'
                                Alpha: [92x1 double]
                                 Bias: 46.4880
                     KernelParameters: [1x1 struct]
                      NumObservations: 94
    HyperparameterOptimizationResults: [1x1 BayesianOptimization]
                       BoxConstraints: [94x1 double]
                      ConvergenceInfo: [1x1 struct]
                      IsSupportVector: [94x1 logical]
                               Solver: 'SMO'

  Properties, Methods</pre>

```matlab
% 优化搜索了 BoxConstraint、KernelScale 和 Epsilon。
% 输出是具有最小估计交叉验证损失的回归。
% The optimization searched over BoxConstraint, KernelScale, and Epsilon.
% The output is the regression with the minimum estimated cross-validation loss.
```
