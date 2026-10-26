%% 案例2：Fisher 鸢尾花数据的 K-均值聚类
% 对应书稿 4.6.2 节：忽略品种做聚类，再与真实品种对照（外部评估）
clear; clc;

load fisheriris                     % meas: 150×4 测量值；species: 品种名

% 1. K-均值聚类：k=3（默认平方欧氏距离；Replicates 多算几遍取最好）
idx = kmeans(meas, 3, 'Replicates', 5);

% 2. 轮廓评价（内部评估）：轮廓值应均大于 0，越大越合理
figure; silhouette(meas, idx);
title('鸢尾花 K-均值聚类的轮廓图');
s = silhouette(meas, idx);
fprintf('平均轮廓系数 = %.3f\n', mean(s));

% 3. 与真实品种对照（外部评估：混淆矩阵，行=品种，列=聚类类别）
crosstab(species, idx)

% 4. 可视化：花瓣长×宽平面上，聚类结果 vs 真实品种
figure;
subplot(1,2,1); gscatter(meas(:,3), meas(:,4), idx, 'bgr');
title('K-均值聚类结果（k=3）'); xlabel('花瓣长度 (cm)'); ylabel('花瓣宽度 (cm)');
subplot(1,2,2); gscatter(meas(:,3), meas(:,4), species, 'bgr');
title('真实品种'); xlabel('花瓣长度 (cm)'); ylabel('花瓣宽度 (cm)');
