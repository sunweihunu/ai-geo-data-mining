
%二分类线性判别
UNDP2;                                              %将work文件夹的数据导入内存
T=[C1;C2];                                          %将两个样本的数据合并为训练样本
G=[zeros(length(C1),1)
   ones(length(C2),1)];                             %定义一个分类变量表示的类别数组
P=ones(14,1)/14;
[Class,E]=classify(S,T,G);                          %利用线性判别法对待判样品分类
CT=classify(T,T,G);                                 %训练样本的判别分类
Class,E                                             %输出部分结果