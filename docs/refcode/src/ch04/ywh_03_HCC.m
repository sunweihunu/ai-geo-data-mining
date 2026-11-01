%    基于余弦测度距离的层次聚类


% ========= Step 1: 基于余弦测度距离的层次聚类
% 根据 K 均值聚类的结果，我们也不妨使用余弦来测度距离。
% 由此生成的层次结构树很不一样，让我们能够以一种完全不同的方式观察鸢尾花数据的组结构。
cosD = pdist(meas,'cosine');
clustTreeCos = linkage(cosD,'average');
cophenet(clustTreeCos,cosD)

%  ========= Step 2: 查看层次聚类图
figure;
[h,nodes] = dendrogram(clustTreeCos,0);
h_gca = gca;
h_gca.TickDir = 'out';
h_gca.TickLength = [.002 0];
h_gca.XTickLabel = [];
title('基于余弦测度距离的层次聚类图');
% 此树的最高级别将鸢尾花标本分成两个区别很大的组。
% 树状图显示，使用余弦距离，相对于组间差异的组内差异远小于使用欧几里德距离的情况。
% 这正是您期望的数据结果，因为对于从原点出发的相同“方向”上的对象，余弦距离将其两两距离计为零。


% ========= Step 3: 简化图结构，再次查看层次聚类图
% 包含 150 个观测值的图较为杂乱，但您可以制作简化的树状图，不显示树中靠近底部的级别。
figure;
[h,nodes] = dendrogram(clustTreeCos,12);
title('简化图结构，再次查看层次聚类图');

% 此树中的三个最高节点划分出三个大小相同的组，以及一个与任何其他组都不相近的标本（标记为叶节点 5）。
[sum(ismember(nodes,[11 12 9 10])) sum(ismember(nodes,[6 7 8])) ...
                  sum(ismember(nodes,[1 2 4 3])) sum(nodes==5)]
              

% ========= Step 4: 使用 cluster 函数来裁剪树
% 在很多情况下，树状图结果或许已能满足分类要求。但是，您可以更进一步，
% 使用 cluster 函数来裁剪树并将观测值显式划分为特定的聚类，就像使用 K 均值一样。
% 根据使用余弦距离的层次结构创建聚类，指定连接高度以在三个最高节点下方裁剪树，
% 创建四个聚类，然后绘制经过聚类的原始数据。
figure;
hidx = cluster(clustTreeCos,'criterion','distance','cutoff',.006);
for i = 1:5
    clust = find(hidx==i);
    plot3(meas(clust,1),meas(clust,2),meas(clust,3),ptsymb{i});
    hold on
end
hold off
xlabel('Sepal Length');
ylabel('Sepal Width');
zlabel('Petal Length');
view(-137,10);
grid on
title('使用 cluster 函数来裁剪树');
% 此图显示，就其性质而言，使用余弦距离的层次聚类结果与三簇 K 均值聚类的结果类似。
% 但是，创建层次聚类树可以一次性可视化所有结果，而在 K 均值聚类中需要使用不同的 K 值进行大量试验。

% ========= Step 5: 基于单连接距离对鸢尾花数据进行层次聚类
% 层次聚类还允许您使用不同的连接进行试验。
% 例如，相比基于平均距离连接聚类，基于单连接距离对鸢尾花数据进行聚类时，
% 往往将距离更大的对象连接在一起，从而给出对数据结构的另一种解释。
figure; 
clustTreeSng = linkage(eucD,'single');
[h,nodes] = dendrogram(clustTreeSng,0);
h_gca = gca;
h_gca.TickDir = 'out';
h_gca.TickLength = [.002 0];
h_gca.XTickLabel = [];
title('基于单连接距离对鸢尾花数据进行层次聚类')