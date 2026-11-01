# cart_exp11.mlx

「决策树（CART）」目录 · 对应书稿 **第08章 决策树** · 20.3 KB · 代码 35 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DecisionTree_v2/cart_exp11.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DecisionTree_v2/cart_exp11.mlx" download>下载 cart_exp11.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**分类差额(margin)是真实类别的分类评分与错误类别的最大分类评分之间的差值。**

分类差额是一个列向量，其行数与矩阵 X 中的行数相同 每个样本都有对应的分类差额

## 脚本内容

```matlab
% 分类差额(margin)是真实类别的分类评分与错误类别的最大分类评分之间的差值。
% 分类差额是一个列向量，其行数与矩阵 X 中的行数相同
% 每个样本都有对应的分类差额
% 分类差额值高，高值比低值的预测更可靠。
% The classification margin is the difference between the classification score
% for the true class and maximal classification score for the false classes.
% The classification margin is a column vector with the same number of rows
% as in the matrix X. A high value of margin indicates a more reliable prediction than a low value.

% 优势(edge)是分类差额的加权平均值。 权重是 tree.Prior 中的类概率。
% 如果您在权重名称-值对中提供权重，
% 则这些权重将被归一化以求和到相应类别中的先验概率，然后用于计算加权平均值。
% The edge is the weighted mean value of the classification margin.
% The weights are the class probabilities in tree.Prior.
% If you supply weights in the weights name-value pair,
% those weights are normalized to sum to the prior probabilities in the respective classes,
% and are then used to compute the weighted average.

load fisheriris
X = meas(:,1:2);
obj1 = fitcdiscr(X,species);
M1 = margin(obj1,X,species);
E1 = edge(obj1,X,species);
figure;subplot(2,2,1)
plot(1:150,M1,'ro');hold on;
subplot(2,2,2)
plot(1:150,E1,'r*');

obj2 = fitcdiscr(meas,species);
M2 = margin(obj2,meas,species);
E2 = edge(obj2,meas,species);
subplot(2,2,3)
plot(1:150,M2,'bo')
subplot(2,2,4)
plot(1:150,E2,'b*');
```
