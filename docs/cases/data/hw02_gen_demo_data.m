%% gen_demo_data.m — HW02 气候篇 示例数据生成
%  生成 data/华南.mat，字段 time/H500/SST/indices/label，供 main_demo.m 跑通。
%  运行方式：cd 到本作业根目录后执行 >> gen_demo_data
%  数据特征：在 H500(500hPa高度场) 注入一个空间局部、时间周期性的信号模态，
%           并让二分类 label 由该模态时间系数驱动，使 EOF+SVM/决策树 AUC>0.5。
clear; clc;
if ~isfolder('data'), mkdir('data'); end
rng(42);

nt = 41;                                   % 1980-2020 共 41 年
time = datetime(1980,1,1) + calyears(0:nt-1)';

% H500: nt×36×72 (2.5° 格点)。先放背景+噪声
H500 = 5500 + 30*randn(nt,36,72);
% 注入信号模态：时间上 ~1.2 个周期，空间上以(行10,列30)为中心的高斯包络
sig = sin((1:nt)/nt*2*pi*1.2);
[Yg,Xg] = ndgrid(1:36,1:72);
weight = exp(-((Yg-10).^2/60) - ((Xg-30).^2/200));
for i = 1:nt
    H500(i,:,:) = H500(i,:,:) + 80*sig(i)*weight;
end

% label 由 sig 驱动（sig 高→事件概率高）
prob = 1./(1 + exp(-(sig-mean(sig))/std(sig)*1.6));
label = double(rand(nt,1) < prob');

% SST 与 74 项环流指数（噪声为主，供 select_precursor 做对比）
SST = 18 + 6*randn(nt,18,36);
indices = 5*randn(nt,74);

save('data/华南.mat','time','H500','SST','indices','label','-v7');
fprintf('已生成 data/华南.mat (nt=%d, 事件率=%.2f)\n', nt, mean(label));
