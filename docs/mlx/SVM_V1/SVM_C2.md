# SVM_C2.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 3.4 KB · 代码 20 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_C2.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/SVM_V1/SVM_C2.mlx" download>下载 SVM_C2.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**训练和交叉验证 SVM 分类器**

加载 ionosphere 数据集。

## 脚本内容

```matlab
% 训练和交叉验证 SVM 分类器
% 加载 ionosphere 数据集。

load ionosphere
rng(1); % For reproducibility
% 使用径向基核训练 SVM 分类器。让软件计算核函数的缩放值。对预测变量进行标准化。

SVMModel = fitcsvm(X,Y,'Standardize',true,'KernelFunction','RBF',...
    'KernelScale','auto');
% SVMModel 是经过训练的 ClassificationSVM 分类器。

% 交叉验证 SVM 分类器。默认情况下，软件使用 10 折交叉验证。

CVSVMModel = crossval(SVMModel);
% CVSVMModel 是 ClassificationPartitionedModel 交叉验证的分类器。

% 估计样本外的误分类率。

classLoss = kfoldLoss(CVSVMModel) % classLoss = 0.0484
% 泛化率约为 5%。
```
