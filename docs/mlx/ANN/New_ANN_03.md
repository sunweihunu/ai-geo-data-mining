# New_ANN_03.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 78.4 KB · 代码 23 行 · 图窗 2

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/New_ANN_03.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/ANN/New_ANN_03.mlx" download>下载 New_ANN_03.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**此例子用来展示plotfit的主要功能**

## 脚本内容

```matlab
% 此例子用来展示plotfit的主要功能

% plotfit(net,inputs,targets)
% 在输入输入范围内绘制网络的输出函数，
% 并绘制与输入值相关联的目标目标和输出数据点。
% 误差条显示输出和目标之间的差异。
%
% 该图仅针对具有一个输入(X) 的网络出现。%
% 如果网络有多个输出(Y) ，则仅展示第一个输出/目标。

% plotfit(net,inputs,targets) plots the output function of a network across the range of the inputs
% inputs and also plots target targets and output data points associated with values in inputs.
% Error bars show the difference between outputs and targets.

% The plot appears only for networks with one input.
% Only the first output/targets appear if the network has more than one output.


clear;
[x,t] = simplefit_dataset;
net = feedforwardnet(10);
net = train(net,x,t);
```

<img src="../New_ANN_03_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
plotfit(net,x,t)
```

<img src="../New_ANN_03_media/figure_1.png" alt="图窗 2" loading="lazy" />
