# SVM_C14.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 136.4 KB · 代码 128 行 · 图窗 6

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_C14.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/SVM_V1/SVM_C14.mlx" download>下载 SVM_C14.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**使用 bayesopt 优化交叉验证分类器**

此示例说明如何使用 bayesopt 函数优化 SVM 分类。 或者，您可以使用 OptimizeHyperparameters 名称-值参数来优化分类器。

## 脚本内容

```matlab
% 使用 bayesopt 优化交叉验证分类器
% 此示例说明如何使用 bayesopt 函数优化 SVM 分类。
% 或者，您可以使用 OptimizeHyperparameters 名称-值参数来优化分类器。
% 有关示例，请参阅使用贝叶斯优化优化分类器拟合。
% Optimize Cross-Validated Classifier Using bayesopt
% This example shows how to optimize an SVM classification using the bayesopt function.
% Alternatively, you can optimize a classifier by using
% the OptimizeHyperparameters name-value argument.
% For an example, see Optimize Classifier Fit Using Bayesian Optimization.
```

## 生成数据

分类适用于来自高斯混合模型的点的位置。在 The Elements of Statistical Learning, Hastie、Tibshirani 和 Friedman (2009) 中，第 17 页描述了该模型。该模型首先为“绿色”类生成 10 个基点，分布为具有均值 (1,0) 和单位方差的二维独立法线。它还为“红色”类生成 10 个基点，分布为具有均值 (0,1) 和单位方差的二维独立法线。对于每个类（绿色和红色），生成 100 个随机点，如下所示： 随机均匀地选择一个合适颜色的基点m。 生成具有均值为 m 且方差为 I/5 的二维正态分布的独立随机点，其中 I 是 2×2 单位矩阵。在这个例子中，使用方差 I/50 来更清楚地展示优化的优势。 为每个类生成 10 个基点。 Generate Data The classification works on locations of points from a Gaussian mixture model. In The Elements of Statistical Learning, Hastie, Tibshirani, and Friedman (2009), page 17 describes the model. The model begins with generating 10 base points for a "green" class, distributed as 2-D independent normals with mean (1,0) and unit variance. It also generates 10 base points for a "red" class, distributed as 2-D independent normals with mean (0,1) and unit variance. For each class (green and red), generate 100 random points as follows: Choose a base point m of the appropriate color uniformly at random. Generate an independent random point with 2-D normal distribution with mean m and variance I/5, where I is the 2-by-2 identity matrix. In this example, use a variance I/50 to show the advantage of optimization more clearly. Generate the 10 base points for each class.

```matlab
rng('default') % For reproducibility
grnpop = mvnrnd([1,0],eye(2),10);
redpop = mvnrnd([0,1],eye(2),10);
% View the base points.

plot(grnpop(:,1),grnpop(:,2),'go')
hold on
plot(redpop(:,1),redpop(:,2),'ro')
hold off
```

<img src="../SVM_C14_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
% 由于一些红色基点靠近绿色基点，因此仅根据位置很难对数据点进行分类。
% 生成每个类的 100 个数据点。
% Since some red base points are close to green base points,
% it can be difficult to classify the data points based on location alone.
% Generate the 100 data points of each class.

redpts = zeros(100,2);grnpts = redpts;
for i = 1:100
    grnpts(i,:) = mvnrnd(grnpop(randi(10),:),eye(2)*0.02);
    redpts(i,:) = mvnrnd(redpop(randi(10),:),eye(2)*0.02);
end

% View the data points.
figure
plot(grnpts(:,1),grnpts(:,2),'go')
hold on
plot(redpts(:,1),redpts(:,2),'ro')
hold off
```

<img src="../SVM_C14_media/figure_1.png" alt="图窗 2" loading="lazy" />

## 准备分类数据

将数据放入一个矩阵中，并制作一个向量 grp 标记每个点的类别。 1表示绿色类，-1表示红色类。 Prepare Data For Classification Put the data into one matrix, and make a vector grp that labels the class of each point. 1 indicates the green class, and -1 indicates the red class.

```matlab
cdata = [grnpts;redpts];
grp = ones(200,1);
grp(101:200) = -1;
```

## 准备交叉验证

为交叉验证设置一个分区。 此步骤修复了优化在每个步骤中使用的训练集和测试集。 Prepare Cross-Validation Set up a partition for cross-validation. This step fixes the train and test sets that the optimization uses at each step.

```matlab
c = cvpartition(200,'KFold',10);

