# PCA_M01.mlx

「降维（DR）」目录 · 对应书稿 **第05章 降维** · 47.0 KB · 代码 99 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DR/PCA_M01.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DR/PCA_M01.mlx" download>下载 PCA_M01.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**主成分分析（第一套方法）**

## 脚本内容

```matlab
%主成分分析（第一套方法）
clear all;      %清理内存
%数据标准化并计算相关系数
% load C:\MATLAB7\work\cities2003
cities2003 %调出保存的数据
data=[data(:,1),data(:,2),data(:,3),365-data(:,4)];
mv=mean(data);                               %计算各变量的均值
st=std(data);                                %计算各变量的标准差
[n,m]=size(data);                            %计算矩阵的函数和列数
X=(data-mv(ones(n,1),:))./st(ones(n,1),:);   %原始数据集体标准化
X
%基于标准化数据计算相关系数的三种方法
R=X'*X/(n-1);                                %计算相关系数矩阵
R=cov(X);                                    %计算相关系数矩阵
R=corrcoef(X);                               %计算相关系数矩阵
R

%主成分分析的完整计算过程
[U,V]=eig(R);                                %计算特征向量和特征值矩阵
E=transpose(rot90(U));                       %将特征向量矩阵P旋转90度再转置
G=rot90(rot90(V));                           %将对角矩阵旋转180度
eigv=diag(G);                                %提取角矩阵的对角线元素
per=100*eigv/sum(eigv);                      %计算方差贡献百分比
Cum=cumsum(per);                             %计算方差贡献累计百分比
C=sqrtm(G);                                  %将对角矩阵对角线元素化为平方根
A=-E*C;                                      %计算载荷矩阵(转换为负值)
Co1=A(:,1).^2;                               %提取1个主成分的公因子方差
Co2=Co1+A(:,2).^2;                           %提取2个主成分的公因子方差
Co3=Co2+A(:,3).^2;                           %提取3个主成分的公因子方差
Co4=Co3+A(:,4).^2;                           %提取4个主成分的公因子方差
Comm=[Co1,Co2,Co3,Co4];                      %将4个公因子方差向量合并为一个矩阵
H=A(:,1:2);                                  %提取第一、第二主成分的载荷
Z=X*(-E);                                    %计算主成分得分(转换为负值)
stdr=std(Z);                                 %计算主成分得分的标准差
F=Z./stdr(ones(n,1),:);                      %主成分得分集体标准化
f=F(:,1:2);                                  %提取第一、第二主成分的标准化得分
E,G,Cum,Co2,H,f                              %输出常用结果

%一些图形的绘制
%特征值分布的折线图
figure(1);                                   %创造第一个图形窗口
plot(eigv,'rO');                             %绘制特征值的散点图
xlabel('Component number');                  %横轴标签(成分数)
ylabel('Eigenvalue');                        %纵轴标签（特征值）
hold on                                      %保持图形
plot(eigv,'g-');                             %将特征值的散点连接起来
hold off                                     %第一次绘图结束
%主成分载荷图
figure(2);                                   %创造第二个图形窗口
a1=A(:,1);a2=A(:,2);                         %提取载荷矩阵中的向量
plot(a1,a2,'rd');                            %绘制主成分载荷图
xlabel('PC axis1');                          %横轴标签(主轴1)
ylabel('PC axis2');                          %纵轴标签(主轴2)
grid on                                      %添加网格
%主成分得分图
figure(3);                                   %创造第三个图形窗口
f1=F(:,1);f2=F(:,2);                         %提取得分矩阵中的向量
plot(f1,f2,'r+');                            %绘制主成分得分图
xlabel('Score1');                            %横轴标签(第一主成分)
ylabel('Score2');                            %纵轴标签(第二主成分)
grid on                                      %添加网格

%计算T平方统计量(1)
L=F.^2;                                      %标准化主成分数值取平方
T=L(:,1)+L(:,2)+L(:,3)+L(:,4);               %计算T统计量

%特征向量图(效果等价于主成分载荷图)
figure(4);                                   %创造第二个图形窗口
e1=-E(:,1);e2=-E(:,2);                       %提取特征向量并转换符号
plot(e1,e2,'rd');                            %绘制特征向量图
xlabel('PC axis1');                          %横轴标签(主轴1)
ylabel('PC axis2');                          %纵轴标签(主轴2)
grid on                                      %添加网格

%几个用于检验的语句
%计算再生相关系数矩阵
Rp=H*H';                                     %计算再生相关矩阵
Re=R-Rp;                                     %计算相关矩阵的残差矩阵
%计算非标准化数据协方差矩阵的三种方法
Covz=Z'*Z/(n-1);                             %计算协方差矩阵
Covz=cov(Z);                                 %计算协方差矩阵
%计算主成分得分相关系数的四种方法
Rz=F'*F/(n-1);                               %计算相关系数矩阵
Rz=cov(F);                                   %计算协方差矩阵
Rz=corrcoef(F);                              %计算相关系数矩阵
Rz=corrcoef(Z);                              %计算相关系数矩阵

%综合得分

S=Z(:,1)+Z(:,2)+Z(:,3)+Z(:,4)                %非标准化得分四列加和
S1=F(:,1)*eigv(1)^0.5+F(:,2)*eigv(2)^0.5+F(:,3)*eigv(3)^0.5+F(:,4)*eigv(4)^0.5

%计算T平方统计量(2)
for i=1:n
    T=sumsqr(F(i,:));
end

%数据重构
data=[data(:,1),data(:,2),data(:,3),365-data(:,4)];
```
