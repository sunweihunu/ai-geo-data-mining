# New_ANN_05.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 95.9 KB · 代码 26 行 · 图窗 4

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/New_ANN_05.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/ANN/New_ANN_05.mlx" download>下载 New_ANN_05.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**Construct and Train a Function Fitting Network**

## 脚本内容

## Construct and Train a Function Fitting Network

Load the training data.

```matlab
[x,t] = simplefit_dataset;
% The 1-by-94 matrix |x| contains the input values and the 1-by-94 matrix |t|
% contains the associated target output values.
```

## 用默认参数构建网络

Construct a function fitting neural network with one hidden layer of size 10.

```matlab
net = fitnet(10);
% View the network.
view(net)
```

<img src="../New_ANN_05_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
% The sizes of the input and output are zero. The software adjusts
% the sizes of these during training according to the training data.
% Train the network |net| using the training data.
net = train(net,x,t);
```

<img src="../New_ANN_05_media/figure_1.png" alt="图窗 2" loading="lazy" />

```matlab
% View the trained network.
view(net)
```

<img src="../New_ANN_05_media/figure_2.png" alt="图窗 3" loading="lazy" />

```matlab
% You can see that the sizes of the input and output are 1.
% Estimate the targets using the trained network.
y = net(x);
% Assess the performance of the trained network. The default performance function is mean squared error.
perf = perform(net,y,t)
```

<pre class="mlx-out">perf = 3.2666e-05</pre>

## 换成trainbr训练函数

```matlab
% The default training algorithm for a function fitting network is
% Levenberg-Marquardt ( |'trainlm'| ). Use the Bayesian regularization training algorithm and
% compare the performance results.
net = fitnet(10,'trainbr');
net = train(net,x,t);
```

<img src="../New_ANN_05_media/figure_3.png" alt="图窗 4" loading="lazy" />

```matlab
y = net(x);
perf = perform(net,y,t)
```

<pre class="mlx-out">perf = 2.2988e-10</pre>

```matlab
% The Bayesian regularization training algorithm improves the performance of the network in terms of
% estimating the target values.
```
