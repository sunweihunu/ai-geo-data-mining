# New_ANN_11.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 32.7 KB · 代码 25 行 · 图窗 1

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/New_ANN_11.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/ANN/New_ANN_11.mlx" download>下载 New_ANN_11.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**训练后分析 (regression)**

经过训练的网络的性能在一定程度上可以通过基于训练集、验证集和测试集的误差来度量， 但更详细地调查网络响应通常是有用的。一种选择是执行网络响应和对应目标之间的回归分析。

## 脚本内容

```matlab
% 训练后分析 (regression)
% 经过训练的网络的性能在一定程度上可以通过基于训练集、验证集和测试集的误差来度量，
% 但更详细地调查网络响应通常是有用的。一种选择是执行网络响应和对应目标之间的回归分析。
% 例程 regression 就是为执行此分析而设计的。
% 以下命令说明如何对经过训练的网络执行回归分析。

x = [-1:.05:1];
t = sin(2*pi*x)+0.1*randn(size(x));
net = feedforwardnet(10);
net = train(net,x,t);
```

<img src="../New_ANN_11_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
y = net(x);
[r,m,b] = regression(t,y)
```

<pre class="mlx-out">r = 0.9625
m = 0.9867
b = -0.0376</pre>

```matlab
% r =    0.9935
% m =    0.9874
% b =   -0.0067
% 将网络输出和对应的目标传递给 regression。它返回三个参数。
% 前两个参数 m 和 b 对应于使目标与网络输出具有最佳线性回归的斜率和 y 截距。
% 如果存在完美拟合（输出完全等于目标），则斜率为 1，y 截距为 0。在此示例中，您可以看到数值非常接近它们。
% regression 返回的第三个变量是输出和目标之间的相关系数（R 值）。
% 它用于衡量目标解释输出变化的程度。如果此数值等于 1，则目标和输出之间就有完美的相关性。
% 在此示例中，该数值非常接近 1，这表明拟合良好。
%
% 下图显示 regression 提供的图形输出。它是网络输出（用空心圆表示）对目标的图。
% 最佳线性拟合由虚线表示。实线表示完美拟合（输出等于目标）。
% 在此示例中，由于拟合非常好，很难区分最佳线性拟合线和完美拟合线。
```
