% 使用深度学习对网络摄像头图像进行分类
% 此示例说明如何使用预训练的深度卷积神经网络GoogLeNet 
% 摄像头只抓取一张图像进行分类。
% 对该图像，显示排名靠前的预测值

clear camera
camera = webcam;
net = googlenet;
inputSize = net.Layers(1).InputSize(1:2)

% 预测出的类可能快速更改。因此，将排名靠前的预测值显示在一起会有所帮助。您可以通过绘制预测分数靠前的类来显示排名前五的预测值及其概率。
% 
% 对相机的快照进行分类。显示来自相机的图像以及预测的标签及其概率。使用 classify 函数的 score 输出显示排名前五的预测值的概率直方图。
% 
% 创建图窗窗口。首先，调整窗口大小以使宽度增加一倍，并创建两个子图。

h = figure;
h.Position(3) = 2*h.Position(3);
ax1 = subplot(1,2,1);
ax2 = subplot(1,2,2);
% 在左侧子图中，将图像和分类显示在一起。

im = snapshot(camera);
image(ax1,im)
im = imresize(im,inputSize);
[label,score] = classify(net,im);
title(ax1,{char(label),num2str(max(score),2)});
% 通过选择分数最高的类来选择排名前五的预测值。

[~,idx] = sort(score,'descend');
idx = idx(5:-1:1);
classes = net.Layers(end).Classes;
classNamesTop = string(classes(idx));
scoreTop = score(idx);
% 将排名前五的预测值显示为直方图。

barh(ax2,scoreTop)
xlim(ax2,[0 1])
title(ax2,'Top 5')
xlabel(ax2,'Probability')
yticklabels(ax2,classNamesTop)
ax2.YAxisLocation = 'right';