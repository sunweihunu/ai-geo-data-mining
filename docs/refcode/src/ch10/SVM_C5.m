% 优化 SVM 分类器
% 使用 fitcsvm 自动优化超参数。
% 
% 加载 ionosphere 数据集。

load ionosphere
% 通过使用自动超参数优化，找到最小化五折交叉验证损失的超参数。
% 为了实现可再现性，请设置随机种子并使用 'expected-improvement-plus' 采集函数。

rng default
Mdl = fitcsvm(X,Y,'OptimizeHyperparameters','auto', ...
    'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName', ...
    'expected-improvement-plus'))