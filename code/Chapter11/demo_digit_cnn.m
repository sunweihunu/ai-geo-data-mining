%% demo_digit_cnn.m —— 从头构建 CNN 识别手写数字
% 对应《人工智能与地理数据挖掘》第11章 案例二（11.7.2 节）
% 数据：手写数字图像（0—9 共 10 类，28×28 灰度图）。
%   优先使用当前目录下的 DigitDataset 文件夹（按数字 0—9 分子文件夹存放，
%   子文件夹名即类别标签）；若不存在，则使用 MATLAB 自带的示例数据集。

clear; clc;

% 1) 读入数字图像数据集
if exist('DigitDataset', 'dir')
    dataFolder = 'DigitDataset';
else
    dataFolder = fullfile(matlabroot, 'toolbox', 'nnet', 'nndemos', ...
                          'nndatasets', 'DigitDataset');
    fprintf('未找到本地 DigitDataset，改用 MATLAB 自带示例数据集：\n%s\n', dataFolder);
end
imds = imageDatastore(dataFolder, ...
    'IncludeSubfolders', true, ...
    'LabelSource', 'foldernames');

% 2) 随机划分：每个类别 750 张训练、其余验证
[imdsTrain, imdsValid] = splitEachLabel(imds, 750, 'randomized');

% 3) 定义网络结构：输入 -> 卷积 -> 批标准化 -> ReLU -> 最大池化 -> 全连接 -> softmax -> 分类层
layers = [
    imageInputLayer([28 28 1])                    % 单通道 28×28 图像输入
    convolution2dLayer(3, 16, 'Padding', 'same')  % 3×3 卷积核，16 个特征图
    batchNormalizationLayer                       % 批标准化
    reluLayer                                     % ReLU 激活
    maxPooling2dLayer(2, 'Stride', 2)             % 2×2 最大池化
    fullyConnectedLayer(10)                       % 全连接到 10 个类别
    softmaxLayer                                  % 输出类别概率
    classificationLayer];                         % 交叉熵损失

% 4) 训练选项（求解器、最大轮数、验证数据与频率、训练进度图）
options = trainingOptions('sgdm', ...
    'MaxEpochs', 10, ...
    'ValidationData', imdsValid, ...
    'ValidationFrequency', 30, ...
    'Plots', 'training-progress');

% 5) 训练并评估
net = trainNetwork(imdsTrain, layers, options);
YPred = classify(net, imdsValid);
accuracy = mean(YPred == imdsValid.Labels);
fprintf('验证集正确率 = %.2f%%\n', accuracy * 100);
