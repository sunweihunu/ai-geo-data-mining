%% FA_03_COV.m —— 从协方差矩阵出发，factoran 求最大似然解（2 因子）
% 对应书稿 5.4.3 节（表 5-13 FA_03_COV 行）。
% 注意：X 为协方差矩阵（'Xtype','cov'）时，factoran 不能计算因子得分。
% 若中文注释乱码：主页->预设->编辑器，将编码改为 UTF-8。

clear; clc; close all;

X = Regions2004;                           % 31x8 原始数据

% 从协方差矩阵出发求解（与 FA_02_2F 的原始数据解对照）
[Lambda, Psi, T, Stats] = factoran(cov(X), 2, 'Xtype', 'cov');

disp('载荷矩阵 Lambda：');  disp(Lambda);
disp('特殊方差 Psi：');     disp(Psi');
disp('卡方检验 p 值：');    disp(Stats.p);
