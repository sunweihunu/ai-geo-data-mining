%% 案例2（续）：Fisher 鸢尾花数据的层次聚类
% 对应书稿 4.6.2 节：谱系图人工画线选类数，切 3 类后与品种对照
clear; clc;

load fisheriris

% 1. 层次聚类：组间平均法 + 欧氏距离
Z = linkage(meas, 'average', 'euclidean');

% 2. 画完整谱系图：从上往下画一条线即可分 2、3、4 类观察
figure; dendrogram(Z, 0);           % 参数 0 表示显示全部 150 个叶子
title('鸢尾花层次聚类谱系图（组间平均法）'); ylabel('合并距离');

% 3. 聚类质量：Cophenetic 相关系数
C = cophenet(Z, pdist(meas))        % 越接近 1，谱系图与原始距离越一致

% 4. 切 3 类并与真实品种对照
T = cluster(Z, 'maxclust', 3);
crosstab(species, T)                % 混淆矩阵：行=品种，列=类别
