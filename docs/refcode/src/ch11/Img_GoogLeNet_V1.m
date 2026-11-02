% 使用预训练网络对图像进行分类
% 此示例使用：
% Deep Learning Toolbox
% Deep Learning Toolbox Model for GoogLeNet Network
% 此示例说明如何使用预训练的深度卷积神经网络 GoogLeNet 对图像进行分类。

% GoogLeNet 已经对超过一百万个图像进行了训练，可以将图像分为 1000 个对象类别
% （例如键盘、咖啡杯、铅笔和多种动物）。该网络已基于大量图像学习了丰富的特征表示。
% 网络以图像作为输入，然后输出图像中对象的标签以及每个对象类别的概率。

%% 加载预训练网络
% 加载预训练的 GoogLeNet 网络。您还可以选择加载不同的预训练网络进行图像分类。
% 此步骤需要 Deep Learning Toolbox™ Model for GoogLeNet Network 支持包。
% 如果没有安装所需的支持包，软件会提供下载链接。

net = googlenet;

%% 读取图像并调整图像大小
% 要分类的图像的大小必须与网络的输入大小相同。对于 GoogLeNet，
% 网络输入大小是图像输入层的 InputSize 属性。

% 读取要分类的图像，并将其大小调整为网络的输入大小。调整大小会略微更改图像的纵横比。

I = imread("peppers.png");
inputSize = net.Layers(1).InputSize;
I = imresize(I,inputSize(1:2));
%% 分类并显示图像
% 对图像进行分类并显示图像及预测标签。

label = classify(net,I);
figure
imshow(I)
title(string(label))