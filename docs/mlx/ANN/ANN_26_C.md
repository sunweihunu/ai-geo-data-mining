# ANN_26_C.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 21.2 KB · 代码 13 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/ANN_26_C.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/ANN/ANN_26_C.mlx" download>下载 ANN_26_C.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**竞争型网络（无目标分类）**

福冈与中国城市分类（标准化数据）

## 脚本内容

```matlab
%竞争型网络（无目标分类）
%福冈与中国城市分类（标准化数据）
clear                                       %清理内存
P=[-1.0972 -0.5551 0.2582 1.7039 0.8907 -0.5551 -0.6454
-1.2094 -0.3634 0.1092 1.4278 0.9143 -1.1919 0.3134
1.1834 0.7953 -0.3282 -0.3814 0.0536 -1.8522 0.5293
-1.6362 -1.1296 0.0680 0.7742 0.8357 0.8203 0.2676
-1.4575 -1.0634 -0.2752 1.2135 0.9946 0.1626 0.4254];
net=newc(minmax(P),2);                      %创建一个五变量二分类的竞争型网络
net.trainParam.epochs=1000;                 %指定最大训练次数
net=train(net,P);                           %训练网络
Y=sim(net,P)                                %仿真结果
Yc=vec2ind(Y)                               %输出分类向量
```
