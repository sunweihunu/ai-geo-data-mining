# ANN_17_LVQ.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 29.2 KB · 代码 23 行 · 图窗 1

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/ANN_17_LVQ.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/ANN/ANN_17_LVQ.mlx" download>下载 ANN_17_LVQ.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**基于LVQ网络的国家三类型判别（5个神经元）**

## 脚本内容

```matlab
%基于LVQ网络的国家三类型判别（5个神经元）
clear                                       %清理内存
UNDP3                                       %将work文件夹的数据导入内存
X=[C1;C2;C3;S];                             %全部变量合并为一个矩阵
n=length([C1;C2;C3]);                       %训练样本长度
m=length(S);                                %待判样本长度
A=mean(X);                                  %计算全部变量的均值
Mt=A(ones(n,1),:);                          %均值向量平移为矩阵
Ms=A(ones(m,1),:);                          %均值向量平移为矩阵
P=([C1;C2;C3]./Mt)';                        %将三个子样本的数据合并为训练样本
Tc=[ones(length(C1),1)
   2*ones(length(C2),1)
   3*ones(length(C3),1)]';                  %定义一个顺序变量表示的目标输出
T=ind2vec(Tc);                              %输出初始分类
net=newlvq(minmax(P),5,[0.3 0.5 0.2], 0.05,'learnlv2');
                                            %创建学习向量量化网络
net.trainParam.epochs=500;                  %指定最大训练次数
net=train(net,P,T);                         %训练网络
```

<img src="../ANN_17_LVQ_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
Y=sim(net,P)                                %仿真结果
```

<pre class="mlx-out">Y = 3x44
     1     1     1     1     1     1     1     1     1     1     1     1     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0
     0     0     0     0     0     0     0     0     0     0     0     0     1     1     1     1     1     1     1     1     1     1     1     1     1     1     1     1     1     1     1     1     1     1     1     0     0     0     0     0     0     0     0     0
     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     1     1     1     1     1     1     1     1     1</pre>

```matlab
Yc=vec2ind(Y)                               %模拟的分类向量
```

<pre class="mlx-out">Yc = 1x44
     1     1     1     1     1     1     1     1     1     1     1     1     2     2     2     2     2     2     2     2     2     2     2     2     2     2     2     2     2     2     2     2     2     2     2     3     3     3     3     3     3     3     3     3</pre>

```matlab
P_test=(S./Ms)';                            %待判样品信号
y_test=sim(net,P_test);                     %待判样品测试
yc_test=vec2ind(y_test)                     %待判样品的分类结果
```

<pre class="mlx-out">yc_test = 1x18
     1     1     1     1     1     2     2     2     2     2     2     2     2     2     2     3     2     3</pre>
