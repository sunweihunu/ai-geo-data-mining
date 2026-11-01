# ANN_14_3C.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 25.6 KB · 代码 21 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/ANN_14_3C.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/ANN/ANN_14_3C.mlx" download>下载 ANN_14_3C.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**三分类感知器模型**

## 脚本内容

```matlab
%三分类感知器模型
clear                                       %清理内存
UNDP3                                       %将work文件夹的数据导入内存
X=[C1;C2;C3;S];                             %全部变量合并为一个矩阵
n=length([C1;C2;C3]);                       %训练样本长度
m=length(S);                                %待判样本长度
A=mean(X);                                  %计算全部变量的均值
Mt=A(ones(n,1),:);                          %均值向量平移为矩阵
Ms=A(ones(m,1),:);                          %均值向量平移为矩阵
P=([C1;C2;C3]./Mt)';                        %将三个子样本的数据合并为训练样本
G1=[zeros(length(C1),1); zeros(length(C2),1); ones(length(C3),1)];
                                            %定义第一个分类变量表示的类别数组
G2=[zeros(length(C1),1); ones(length(C2),1); zeros(length(C3),1)];
                                            %定义第二个顺序变量表示的类别数组
T=[G1,G2]';                                 %三分类的双目标输出
Q=(S./Ms)';                                 %待判样品信息
net=newp(minmax(P),2);                      %构建一个双输出感知器网络
net.trainParam.epochs=500;                  %指定最大训练次数
net=train(net,P,T);                         %网络训练
Yp=sim(net,P)                               %训练样品的预报结果
Y=sim(net,Q)                                %给出待判样品的仿真结果
```
