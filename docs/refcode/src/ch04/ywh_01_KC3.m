% 3簇的k-means聚类

% 3簇的k-means聚类% 您可以增加簇数以查看 kmeans 是否可以在数据中找到进一步的分组结构。
% 这次，使用可选的 'Display' 名称-值对组参数显示聚类算法中有关每次迭代的信息。
[cidx3,cmeans3] = kmeans(meas,3,'Display','iter');

% 在每次迭代时，kmeans 算法（请参阅 算法）在簇之间重新分配点，以减小点到质心距离的总和，
% 然后重新计算新簇分配的簇质心。请注意，距离总和与重新分配次数随着每次迭代而减小，直到算法达到最小值。
% kmeans 中使用的算法由两个阶段组成。
% 在此示例中，算法的第二阶段未进行任何重新分配，表明第一阶段在进行几次迭代后就达到了最小值。
% 默认情况下，kmeans 使用随机选择的一组初始质心位置开始聚类过程。
% kmeans 算法会收敛于作为局部最小值的解；也就是说，kmeans 可对数据进行分区，
% 使得将任一点移到其他簇都会增加距离总和。但是，同许多其他类型的数值最小化问题一样，kmeans 达到的解有时取决于起点。
% 因此，该数据可能存在其他具有更小距离总和的解（局部最小值）。
% 您可以使用可选的 'Replicates' 名称-值对组参数来检验不同的解。指定多次重复时，
% kmeans 会在每次重复时从不同的随机选择质心重新开始聚类过程。
% kmeans 随后返回所有重复中距离总和最小的解。
[cidx3,cmeans3,sumd3] = kmeans(meas,3,'replicates',5,'display','final');

%
% 输出表明，即使对于这样相对简单的问题，也存在非全局最小值。这五次重复分别从一组不同的初始质心开始。
% 根据起始位置，kmeans 达到两个不同的解之一。
% 但是，kmeans 最终返回的解是所有重复中距离总和最小的解。
% 第三个输出参数包含每个簇中对于该最佳解的距离总和。
sum(sumd3)


% 该三簇解的轮廓图显示，有一个簇区分效果很好，但另外两个簇的区别不是很明显。
figure;
[silh3,h] = silhouette(meas,cidx3,'sqeuclidean');
title('3簇的k-means聚类的轮廓图');

%%
% Again, you can plot the raw data to see how |kmeans| has assigned the
% points to clusters.
figure;
for i = 1:3
    clust = find(cidx3==i);
    plot3(meas(clust,1),meas(clust,2),meas(clust,3),ptsymb{i});
    hold on
end
plot3(cmeans3(:,1),cmeans3(:,2),cmeans3(:,3),'ko');
plot3(cmeans3(:,1),cmeans3(:,2),cmeans3(:,3),'kx');
hold off
xlabel('Sepal Length');
ylabel('Sepal Width');
zlabel('Petal Length');
view(-137,10);
grid on
title ('基于前三个维度的3簇的散点图');

% 您可以看到，kmeans 已将双簇解中的上方簇一分为二，而且这两个簇非常接近。
% 跟之前的双簇解相比，这个三簇解是否更为有用取决于您在聚类后要对数据进行的操作。
% silhouette 的第一个输出参数包含每个点的轮廓值，您可以使用这些值对两个解进行定量比较。
% 双簇解的平均轮廓值更大，表明就簇的区分效果而言，这是更好的解。
[mean(silh2) mean(silh3)]