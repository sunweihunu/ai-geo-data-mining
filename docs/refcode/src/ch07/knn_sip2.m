% ======== Find k-Nearest Neighbors Using Different Distance Metrics ========
% https://ww2.mathworks.cn/help/stats/knnsearch.html?s_tid=srchtitle_knnsearch_1

% Find the 10 nearest neighbors in X to each point in Y,
% first using the Minkowski distance metric and then using the Chebychev distance metric.
% 
%% Load Fisher's iris data set.

load fisheriris
X = meas(:,3:4);    % Measurements of original flowers
Y = [5 1.45;6 2;2.75 .75];  % New flower data

%% Perform a knnsearch between X and the query points Y 
% using Minkowski and Chebychev distance metrics.
[mIdx,mD] = knnsearch(X,Y,'K',10,'Distance','minkowski','P',5);
[cIdx,cD] = knnsearch(X,Y,'K',10,'Distance','chebychev');
% K — Number of nearest neighbors
% 1 (default) | positive integer

%% Visualize the results of the two nearest neighbor searches. 
% Plot the training data. Plot the query points with the marker X. Use circles to denote the Minkowski nearest neighbors. Use pentagrams to denote the Chebychev nearest neighbors.
gscatter(X(:,1),X(:,2),species)
line(Y(:,1),Y(:,2),'Marker','x','Color','k',...
   'Markersize',10,'Linewidth',2,'Linestyle','none')
line(X(mIdx,1),X(mIdx,2),'Color',[.5 .5 .5],'Marker','o',...
   'Linestyle','none','Markersize',10)
line(X(cIdx,1),X(cIdx,2),'Color','r','Marker','p',...
   'Linestyle','none','Markersize',10)
legend('setosa','versicolor','virginica','query point',...
'minkowski','chebychev','Location','best')