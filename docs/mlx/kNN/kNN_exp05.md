# kNN_exp05.mlx

「k 最近邻（kNN）」目录 · 对应书稿 **第07章 k最近邻（kNN）模型** · 3.8 KB · 代码 46 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/kNN/kNN_exp05.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/kNN/kNN_exp05.mlx" download>下载 kNN_exp05.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**完全按照定义自己写代码**

仅供参考，需要进一步仔细检查代码

## 脚本内容

```matlab
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
```
