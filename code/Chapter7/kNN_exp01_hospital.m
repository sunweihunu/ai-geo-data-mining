%% kNN_exp01_hospital.m —— 第7章 案例1：为医院新病人寻找最相似的病人
% 对应书稿《第07章 k最近邻（kNN）模型》7.8.1 节
% 数据：MATLAB 内置 hospital 数据集（100 个病人，需 Statistics and Machine Learning Toolbox）
% 示例数据文件：data/hospital_new_patients.csv（与本脚本中的 Y 取值一致）
% 运行前请将 MATLAB 当前文件夹切换到本脚本所在目录

clear; clc; close all;

%% （1）训练样本的自变量：100 个历史病人的年龄与体重（100×2）
load hospital                        % 载入内置医院数据
X = [hospital.Age  hospital.Weight];

%% （2）待测样本：5 个新病人的年龄与体重（示例数值，5×2）
Y = [20 162;
     35 190;
     42 165;
     50 199;
     62 180];

%% （3）找最近邻：不指定 'K' 时默认 k=1，返回 5×1 的邻居索引
Idx = knnsearch(X, Y);

%% （4）查看 5 个邻居病人的年龄与体重
fprintf('找到的最近邻病人（年龄，体重）：\n');
disp(X(Idx, :));

%% （5）可视化：蓝色 * 为新病人，红色 o 为查到的最近邻
figure; hold on;
plot(X(:,1), X(:,2), 'k.', 'MarkerSize', 10);            % 全部历史病人
plot(Y(:,1), Y(:,2), 'b*', 'MarkerSize', 12);            % 新病人（待测样本）
plot(X(Idx,1), X(Idx,2), 'ro', 'MarkerSize', 12, ...
     'LineWidth', 2);                                    % 最近邻
xlabel('年龄'); ylabel('体重');
title('医院病人的 kNN 查询（k=1）');
legend('历史病人', '新病人', '最近邻', 'Location', 'best');
hold off;
