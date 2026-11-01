% 训练和交叉验证 SVM 分类器
% 加载 ionosphere 数据集。

load ionosphere
rng(1); % For reproducibility
% 使用径向基核训练 SVM 分类器。让软件计算核函数的缩放值。对预测变量进行标准化。

SVMModel = fitcsvm(X,Y,'Standardize',true,'KernelFunction','RBF',...
    'KernelScale','auto');
% SVMModel 是经过训练的 ClassificationSVM 分类器。

% 交叉验证 SVM 分类器。默认情况下，软件使用 10 折交叉验证。

CVSVMModel = crossval(SVMModel);
% CVSVMModel 是 ClassificationPartitionedModel 交叉验证的分类器。

% 估计样本外的误分类率。

classLoss = kfoldLoss(CVSVMModel) % classLoss = 0.0484
% 泛化率约为 5%。