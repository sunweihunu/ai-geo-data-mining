# knn_sip4.mlx

「k 最近邻（kNN）」目录 · 对应书稿 **第07章 k最近邻（kNN）模型** · 4.1 KB · 代码 47 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/kNN/knn_sip4.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/kNN/knn_sip4.mlx" download>下载 knn_sip4.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**Search for Nearest Neighbors of Query Data Using Minkowski Distance**

Grow a Kd-tree nearest neighbor searcher object by using the createns function. Pass the object and query data to the knnsearch function to find k-nearest neighbors.

## 脚本内容

```matlab
% Search for Nearest Neighbors of Query Data Using Minkowski Distance
% Grow a Kd-tree nearest neighbor searcher object by using the createns function.
% Pass the object and query data to the knnsearch function to find k-nearest neighbors.
%
% Load Fisher's iris data set.

load fisheriris
% Remove five irises randomly from the predictor data to use as a query set.

rng(1)                      % For reproducibility
n = size(meas,1);           % Sample size
qIdx = randsample(n,5);     % Indices of query data
tIdx = ~ismember(1:n,qIdx); % Indices of training data
Q = meas(qIdx,:);
X = meas(tIdx,:);
% Grow a four-dimensional Kd-tree using the training data.
% Specify the Minkowski distance for finding nearest neighbors.

Mdl = createns(X,'Distance','minkowski')
% Mdl =
%   KDTreeSearcher with properties:
%
%        BucketSize: 50
%          Distance: 'minkowski'
%     DistParameter: 2
%                 X: [145x4 double]

% Because X has four columns and the distance metric is Minkowski,
% createns creates a KDTreeSearcher model object by default.
% The Minkowski distance exponent is 2 by default.

% Find the indices of the training data (Mdl.X) that are the two nearest neighbors
% of each point in the query data (Q).

IdxNN = knnsearch(Mdl,Q,'K',2)
% IdxNN = 5�2
%
%     17     4
%      6     2
%      1    12
%     89    66
%    124   100
%
% Each row of IdxNN corresponds to a query data observation,
% and the column order corresponds to the order of the nearest neighbors,
% with respect to ascending distance.
% For example, based on the Minkowski distance, the second nearest neighbor of Q(3,:) is X(12,:).
```
