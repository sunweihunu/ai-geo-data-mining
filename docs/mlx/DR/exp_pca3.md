# exp_pca3.mlx

「降维（DR）」目录 · 对应书稿 **第05章 降维** · 27.4 KB · 代码 36 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DR/exp_pca3.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DR/exp_pca3.mlx" download>下载 exp_pca3.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**计算主成分解释的变异性百分比。显示主成分空间中的数据表示。**

## 脚本内容

```matlab
% 计算主成分解释的变异性百分比。显示主成分空间中的数据表示。
%
clear all
% 加载样本数据集。

load imports-85
% 数据矩阵 X 在第 3 列至第 15 列中有 13 个连续变量：
% 轴距、长度、宽度、高度、整备重量、引擎大小、缸径、冲程、压缩比、马力、峰值转速
% 、城市油耗和高速公路油耗。

% 计算由这些变量的主成分解释的变异性百分比。

[coeff,score,latent,tsquared,explained] = pca(X(:,3:15));

explained


% 前三个成分解释所有变异性的 99.95%。
%
% 可视化前三个主成分的空间中的数据表示。

scatter3(score(:,1),score(:,2),score(:,3))
axis equal
xlabel('1st Principal Component')
ylabel('2nd Principal Component')
zlabel('3rd Principal Component')

% 数据在第一主成分轴上具有最大变异性。在第一个轴的所有可能选择中，
% 这是有可能得到的最大方差。在剩余可供第二主成分轴使用的所有可能选择中，
% 该选择具有最大变异性。第三主成分轴具有第三大变异性，
% 它显著小于在第二主成分轴上的变异性。
% 第四至第十三主成分轴不值得研究，因为它们只解释数据中所有变异性的 0.05%。
%
% 要跳过任何输出，您可以在对应的元素中使用 ~。例如，如果您不想得到 T 方值，请指定

% [coeff,score,latent,~,explained] = pca(X(:,3:15));
```
