# ANN_25_C.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 21.1 KB · 代码 15 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/ANN_25_C.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/ANN/ANN_25_C.mlx" download>下载 ANN_25_C.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**福冈与中国六城市的相似性比较（变量除以标准差）**

## 脚本内容

```matlab
%福冈与中国六城市的相似性比较（变量除以标准差）
clear                                       %清理内存
P=[14.1865 14.7286 15.5418 16.9876 16.1744 14.7286
2.8297 3.6757 4.1483 5.4669 4.9534 2.8472
6.9131 6.5251 5.4016 5.3484 5.7834 3.8775
-3.1628 -2.6561 -1.4586 -0.7523 -0.6909 -0.7062
0.8319 1.2260 2.0142 3.5029 3.2840 2.4521]; %训练样本的输入变量
net=newc([-1 1;-1 1;-1 1;-1 1;-1 1],3);     %创建五变量二分类的竞争型网络
net.trainParam.epochs=1000;                 %指定最大训练次数
net=train(net,P);                           %训练网络
Y=sim(net,P);                               %数值仿真结果
Yc=vec2ind(Y)                               %给出分类向量
Q=[14.6383 4.3525 6.2591 -1.2590 2.7148]';  %输入福冈的信号
y_test=sim(net,Q);                          %福冈数值仿真
yc_test=vec2ind(y_test)                     %福冈归类结果
```
