%% gen_demo_data.m — HW01 水文篇 示例数据生成
%  生成 data/北江石角站.mat，字段 time/P/E/Q，供 main_demo.m 跑通。
%  运行方式：cd 到本作业根目录后执行 >> gen_demo_data
%  数据特征：P(降雨)有年周期；Q(径流)由当月及前两月降雨驱动并扣蒸发，
%           使 Lasso/线性/BP 模型能学到有意义的预报关系（R²>0）。
clear; clc;
if ~isfolder('data'), mkdir('data'); end
rng(42);

year0 = 1980; year1 = 2020;
time = datetime(year0,1,1) + calmonths(0:(year1-year0)*12)';   % 月尺度
n = numel(time);
mth = month(time);

% 降雨：夏季峰值，年周期 + 噪声
P = 80 + 130*sin(2*pi*mth/12 - 1.2) + 35*randn(n,1);
P = max(P, 5);
% 蒸发：与辐射同相，略滞后
E = 70 + 45*sin(2*pi*mth/12 - 2.0) + 8*randn(n,1);
E = max(E, 10);
% 径流：当月+前1+前2月降雨驱动，扣蒸发
P1 = circshift(P,1); P2 = circshift(P,2);
Q = 400 + 3.2*P + 2.2*P1 + 1.3*P2 - 1.8*E + 180*randn(n,1);
Q = max(Q, 80);

save('data/北江石角站.mat','time','P','E','Q','-v7');
fprintf('已生成 data/北江石角站.mat (%d 个月; <Q>=%.0f m3/s)\n', n, mean(Q));
