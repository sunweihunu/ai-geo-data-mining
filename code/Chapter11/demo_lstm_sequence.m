%% demo_lstm_sequence.m —— LSTM 序列分类骨架示例
% 对应《人工智能与地理数据挖掘》第11章 11.7.2 节末尾（LSTM 时序问题参考）。
% 以“序列 -> 单个类别”的多对一结构为例：输入为 cell 数组 sequences，
% 每个元素是一个 numFeatures×numTimeSteps 的数值矩阵；labels 为类别标签。
% 使用时替换为自己的序列数据即可；细节请参考 MATLAB 文档
% “使用深度学习进行序列分类”示例。

clear; clc;

% ---- 以下用伪数据示意，请替换为实际序列数据 ----
% numFeatures = 12; numTimeSteps = 50; numObs = 1000; numClasses = 4;
% sequences = cell(numObs, 1);
% for k = 1:numObs
%     sequences{k} = randn(numFeatures, numTimeSteps);
% end
% labels = categorical(randi(numClasses, numObs, 1));

% 1) 定义网络：序列输入 -> LSTM -> 全连接 -> softmax -> 分类层
layers = [
    sequenceInputLayer(numFeatures)
    lstmLayer(100, 'OutputMode', 'last')   % 多对一：只取最后时刻输出
    fullyConnectedLayer(numClasses)
    softmaxLayer
    classificationLayer];

% 2) 训练选项（时序问题默认推荐 adam）
options = trainingOptions('adam', ...
    'MaxEpochs', 30, ...
    'MiniBatchSize', 64, ...
    'Plots', 'training-progress');

% 3) 训练与预测
% net = trainNetwork(sequences, labels, layers, options);
% YPred = classify(net, sequences);
