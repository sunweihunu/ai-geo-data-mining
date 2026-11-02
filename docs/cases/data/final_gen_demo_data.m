%% gen_demo_data.m — FINAL 大作业 示例数据生成
%  生成 data/广州.mat，字段 LST/urbanMask/factors/gridLonLat/time，供 main_demo.m 跑通。
%  运行方式：cd 到本作业根目录后执行 >> gen_demo_data
%  数据特征：城区(中心 0.15°²) LST 比乡村高约 8℃，并叠加年周期；
%           六要素因子(impervious/NDVI/buildingH/water/pop/soilPerm/birdRich)
%           均由城区掩膜驱动，使 fit_drivers 学到强驱动关系(R²>0.6)。
clear; clc;
if ~isfolder('data'), mkdir('data'); end
rng(42);

[ny,nx] = deal(120,120);
[lon,lat] = meshgrid(linspace(112.8,113.8,nx), linspace(22.8,23.8,ny));
gridLonLat = [lon(:) lat(:)];
npx = ny*nx;

% 城区掩膜：距中心 0.15° 内
d2c = (lon-mean(lon(:))).^2 + (lat-mean(lat(:))).^2;
urbanMask = d2c < 0.15;
uf = double(urbanMask);

% 六要素
factors.impervious = uf + 0.1*randn(ny,nx);
factors.NDVI       = 0.45 - 0.32*uf + 0.05*randn(ny,nx);
factors.buildingH  = 28*uf.*(0.5+rand(ny,nx));
factors.water      = 0.1*(rand(ny,nx)<0.05);
factors.pop        = 5000*uf.*(0.5+rand(ny,nx));
factors.soilPerm   = 0.5 - 0.4*uf + 0.05*randn(ny,nx);
factors.birdRich   = 18*(1-uf).*(0.7+0.3*rand(ny,nx));

% LST 时序：城区+8℃，年周期，噪声
nt = 88;                                        % 11年×8景
time = datetime(2013,1,1) + calmonths(floor((0:nt-1)/8));
season = sin(2*pi*(0:nt-1)/8 + 1)';             % nt×1
urbanEffect = 8*uf(:)';                         % 1×npx
LST = 25 + season + urbanEffect + 4*randn(nt,npx);

save('data/广州.mat','LST','urbanMask','factors','gridLonLat','time','-v7');
fprintf('已生成 data/广州.mat (%dx%d, nt=%d)\n', ny, nx, nt);
