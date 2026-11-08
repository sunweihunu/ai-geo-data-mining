# knn_sip1.mlx

「k 最近邻（kNN）」目录 · 对应书稿 **第07章 k最近邻（kNN）模型** · 14.5 KB · 代码 17 行 · 图窗 1

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/kNN/knn_sip1.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/kNN/knn_sip1.mlx" download>下载 knn_sip1.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

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

<pre class="mlx-out">ans = 5x2
    25   171
    25   171
    39   164
    49   170
    50   172</pre>

## compare the results

```matlab
figure;
plot(X(Idx,1),X(Idx,2),'ro','MarkerFaceColor','r')
hold on;
plot(Y(:,1),Y(:,2),'bo','MarkerFaceColor','b')
legend('Old Patients','New Patients','Location','southeast')
```

<img src="../knn_sip1_media/figure_0.png" alt="图窗 1" loading="lazy" />