% 为贝叶斯优化准备变量
% 设置一个函数，该函数接受输入 z = [rbf_sigma,boxconstraint] 并返回 z 的交叉验证损失值。 将 z 的分量作为 1e-5 和 1e5 之间的正对数转换变量。 选择范围很广，因为您不知道哪些值可能是好的。
% Prepare Variables for Bayesian Optimization
% Set up a function that takes an input z = [rbf_sigma,boxconstraint] and returns the cross-validation loss value of z. Take the components of z as positive, log-transformed variables between 1e-5 and 1e5. Choose a wide range, because you don't know which values are likely to be good.

sigma = optimizableVariable('sigma',[1e-5,1e5],'Transform','log');
box = optimizableVariable('box',[1e-5,1e5],'Transform','log');
```

## 目标函数

此函数句柄计算参数 [sigma,box] 处的交叉验证损失。 有关详细信息，请参阅 kfoldLoss。 bayesopt 将变量 z 作为单行表传递给目标函数。 Objective Function This function handle computes the cross-validation loss at parameters [sigma,box]. For details, see kfoldLoss. bayesopt passes the variable z to the objective function as a one-row table.

```matlab
minfn = @(z)kfoldLoss(fitcsvm(cdata,grp,'CVPartition',c,...
    'KernelFunction','rbf','BoxConstraint',z.box,...
    'KernelScale',z.sigma));
```

## 优化分类器

使用 bayesopt 搜索最佳参数 [sigma,box]。 为了重现性，请选择“预期改进加”采集功能。 默认采集函数取决于运行时间，因此可以给出不同的结果。 Optimize Classifier Search for the best parameters [sigma,box] using bayesopt. For reproducibility, choose the 'expected-improvement-plus' acquisition function. The default acquisition function depends on run time, and so can give varying results.

```matlab
results = bayesopt(minfn,[sigma,box],'IsObjectiveDeterministic',true,...
    'AcquisitionFunctionName','expected-improvement-plus')
