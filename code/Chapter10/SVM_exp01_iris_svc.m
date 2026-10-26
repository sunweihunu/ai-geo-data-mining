%% SVM_exp01_iris_svc.m  鸢尾花二分类：fitcsvm + predict
% 对应《第10章 支持向量机》10.8.1 案例一（图 10-14）
% 环境：MATLAB R2018a+，Statistics and Machine Learning Toolbox
% 数据：MATLAB 自带 fisheriris（150 样本、4 特征、3 类）
% 说明：去掉 setosa 一类，用花瓣长度/宽度做 versicolor-virginica 二分类

clear; clc;

% 1) 数据准备与标准化（SVM 求解用到偏导，务必标准化）
load fisheriris                       % meas(150x4), species(150x1)
idx = ~strcmp(species, 'setosa');     % 去掉 setosa，保留两类做二元分类
X = meas(idx, 3:4);                   % 花瓣长度(x1)、花瓣宽度(x2)
y = species(idx);
X = (X - mean(X)) ./ std(X);          % 标准化

% 2) 训练 RBF 核 SVC 模型
Mdl = fitcsvm(X, y, 'KernelFunction', 'rbf', ...
              'KernelScale', 'auto');
sv  = Mdl.IsSupportVector;            % 支持向量的行下标
yp  = predict(Mdl, X);                % 回代预测
acc = mean(strcmp(yp, y));            % 回代正确率
fprintf('支持向量 %d 个，回代正确率 = %.2f%%\n', sum(sv), 100*acc);

% 3) 可视化决策边界与支持向量
d = 0.02;
[x1g, x2g] = meshgrid(min(X(:,1))-0.3:d:max(X(:,1))+0.3, ...
                      min(X(:,2))-0.3:d:max(X(:,2))+0.3);
Xgrid  = [x1g(:) x2g(:)];
labels = predict(Mdl, Xgrid);         % 网格点类别，用于画分类区
figure; hold on
gscatter(Xgrid(:,1), Xgrid(:,2), cellstr(labels), ...
         [0.85 0.92 0.98]);           % 分类区背景
gscatter(X(:,1), X(:,2), y);          % 训练样本
plot(X(sv,1), X(sv,2), 'ko', 'MarkerSize', 11);   % 圈出支持向量
xlabel('花瓣长度（标准化）'); ylabel('花瓣宽度（标准化）');
title('鸢尾花二分类：SVC 决策边界与支持向量');
