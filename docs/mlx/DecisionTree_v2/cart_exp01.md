# cart_exp01.mlx

「决策树（CART）」目录 · 对应书稿 **第08章 决策树** · 67.3 KB · 代码 35 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DecisionTree_v2/cart_exp01.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DecisionTree_v2/cart_exp01.mlx" download>下载 cart_exp01.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**导入鸢尾花数据集**

## 脚本内容

```matlab
clear
% 导入鸢尾花数据集
load fisheriris

% Train a default classification tree using the entire data set.
% 训练
Mdl = fitctree(meas,species);

% figure;
view(Mdl)  % 文字描述的分类树
view(Mdl,'Mode','graph')  % 画图描述的分类树

% 预测
cc=predict(Mdl,meas);


% 画图：第1种画法：分类散点图
figure;n=150;
gscatter(1:n,ones(n),species)  % 第一行是原始分类
hold on;
gscatter(1:n,2*ones(n),cc)  % 第2行是预测的分类
ylim([0 3]);

% 画图: 第2种画法：混淆图
figure
cm = confusionchart(species,cc);
cm.Title = 'CART用于鸢尾花数据集 ';

% 评估结果 1： 计算分类模型Mdl中定义的损失函数
resuberror = resubLoss(Mdl)

% 评估结果 2： 计算预测不同（错误）的个数，
Ysame = strcmp(cc,species); % True when ==
num_diff=sum(~Ysame) % How many are different?
num_diff/n  % 重新计算损失函数
```
