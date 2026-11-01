# ANN_01_Lin.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 53.0 KB · 代码 22 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/ANN_01_Lin.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/ANN/ANN_01_Lin.mlx" download>下载 ANN_01_Lin.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**人工神经网络**

线性网络——单输入-单输出（最大积雪深度与灌溉面积的关系）

## 脚本内容

```matlab
%人工神经网络
%线性网络——单输入-单输出（最大积雪深度与灌溉面积的关系）
x=[15.2 10.4 21.2 18.6 26.4 23.4 13.5 16.7 24.0 19.1];
y=[28.6 19.3 40.5 35.6 48.9 45.0 29.2 34.1 46.7 37.4];
P=x/10;                                     %输入数据全部除以10
T=y/10;                                     %目标数据全部除以10
net=newlin(minmax(P),1,0,0.01);             %构建一个单输出线性网络
net.trainParam.epochs=3000;                 %指定最大计算次数
net=train(net,P,T);                         %网络训练
Y=sim(net,P);Y                              %仿真与数值输出
figure                                      %创建另外一个图形窗口
plot(P,T,'r+');                             %绘制散点图
xlabel('Maximum snow depth');               %横轴标签（最大积雪深度）
ylabel('Irrigation area');                  %纵轴标签（灌溉面积）
hold on                                     %保持图形
plot(P,Y,'b-');                             %添加趋势线
hold off                                    %结束绘图
w=net.iw{1,1}                               %给出权数/回归系数
b=net.b{1}                                  %给出阈值/截距
P_test=[27.5/10];                           %预测
y=sim(net,P_test);                          %计算预测结果
Y1981=y*10                                  %将预测值转换为原来的数值单位
```
