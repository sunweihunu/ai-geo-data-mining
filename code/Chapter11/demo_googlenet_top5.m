%% demo_googlenet_top5.m —— 摄像头 + GoogLeNet 预训练网络：实时分类与 Top-5 概率条形图
% 对应《人工智能与地理数据挖掘》第11章 案例一（11.7.1 节）
% 首次运行 googlenet / webcam 会提示安装支持包，按提示链接安装即可。

clear; clc; close all;

% 1) 导入预训练网络与摄像头
net = googlenet;
cam = webcam;

% 2) 读取 GoogLeNet 输入层要求的图像长宽（224×224）
inputSize = net.Layers(1).InputSize;
sz = [inputSize(1) inputSize(2)];

% 3) 建立画布：左边实时画面，右边 Top-5 条形图
h = figure('Name', 'GoogLeNet Top-5');
ax1 = subplot(1, 2, 1);
ax2 = subplot(1, 2, 2);
ax2.PositionConstraint = 'innerposition';

% 4) 循环：图窗不关闭就一直运行
while isvalid(h)
    im = snapshot(cam);                 % 抓帧
    image(im, 'Parent', ax1);           % 显示原始画面
    axis(ax1, 'image'); axis(ax1, 'off');

    imr = imresize(im, sz);             % 缩放到网络输入尺寸
    [label, score] = classify(net, imr);% 分类，返回最优类别与全部类别得分
    title(ax1, char(label), 'FontSize', 14);

    [~, idx] = sort(score, 'descend');  % 得分降序排列
    idx = idx(5:-1:1);                  % 取前 5 名（倒序便于条形图自上而下）
    classNames = net.Layers(end).Classes;
    classTop = string(classNames(idx)); % 前 5 名类别名
    scoreTop = score(idx);

    barh(ax2, scoreTop);                % 横向条形图
    xlim(ax2, [0 1]);
    yticklabels(ax2, classTop);
    title(ax2, 'Top 5');
    xlabel(ax2, '概率');
    drawnow;
end
