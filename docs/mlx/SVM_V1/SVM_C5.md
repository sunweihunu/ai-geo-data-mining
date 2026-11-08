# SVM_C5.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 20.5 KB · 代码 13 行 · 图窗 1

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_C5.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/SVM_V1/SVM_C5.mlx" download>下载 SVM_C5.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**优化 SVM 分类器**

使用 fitcsvm 自动优化超参数。 加载 ionosphere 数据集。

## 脚本内容

```matlab
% 优化 SVM 分类器
% 使用 fitcsvm 自动优化超参数。
%
% 加载 ionosphere 数据集。

load ionosphere
% 通过使用自动超参数优化，找到最小化五折交叉验证损失的超参数。
% 为了实现可再现性，请设置随机种子并使用 'expected-improvement-plus' 采集函数。

rng default
Mdl = fitcsvm(X,Y,'OptimizeHyperparameters','auto', ...
    'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName', ...
    'expected-improvement-plus'))
```

<pre class="mlx-out">|====================================================================================================================|
| Iter | Eval   | Objective   | Objective   | BestSoFar   | BestSoFar   | BoxConstraint|  KernelScale |  Standardize |
|      | result |             | runtime     | (observed)  | (estim.)    |              |              |              |
|====================================================================================================================|
|    1 | Best   |     0.35897 |     0.13855 |     0.35897 |     0.35897 |       3.8653 |       961.53 |         true |
|    2 | Best   |     0.13105 |      6.9825 |     0.13105 |     0.15896 |       429.99 |       0.2378 |        false |
|    3 | Accept |     0.35897 |    0.046303 |     0.13105 |     0.13431 |      0.11801 |       8.9479 |        false |
|    4 | Accept |      0.1339 |      3.1921 |     0.13105 |     0.13255 |    0.0010694 |    0.0032063 |         true |
|    5 | Accept |     0.19943 |      8.4922 |     0.13105 |     0.13109 |       973.65 |      0.13813 |        false |
|    6 | Accept |      0.1339 |      4.1525 |     0.13105 |      0.1311 |       156.67 |      0.39661 |        false |
|    7 | Accept |     0.15385 |      8.8008 |     0.13105 |     0.13111 |        1.094 |    0.0076002 |         true |
|    8 | Accept |     0.23362 |      8.9154 |     0.13105 |      0.1311 |       128.13 |    0.0010773 |         true |
|    9 | Accept |     0.23932 |      9.2851 |     0.13105 |     0.13109 |        386.1 |     0.038543 |         true |
|   10 | Accept |      0.1339 |     0.28853 |     0.13105 |     0.13109 |       315.77 |       2.7922 |        false |
|   11 | Accept |     0.13675 |      6.2675 |     0.13105 |     0.13245 |    0.0043379 |     0.002549 |         true |
|   12 | Accept |     0.19658 |      9.3781 |     0.13105 |     0.13218 |     0.090024 |    0.0010118 |         true |
|   13 | Best   |     0.11111 |    0.051259 |     0.11111 |     0.11112 |    0.0020751 |      0.14377 |         true |
|   14 | Accept |     0.35897 |    0.045479 |     0.11111 |     0.11539 |    0.0011183 |       38.992 |         true |
|   15 | Accept |     0.12821 |     0.14279 |     0.11111 |     0.12133 |    0.0041039 |     0.028542 |         true |
|   16 | Accept |     0.12821 |     0.11293 |     0.11111 |     0.11743 |     0.042304 |     0.099772 |         true |
|   17 | Accept |      0.1339 |       4.029 |     0.11111 |     0.11966 |        985.9 |      0.97042 |        false |
|   18 | Accept |     0.12251 |    0.052924 |     0.11111 |     0.12036 |    0.0010131 |     0.062073 |         true |
|   19 | Accept |     0.12536 |    0.061771 |     0.11111 |     0.12019 |    0.0047321 |     0.088008 |         true |
|   20 | Accept |     0.12821 |    0.076345 |     0.11111 |     0.12047 |    0.0010814 |      0.17444 |         true |
|====================================================================================================================|
| Iter | Eval   | Objective   | Objective   | BestSoFar   | BestSoFar   | BoxConstraint|  KernelScale |  Standardize |
|      | result |             | runtime     | (observed)  | (estim.)    |              |              |              |
|====================================================================================================================|
|   21 | Accept |     0.12821 |      1.5597 |     0.11111 |     0.12057 |     0.023965 |     0.019394 |         true |
|   22 | Accept |     0.12536 |     0.16092 |     0.11111 |     0.12062 |    0.0010834 |     0.013375 |         true |
|   23 | Accept |     0.12251 |    0.067611 |     0.11111 |     0.12083 |    0.0033216 |     0.083882 |         true |
|   24 | Accept |     0.12821 |     0.72317 |     0.11111 |     0.12085 |       143.32 |      0.89899 |        false |
|   25 | Accept |     0.12251 |    0.047966 |     0.11111 |     0.12095 |     0.001011 |     0.075658 |         true |
|   26 | Accept |     0.35897 |    0.043153 |     0.11111 |       0.121 |       998.83 |       860.63 |        false |
|   27 | Accept |     0.11966 |    0.054546 |     0.11111 |     0.12073 |     0.005974 |      0.15671 |         true |
|   28 | Accept |     0.12821 |      2.9071 |     0.11111 |     0.12085 |     0.020203 |    0.0073686 |        false |
|   29 | Accept |      0.1339 |      5.7657 |     0.11111 |      0.1208 |    0.0011575 |    0.0010168 |        false |
|   30 | Accept |     0.22792 |      9.1119 |     0.11111 |     0.12088 |      0.14671 |    0.0010761 |        false |

