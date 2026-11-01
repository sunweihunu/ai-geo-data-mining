% 完全按照定义自己写代码
% 仅供参考，需要进一步仔细检查代码

clc
clear all
close all
warning off
% 1. 导入训练数据：5位同学各自得两门学科（数学和电子）得成绩以及对应结果（过关和没过关）
x=[4 6 7 5 8];
y=[3 7 8 5 8];
c=["Fail","Pass","Pass","Fail","Pass"];

% 2. 选定k值
k=3;

% 3. 输入测试样本：新来的一位同学两门学科的成绩
a=6;b=8;

% 4. 计算和训练数据之间的距离，并排序
distance=[];
for i=1:length(x)
    e=sqrt((x(i)-a)^2+(y(i)-b)^2);
    distance=[distance e];
end

% 距离排序
temp=0;
gemp=0;
for i=1:length(distance)
    for j=1:(length(distance)-i)
        if(distance(j)>distance(j+1))
            temp=distance(j);
            distance(j)=distance(j+1);
            distance(j+1)=temp;
            gemp=c(j);
            c(j)=c(j+1);
            c(j+1)=gemp;
        end
    end
end
% 5. 选取距离最近的k个训练数据的结果中出现频率最高的结果作为最后预测的结果
classy=[];
for i=1:k
    classy=[classy c(i)];
end
output=string(mode(categorical(classy)))
