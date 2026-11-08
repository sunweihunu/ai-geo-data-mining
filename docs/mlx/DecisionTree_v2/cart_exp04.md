# cart_exp04.mlx

「决策树（CART）」目录 · 对应书稿 **第08章 决策树** · 167.8 KB · 代码 29 行 · 图窗 4

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DecisionTree_v2/cart_exp04.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/DecisionTree_v2/cart_exp04.mlx" download>下载 cart_exp04.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

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
```

<img src="../cart_exp04_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
% 计算训练集的损失函数
resubLoss(Md0)  %  5.8158
```

<pre class="mlx-out">ans = 5.8158</pre>

```matlab
% 计算训练集的误差平方的均值（均方误差）
Y0_pre=predict(Md0,X);
mean((Y0_pre-Y).^2) % 缺失值没有处理
```

<pre class="mlx-out">ans = NaN</pre>

## 通过使用fitrtree的自动超参数优化，

找到将五倍交叉验证损失最小化的超参数。 为了重现性，设置随机种子并使用“预期改进加”采集功能。 Use Weight and Horsepower as predictors for MPG. Find hyperparameters that minimize five-fold cross-validation loss by using automatic hyperparameter optimization. For reproducibility, set the random seed and use the 'expected-improvement-plus' acquisition function.

```matlab
rng default
Md1 = fitrtree(X,Y,'OptimizeHyperparameters','auto',...
    'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName',...
    'expected-improvement-plus'))
```

<pre class="mlx-out">|======================================================================================|
| Iter | Eval   | Objective:  | Objective   | BestSoFar   | BestSoFar   |  MinLeafSize |
|      | result | log(1+loss) | runtime     | (observed)  | (estim.)    |              |
|======================================================================================|
|    1 | Best   |      3.2818 |    0.078052 |      3.2818 |      3.2818 |           28 |
|    2 | Accept |      3.4183 |    0.042363 |      3.2818 |      3.2888 |            1 |
|    3 | Best   |      3.1457 |    0.039174 |      3.1457 |      3.1628 |            4 |
|    4 | Best   |      2.9885 |    0.060411 |      2.9885 |      2.9885 |            9 |
|    5 | Accept |      2.9978 |    0.024709 |      2.9885 |      2.9885 |            7 |
|    6 | Accept |      3.0203 |    0.023016 |      2.9885 |      3.0013 |            8 |
|    7 | Accept |      2.9885 |    0.022924 |      2.9885 |      2.9981 |            9 |
|    8 | Best   |      2.9589 |     0.02673 |      2.9589 |      2.9589 |           10 |
|    9 | Accept |       3.078 |    0.021847 |      2.9589 |      2.9888 |           13 |
|   10 | Accept |      4.1881 |    0.029693 |      2.9589 |      2.9592 |           50 |
|   11 | Accept |      3.4182 |    0.022722 |      2.9589 |      2.9592 |            2 |
|   12 | Accept |      3.0376 |    0.023772 |      2.9589 |      2.9591 |            6 |
|   13 | Accept |      3.1453 |    0.023521 |      2.9589 |      2.9591 |           20 |
|   14 | Accept |      2.9589 |    0.037373 |      2.9589 |       2.959 |           10 |
|   15 | Accept |      3.0123 |    0.023748 |      2.9589 |      2.9728 |           11 |
|   16 | Accept |      2.9589 |    0.022511 |      2.9589 |      2.9593 |           10 |
|   17 | Accept |      3.3055 |    0.023479 |      2.9589 |      2.9593 |            3 |
|   18 | Accept |      2.9589 |    0.038031 |      2.9589 |      2.9592 |           10 |
|   19 | Accept |      3.4577 |    0.022504 |      2.9589 |      2.9591 |           37 |
|   20 | Accept |      3.2166 |    0.027208 |      2.9589 |       2.959 |           16 |
|======================================================================================|
| Iter | Eval   | Objective:  | Objective   | BestSoFar   | BestSoFar   |  MinLeafSize |
|      | result | log(1+loss) | runtime     | (observed)  | (estim.)    |              |
|======================================================================================|
|   21 | Accept |       3.107 |    0.024846 |      2.9589 |      2.9591 |            5 |
|   22 | Accept |      3.2818 |    0.022951 |      2.9589 |       2.959 |           24 |
|   23 | Accept |      3.3226 |    0.022101 |      2.9589 |       2.959 |           32 |
|   24 | Accept |      4.1881 |    0.022227 |      2.9589 |      2.9589 |           43 |
|   25 | Accept |      3.1789 |    0.025596 |      2.9589 |      2.9589 |           18 |
|   26 | Accept |      3.0992 |    0.032227 |      2.9589 |      2.9589 |           14 |
|   27 | Accept |      3.0556 |     0.02173 |      2.9589 |      2.9589 |           22 |
|   28 | Accept |      3.0459 |    0.022232 |      2.9589 |      2.9589 |           12 |
|   29 | Accept |      3.2818 |    0.024021 |      2.9589 |      2.9589 |           26 |
|   30 | Accept |      3.4361 |    0.023087 |      2.9589 |      2.9589 |           34 |

__________________________________________________________
Optimization completed.
MaxObjectiveEvaluations of 30 reached.
Total function evaluations: 30
Total elapsed time: 12.7576 seconds
Total objective function evaluation time: 0.87481

Best observed feasible point:
    MinLeafSize
    ___________

        10     

Observed objective function value = 2.9589
Estimated objective function value = 2.9589
Function evaluation time = 0.02673

Best estimated feasible point (according to models):
    MinLeafSize
    ___________

        10     

Estimated objective function value = 2.9589
Estimated function evaluation time = 0.027504</pre>

<img src="../cart_exp04_media/figure_1.png" alt="图窗 2" loading="lazy" />

<img src="../cart_exp04_media/figure_2.png" alt="图窗 3" loading="lazy" />

<pre class="mlx-out">Md1 = 
  RegressionTree
                         ResponseName: 'Y'
                CategoricalPredictors: []
                    ResponseTransform: 'none'
                      NumObservations: 94
    HyperparameterOptimizationResults: [1x1 BayesianOptimization]

  Properties, Methods</pre>

```matlab
view(Md1,'Mode','graph')
```

<img src="../cart_exp04_media/figure_3.png" alt="图窗 4" loading="lazy" />

```matlab
resubLoss(Md1) % 12.1673
```

<pre class="mlx-out">ans = 12.1673</pre>

```matlab
% 计算训练集的误差平方的均值（均方误差）
Y1_pre=predict(Md1,X);
mean((Y1_pre-Y).^2) % 缺失值没有处理
```

<pre class="mlx-out">ans = NaN</pre>

```matlab
% 模型结构大大精简了，训练集的性能下降了
```