__________________________________________________________
Optimization completed.
MaxObjectiveEvaluations of 30 reached.
Total function evaluations: 30
Total elapsed time: 99.2034 seconds
Total objective function evaluation time: 90.9539

Best observed feasible point:
    BoxConstraint    KernelScale    Standardize
    _____________    ___________    ___________

      0.0020751        0.14377         true    

Observed objective function value = 0.11111
Estimated objective function value = 0.12082
Function evaluation time = 0.051259

Best estimated feasible point (according to models):
    BoxConstraint    KernelScale    Standardize
    _____________    ___________    ___________

      0.0033216       0.083882         true    

Estimated objective function value = 0.12088
Estimated function evaluation time = 0.060542</pre>

<img src="../SVM_C5_media/figure_0.png" alt="图窗 1" loading="lazy" />

<pre class="mlx-out">Mdl = 
  ClassificationSVM
                         ResponseName: 'Y'
                CategoricalPredictors: []
                           ClassNames: {'b'  'g'}
                       ScoreTransform: 'none'
                      NumObservations: 351
    HyperparameterOptimizationResults: [1x1 BayesianOptimization]
                                Alpha: [94x1 double]
                                 Bias: 0.0338
                     KernelParameters: [1x1 struct]
                                   Mu: [0.8917 0 0.6413 0.0444 0.6011 0.1159 0.5501 0.1194 0.5118 0.1813 0.4762 0.1550 0.4008 0.0934 0.3442 0.0711 0.3819 -0.0036 0.3594 -0.0240 0.3367 0.0083 0.3625 -0.0574 0.3961 -0.0712 0.5416 -0.0695 … ] (1x34 double)
                                Sigma: [0.3112 0 0.4977 0.4414 0.5199 0.4608 0.4927 0.5207 0.5071 0.4839 0.5635 0.4948 0.6222 0.4949 0.6528 0.4584 0.6180 0.4968 0.6263 0.5191 0.6098 0.5182 0.6038 0.5275 0.5785 0.5085 0.5162 0.5500 … ] (1x34 double)
                       BoxConstraints: [351x1 double]
                      ConvergenceInfo: [1x1 struct]
                      IsSupportVector: [351x1 logical]
                               Solver: 'SMO'

  Properties, Methods</pre>
