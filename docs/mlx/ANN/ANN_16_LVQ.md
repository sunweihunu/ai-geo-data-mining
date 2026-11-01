# ANN_16_LVQ.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 29.1 KB · 代码 18 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/ANN_16_LVQ.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/ANN/ANN_16_LVQ.mlx" download>下载 ANN_16_LVQ.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**基于LVQ网络的国家二类型判别（5个神经元）**

## 脚本内容

```matlab
%基于LVQ网络的国家二类型判别（5个神经元）
clear                                       %清理内存
P=[79.1	76.8 80.0 78.7 73.1 75.0 75.8 66.7 71.3	70.7 72.9 69.8 69.4 66.7
99.0 99.0 99.0 99.0 96.7 74.6 96.4 99.5	98.2 91.2 99.0 92.8 77.8 53.7
23582 29605 23257 25512	12013 17719	3967 6460 4809 6006 3353 4288 4036 3041];
                                            %输入信号
Tc=[1 1 1 1 1 1 2 2 2 2 2 2 2 2];           %目标输出，用1、2表示
T=ind2vec(Tc);                              %输出初始分类
net=newlvq(minmax(P),5,[0.5 0.5]);          %创建学习向量量化网络
net.trainParam.epochs=1500;                 %指定最大训练次数
net=train(net,P,T);                         %训练网络
Y=sim(net,P)                                %仿真结果
Yc=vec2ind(Y)                               %模拟的分类向量
P_test=[78.7 78.2 70.2 68.0
99.0 96.9 97.9 82.8
20659 13943	5648 3105];                     %待判样品信号
y_test=sim(net,P_test);                     %待判样品测试
yc_test=vec2ind(y_test)                     %待判样品的分类结果
```
