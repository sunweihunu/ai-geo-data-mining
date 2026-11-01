# ANN_12_PCA.mlx

「人工神经网络（ANN）」目录 · 对应书稿 **第09章 人工神经网络** · 82.6 KB · 代码 32 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/ANN/ANN_12_PCA.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/ANN/ANN_12_PCA.mlx" download>下载 ANN_12_PCA.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**福冈甜橘引种的主成分分析**

## 脚本内容

```matlab
%福冈甜橘引种的主成分分析
clear                                       %清理内存
CN=['合肥';'武汉';'长沙';'桂林';'温州';'成都';'福岗'];
X=[15.7  970   2209  -20.6  1.9
16.3  1260  2085  -17.3  2.8
17.2  1422  1726  -9.5   4.6
18.8  1874  1709  -4.9   8.0
17.9  1698  1848  -4.5  7.5
16.3  976   1239  -4.6   5.6
16.2  1492  2000  -8.2  6.2];
Y=zscore(X);                                %原始变量集体标准化
% [E,score,eigv,T]=princomp(Y);               %调用主成分分析程序
[E,score,eigv,T]=pca(Y);               %调用主成分分析程序
F=score(:,1:2);                             %提取第一、第二主成分的得分
plot(F(:,1),F(:,2),'b+');                   %二维二维主成分散点图
xlabel('PC1 score')                         %横轴标签(第一主成分得分)
ylabel('PC2 score')                         %纵轴标签(第二主成分得分)
text(F(:,1),F(:,2),CN,'FontSize',9);        %静态标注各城市（原为交互式gname，批量运行时无法交互）
figure                                      %保持主成分得分图
%基于主成分分析建立神经网络模型
P=F(1:length(F)-1,:)';                      %利用主成分得分构建输入信号
Q=F(length(F),:)';                          %基于主成分得分的待判样品信息
T=[1 1 0 0 0 0];                            %基于主成分得分的目标输出
plotpv(P,T);                                %画出中国六城市两大类别的散点图
net=newp(minmax(P),1);                      %创建一个感知器网络
net.trainParam.epochs=100;                  %指定最大训练次数
net=train(net,P,T);                         %网络训练
Yp=sim(net,P)                               %训练样品的预报结果
Y=sim(net,Q)                                %待判样品的归类结果
figure                                      %保持网络训练过程图
plotpv([P Q],[T Y]);                        %画出城市二类别散点图
handle=plotpc(net.iw{1,1},net.b{1});        %添加分界线
```
