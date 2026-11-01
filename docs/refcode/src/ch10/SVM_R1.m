% 训练线性支持向量机回归模型
% 使用存储在矩阵中的样本数据训练支持向量机 (SVM) 回归模型。
% 加载 carsmall 数据集。
% Train Linear Support Vector Machine Regression Model
% Train a support vector machine (SVM) regression model using sample data 
% stored in matrices.
% Load the carsmall data set.

load carsmall
rng 'default'  % For reproducibility
% 指定马力和重量作为预测变量 (X)，指定 MPG 作为响应变量 (Y)。
% Specify Horsepower and Weight as the predictor variables (X) and
% MPG as the response variable (Y).

X = [Horsepower,Weight];
Y = MPG;
% 训练默认的 SVM 回归模型。
% Train a default SVM regression model.

Mdl = fitrsvm(X,Y)
% Mdl 是经过训练的 RegressionSVM 模型。
% Mdl is a trained RegressionSVM model.

% 检查模型是否收敛。
% Check the model for convergence.

Mdl.ConvergenceInfo.Converged
% 0 indicates that the model did not converge.
% 0 表示模型没有收敛。

% 使用标准化数据重新训练模型。
% Retrain the model using standardized data.

MdlStd = fitrsvm(X,Y,'Standardize',true)
% 检查模型是否收敛。
% Check the model for convergence.

MdlStd.ConvergenceInfo.Converged
% 1 表示模型确实收敛了。
% 1 indicates that the model did converge.

% 计算新模型的重新代入（样本内）均方误差。
% Compute the resubstitution (in-sample) mean-squared error for the new model.


lStd = resubLoss(MdlStd)
% lStd = 17.0256