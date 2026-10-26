%% demo_alexnet_webcam.m —— 摄像头 + AlexNet 预训练网络的实时图像分类
% 对应《人工智能与地理数据挖掘》第11章 案例一（11.7.1 节）
% 首次运行 alexnet / webcam 会提示安装支持包，点击提示中的链接按流程安装即可。
% 无 GPU 也能运行，普通笔记本 CPU 即可。

clear; clc;

% 1) 导入预训练网络与摄像头（首次使用各需安装一次支持包）
net = alexnet;
cam = webcam;

% 2) 死循环：反复抓帧 -> 缩放到输入层尺寸 -> 分类 -> 显示
while true
    im = snapshot(cam);                 % 抓取当前一帧图像
    im = imresize(im, [227 227]);       % AlexNet 输入层要求 227×227
    label = classify(net, im);          % 预训练网络直接分类
    image(im);
    title(char(label), 'FontSize', 16); % 显示图像并标注类别名
    drawnow;
end
