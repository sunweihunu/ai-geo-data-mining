# cart_exp01.mlx

「决策树（CART）」目录 · 对应书稿 **第08章 决策树** · 67.3 KB · 代码 35 行 · 图窗 3

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DecisionTree_v2/cart_exp01.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/DecisionTree_v2/cart_exp01.mlx" download>下载 cart_exp01.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

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
```

<pre class="mlx-out">Decision tree for classification
1  if x3&lt;2.45 then node 2 elseif x3&gt;=2.45 then node 3 else setosa
2  class = setosa
3  if x4&lt;1.75 then node 4 elseif x4&gt;=1.75 then node 5 else versicolor
4  if x3&lt;4.95 then node 6 elseif x3&gt;=4.95 then node 7 else versicolor
5  class = virginica
6  if x4&lt;1.65 then node 8 elseif x4&gt;=1.65 then node 9 else versicolor
7  class = virginica
8  class = versicolor
9  class = virginica</pre>

```matlab
view(Mdl,'Mode','graph')  % 画图描述的分类树
```

<img src="../cart_exp01_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
% 预测
cc=predict(Mdl,meas);


% 画图：第1种画法：分类散点图
figure;n=150;
gscatter(1:n,ones(n),species)  % 第一行是原始分类
hold on;
gscatter(1:n,2*ones(n),cc)  % 第2行是预测的分类
ylim([0 3]);
```

<img src="../cart_exp01_media/figure_1.png" alt="图窗 2" loading="lazy" />

```matlab
% 画图: 第2种画法：混淆图
figure
cm = confusionchart(species,cc);
cm.Title = 'CART用于鸢尾花数据集 ';
```

<img src="../cart_exp01_media/figure_2.png" alt="图窗 3" loading="lazy" />

```matlab
% 评估结果 1： 计算分类模型Mdl中定义的损失函数
resuberror = resubLoss(Mdl)
```

<pre class="mlx-out">resuberror = 0.0200</pre>

```matlab
% 评估结果 2： 计算预测不同（错误）的个数，
Ysame = strcmp(cc,species); % True when ==
num_diff=sum(~Ysame) % How many are different?
```

<pre class="mlx-out">num_diff = 3</pre>

```matlab
num_diff/n  % 重新计算损失函数
```

<pre class="mlx-out">ans = 0.0200</pre>
