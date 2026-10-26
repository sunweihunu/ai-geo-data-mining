%% SVM_exp02_svr_sine.m  一元非线性回归：fitrsvm + predict
% 对应《第10章 支持向量机》10.8.2 案例二
% 环境：MATLAB R2018a+，Statistics and Machine Learning Toolbox
% 流程：标准化 -> 高斯核 SVR -> 预测 -> 反标准化 -> 性能评估

clear; clc; rng(42);

% 1) 构造正弦+噪声数据并标准化
x = linspace(-3, 3, 60)';
y = sin(0.9*x) + 0.12*randn(size(x));   % 正弦 + 噪声
xs = (x - mean(x)) / std(x);            % 标准化
ys = (y - mean(y)) / std(y);

% 2) 训练高斯核 SVR 模型
Mdl = fitrsvm(xs, ys, 'KernelFunction', 'gaussian', ...
              'KernelScale', 0.9);
yb  = predict(Mdl, xs);                 % 标准化尺度上的预测

% 3) 反标准化（还原原始数量级）后再做性能评估
yhat = yb * std(y) + mean(y);
fprintf('相关系数 r = %.3f，RMSE = %.3f\n', corr(y, yhat), ...
        sqrt(mean((y - yhat).^2)));

% 4) 可视化
figure; plot(x, y, 'bo'); hold on;
plot(x, yhat, 'r-', 'LineWidth', 1.8);  % SVR 回归曲线
legend('样本', 'SVR 预测'); xlabel('x'); ylabel('y');
title('一元非线性函数的 SVR 回归');

% 扩展：把核函数换成 linear / polynomial 对比（对应书稿图 10-7）
% Mdl2 = fitrsvm(xs, ys, 'KernelFunction', 'polynomial', 'KernelScale', 0.9);
% Mdl3 = fitrsvm(xs, ys, 'KernelFunction', 'linear',       'KernelScale', 0.9);
