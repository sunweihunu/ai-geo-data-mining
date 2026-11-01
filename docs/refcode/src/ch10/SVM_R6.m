% 优化 SVM 回归
% 此示例展示了如何使用 fitrsvm 自动优化超参数。 
% 该示例使用 carsmall 数据。
% 加载 carsmall 数据集。
% Optimize SVM Regression
% This example shows how to optimize hyperparameters automatically using fitrsvm. 
% The example uses the carsmall data.
% Load the carsmall data set.
clear
load carsmall
%% 指定马力和重量作为预测变量 (X)，指定 MPG 作为响应变量 (Y)。
% Specify Horsepower and Weight as the predictor variables (X) and MPG as the response variable (Y).
X = [Horsepower Weight];
Y = MPG;

%% 通过使用自动超参数优化，找到将五倍交叉验证损失最小化的超参数。
% 为了重现性，设置随机种子并使用“预期改进加”采集功能。
% Find hyperparameters that minimize five-fold cross-validation loss
% by using automatic hyperparameter optimization.
% For reproducibility, set the random seed and use the 'expected-improvement-plus' 
% acquisition function.

rng default
Mdl = fitrsvm(X,Y,'OptimizeHyperparameters','auto',...
    'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName',...
    'expected-improvement-plus'))

% 优化搜索了 BoxConstraint、KernelScale 和 Epsilon。 
% 输出是具有最小估计交叉验证损失的回归。
% The optimization searched over BoxConstraint, KernelScale, and Epsilon. 
% The output is the regression with the minimum estimated cross-validation loss.