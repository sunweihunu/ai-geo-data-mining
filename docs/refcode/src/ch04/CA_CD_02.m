% clusterdata 
% 最短距离法&马氏距离
S=['福岗';'合肥';'武汉';'长沙';'桂林';'温州';'成都'];
blank=[' 属于 ';' 属于 ';' 属于 ';' 属于 ';' 属于 ';' 属于 ';' 属于 '];
X=[16.2  1492  2000  -8.2  6.2
15.7  970   2209  -20.6  1.9
16.3  1260  2085  -17.3  2.8
17.2  1422  1726  -9.5   4.6
18.8  1874  1709  -4.9   8.0
17.9  1698  1848  -4.5   7.5
16.3  976   1239  -4.6   5.6];  

T0 = clusterdata(X,0.8);
 [S blank num2str(T0) ]
 
T1 = clusterdata(X,4);
 [S blank num2str(T1) ]
 
T2 = clusterdata(X,'Distance' ,'squaredeuclidean','Linkage','centroid','Maxclust',4);
 [S blank num2str(T2) ]
% 
% D=pdist(X,'mahal');               %基于主成分得分计算标准欧式距离
% M=squareform(D);                  %排出欧式距离矩阵
% Z=linkage(D,'single');            %根据最短距离法聚类
% H=dendrogram(Z,'labels',S);       %画出聚类谱系图并添加样品标签           
% xlabel('City');                   %谱系图的横轴标签
% ylabel('Scale');                  %谱系图的纵轴标签
% C=cophenet(Z,D);                  %计算Cophenetic相关系数
% T=cluster(Z,3);                   %指定分类数目