# SVM_C7.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 5.4 KB · 代码 58 行 · 运行输出 2

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_C7.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/SVM_V1/SVM_C7.mlx" download>下载 SVM_C7.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**预测 SVM 分类器的标签和后验概率**

使用 SVM 分类器标记新的观察结果。 加载电离层数据集。

## 脚本内容

```matlab
% 预测 SVM 分类器的标签和后验概率
% 使用 SVM 分类器标记新的观察结果。
%
% 加载电离层数据集。
% 假设最后 10 个数据点是新观察结果，在训练 SVM 分类器之后刚获得。
% Predict Labels and Posterior Probabilities of SVM Classifiers
% Label new observations using an SVM classifier.
%
% Load the ionosphere data set.
% Assume that the last 10 observations become available
% after you train the SVM classifier.
%
% load ionosphere
rng(1); % For reproducibility
n = size(X,1);       % Training sample size
isInds = 1:(n-10);   % In-sample indices
oosInds = (n-9):n;   % Out-of-sample indices
% 训练一个 SVM 分类器。
% 标准化数据并指定 'g' 是正类。
% 通过减少经过训练的 SVM 分类器的大小来节省内存。
% Train an SVM classifier.
% Standardize the data and specify that % 'g' is the positive class.
% Conserve memory by reducing the size of the trained SVM classifier.

SVMModel = fitcsvm(X(isInds,:),Y(isInds),'Standardize',true,...
    'ClassNames',{'b','g'});
CompactSVMModel = compact(SVMModel);
whos('SVMModel','CompactSVMModel')
```

<pre class="mlx-out">  Name                 Size             Bytes  Class                                                 Attributes

  CompactSVMModel      1x1              30651  classreg.learning.classif.CompactClassificationSVM              
  SVMModel             1x1             137751  ClassificationSVM</pre>

```matlab
% CompactClassificationSVM 分类器（CompactSVMModel）使用更少的空间
% 比 ClassificationSVM 分类器 (SVMModel)，因为 SVMModel 存储数据。
% 估计最佳得分到后验概率转换函数。
% The CompactClassificationSVM classifier (CompactSVMModel) uses less space
% than the ClassificationSVM classifier (SVMModel) because SVMModel stores the data.
% Estimate the optimal score-to-posterior-probability transformation function.

CompactSVMModel = fitPosterior(CompactSVMModel,...
    X(isInds,:),Y(isInds))
```

<pre class="mlx-out">CompactSVMModel = 
  CompactClassificationSVM
             ResponseName: 'Y'
    CategoricalPredictors: []
               ClassNames: {'b'  'g'}
           ScoreTransform: '@(S)sigmoid(S,-1.968336e+00,3.121821e-01)'
                    Alpha: [88x1 double]
                     Bias: -0.2142
         KernelParameters: [1x1 struct]
                       Mu: [0.8886 0 0.6365 0.0457 0.5933 0.1200 0.5414 0.1217 0.5020 0.1872 0.4659 0.1596 0.3889 0.0970 0.3308 0.0723 0.3685 -0.0039 0.3453 -0.0256 0.3231 0.0097 0.3490 -0.0596 0.3839 -0.0731 0.5343 -0.0718 0.3659 … ] (1x34 double)
                    Sigma: [0.3151 0 0.5032 0.4476 0.5251 0.4668 0.4966 0.5275 0.5107 0.4896 0.5681 0.5011 0.6267 0.5009 0.6569 0.4639 0.6214 0.5035 0.6296 0.5265 0.6128 0.5250 0.6067 0.5349 0.5817 0.5157 0.5212 0.5577 0.5787 0.5151 … ] (1x34 double)
           SupportVectors: [88x34 double]
      SupportVectorLabels: [88x1 double]

  Properties, Methods</pre>

```matlab
% 最优得分变换函数（CompactSVMModel.ScoreTransform）是 sigmoid 函数，
% 因为这些类是不可分割的。
% 预测样本外（测试集）的待测样本的标签和正类后验概率。
% 因为真实标签可用，所以将它们与预测标签进行比较。
% The optimal score transformation function (CompactSVMModel.ScoreTransform)
% is the sigmoid function because the classes are inseparable.
% Predict the out-of-sample labels and positive class posterior probabilities.
% Because true labels are available, compare them with the predicted labels.

[labels,PostProbs] = predict(CompactSVMModel,X(oosInds,:));
table(Y(oosInds),labels,PostProbs(:,2),'VariableNames',...
    {'TrueLabels','PredictedLabels','PosClassPosterior'})
```

```matlab
% PostProbs 是一个 10×2 矩阵，
% 其中第一列是负类后验概率，
% 第二列是正类后验概率
% 对应于新的观察结果。
% PostProbs is a 10-by-2 matrix,
% where the first column is the negative class posterior probabilities,
% and the second column is the positive class posterior probabilities
% corresponding to the new observations.
```
