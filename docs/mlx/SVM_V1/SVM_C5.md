# SVM_C5.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 20.5 KB · 代码 13 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_C5.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/SVM_V1/SVM_C5.mlx" download>下载 SVM_C5.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

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
