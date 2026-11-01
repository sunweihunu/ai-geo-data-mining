# knn_sip2.mlx

「k 最近邻（kNN）」目录 · 对应书稿 **第07章 k最近邻（kNN）模型** · 23.3 KB · 代码 22 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/kNN/knn_sip2.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/kNN/knn_sip2.mlx" download>下载 knn_sip2.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**======== Find k-Nearest Neighbors Using Different Distance Metrics ========**

https://ww2.mathworks.cn/help/stats/knnsearch.html?s_tid=srchtitle_knnsearch_1

## 脚本内容

```matlab
% ======== Find k-Nearest Neighbors Using Different Distance Metrics ========
% https://ww2.mathworks.cn/help/stats/knnsearch.html?s_tid=srchtitle_knnsearch_1

% Find the 10 nearest neighbors in X to each point in Y,
% first using the Minkowski distance metric and then using the Chebychev distance metric.
%
```

## Load Fisher's iris data set.

```matlab
load fisheriris
X = meas(:,3:4);    % Measurements of original flowers
Y = [5 1.45;6 2;2.75 .75];  % New flower data
```

## Perform a knnsearch between X and the query points Y

using Minkowski and Chebychev distance metrics.

```matlab
[mIdx,mD] = knnsearch(X,Y,'K',10,'Distance','minkowski','P',5);
[cIdx,cD] = knnsearch(X,Y,'K',10,'Distance','chebychev');
% K — Number of nearest neighbors
% 1 (default) | positive integer
```

## Visualize the results of the two nearest neighbor searches.

Plot the training data. Plot the query points with the marker X. Use circles to denote the Minkowski nearest neighbors. Use pentagrams to denote the Chebychev nearest neighbors.

```matlab
gscatter(X(:,1),X(:,2),species)
line(Y(:,1),Y(:,2),'Marker','x','Color','k',...
   'Markersize',10,'Linewidth',2,'Linestyle','none')
line(X(mIdx,1),X(mIdx,2),'Color',[.5 .5 .5],'Marker','o',...
   'Linestyle','none','Markersize',10)
line(X(cIdx,1),X(cIdx,2),'Color','r','Marker','p',...
   'Linestyle','none','Markersize',10)
legend('setosa','versicolor','virginica','query point',...
'minkowski','chebychev','Location','best')
```
