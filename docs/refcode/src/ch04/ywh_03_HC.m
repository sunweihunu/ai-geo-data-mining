
% Clustering Fisher's Iris Data Using Hierarchical Clustering
% K 均值聚类只产生一个鸢尾花数据分区，但您可能还想按照不同的分组尺度来研究数据。
% 要实现这一点，您可以通过层次聚类创建层次聚类树。
% 首先，使用鸢尾花数据中观测值之间的距离创建一个聚类树。先使用欧几里德距离。
eucD = pdist(meas,'euclidean');
clustTreeEuc = linkage(eucD,'average');

% 共性相关是验证聚类树与原始距离是否一致的一种方法。较大的值表明树对距离的拟合良好，
% 即观测值之间的两两连接与它们实际上的两两距离是相关的。此树对距离的拟合看起来相当好。
cophenet(clustTreeEuc,eucD)

% 要可视化聚类的层次结构，可以绘制树状图。
figure;
[h,nodes] = dendrogram(clustTreeEuc,0);
h_gca = gca;
h_gca.TickDir = 'out';
h_gca.TickLength = [.002 0];
h_gca.XTickLabel = [];
title('基于欧几里德距离的层次聚类树');

% 
% 树中的根节点远远高于其余节点，证实了您在 K 均值聚类中所看到的：两个很大的、区别明显的观测值组。
% 在每个组中可以看到，随着距离尺度越来越小，较低级别的组逐渐出现。
% 有许多级别不同、大小不同、区别度不同的组。
