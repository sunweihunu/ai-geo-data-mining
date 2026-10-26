%% FA_02_3F.m —— factoran 最大似然解（3 因子，从原始数据矩阵出发）
% 与 FA_02_2F.m 对照：比较取 2 个与 3 个公因子时载荷结构与检验结果，
% 结合累计方差贡献率与 Stats.p 判断合适的因子个数。
% 若中文注释乱码：主页->预设->编辑器，将编码改为 UTF-8。

clear; clc; close all;

X = Regions2004;                           % 31x8 原始数据

[Lambda, Psi, T, Stats, F] = factoran(X, 3, 'Score', 'wls');

disp('载荷矩阵 Lambda（8x3）：'); disp(Lambda);
disp('特殊方差 Psi：');          disp(Psi');
disp('卡方检验 p 值：');         disp(Stats.p);

% 前 3 个因子的累计方差贡献率（载荷列平方和 / 变量个数）
rate = sum(Lambda .^ 2) / size(X, 2);
fprintf('各因子方差贡献率：%.1f%%  %.1f%%  %.1f%%\n', rate * 100);
fprintf('累计方差贡献率：%.1f%%\n', 100 * sum(rate));
