% Optimize Classification Tree
% This example shows how to optimize hyperparameters automatically using fitctree. 
% The example uses Fisher's iris data.
% Load Fisher's iris data.
load fisheriris
X = meas;
Y = species;

% 不经过优化的训练分类树
Md0 = fitctree(X,Y);
% 计算分类模型Md0中的损失函数
resuberror = resubLoss(Md0)   % resuberror =  0.0200
% 预测
cc0=predict(Md0,meas);
figure
cm0 = confusionchart(species,cc0);
cm0.Title = '不经过优化的分类树 ';
% 展示结构
view(Md0,'Mode','graph');


% 经过优化的训练分类树
% rng(12345) %  resuberror =    0.0267
rng(6794050) %  resuberror =  0.0267

% Optimize the cross-validation loss of the classifier, 
% using the data in meas to predict the response in species.
Mdl = fitctree(X,Y,'OptimizeHyperparameters','auto')
% 计算分类模型Mdl中的损失函数
resuberror = resubLoss(Mdl)

% 预测
cc1=predict(Mdl,meas);
cm1 = confusionchart(species,cc1);
cm1.Title = '优化的分类树 ';

% 展示结构
view(Mdl,'Mode','graph');

% 本示例因为数据规模太小，所有数据集都作为了训练集
% 经过优化后，损失函数还略微变差了
% 但是模型树的结构精简了，泛化能力可能提高了
