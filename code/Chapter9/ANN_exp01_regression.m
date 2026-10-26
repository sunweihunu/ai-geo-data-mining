%% 案例1：一元非线性函数的 BP 网络回归（fitnet + trainlm + train + sim）
% 对应书稿《人工智能与地理数据挖掘》第09章 9.9.1（图 9-15）
clear; clc;

% 1) 生成模拟数据：y = sin(x) + 0.16x + 噪声（与插图脚本 gen_figures.py 一致，种子 42）
rng(42);
x = linspace(0, 6, 60)';                       % 60×1 自变量
y = sin(x) + 0.16*x + 0.10*randn(size(x));     % 60×1 因变量

% 2) 数据分割：前 48 个训练，后 12 个验证（行向量 = 样本）
P = x(1:48)';      T = y(1:48)';               % 训练集
Q = x(49:60)';     V = y(49:60)';              % 验证集

% 3) 创建 1-8-1 多层前馈网络：隐层 tansig，输出层 purelin
net = fitnet(8);                    % 隐含层 8 个节点
net.trainFcn = 'trainlm';           % 中小规模回归：推荐 trainlm / trainbr
net.divideFcn = 'dividerand';       % 内部再随机划分训练/验证/测试
net.trainParam.epochs = 500;        % 最大训练轮数
net.trainParam.goal   = 1e-4;       % 误差目标（均方误差）

% 4) 训练（BP 类算法自动完成前向计算与误差反向传播）
[net, tr] = train(net, P, T);

% 5) 预测：sim 模拟网络
y_fit_train = sim(net, P);          % 训练集预测
y_fit_valid = sim(net, Q);          % 验证集预测

% 6) 性能评估：mse 与相关系数
fprintf('训练集 MSE = %.4f，R = %.4f\n', ...
        mse(y_fit_train - T), corr(y_fit_train, T));
fprintf('验证集 MSE = %.4f，R = %.4f\n', ...
        mse(y_fit_valid - V), corr(y_fit_valid, V));

% 7) 可视化
figure; hold on;
plot(x, y, 'k.', 'MarkerSize', 10);                      % 全部样本
xx = linspace(0, 6, 200)';
plot(xx, sin(xx) + 0.16*xx, 'k--', 'LineWidth', 1.2);    % 真实关系
plot(xx, sim(net, xx'), 'r-', 'LineWidth', 1.8);         % 网络拟合
xlabel('自变量 x'); ylabel('因变量 y');
legend('样本', '真实关系', '1-8-1 网络拟合', 'Location', 'northwest');
title('案例1：BP 网络非线性回归');
