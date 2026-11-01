# kNN_exp04.mlx

「k 最近邻（kNN）」目录 · 对应书稿 **第07章 k最近邻（kNN）模型** · 3.8 KB · 代码 16 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/kNN/kNN_exp04.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/kNN/kNN_exp04.mlx" download>下载 kNN_exp04.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**利用fitcknn函数进行kNN分类**

Construct a KNN classifier for the Fisher iris data as in Construct KNN Classifier.

## 脚本内容

```matlab
% 利用fitcknn函数进行kNN分类
% Construct a KNN classifier for the Fisher iris data as in Construct KNN Classifier.
load fisheriris
% X = meas;
X =meas(:,3:4);
Y = species;
Mdl = fitcknn(X,Y,'NumNeighbors',4);

% Predict the classification of an average flower.
%  对数据集的平均值对应的虚拟点（花）进行分类
flwr = mean(X); % an average flower
flwrClass = predict(Mdl,flwr)

%  对三个新数据点进行分类
newpoint2 = [5 1.45;6 2;2.75 .75];
newClass = predict(Mdl,newpoint2)
```
