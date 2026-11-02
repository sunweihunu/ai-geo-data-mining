%% gen_demo_data.m — HW04 土壤篇 示例数据生成
%  生成 data/三江平原.mat，字段 samples/reflectance/DEM/climate/gridLonLat/gridX。
%  运行方式：cd 到本作业根目录后执行 >> gen_demo_data
%  关键：samples 的 SOC 与格网前 nS 个像元的特征(NDVI/BI/DEM)同源生成，
%       与 main_demo.m 中 X=Fg.table(1:nS) 严格对齐（均为列优先线性索引），
%       使线性/KNN 回归能学到正 R²。
clear; clc;
if ~isfolder('data'), mkdir('data'); end
rng(42);

[ny,nx] = deal(100,100);
[lon,lat] = meshgrid(linspace(130,133,nx), linspace(45,47,ny));
DEM = 100 + 300*exp(-((lon-131.5).^2+(lat-46).^2)/0.4);

% 6 波段反射率（与 DEM 弱相关；波段顺序假设 B,G,R,NIR,SWIR1,SWIR2）
reflectance = zeros(ny,nx,6);
base = 0.05 + 0.0004*DEM;
for b = 1:6
    reflectance(:,:,b) = base + 0.02*randn(ny,nx) + 0.001*b;
end

% 复制 build_features.m 的特征公式，保证 SOC 与其输出一致
R = reshape(reflectance, ny*nx, 6);
NIR=R(:,4); Red=R(:,3); Green=R(:,2); Blue=R(:,1); SWIR1=R(:,5);
NDVI = (NIR-Red)./(NIR+Red+eps);
BI   = (SWIR1+Blue)./(Green+Red+eps);
CI   = (NIR-Green)./(Green+eps);
Dv   = DEM(:);
% SOC：NDVI(+)、BI(-)、DEM(+) 驱动
SOC = 12 + 40*NDVI - 25*BI + 0.03*(Dv-100) + 2.5*randn(ny*nx,1);

nS = 320;
% 采样点取格网前 nS 个像元(列优先)，与 main_demo 的 X=Fg.table(1:nS) 对齐
samples = [lon(1:nS), lat(1:nS), SOC(1:nS)];

gridLonLat = [lon(:) lat(:)];
gridX = [NDVI, BI, CI, Dv];
climate = struct('rain',800,'temp',3);

save('data/三江平原.mat','samples','reflectance','DEM','climate','gridLonLat','gridX','-v7');
fprintf('已生成 data/三江平原.mat (采样点 %d, SOC 均值 %.1f)\n', nS, mean(samples(:,3)));
