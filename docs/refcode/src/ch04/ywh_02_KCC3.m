% =====  Step 1 使用余弦距离 进行kmeans 聚类
% 您还可以使用不同距离对这些数据进行聚类。余弦距离可能适用于这些数据，
% 因为它会忽略测量值的绝对大小，只考虑相对大小。
% 因此，对于两朵大小不同但花瓣和萼片的形状相似的花，
% 使用平方欧几里德距离可能不接近，但使用余弦距离则会接近。
[cidxCos,cmeansCos] = kmeans(meas,3,'dist','cos');

%  ===== Step 2 是有轮廓图查看聚类效果
% 从轮廓图中可以看出，这些簇的区分效果好像只比使用平方欧几里德距离时稍好一点。
figure;
[silhCos,h] = silhouette(meas,cidxCos,'cos');
[mean(silh2) mean(silh3) mean(silhCos)]
% 请注意，簇的顺序与之前的轮廓图不一样。这是因为 kmeans 会随机选择初始簇分配。
title('3簇的基于余弦距离k-means聚类的轮廓图');


% ===== Step 3 绘制原始数据
% 通过绘制原始数据，您可以看到使用两种不同距离创建的簇在形状上的差异。
% 两个解较为相似，但使用余弦距离时，上方的两个簇向原点拉伸。
figure;
for i = 1:3
    clust = find(cidxCos==i);
    plot3(meas(clust,1),meas(clust,2),meas(clust,3),ptsymb{i});
    hold on
end
hold off
xlabel('Sepal Length');
ylabel('Sepal Width');
zlabel('Petal Length');
view(-137,10);
grid on
title ('基于前三个维度和余弦距离的3簇的散点图');
% 此图不包括簇质心，因为使用余弦距离时，质心是以原始数据空间原点为起点的射线。


% ===== Step 4 绘制归一化数据点的平行坐标图
% 但是，您可以绘制归一化数据点的平行坐标图，以直观地了解簇质心的差异。
figure
lnsymb = {'b-','r-','m-'};
names = {'SL','SW','PL','PW'};
meas0 = meas ./ repmat(sqrt(sum(meas.^2,2)),1,4);
ymin = min(min(meas0));
ymax = max(max(meas0));
for i = 1:3
    subplot(1,3,i);
    plot(meas0(cidxCos==i,:)',lnsymb{i});
    hold on;
    plot(cmeansCos(i,:)','k-','LineWidth',2);
    hold off;
    title(sprintf('Cluster %d',i));
    xlim([.9, 4.1]);
    ylim([ymin, ymax]);
    h_gca = gca;
    h_gca.XTick = 1:4;
    h_gca.XTickLabel = names;
end
title ('归一化数据点的平行坐标图');

% 从图中可以清楚地看出，三个簇所包含的标本在花瓣和萼片的平均相对大小方面明显不同。
% 第一个簇的花瓣严格小于萼片。后面两个簇的花瓣和萼片的大小重叠，但第三个簇的重叠超过第二个簇。您还可以看到，
% 第二个和第三个簇包含一些非常相似的标本。


% ===== Step 5 绘制边缘交界处的五个点
% 因为我们知道数据中每个观测值所属的品种，所以可以将 kmeans 发现的簇与实际品种进行比较，
% 以了解这三个品种是否具有明显不同的物理特性。
% 实际上，如下图所示，使用余弦距离创建的簇与实际品种分组的不同之处只有五朵花。
% 这五个点（用星形标记绘制）都靠近上方两个簇的边缘交界处。
 figure;
% subplot(1,1,1);
for i = 1:3
    clust = find(cidxCos==i);
    plot3(meas(clust,1),meas(clust,2),meas(clust,3),ptsymb{i});
    hold on
end
xlabel('Sepal Length');
ylabel('Sepal Width');
zlabel('Petal Length');
view(-137,10);
grid on
sidx = grp2idx(species);
miss = find(cidxCos ~= sidx);
plot3(meas(miss,1),meas(miss,2),meas(miss,3),'k*');
legend({'setosa','versicolor','virginica'});
hold off
title ('基于前三个维度和余弦距离的kmeans聚类和实际类别差异（星号）');