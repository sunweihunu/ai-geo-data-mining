# SVM_C7.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 5.4 KB · 代码 58 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_C7.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/SVM_V1/SVM_C7.mlx" download>下载 SVM_C7.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

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
% CompactClassificationSVM 分类器（CompactSVMModel）使用更少的空间
% 比 ClassificationSVM 分类器 (SVMModel)，因为 SVMModel 存储数据。
% 估计最佳得分到后验概率转换函数。
% The CompactClassificationSVM classifier (CompactSVMModel) uses less space
% than the ClassificationSVM classifier (SVMModel) because SVMModel stores the data.
% Estimate the optimal score-to-posterior-probability transformation function.

CompactSVMModel = fitPosterior(CompactSVMModel,...
    X(isInds,:),Y(isInds))

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
% PostProbs 是一个 10×2 矩阵，
% 其中第一列是负类后验概率，
% 第二列是正类后验概率
% 对应于新的观察结果。
% PostProbs is a 10-by-2 matrix,
% where the first column is the negative class posterior probabilities,
% and the second column is the positive class posterior probabilities
% corresponding to the new observations.
```
