%% gen_demo_data.m — HW03 地貌篇 示例数据生成
%  生成 data/安宁河.mat，字段 DEM/inventory/factors/factorNames/ref，供 main_demo.m 跑通。
%  运行方式：cd 到本作业根目录后执行 >> gen_demo_data
%  数据特征：DEM 含两座高斯形态山体；滑坡编目点偏向陡坡(梯度大)处，
%           使 derive_factors 派生的坡度/TWI 与易发性相关。
clear; clc;
if ~isfolder('data'), mkdir('data'); end
rng(42);

[ny,nx] = deal(150,150);
[Xg,Yg] = meshgrid(linspace(101,103,nx), linspace(25,27,ny));
DEM = 600 ...
    + 1500*exp(-((Xg-102.0).^2+(Yg-26.0).^2)/0.35) ...
    + 400 *exp(-((Xg-101.5).^2+(Yg-26.4).^2)/0.15) ...
    + 50*randn(ny,nx);

% 滑坡编目：陡坡处按概率布点
[Gx,Gy] = gradient(DEM);
gradmag = sqrt(Gx.^2 + Gy.^2);
prob = gradmag(:) / max(gradmag(:));
cand = find(rand(ny*nx,1) < prob*0.25);
inventory = [Xg(cand) Yg(cand)];
if size(inventory,1) > 200, inventory = inventory(1:200,:); end

factors = {}; factorNames = {};
ref = DEM > mean(DEM(:));                  % 占位地质易发性基准（用于 Kappa 验证）

save('data/安宁河.mat','DEM','inventory','factors','factorNames','ref','-v7');
fprintf('已生成 data/安宁河.mat (%dx%d, 编目点 %d)\n', ny, nx, size(inventory,1));
