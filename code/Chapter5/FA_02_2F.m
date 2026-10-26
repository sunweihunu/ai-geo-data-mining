%% FA_02_2F.m —— factoran 最大似然解（2 因子，从原始数据矩阵出发）
% 要求随机变量服从正态分布。对应书稿 5.4.3 节（表 5-12 第 2 种方法）。
% 若中文注释乱码：主页->预设->编辑器，将编码改为 UTF-8。

clear; clc; close all;

X = Regions2004;                           % 31x8 原始数据

% Lambda：8x2 旋转后载荷矩阵；Psi：8 个特殊方差；
% T：旋转矩阵；Stats：模型检验（H0：因子数=2，看 Stats.p 是否大于显著性水平）；
% F：31x2 因子得分（'Score','wls' 指定加权最小二乘法估计得分）
[Lambda, Psi, T, Stats, F] = factoran(X, 2, 'Score', 'wls');

disp('载荷矩阵 Lambda：');    disp(Lambda);
disp('特殊方差 Psi：');       disp(Psi');
disp('卡方检验 p 值：');      disp(Stats.p);

% 因子得分散点图
regions = {'北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江', ...
           '上海','江苏','浙江','安徽','福建','江西','山东','河南','湖北', ...
           '湖南','广东','广西','海南','重庆','四川','贵州','云南','西藏', ...
           '陕西','甘肃','青海','宁夏','新疆'};
figure;
plot(F(:,1), F(:,2), 'o'); hold on;
line([0 0],[-2.5 2.5]); line([-2.5 2.5],[0 0]);
text(F(:,1)+0.05, F(:,2)+0.05, regions, 'FontSize', 7);
xlabel('F_1 因子得分'); ylabel('F_2 因子得分');
axis equal; axis([-2.5 2.5 -2.5 2.5]);
title('factoran 最大似然解（2 因子）的因子得分');
