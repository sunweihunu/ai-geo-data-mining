# SVM_C8.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 4.8 KB · 代码 46 行 · 运行输出 3

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_C8.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/SVM_V1/SVM_C8.mlx" download>下载 SVM_C8.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**减少 SVM 分类器的大小**

通过删除训练数据来减小完整支持向量机 (SVM) 分类器的大小。全SVM分类器（即ClassificationSVM分类器）保存训练数据。为了提高效率，请使用较小的分类器。 加载电离层数据集。

## 脚本内容

```matlab
% 减少 SVM 分类器的大小
% 通过删除训练数据来减小完整支持向量机 (SVM) 分类器的大小。全SVM分类器（即ClassificationSVM分类器）保存训练数据。为了提高效率，请使用较小的分类器。
% 加载电离层数据集。
% Reduce Size of SVM Classifier
% Reduce the size of a full support vector machine (SVM) classifier by removing the training data. Full SVM classifiers (that is, ClassificationSVM classifiers) hold the training data. To improve efficiency, use a smaller classifier.
% Load the ionosphere data set.

load ionosphere
% 训练 SVM 分类器。标准化预测数据并指定类的顺序。
% Train an SVM classifier.
% Standardize the predictor data and specify the order of the classes.

SVMModel = fitcsvm(X,Y,'Standardize',true,...
    'ClassNames',{'b','g'})
```

<pre class="mlx-out">SVMModel = 
  ClassificationSVM
             ResponseName: 'Y'
    CategoricalPredictors: []
               ClassNames: {'b'  'g'}
           ScoreTransform: 'none'
          NumObservations: 351
                    Alpha: [90x1 double]
                     Bias: -0.1342
         KernelParameters: [1x1 struct]
                       Mu: [0.8917 0 0.6413 0.0444 0.6011 0.1159 0.5501 0.1194 0.5118 0.1813 0.4762 0.1550 0.4008 0.0934 0.3442 0.0711 0.3819 -0.0036 0.3594 -0.0240 0.3367 0.0083 0.3625 -0.0574 0.3961 -0.0712 0.5416 -0.0695 0.3784 … ] (1x34 double)
                    Sigma: [0.3112 0 0.4977 0.4414 0.5199 0.4608 0.4927 0.5207 0.5071 0.4839 0.5635 0.4948 0.6222 0.4949 0.6528 0.4584 0.6180 0.4968 0.6263 0.5191 0.6098 0.5182 0.6038 0.5275 0.5785 0.5085 0.5162 0.5500 0.5759 0.5080 … ] (1x34 double)
           BoxConstraints: [351x1 double]
          ConvergenceInfo: [1x1 struct]
          IsSupportVector: [351x1 logical]
                   Solver: 'SMO'

  Properties, Methods</pre>

```matlab
% SVMModel 是一个ClassificationSVM 分类器。
% SVMModel is a ClassificationSVM classifier.

% 减小SVMModel（SVM 分类器）的大小
% Reduce the size of the SVM classifier.

CompactSVMModel = compact(SVMModel)
```

<pre class="mlx-out">CompactSVMModel = 
  CompactClassificationSVM
             ResponseName: 'Y'
    CategoricalPredictors: []
               ClassNames: {'b'  'g'}
           ScoreTransform: 'none'
                    Alpha: [90x1 double]
                     Bias: -0.1342
         KernelParameters: [1x1 struct]
                       Mu: [0.8917 0 0.6413 0.0444 0.6011 0.1159 0.5501 0.1194 0.5118 0.1813 0.4762 0.1550 0.4008 0.0934 0.3442 0.0711 0.3819 -0.0036 0.3594 -0.0240 0.3367 0.0083 0.3625 -0.0574 0.3961 -0.0712 0.5416 -0.0695 0.3784 … ] (1x34 double)
                    Sigma: [0.3112 0 0.4977 0.4414 0.5199 0.4608 0.4927 0.5207 0.5071 0.4839 0.5635 0.4948 0.6222 0.4949 0.6528 0.4584 0.6180 0.4968 0.6263 0.5191 0.6098 0.5182 0.6038 0.5275 0.5785 0.5085 0.5162 0.5500 0.5759 0.5080 … ] (1x34 double)
           SupportVectors: [90x34 double]
      SupportVectorLabels: [90x1 double]

  Properties, Methods</pre>

```matlab
% CompactSVMModel 是 CompactClassificationSVM 分类器。
% 显示每个分类器使用的内存量。
% CompactSVMModel is a CompactClassificationSVM classifier.
% Display the amount of memory used by each classifier.

whos('SVMModel','CompactSVMModel')
```

<pre class="mlx-out">  Name                 Size             Bytes  Class                                                 Attributes

  CompactSVMModel      1x1              31227  classreg.learning.classif.CompactClassificationSVM              
  SVMModel             1x1             141317  ClassificationSVM</pre>

```matlab
%   Name                 Size             Bytes  Class                                                 Attributes
%
%   CompactSVMModel      1x1              31058  classreg.learning.classif.CompactClassificationSVM
%   SVMModel             1x1             141148  ClassificationSVM

% 完整 SVM 分类器 (SVMModel) 比紧凑型 SVM 分类器 (CompactSVMModel) 大四倍多。
% 要有效地标记新观测值，您可以从 MATLAB® 工作区中删除 SVMModel，
% 然后传递 CompactSVMModel 和新的预测变量值进行预测。
% The full SVM classifier (SVMModel) is more than four times larger than
% the compact SVM classifier (CompactSVMModel).
% To label new observations efficiently,
% you can remove SVMModel from the MATLAB® Workspace,
% and then pass CompactSVMModel and new predictor values to predict.

% 要进一步减小紧凑型 SVM 分类器的大小，请使用 discardSupportVectors 函数丢弃支持向量。
% To further reduce the size of the compact SVM classifier,
% use the discardSupportVectors function to discard support vectors.
```
