# knn_sip1.mlx

「k 最近邻（kNN）」目录 · 对应书稿 **第07章 k最近邻（kNN）模型** · 14.5 KB · 代码 17 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/kNN/knn_sip1.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/kNN/knn_sip1.mlx" download>下载 knn_sip1.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**====== Find Nearest Neighbors  ======**

https://ww2.mathworks.cn/help/stats/knnsearch.html?s_tid=srchtitle_knnsearch_1

## 脚本内容

```matlab
%  ====== Find Nearest Neighbors  ======
% https://ww2.mathworks.cn/help/stats/knnsearch.html?s_tid=srchtitle_knnsearch_1

% Find the patients in the hospital data set that most closely resemble the patients in Y,
% according to age and weight.
```

## Load the hospital data set.

```matlab
load hospital;
X = [hospital.Age hospital.Weight];
Y = [20 162; 30 169; 40 168; 50 170; 60 171];   % New patients
```

## Perform a knnsearch between X and Y to find indices of nearest neighbors.

```matlab
Idx = knnsearch(X,Y);
% Find the patients in X closest in age and weight to those in Y.

X(Idx,:)
```

## compare the results

```matlab
figure;
plot(X(Idx,1),X(Idx,2),'ro','MarkerFaceColor','r')
hold on;
plot(Y(:,1),Y(:,2),'bo','MarkerFaceColor','b')
legend('Old Patients','New Patients','Location','southeast')
```
