# ANN_09_p.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 25.2 KB · 代码 14 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/ANN_09_p.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/ANN/ANN_09_p.mlx" download>下载 ANN_09_p.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**福冈归属的感知器判别（基于原始数据）**

## 脚本内容

```matlab
%福冈归属的感知器判别（基于原始数据）
clear                                       %清理内存
P=[15.7 16.3 17.2 18.8 17.9 16.3
970 1260 1422 1874 1698 976
2209 2085 1726 1709 1848 1239
-20.6 -17.3	-9.5 -4.9 -4.5 -4.6
1.9	2.8	4.6	8 7.5 5.6];                     %训练样本输入变量
T=[1 1 0 0 0 0];                            %目标输出
Q=[16.2 1492.0 2000.0 -8.2 6.2]';           %待判样品信息
net=newp(minmax(P),1);                      %构建一个单输出感知器网络
net.trainParam.epochs=500;                  %指定最大训练次数
net=train(net,P,T);                         %网络训练
Yp=sim(net,P)                               %训练样品的预报结果
Y=sim(net,Q)                                %给出待判样品的仿真结果
```
