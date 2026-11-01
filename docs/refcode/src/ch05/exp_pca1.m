

% coeff = pca(X) 返回 n×p 数据矩阵 X 的主成分系数，也称为载荷。
% X 的行对应于观测值，列对应于变量。系数矩阵是 p×p 矩阵。

% coeff 的每列包含一个主成分的系数，并且这些列按成分方差的降序排列。
% 默认情况下，pca 将数据中心化，并使用奇异值分解 (SVD) 算法。
 
clear all
%  Step 1
%  加载样本数据集。
load hald

% Step 2
% 原料数据有 4 个变量的 13 个观测值。
% 找出原料数据的主成分。

 [coeff,score,latent,tsquared,explained] = pca(ingredients)
 
%  coeff 的行包含四个原料变量的系数，其列对应于四个主成分。

% Step3  画图（载荷图和得分图合二为一）
biplot(coeff(:,1:2),'scores',score(:,1:2),'varlabels',{'v_1','v_2','v_3','v_4'});

% Step4  画图： 前两个主成份下的散点图（得分图）
figure;
scatter(score(:,1),score(:,2))
axis equal
xlabel('1st Principal Component')
ylabel('2nd Principal Component')