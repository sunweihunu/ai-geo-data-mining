%% gen_demo_data.m — HW06 动物篇 示例数据生成
%  生成 data/川金丝猴_西南山地.mat，字段 presence/env/envNames/gridLonLat/gridX。
%  运行方式：cd 到本作业根目录后执行 >> gen_demo_data
%  数据特征：5 个 BIOCLIM 因子按经纬度构造；出现点落在“适宜区”
%           (BIO1∈[8,13], BIO12∈[850,1250])，使 RF/SVM 能学到分布关系(AUC>0.5)。
%  列顺序：[BIO1_temp, BIO12_precip, BIO4_seas, BIO15_alt, BIO3_iso]
%         —— future_shift 中第1列(温度)施加深海升温扰动。
clear; clc;
if ~isfolder('data'), mkdir('data'); end
rng(42);

[ny,nx] = deal(150,150);
[lon,lat] = meshgrid(linspace(100,105,nx), linspace(28,33,ny));
gridLonLat = [lon(:) lat(:)];

BIO = zeros(ny,nx,5);
BIO(:,:,1) = 10  + 4*(lon-102.5)                       + 0.5*randn(ny,nx); % BIO1 温度(经向)
BIO(:,:,2) = 1000 + 250*(1-((lat-30.5)/2.5).^2)        + 60*randn(ny,nx);  % BIO12 降水(纬向峰)
BIO(:,:,3) = 0.5 + 0.3*rand(ny,nx);                                        % BIO4
BIO(:,:,4) = 500 + 2000*exp(-((lon-102.5).^2+(lat-30.5).^2)/4);            % BIO15 海拔
BIO(:,:,5) = 5   + 2*randn(ny,nx);                                         % BIO3

gridX = reshape(BIO, ny*nx, 5);

% 适宜区
mask = BIO(:,:,1)>8 & BIO(:,:,1)<13 & BIO(:,:,2)>850 & BIO(:,:,2)<1250;
idx = find(mask);
npres = min(200, numel(idx));
sel = idx(randperm(numel(idx), npres));
presence = gridLonLat(sel,:);

env = squeeze(num2cell(BIO,[1 2]));             % 1×5 cell，每格 ny×nx 栅格
envNames = ["BIO1_temp","BIO12_precip","BIO4_seas","BIO15_alt","BIO3_iso"];

save('data/川金丝猴_西南山地.mat','presence','env','envNames','gridLonLat','gridX','-v7');
fprintf('已生成 data/川金丝猴_西南山地.mat (出现点 %d, 适宜像元 %d)\n', npres, numel(idx));
