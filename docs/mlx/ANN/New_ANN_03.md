# New_ANN_03.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 78.4 KB · 代码 23 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/New_ANN_03.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/ANN/New_ANN_03.mlx" download>下载 New_ANN_03.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

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
plotfit(net,x,t)
```
