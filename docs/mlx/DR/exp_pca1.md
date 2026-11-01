# exp_pca1.mlx

「降维（DR）」目录 · 对应书稿 **第05章 降维** · 28.9 KB · 代码 28 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DR/exp_pca1.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DR/exp_pca1.mlx" download>下载 exp_pca1.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**coeff = pca(X) 返回 n×p 数据矩阵 X 的主成分系数，也称为载荷。**

X 的行对应于观测值，列对应于变量。系数矩阵是 p×p 矩阵。

## 脚本内容

```matlab
% coeff = pca(X) 返回 n×p 数据矩阵 X 的主成分系数，也称为载荷。
% X 的行对应于观测值，列对应于变量。系数矩阵是 p×p 矩阵。

% coeff 的每列包含一个主成分的系数，并且这些列按成分方差的降序排列。
% 默认情况下，pca 将数据中心化，并使用奇异值分解 (SVD) 算法。

clear all
%  Step 1
%  加载样本数据集。
load hald

% Step 2
% 原料数据有 4 个变量的 13 个观测值。
% 找出原料数据的主成分。

 [coeff,score,latent,tsquared,explained] = pca(ingredients)

%  coeff 的行包含四个原料变量的系数，其列对应于四个主成分。

% Step3  画图（载荷图和得分图合二为一）
biplot(coeff(:,1:2),'scores',score(:,1:2),'varlabels',{'v_1','v_2','v_3','v_4'});

% Step4  画图： 前两个主成份下的散点图（得分图）
figure;
scatter(score(:,1),score(:,2))
axis equal
xlabel('1st Principal Component')
ylabel('2nd Principal Component')
```
