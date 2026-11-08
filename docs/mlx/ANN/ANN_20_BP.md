# ANN_20_BP.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 31.6 KB · 代码 29 行 · 图窗 1

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/ANN_20_BP.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/ANN/ANN_20_BP.mlx" download>下载 ANN_20_BP.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**通勤方式选择的BP网络（任意数目的神经元）**

## 脚本内容

```matlab
%通勤方式选择的BP网络（任意数目的神经元）
clear                                       %清理内存
P=[18 21 23	23 28 31 36	42 46 48 55	56 58 18 20	25 27 28 30	32 33 33 38	41 45 48 52	56
0 0	0 0	0 0	0 0	0 0	0 0	0 1	1 1	1 1	1 1	1 1	1 1	1 1	1 1
850	1200 850 950 1200 850 1500 1000	950	1200 1800 2100 1800	850	1000 1200 1300 1500	950	1000 1800 1000 1200	1500 1800 1000 1500	1800];
                                            %输入变量
T=[0 0 1 1 1 0 1 1 1 0 1 1 1 0 0 0 0 0 1 0 0 0 0 0 1 0 1 1];
                                            %目标输出
net=newff(minmax(P),[2,3,1],{'logsig','tansig','purelin'},'trainlm');
```

<pre class="mlx-out">Warning: NEWFF used in an obsolete way.
          See help for NEWFF to update calls to the new argument list.</pre>

```matlab
                                            %创建一个隐含层包括6个神经元的BP网络
net.trainParam.epochs=2000;                 %最大学习次数
net.trainParam.goal=0.0001;                 %训练误差0.0001，小于次数可以终止学习
net=train(net,P,T);                         %训练网络
```

<img src="../ANN_20_BP_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
Y=sim(net,P)';Y                             %训练样本的仿真结果
```

<pre class="mlx-out">Y = 28x1
   -0.0000
   -0.0000
    0.7857
    0.7857
    0.7857
    0.7857
    0.7857
    0.7857
    0.7857
    0.7857</pre>

```matlab
w1=net.iw{1}                                %输出第一层权数向量
```

<pre class="mlx-out">w1 = 2x3
    4.7885  -64.3170   -0.1197
   10.6982    0.4124   -0.2383</pre>

```matlab
b1=net.b{1}                                 %输出第一层阈值
```

<pre class="mlx-out">b1 = 2x1
   29.9805
   14.8925</pre>

```matlab
w2=net.lw{2,1}                              %输出第二层权数向量
```

<pre class="mlx-out">w2 = 3x2
1.4594    3.7784
   15.3694    0.3931
   -2.7333   -8.0080</pre>

```matlab
b2=net.b{2}                                 %输出第二层阈值
```

<pre class="mlx-out">b2 = 3x1
   -4.5133
   -5.5547
    4.1330</pre>

```matlab
w3=net.lw{3,2}                              %输出第三层权数向量
```

<pre class="mlx-out">w3 = 1x3
   46.4624  -28.7950    8.4372</pre>

```matlab
b3=net.b{3}                                 %输出第三层阈值
```

<pre class="mlx-out">b3 = 9.2243</pre>

```matlab
for i=1:length(Y)                           %将仿真结果转换为0-1表示
    if Y(i)>=0.5
        y(i)=1;
    else
        y(i)=0;
    end
end
y=y                                         %输出第二层的结果
```

<pre class="mlx-out">y = 1x28
     0     0     1     1     1     1     1     1     1     1     1     1     1     0     0     0     0     0     1     0     0     0     0     1     1     1     1     1</pre>

```matlab
r=1-sum(abs(y-T))/length(Y)                 %计算预测正确率
```

<pre class="mlx-out">r = 0.8571</pre>
