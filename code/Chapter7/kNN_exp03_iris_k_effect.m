%% kNN_exp03_iris_k_effect.m —— 第7章 案例3：k 对鸢尾花分类性能的影响
% 对应书稿《第07章 k最近邻（kNN）模型》7.8.3 节
% 数据：MATLAB 内置 fisheriris，本例使用全部 4 个属性
% 思路：k=1..10 逐个训练 kNN 分类器，统计训练集回代正确率与 10 折交叉验证正确率，
%       画出性能随 k 变化的曲线（书稿图 7-13）

clear; clc; close all;

load fisheriris
ks = (1:10)';
accTrain = zeros(size(ks));
accCV    = zeros(size(ks));

rng(1);                              % 固定随机种子，保证交叉验证结果可重复
for i = 1:numel(ks)
    Mdl = fitcknn(meas, species, 'K', ks(i));       % 以 150 个标本为训练集
    pred = predict(Mdl, meas);                      % 在训练集上回代预测
    accTrain(i) = mean(strcmp(pred, species));      % 训练集分类正确率

    CVModel = crossval(Mdl, 'KFold', 10);           % 10 折交叉验证（验证性能）
    accCV(i) = 1 - kfoldLoss(CVModel);
end

T = table(ks, accTrain, accCV, ...
          'VariableNames', {'k', 'TrainAcc', 'CVAcc'});
disp(T);
% 课件观察：训练集上 k=1、k=2 分类正确率均为 100%，k>=3 开始出现错分样本；
% 交叉验证正确率更能反映泛化性能，可据其随 k 的变化曲线选取较优的 k（7.2.5 节）。

figure;
plot(ks, accTrain, 'o-', 'LineWidth', 1.5); hold on;
plot(ks, accCV,    's--', 'LineWidth', 1.5);
xlabel('k'); ylabel('分类正确率');
xlim([0.5 10.5]);
legend('训练集回代', '10 折交叉验证', 'Location', 'best');
title('k 对 kNN 鸢尾花分类性能的影响（4 个属性）');
grid on; hold off;
