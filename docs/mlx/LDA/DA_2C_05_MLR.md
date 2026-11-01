# DA_2C_05_MLR.mlx

「判别分析（LDA）」目录 · 对应书稿 **第06章 线性模型** · 3.8 KB · 代码 31 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/LDA/DA_2C_05_MLR.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/LDA/DA_2C_05_MLR.mlx" download>下载 DA_2C_05_MLR.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**回归分析**

准备工作

## 脚本内容

```matlab
%回归分析
%准备工作
UNDP2;                                              %将work文件夹的数据导入内存
T=[C1;C2];                                          %将两个样本的数据合并为训练样本
[n,m]=size(T);                                      %计算训练样本数组的行列数
A1=mean(C1);A2=mean(C2);                            %分别计算两个样本的均值
A=mean(T);                                          %计算两个样本合并后的均值
n1=length(C1);n2=length(C2);                        %分别计算两个样本的样品数目
n=length(T);                                        %两个样本包含的样品总数
CV1=cov(C1);CV2=cov(C2);                            %分别计算两个样本的协方差
S1=(n1-1)*CV1;S2=(n2-1)*CV2;                        %分别计算两个样本的离差平方和
sigma=(S1+S2)/(n-2);                                %计算两个样本的共同协方差
M=inv(sigma);                                       %计算共同协方差的逆矩阵

%最小二乘计算
U=[T;A1;A2];                                        %训练样本与数组均值矩阵
V=A(ones(n+2,1),:);                                 %训练样本均值平移为矩阵
y=U-V;                                              %数据中心化
Ma=y*M*y';                                          %计算马氏距离矩阵
z=Ma(:,n+1)-Ma(:,n+2);                              %计算马氏距离之差
co=(abs(z(n+1))+abs(z(n+2)))^0.5;                   %计算规范化系数
Y=z(1:n);                                           %提取判别得分作为因变量
X=[ones(n,1),T];                                    %利用训练样本数组构造自变量
B=regress(Y,X);                                     %线性回归分析
Cf=(S*B(2:4)+B(1));                                 %计算待判样品的得分
Cfc=(S*B(2:4)+B(1))/co;                             %计算待判样品的规范化得分

%规范化最小二乘计算
Yc=z(1:n)/co;                                       %判别得分规范化作为因变量
Bc=regress(Yc,X);                                   %基于规范化得分的线性回归
Cfc=(S*Bc(2:4)+Bc(1));                              %计算待判样品的规范化得分
```
