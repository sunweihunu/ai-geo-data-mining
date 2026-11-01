clear
% 导入鸢尾花数据集
load fisheriris

% Train a default classification tree using the entire data set.
% 训练
Mdl = fitctree(meas,species);

% figure;
view(Mdl)  % 文字描述的分类树
view(Mdl,'Mode','graph')  % 画图描述的分类树

% 预测
cc=predict(Mdl,meas);


% 画图：第1种画法：分类散点图
figure;n=150;
gscatter(1:n,ones(n),species)  % 第一行是原始分类
hold on;
gscatter(1:n,2*ones(n),cc)  % 第2行是预测的分类
ylim([0 3]);

% 画图: 第2种画法：混淆图
figure
cm = confusionchart(species,cc);
cm.Title = 'CART用于鸢尾花数据集 ';

% 评估结果 1： 计算分类模型Mdl中定义的损失函数
resuberror = resubLoss(Mdl)

% 评估结果 2： 计算预测不同（错误）的个数，
Ysame = strcmp(cc,species); % True when ==
num_diff=sum(~Ysame) % How many are different?
num_diff/n  % 重新计算损失函数