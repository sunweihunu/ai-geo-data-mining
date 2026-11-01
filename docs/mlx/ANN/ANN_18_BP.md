# ANN_18_BP.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 30.9 KB · 代码 30 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/ANN_18_BP.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/ANN/ANN_18_BP.mlx" download>下载 ANN_18_BP.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**BP网络**

通勤方式选择的BP网络（原始数据）

## 脚本内容

```matlab
%BP网络
%通勤方式选择的BP网络（原始数据）
clear                                       %清理内存
P=[18 21 23	23 28 31 36	42 46 48 55	56 58 18 20	25 27 28 30	32 33 33 38	41 45 48 52	56
0 0	0 0	0 0	0 0	0 0	0 0	0 1	1 1	1 1	1 1	1 1	1 1	1 1	1 1
850	1200 850 950 1200 850 1500 1000	950	1200 1800 2100 1800	850	1000 1200 1300 1500	950	1000 1800 1000 1200	1500 1800 1000 1500	1800];
                                            %输入变量
T=[0 0 1 1 1 0 1 1 1 0 1 1 1 0 0 0 0 0 1 0 0 0 0 0 1 0 1 1];
                                            %目标输出
net=newff(minmax(P),[1,1],{'logsig','purelin'},'trainlm');
                                            %创建一个隐含层包括2个神经元的BP网络
net.trainParam.epochs=2000;                 %最大学习次数
net.trainParam.goal=0.0001;                 %训练误差0.0001，小于次数可以终止学习
net=train(net,P,T);                         %训练网络
Y=sim(net,P)';Y                             %训练样本的仿真结果
w1=net.iw{1}                                %输出第一层权数向量
b1=net.b{1}                                 %输出第一层阈值
w2=net.lw{2}                                %输出第二层权数向量
b2=net.b{2}                                 %输出第二层阈值

%BP网络的补充代码
for i=1:length(Y)                           %将仿真结果转换为0-1表示
    if Y(i)>=0.5
        y(i)=1;
    else
        y(i)=0;
    end
end
y                                           %输出预测结果
r=1-sum(abs(y-T))/length(Y)                 %计算预测正确率
```
