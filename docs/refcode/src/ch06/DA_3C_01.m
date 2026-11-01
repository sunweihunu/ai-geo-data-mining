
%三分类线性判别
UNDP3                                               %将work文件夹的数据导入内存
T=[C1;C2;C3];                                       %将三个子样本的数据合并为训练样本
G=[ones(length(C1),1)
   2*ones(length(C2),1)
   3*ones(length(C3),1)];                           %定义一个顺序变量表示的类别数组
[Class,E]=classify(S,T,G,[],[0.3,0.5,0.2]);         %利用线性判别法对待判样品分类
CT=classify(T,T,G);                                 %训练样本的判别分类
Class,E                                             %输出结果