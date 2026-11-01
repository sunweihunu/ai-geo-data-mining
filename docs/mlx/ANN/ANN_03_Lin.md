# ANN_03_Lin.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 46.2 KB · 代码 22 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/ANN_03_Lin.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/ANN/ANN_03_Lin.mlx" download>下载 ANN_03_Lin.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**线性网络——多输入-单输出（交通运输业的影响因素）**

## 脚本内容

```matlab
%线性网络——多输入-单输出（交通运输业的影响因素）
clear                                       %清理内存
X=[57.82 58.05 59.15 63.83 65.36 67.26 66.92 67.79 75.65 80.57 79.02 80.52 86.88 95.48 109.71 126.5 138.89 160.56
27.05 28.89	33.02 35.23	24.94 32.95	30.35 38.7 47.99 54.18 58.73 59.85 64.57 70.97 81.54 94.01 103.23 119.33
14.54 16.83	12.26 12.87	11.65 12.87	10.8 10.93 14.71 17.56 20.32 18.67 25.34 25.06 29.69 43.86 48.9	60.98];
y=[3.09	3.4	3.88 3.9 3.22 3.76 3.59	4.03 4.34 4.65 4.78	5.04 5.59 6.01 7.03	10.03 10.83	12.9];
P=X/40;                                     %输入变量全部除以40
T=y;                                        %输出变量不变
net=newlin(minmax(P),1,0,0.01);             %构建一个单输出线性网络
net.trainParam.epochs=20000;                %指定最大训练次数
net=train(net,P,T);                         %网络训练
Y=sim(net,P)                                %仿真并输出结果
figure;                                     %保留误差曲线图
t=1:length(Y);                              %定义时序
plot(t,T,'r+');                             %绘制输出变量散点图
xlabel('t');                                %横轴标签（时序）
ylabel('Y');                                %纵轴标签（运输业产值）
hold on                                     %保持图形
plot(t,Y,'b-');                             %在散点图中添加仿真曲线
hold off                                    %结束绘图
w=net.iw{1,1}                               %输出权数向量
b=net.b{1}                                  %输出阈值
```
