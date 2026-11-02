%% gen_demo_data.m — HW05 植被篇 示例数据生成
%  生成 data/青藏高原.mat，字段 NDVI/time/lon/lat/climate，供 main_demo.m 跑通。
%  运行方式：cd 到本作业根目录后执行 >> gen_demo_data
%  关键约束：
%   - nt = 21年×23景 = 483，使 reshape(NDVI(:,1),23,[]) 严格成立；
%   - NDVI 含清晰年周期(周期23)+长期上升趋势，使物候提取与 trend_mk 显著；
%   - climate.temp/rain 与 NDVI 同相。
clear; clc;
if ~isfolder('data'), mkdir('data'); end
rng(42);

nyrs = 21; nper = 23; nt = nyrs*nper;          % 483
time = datetime(2000,1,1) + hours(16*(0:nt-1))';
npix = 500;
phase = linspace(0, 2*pi, npix);                % 各像元年相位略有差异
yr_idx = (0:nt-1)';

% 年周期(周期=23) + 上升趋势 + 噪声
NDVI = 0.35 ...
     + 0.25*sin(2*pi*yr_idx/23 + phase) ...
     + 0.0015*yr_idx ...                        % 上升趋势 → trend_mk 斜率>0
     + 0.04*randn(nt,npix);
NDVI = max(min(NDVI,0.9),0.1);

lon = linspace(90,95,npix);
lat = linspace(28,35,npix);

% 气候（月尺度）
clim_t = datetime(2000,1,1) + calmonths(0:nt-1)';
cm = month(clim_t);
climate.temp = 5  + 12*sin(2*pi*cm/12 - 1)   + randn(nt,1);
climate.rain = 60 + 90*sin(2*pi*cm/12 - 1.5) + 15*randn(nt,1);

save('data/青藏高原.mat','NDVI','time','lon','lat','climate','-v7');
fprintf('已生成 data/青藏高原.mat (nt=%d × npix=%d)\n', nt, npix);