```

<pre class="mlx-out">|=====================================================================================================|
| Iter | Eval   | Objective   | Objective   | BestSoFar   | BestSoFar   |        sigma |          box |
|      | result |             | runtime     | (observed)  | (estim.)    |              |              |
|=====================================================================================================|
|    1 | Best   |        0.61 |    0.078152 |        0.61 |        0.61 |   0.00013375 |        13929 |
|    2 | Best   |       0.345 |    0.091827 |       0.345 |       0.345 |        24526 |        1.936 |
|    3 | Accept |        0.61 |    0.099195 |       0.345 |       0.345 |    0.0026459 |   0.00084929 |
|    4 | Accept |       0.345 |    0.051495 |       0.345 |       0.345 |       3506.3 |   6.7427e-05 |
|    5 | Accept |       0.345 |    0.056167 |       0.345 |       0.345 |       9135.2 |       571.87 |
|    6 | Accept |       0.345 |    0.057698 |       0.345 |       0.345 |        99701 |        10223 |
|    7 | Best   |       0.295 |     0.05351 |       0.295 |       0.295 |       455.88 |       9957.4 |
|    8 | Best   |        0.24 |     0.69781 |        0.24 |        0.24 |        31.56 |        99389 |
|    9 | Accept |        0.24 |      0.9007 |        0.24 |        0.24 |       10.451 |        64429 |
|   10 | Accept |        0.35 |    0.059988 |        0.24 |        0.24 |       17.331 |   1.0264e-05 |
|   11 | Best   |        0.23 |     0.61787 |        0.23 |        0.23 |       16.005 |        90155 |
|   12 | Best   |         0.1 |     0.09615 |         0.1 |         0.1 |      0.36562 |        80878 |
|   13 | Accept |       0.115 |    0.063693 |         0.1 |         0.1 |       0.1793 |        68459 |
|   14 | Accept |       0.105 |    0.064091 |         0.1 |         0.1 |       0.2267 |        95421 |
|   15 | Best   |       0.095 |    0.051956 |       0.095 |       0.095 |      0.28999 |    0.0058227 |
|   16 | Best   |       0.075 |    0.054433 |       0.075 |       0.075 |      0.30554 |       8.9017 |
|   17 | Accept |       0.085 |    0.049803 |       0.075 |       0.075 |      0.41122 |       4.4476 |
|   18 | Accept |       0.085 |     0.05144 |       0.075 |       0.075 |      0.25565 |       7.8038 |
|   19 | Accept |       0.075 |    0.050594 |       0.075 |       0.075 |      0.32869 |       18.076 |
|   20 | Accept |       0.085 |    0.051998 |       0.075 |       0.075 |      0.32442 |       5.2118 |
|=====================================================================================================|
| Iter | Eval   | Objective   | Objective   | BestSoFar   | BestSoFar   |        sigma |          box |
|      | result |             | runtime     | (observed)  | (estim.)    |              |              |
|=====================================================================================================|
|   21 | Accept |         0.3 |    0.053173 |       0.075 |       0.075 |       1.3592 |    0.0098067 |
|   22 | Accept |        0.12 |    0.054056 |       0.075 |       0.075 |      0.17515 |   0.00070913 |
|   23 | Accept |       0.175 |    0.058164 |       0.075 |       0.075 |       0.1252 |     0.010749 |
|   24 | Accept |       0.105 |     0.05638 |       0.075 |       0.075 |       1.1664 |        31.13 |
|   25 | Accept |         0.1 |    0.056555 |       0.075 |       0.075 |      0.57465 |       2013.8 |
|   26 | Accept |        0.12 |    0.053356 |       0.075 |       0.075 |      0.42922 |   1.1602e-05 |
|   27 | Accept |        0.12 |    0.055207 |       0.075 |       0.075 |      0.42956 |   0.00027218 |
|   28 | Accept |       0.095 |    0.057458 |       0.075 |       0.075 |       0.4806 |       13.452 |
|   29 | Accept |       0.105 |    0.071769 |       0.075 |       0.075 |      0.19755 |       943.87 |
|   30 | Accept |       0.205 |    0.058836 |       0.075 |       0.075 |       3.5051 |       93.492 |

__________________________________________________________
Optimization completed.
MaxObjectiveEvaluations of 30 reached.
Total function evaluations: 30
Total elapsed time: 16.6231 seconds
Total objective function evaluation time: 3.8735

Best observed feasible point:
     sigma      box  
    _______    ______

    0.30554    8.9017

Observed objective function value = 0.075
Estimated objective function value = 0.075
Function evaluation time = 0.054433

Best estimated feasible point (according to models):
     sigma      box  
    _______    ______

    0.32869    18.076

Estimated objective function value = 0.075
Estimated function evaluation time = 0.054116</pre>

<img src="../SVM_C14_media/figure_2.png" alt="图窗 3" loading="lazy" />

<img src="../SVM_C14_media/figure_3.png" alt="图窗 4" loading="lazy" />

<pre class="mlx-out">results = 
  BayesianOptimization with properties:

                      ObjectiveFcn: @(z)kfoldLoss(fitcsvm(cdata,grp,'CVPartition',c,'KernelFunction','rbf','BoxConstraint',z.box,'KernelScale',z.sigma))
              VariableDescriptions: [1x2 optimizableVariable]
                           Options: [1x1 struct]
                      MinObjective: 0.0750
                   XAtMinObjective: [1x2 table]
             MinEstimatedObjective: 0.0750
          XAtMinEstimatedObjective: [1x2 table]
           NumObjectiveEvaluations: 30
                  TotalElapsedTime: 16.6231
                         NextPoint: [1x2 table]
                            XTrace: [30x2 table]
                    ObjectiveTrace: [30x1 double]
                  ConstraintsTrace: []
                     UserDataTrace: {30x1 cell}
      ObjectiveEvaluationTimeTrace: [30x1 double]
                IterationTimeTrace: [30x1 double]
                        ErrorTrace: [30x1 double]
                  FeasibilityTrace: [30x1 logical]
       FeasibilityProbabilityTrace: [30x1 double]
               IndexOfMinimumTrace: [30x1 double]
             ObjectiveMinimumTrace: [30x1 double]
    EstimatedObjectiveMinimumTrace: [30x1 double]</pre>

```matlab
% 从 XAtMinEstimatedObjective 属性或使用 bestPoint 函数获取最佳估计可行点。 默认情况下，bestPoint 函数使用“min-visited-upper-confidence-interval”标准。 有关详细信息，请参阅 bestPoint 的 Criterion 名称-值参数。
% Obtain the best estimated feasible point from the XAtMinEstimatedObjective property or by using the bestPoint function. By default, the bestPoint function uses the 'min-visited-upper-confidence-interval' criterion. For details, see the Criterion name-value argument of bestPoint.

