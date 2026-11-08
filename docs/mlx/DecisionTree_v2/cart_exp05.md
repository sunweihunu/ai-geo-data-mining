# cart_exp05.mlx

「决策树（CART）」目录 · 对应书稿 **第08章 决策树** · 86.2 KB · 代码 24 行 · 图窗 2

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DecisionTree_v2/cart_exp05.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/DecisionTree_v2/cart_exp05.mlx" download>下载 cart_exp05.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**Construct and display a full classification tree for Fisher's iris data.**

导入数据集

## 脚本内容

```matlab
% Construct and display a full classification tree for Fisher's iris data.
% 导入数据集
load fisheriris;
varnames = {'SL','SW','PL','PW'};

% 训练分类树
t1 = fitctree(meas,species,'MinParentSize',5,'PredictorNames',varnames);
% 查看分类树结构
view(t1,'Mode','graph');
```

<img src="../cart_exp05_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
% 计算分类模型中的损失函数
resuberror = resubLoss(t1)
```

<pre class="mlx-out">resuberror = 0.0133</pre>

```matlab
% Figure Classification tree viewer contains an axes object
% and other objects of type uimenu, uicontrol.
% The axes object contains 21 objects of type line, text.

% 从最优减枝序列中找到最大一个减枝后的树，
% Construct and display the next largest tree from the optimal pruning sequence.
t2 = prune(t1,'Level',1);
% 展示结构
view(t2,'Mode','graph');
```

<img src="../cart_exp05_media/figure_1.png" alt="图窗 2" loading="lazy" />

```matlab
% 计算分类模型中的损失函数
resuberror = resubLoss(t2)
```

<pre class="mlx-out">resuberror = 0.0267</pre>
