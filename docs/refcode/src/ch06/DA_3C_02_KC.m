
%快速聚类与判别
UNDP3                                               %调入数据
T=[C1;C2;C3];                                       %将三个子样本的数据合并为训练样本
G=kmeans(T,3);                                      %快速聚类
[Class,E]=classify(S,T,G);                          %基于快速聚类结果对待判样品分类
CT=classify(T,T,G);                                 %计算训练样本的判别结果
Class,E                                             %输出部分结果