results.XAtMinEstimatedObjective
```

```matlab
% ans=1×2 table
%      sigma      box
%     _______    ______
%
%     0.32869    18.076

z = bestPoint(results)
```

```matlab
% z=1×2 table
%      sigma      box
%     _______    ______
%
%     0.32869    18.076

% 使用最佳点来训练一个新的、优化的 SVM 分类器。
% Use the best point to train a new, optimized SVM classifier.

SVMModel = fitcsvm(cdata,grp,'KernelFunction','rbf', ...
    'KernelScale',z.sigma,'BoxConstraint',z.box);

% 要可视化支持向量分类器，预测网格上的分数。
% To visualize the support vector classifier, predict scores over a grid.

d = 0.02;
[x1Grid,x2Grid] = meshgrid(min(cdata(:,1)):d:max(cdata(:,1)), ...
    min(cdata(:,2)):d:max(cdata(:,2)));
xGrid = [x1Grid(:),x2Grid(:)];
[~,scores] = predict(SVMModel,xGrid);

% 绘制分类边界。
% Plot the classification boundaries.

figure
h(1:2) = gscatter(cdata(:,1),cdata(:,2),grp,'rg','+*');
hold on
h(3) = plot(cdata(SVMModel.IsSupportVector,1) ,...
    cdata(SVMModel.IsSupportVector,2),'ko');
contour(x1Grid,x2Grid,reshape(scores(:,2),size(x1Grid)),[0 0],'k');
legend(h,{'-1','+1','Support Vectors'},'Location','Southeast');
```

<img src="../SVM_C14_media/figure_4.png" alt="图窗 5" loading="lazy" />

## 评估新数据的准确性

生成和分类新的测试数据点。 Evaluate Accuracy on New Data Generate and classify new test data points.

```matlab
grnobj = gmdistribution(grnpop,.2*eye(2));
redobj = gmdistribution(redpop,.2*eye(2));

newData = random(grnobj,10);
newData = [newData;random(redobj,10)];
grpData = ones(20,1);  % green = 1
grpData(11:20) = -1; % red = -1

v = predict(SVMModel,newData);

% 计算测试数据集的误分类率。
% Compute the misclassification rates on the test data set.

L = loss(SVMModel,newData,grpData)
```

<pre class="mlx-out">L = 0.3500</pre>

```matlab
% L = 0.3500
```

## 查看哪些新数据点被正确分类。

用红色圈出正确分类的点，用黑色圈出分类错误的点。 See which new data points are correctly classified. Circle the correctly classified points in red, and the incorrectly classified points in black.

```matlab
h(4:5) = gscatter(newData(:,1),newData(:,2),v,'mc','**');

mydiff = (v == grpData); % Classified correctly

for ii = mydiff % Plot red squares around correct pts
    h(6) = plot(newData(ii,1),newData(ii,2),'rs','MarkerSize',12);
end

for ii = not(mydiff) % Plot black squares around incorrect pts
    h(7) = plot(newData(ii,1),newData(ii,2),'ks','MarkerSize',12);
end
legend(h,{'-1 (training)','+1 (training)','Support Vectors', ...
    '-1 (classified)','+1 (classified)', ...
    'Correctly Classified','Misclassified'}, ...
    'Location','Southeast');
hold off
```

<img src="../SVM_C14_media/figure_5.png" alt="图窗 6" loading="lazy" />
