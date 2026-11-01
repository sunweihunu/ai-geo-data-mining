# cart_exp02.mlx

「决策树（CART）」目录 · 对应书稿 **第08章 决策树** · 151.0 KB · 代码 42 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DecisionTree_v2/cart_exp02.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DecisionTree_v2/cart_exp02.mlx" download>下载 cart_exp02.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**Optimize Classification Tree**

This example shows how to optimize hyperparameters automatically using fitctree. The example uses Fisher's iris data.

## 脚本内容

```matlab
% Optimize Classification Tree
% This example shows how to optimize hyperparameters automatically using fitctree.
% The example uses Fisher's iris data.
% Load Fisher's iris data.
load fisheriris
X = meas;
Y = species;

% 不经过优化的训练分类树
Md0 = fitctree(X,Y);
% 计算分类模型Md0中的损失函数
resuberror = resubLoss(Md0)   % resuberror =  0.0200
% 预测
cc0=predict(Md0,meas);
figure
cm0 = confusionchart(species,cc0);
cm0.Title = '不经过优化的分类树 ';
% 展示结构
view(Md0,'Mode','graph');


% 经过优化的训练分类树
% rng(12345) %  resuberror =    0.0267
rng(6794050) %  resuberror =  0.0267

% Optimize the cross-validation loss of the classifier,
% using the data in meas to predict the response in species.
Mdl = fitctree(X,Y,'OptimizeHyperparameters','auto')
% 计算分类模型Mdl中的损失函数
resuberror = resubLoss(Mdl)

% 预测
cc1=predict(Mdl,meas);
cm1 = confusionchart(species,cc1);
cm1.Title = '优化的分类树 ';

% 展示结构
view(Mdl,'Mode','graph');

% 本示例因为数据规模太小，所有数据集都作为了训练集
% 经过优化后，损失函数还略微变差了
% 但是模型树的结构精简了，泛化能力可能提高了
```
