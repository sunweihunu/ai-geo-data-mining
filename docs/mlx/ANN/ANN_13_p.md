# ANN_13_p.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 60.5 KB · 代码 15 行 · 图窗 3

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/ANN_13_p.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/ANN/ANN_13_p.mlx" download>下载 ANN_13_p.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**基于方差极大正交旋转因子得分的福冈判别**

## 脚本内容

```matlab
%基于方差极大正交旋转因子得分的福冈判别
clear                                       %清理内存
P=[-1.0814 -0.4748 0.0010 1.4951 1.0309	-1.1319
-1.1878 -0.9568 0.1447 0.2059 0.1168 1.8851];
                                            %输入信号
T=[1 1 0 0 0 1];                            %目标输出（已知类别）
Q=[0.1610 -0.2077]';                        %待判样品——福冈的因子得分
plotpv(P,T);                                %画出两类城市的散点图
```

<img src="../ANN_13_p_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
net=newp(minmax(P),1);                      %创建一个感知器网络
net.trainParam.epochs=100;                  %指定最大训练次数
net=train(net,P,T);                         %训练网络
```

<img src="../ANN_13_p_media/figure_1.png" alt="图窗 2" loading="lazy" />

```matlab
Y=sim(net,Q)                                %输出仿真结果
```

<pre class="mlx-out">Y = 0</pre>

```matlab
figure;                                     %保持仿真过程图
plotpv([P Q],[T Y]);                        %画出七城市二类别散点图
handle=plotpc(net.iw{1,1},net.b{1});        %添加类别分界线
```

<img src="../ANN_13_p_media/figure_2.png" alt="图窗 3" loading="lazy" />
