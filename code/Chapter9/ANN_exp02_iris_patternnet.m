%% 案例2：Fisher 鸢尾花的 BP 网络多分类（patternnet + trainscg + train + sim）
% 对应书稿《人工智能与地理数据挖掘》第09章 9.9.2
clear; clc;

% 1) 载入内置数据集
load fisheriris                        % meas: 150×4 测量值；species: 150×1 品种名

% 2) 整理为网络输入/目标：列向量 = 样本；目标为 one-hot 编码
X = meas';                             % 4×150
labels = grp2idx(species);             % 品种名 → 1/2/3
T = ind2vec(labels');                  % 3×150 目标向量

% 3) 创建分类网络：隐层 tansig（10 节点），输出层 softmax
net = patternnet(10);                  % 中小规模分类建议 'trainrp'，
net.trainFcn = 'trainscg';             % 大规模分类/回归建议 'trainscg'

% 4) 训练（内部按比例随机划分训练/验证/测试，并自动应用早停）
[net, tr] = train(net, X, T);

% 5) 预测：sim 输出各类概率（每列和为 1），取最大者为类别
Y    = sim(net, X);                    % 3×150
pred = vec2ind(Y);                     % 概率最大的类别编号

% 查看第 1 个样本属于三类的概率
fprintf('第 1 个样本的类概率：setosa=%.3f，versicolor=%.3f，virginica=%.3f\n', ...
        Y(1,1), Y(2,1), Y(3,1));

% 6) 性能评估：回代正确率与混淆矩阵
accuracy = mean(pred == labels);
fprintf('回代正确率 = %.2f%%\n', 100*accuracy);

figure;
plotconfusion(T, Y);                   % 三类混淆矩阵
title('案例2：鸢尾花 BP 网络分类');
