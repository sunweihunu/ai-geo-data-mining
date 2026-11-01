
% % 详细介绍见
% % https://ww2.mathworks.cn/help/stats/clusterdata.html

rng('default');  % For reproducibility
X = [gallery('uniformdata',[10 3],12); ...
    gallery('uniformdata',[10 3],13)+1.2; ...
    gallery('uniformdata',[10 3],14)+2.5];
y = [ones(10,1);2*(ones(10,1));3*(ones(10,1))]; % 实际的类别

figure;
scatter3(X(:,1),X(:,2),X(:,3),100,y)  % 实际的类别图
title('Randomly Generated Data in Three Clusters');

% T1 = clusterdata(X,3);
% scatter3(X(:,1),X(:,2),X(:,3),100,T1,'filled')
% title('Result of Clustering');

T = clusterdata(X,'Maxclust',3);  % 假设是3类
find(T==2)
figure;
scatter3(X(:,1),X(:,2),X(:,3),100,T,'filled') % 分成3类的图
title('Result of Clustering using 3 clusters');


T = clusterdata(X,'Maxclust',5);  % 假设是5类
find(T==2)
figure;
scatter3(X(:,1),X(:,2),X(:,3),100,T,'filled') % 分成5类的图
title('Result of Clustering using 5 clusters');

