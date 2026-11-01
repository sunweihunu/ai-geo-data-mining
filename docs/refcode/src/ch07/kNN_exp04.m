
% 利用fitcknn函数进行kNN分类
% Construct a KNN classifier for the Fisher iris data as in Construct KNN Classifier.
load fisheriris
% X = meas;    
X =meas(:,3:4);
Y = species; 
Mdl = fitcknn(X,Y,'NumNeighbors',4);

% Predict the classification of an average flower.
%  对数据集的平均值对应的虚拟点（花）进行分类
flwr = mean(X); % an average flower
flwrClass = predict(Mdl,flwr)

%  对三个新数据点进行分类
newpoint2 = [5 1.45;6 2;2.75 .75];
newClass = predict(Mdl,newpoint2)
