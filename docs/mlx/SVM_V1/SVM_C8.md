# SVM_C8.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 4.8 KB · 代码 46 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_C8.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/SVM_V1/SVM_C8.mlx" download>下载 SVM_C8.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

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

% SVMModel 是一个ClassificationSVM 分类器。
% SVMModel is a ClassificationSVM classifier.

% 减小SVMModel（SVM 分类器）的大小
% Reduce the size of the SVM classifier.

CompactSVMModel = compact(SVMModel)

% CompactSVMModel 是 CompactClassificationSVM 分类器。
% 显示每个分类器使用的内存量。
% CompactSVMModel is a CompactClassificationSVM classifier.
% Display the amount of memory used by each classifier.

whos('SVMModel','CompactSVMModel')
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
