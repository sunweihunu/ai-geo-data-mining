# ANN_23_C.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 21.0 KB · 代码 16 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/ANN_23_C.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/ANN/ANN_23_C.mlx" download>下载 ANN_23_C.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**竞争型网络（有目标分类）**

福冈与中国六城市的相似性比较（数据未经标准化）

## 脚本内容

```matlab
%竞争型网络（有目标分类）
%福冈与中国六城市的相似性比较（数据未经标准化）
clear                                       %清理内存
P=[15.7	16.3 17.2 18.8 17.9 16.3
970 1260 1422 1874 1698 976
2209 2085 1726 1709	1848 1239
-20.6 -17.3	-9.5 -4.9 -4.5 -4.6
1.9	2.8	4.6	8.0	7.5	5.6];                   %输入变量
net=newc(minmax(P),2);                      %创建六城市五变量二分类的竞争型网络
net.trainParam.epochs=1000;                 %指定最大训练次数
net=train(net,P);                           %训练网络
Y=sim(net,P);                               %数值仿真结果
Yc=vec2ind(Y)                               %给出分类向量
Q=[16.2 1492 2000 -8.2 6.2]';               %输入福冈的信号
y_test=sim(net,Q);                          %福冈数值仿真
yc_test=vec2ind(y_test)                     %福冈归类结果
```
