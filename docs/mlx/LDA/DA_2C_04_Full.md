# DA_2C_04_Full.mlx

「判别分析（LDA）」目录 · 对应书稿 **第06章 线性模型** · 4.6 KB · 代码 65 行 · 运行输出 3

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/LDA/DA_2C_04_Full.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/LDA/DA_2C_04_Full.mlx" download>下载 DA_2C_04_Full.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**详细的计算过程**

估计模型参数，计算判别得分

## 脚本内容

```matlab
%详细的计算过程
%估计模型参数，计算判别得分
UNDP2;                                              %将work文件夹的数据导入内存
T=[C1;C2];                                          %将两个样本的数据合并为训练样本
A1=mean(C1);A2=mean(C2);                            %分别计算两个样本的均值
A=mean(T);                                          %计算两个样本合并后的均值
Ad=A1-A2;                                           %计算两个样本的均值之差
Am=mean([A1;A2]);                                   %两个样本均值的均值
n1=length(C1);n2=length(C2);                        %分别计算两个样本的样品数目
n=length(T);                                        %两个样本包含的样品总数
CV1=cov(C1);CV2=cov(C2);                            %分别计算两个样本的协方差
S1=(n1-1)*CV1;S2=(n2-1)*CV2;                        %分别计算两个样本的离差平方和
sigma=(S1+S2)/(n-2);                                %计算两个样本的共同协方差
M=inv(sigma);                                       %计算共同协方差的逆矩阵
a=M*Ad';                                            %计算距离判别系数
c=A*a;                                              %计算判别函数的常数
W=T*a-c;                                            %计算训练样本的判别得分

%模型参数和判别得分的规范化处理
w1=A1*a-c;w2=A2*a-c;                                %分别计算两样本判别得分的重心值
w0=A*a-c;                                           %训练样本判别得分的共同重心（0）
co=(abs(w1)+abs(w2))^0.5;                           %计算判别得分的规范化系数
ac=a/co;cc=c/co;                                    %计算规范化模型系数和常数
V=W/co;                                             %训练样本判别得分规范化
for i=1:n                                           %计算训练样本的判别结果
    if V(i)>0
        C(i)=0;
    else
        C(i)=1;
    end
    C;
end
Ch=C';                                              %训练样本的判别结论

%判别检验
%F检验
[n,m]=size(T);                                      %计算训练样本数组的行列数
Sc=S1+S2;                                           %计算两个样本的交叉乘积和矩阵
Si=inv(Sc);                                         %计算交叉乘积和矩阵的逆矩阵
T2=(n-2)*(n1*n2/n*(A1-A2)*Si*(A1-A2)');             %计算T平方值
F=(n-m-1)/(n-2)/m*T2;                               %计算F统计量
Fc=finv(1-0.05,m,n-m-1);                            %计算F统计量的临界值
F,Fc                                                %输出结果
```

<pre class="mlx-out">F = 19.4259
Fc = 3.7083</pre>

```matlab
%等方差检验
f1=1+(1/(n1-1)+ 1/(n2-1)-1/(n1+n2-2))*(2*m^2+3*m-1)/(6*(m+1));
                                                    %计算卡方统计量预备之一
f2=log(det(sigma)^(n-2)/(det(CV1)^(n1-1)* det(CV2)^(n2-1)));
                                                    %计算卡方统计量预备之二
Chq=f1*f2;                                          %计算卡方统计量
df=m*(m+1)/2;                                       %计算判别分析的自由度
Chc=chi2inv(1-0.05,df);                             %计算卡方检验临界值
Chq,Chc                                             %输出结果
```

<pre class="mlx-out">Chq = 28.8738
Chc = 12.5916</pre>

```matlab
%待判样品的得分计算和归类
Cf=(S*a-c)/co;                                      %计算待判样品的规范化得分
for i=1:length(Cf)
    if Cf(i)>0
        D(i)=0;
    else
        D(i)=1;
    end
    D;
end
Class=D'                                            %待判样品的判别结论
```

<pre class="mlx-out">Class = 4x1
     0
     0
     1
     1</pre>
