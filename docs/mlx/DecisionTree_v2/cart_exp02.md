# cart_exp02.mlx

「决策树（CART）」目录 · 对应书稿 **第08章 决策树** · 151.0 KB · 代码 42 行 · 图窗 6

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DecisionTree_v2/cart_exp02.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/DecisionTree_v2/cart_exp02.mlx" download>下载 cart_exp02.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**Optimize Classification Tree**

This example shows how to optimize hyperparameters automatically using fitctree. The example uses Fisher's iris data.

## 脚本内容

```matlab
% Optimize Classification Tree
% This example shows how to optimize hyperparameters automatically using fitctree.
% The example uses Fisher's iris data.
% Load Fisher's iris data.
load fisheriris
X = meas;
Y = species;

% 不经过优化的训练分类树
Md0 = fitctree(X,Y);
% 计算分类模型Md0中的损失函数
resuberror = resubLoss(Md0)   % resuberror =  0.0200
```

<pre class="mlx-out">resuberror = 0.0200</pre>

```matlab
% 预测
cc0=predict(Md0,meas);
figure
cm0 = confusionchart(species,cc0);
cm0.Title = '不经过优化的分类树 ';
```

<img src="../cart_exp02_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
% 展示结构
view(Md0,'Mode','graph');
```

<img src="../cart_exp02_media/figure_1.png" alt="图窗 2" loading="lazy" />

```matlab
% 经过优化的训练分类树
% rng(12345) %  resuberror =    0.0267
rng(6794050) %  resuberror =  0.0267

% Optimize the cross-validation loss of the classifier,
% using the data in meas to predict the response in species.
Mdl = fitctree(X,Y,'OptimizeHyperparameters','auto')
```

<pre class="mlx-out">|======================================================================================|
| Iter | Eval   | Objective   | Objective   | BestSoFar   | BestSoFar   |  MinLeafSize |
|      | result |             | runtime     | (observed)  | (estim.)    |              |
|======================================================================================|
|    1 | Best   |    0.033333 |     0.98522 |    0.033333 |    0.033333 |            2 |
|    2 | Accept |     0.66667 |      0.3192 |    0.033333 |    0.066084 |           72 |
|    3 | Accept |    0.046667 |     0.10098 |    0.033333 |    0.081944 |           24 |
|    4 | Accept |    0.046667 |    0.065775 |    0.033333 |    0.084552 |            7 |
|    5 | Accept |    0.046667 |     0.14664 |    0.033333 |    0.033351 |           22 |
|    6 | Accept |        0.04 |    0.039951 |    0.033333 |    0.033649 |            5 |
|    7 | Accept |        0.04 |    0.038817 |    0.033333 |    0.038689 |            1 |
|    8 | Accept |    0.046667 |    0.034124 |    0.033333 |    0.033288 |           14 |
|    9 | Best   |    0.026667 |     0.04235 |    0.026667 |    0.027363 |            3 |
|   10 | Accept |    0.026667 |    0.043932 |    0.026667 |    0.026689 |            3 |
|   11 | Accept |    0.033333 |    0.035304 |    0.026667 |    0.026727 |            4 |
|   12 | Accept |    0.026667 |     0.03564 |    0.026667 |    0.026704 |            3 |
|   13 | Accept |    0.026667 |    0.036118 |    0.026667 |    0.026692 |            3 |
|   14 | Accept |     0.33333 |     0.03543 |    0.026667 |    0.026675 |           41 |
|   15 | Accept |    0.046667 |     0.04447 |    0.026667 |    0.026675 |           10 |
|   16 | Accept |    0.046667 |     0.03978 |    0.026667 |    0.026675 |           17 |
|   17 | Accept |    0.046667 |    0.038162 |    0.026667 |    0.026668 |           30 |
|   18 | Accept |    0.046667 |    0.037317 |    0.026667 |    0.026669 |            6 |
|   19 | Accept |     0.33333 |    0.047842 |    0.026667 |    0.028394 |           55 |
|   20 | Accept |    0.033333 |    0.036307 |    0.026667 |    0.028927 |            2 |
|======================================================================================|
| Iter | Eval   | Objective   | Objective   | BestSoFar   | BestSoFar   |  MinLeafSize |
|      | result |             | runtime     | (observed)  | (estim.)    |              |
|======================================================================================|
|   21 | Accept |        0.04 |    0.041424 |    0.026667 |    0.028922 |            1 |
|   22 | Accept |    0.033333 |     0.04058 |    0.026667 |    0.029175 |            2 |
|   23 | Accept |    0.046667 |    0.035305 |    0.026667 |    0.029076 |           17 |
|   24 | Accept |    0.046667 |    0.035301 |    0.026667 |    0.029091 |            8 |
|   25 | Accept |    0.046667 |    0.034148 |    0.026667 |    0.028866 |           27 |
|   26 | Accept |    0.033333 |    0.033848 |    0.026667 |    0.028965 |            2 |
|   27 | Accept |    0.046667 |    0.045086 |    0.026667 |    0.028933 |           12 |
|   28 | Accept |    0.033333 |    0.039218 |    0.026667 |    0.028938 |            4 |
|   29 | Accept |    0.046667 |    0.034784 |    0.026667 |    0.028945 |           35 |
|   30 | Accept |    0.046667 |    0.032838 |    0.026667 |    0.028843 |           31 |

__________________________________________________________
Optimization completed.
MaxObjectiveEvaluations of 30 reached.
Total function evaluations: 30
Total elapsed time: 18.1636 seconds
Total objective function evaluation time: 2.5759

Best observed feasible point:
    MinLeafSize
    ___________

         3     

Observed objective function value = 0.026667
Estimated objective function value = 0.028843
Function evaluation time = 0.04235

Best estimated feasible point (according to models):
    MinLeafSize
    ___________

         3     

Estimated objective function value = 0.028843
Estimated function evaluation time = 0.050183</pre>

<img src="../cart_exp02_media/figure_2.png" alt="图窗 3" loading="lazy" />

<img src="../cart_exp02_media/figure_3.png" alt="图窗 4" loading="lazy" />

<pre class="mlx-out">Mdl = 
  ClassificationTree
                         ResponseName: 'Y'
                CategoricalPredictors: []
                           ClassNames: {'setosa'  'versicolor'  'virginica'}
                       ScoreTransform: 'none'
                      NumObservations: 150
    HyperparameterOptimizationResults: [1x1 BayesianOptimization]

  Properties, Methods</pre>

```matlab
% 计算分类模型Mdl中的损失函数
resuberror = resubLoss(Mdl)
```

<pre class="mlx-out">resuberror = 0.0267</pre>

```matlab
% 预测
cc1=predict(Mdl,meas);
cm1 = confusionchart(species,cc1);
cm1.Title = '优化的分类树 ';
```

<img src="../cart_exp02_media/figure_4.png" alt="图窗 5" loading="lazy" />

```matlab
% 展示结构
view(Mdl,'Mode','graph');
```

<img src="../cart_exp02_media/figure_5.png" alt="图窗 6" loading="lazy" />

```matlab
% 本示例因为数据规模太小，所有数据集都作为了训练集
% 经过优化后，损失函数还略微变差了
% 但是模型树的结构精简了，泛化能力可能提高了
```
