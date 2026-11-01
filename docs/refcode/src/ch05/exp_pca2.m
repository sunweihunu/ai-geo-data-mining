
%  ==  加权 PCA  ==  
clear all
% 执行主成分分析时，使用变量的逆方差作为权重。
% == Step1  加载样本数据集。
load hald

%== Step2  使用原料数据的逆方差作为变量权重执行主成分分析。
 [wcoeff,score,latent,~,explained] = pca(ingredients,'VariableWeights','variance')

% 请注意，系数矩阵 wcoeff 不是正交矩阵。

% == Step3  计算正交系数矩阵。
coefforth = inv(diag(std(ingredients)))* wcoeff
% 检查新系数矩阵 coefforth 的正交性。
% 正交矩阵和自己转制相乘以后对角线为1
 coefforth*coefforth'
 
 % == Step4 画图
biplot(wcoeff(:,1:2),'scores',score(:,1:2),'varlabels',{'v_1','v_2','v_3','v_4'});

% figure;
% biplot(coefforth(:,1:2),'scores',score(:,1:2),'varlabels',{'v_1','v_2','v_3','v_4'});

figure;
scatter(score(:,1),score(:,2))
axis equal
xlabel('1st Principal Component')
ylabel('2nd Principal Component')