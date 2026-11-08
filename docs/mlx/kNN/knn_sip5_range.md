# knn_sip5_range.mlx

「k 最近邻（kNN）」目录 · 对应书稿 **第07章 k最近邻（kNN）模型** · 10.7 KB · 代码 27 行 · 图窗 1

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/kNN/knn_sip5_range.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/kNN/knn_sip5_range.mlx" download>下载 knn_sip5_range.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**Find Nearest Points in Clustered Data using rangesearch**

https://ww2.mathworks.cn/help/stats/rangesearch.html

## 脚本内容

```matlab
% Find Nearest Points in Clustered Data using rangesearch
% https://ww2.mathworks.cn/help/stats/rangesearch.html
```

## Generate 5000 random points from each of three distinct multivariate normal distributions.

Shift the means of the distributions so that the randomly generated points are likely to form three separate clusters.

```matlab
rng('default')  % For reproducibility
N = 5;
dist = 10;
%  mvnrnd - Multivariate normal random numbers
%     This MATLAB function returns a matrix R of n random vectors chosen from
%     the same multivariate normal distribution, with mean vector mu and
%     covariance matrix Sigma.
%     R = mvnrnd(mu,Sigma,n)
%     R = mvnrnd(mu,Sigma)
X = [mvnrnd([0 0],eye(2),N);
     mvnrnd(dist*[1 1],eye(2),N);
     mvnrnd(dist*[-1 -1],eye(2),N)];
```

## For each point in X, find the points in X that are within a radius dist away from the point.

For faster computation, specify to keep the indices of the nearest neighbors unsorted. Select the first point in X, and find its nearest neighbors.

```matlab
Idx = rangesearch(X,X,dist,'SortIndices',false);
x = X(1,:);
nearestPoints = X(Idx{1},:);
```

## Find the values in X that are not the nearest neighbors of x.

```matlab
nonNearestIdx = true(size(X,1),1);
nonNearestIdx(Idx{1}) = false;

% Display those points in one color and the nearest neighbors of x in a different color.
scatter(X(nonNearestIdx,1),X(nonNearestIdx,2))
hold on
scatter(nearestPoints(:,1),nearestPoints(:,2))

scatter(x(1),x(2),'black','filled')  % Label the point x with a black, filled circle.
hold off
```

<img src="../knn_sip5_range_media/figure_0.png" alt="图窗 1" loading="lazy" />
