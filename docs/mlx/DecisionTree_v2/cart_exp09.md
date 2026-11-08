# cart_exp09.mlx

「决策树（CART）」目录 · 对应书稿 **第08章 决策树** · 125.9 KB · 代码 38 行 · 图窗 3

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DecisionTree_v2/cart_exp09.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/DecisionTree_v2/cart_exp09.mlx" download>下载 cart_exp09.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**选择合适的树深**

这个例子展示了如何控制决策树的深度，以及如何选择合适的深度。 加载电离层数据。

## 脚本内容

```matlab
% 选择合适的树深
% 这个例子展示了如何控制决策树的深度，以及如何选择合适的深度。
% 加载电离层数据。
load ionosphere

% 生成一组从 10 到 100 的指数间隔值，表示每个叶节点的最小观察数。
leafs = logspace(1,2,10);

% 为电离层数据创建交叉验证的分类树。指定使用叶子中的最小叶子大小来生长每棵树。
rng('default')
N = numel(leafs);
err = zeros(N,1);
for n=1:N
    t = fitctree(X,Y,'CrossVal','On',...
        'MinLeafSize',leafs(n));
    err(n) = kfoldLoss(t);
end
plot(leafs,err);
xlabel('Min Leaf Size');
ylabel('cross-validated error');
```

<img src="../cart_exp09_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
% 最好的叶子大小是每片叶子大约 20 到 50 个观察值之间。


% 将每个叶子至少有 40 个观测值的接近最优树与默认树进行比较，
% 默认树使用每个父节点 10 个观测值和每个叶子节点 1 个观测值。
DefaultTree = fitctree(X,Y);
view(DefaultTree,'Mode','Graph')
```

<img src="../cart_exp09_media/figure_1.png" alt="图窗 2" loading="lazy" />

```matlab
OptimalTree = fitctree(X,Y,'MinLeafSize',40);
view(OptimalTree,'mode','graph')
```

<img src="../cart_exp09_media/figure_2.png" alt="图窗 3" loading="lazy" />

```matlab
resubOpt = resubLoss(OptimalTree);
lossOpt = kfoldLoss(crossval(OptimalTree));
resubDefault = resubLoss(DefaultTree);
lossDefault = kfoldLoss(crossval(DefaultTree));
resubOpt,resubDefault,lossOpt,lossDefault
```

<pre class="mlx-out">resubOpt = 0.0883
resubDefault = 0.0114
lossOpt = 0.1054
lossDefault = 0.1054</pre>

```matlab
% 接近最优的树要小得多，并给出了更高的再代入误差。
% 然而，它为交叉验证的数据提供了类似的准确性。
```
