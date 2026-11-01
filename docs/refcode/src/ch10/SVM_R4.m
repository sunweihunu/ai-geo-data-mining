% Cross-Validate SVM Regression Model
% Load the carsmall data set.
% 交叉验证 SVM 回归模型
% 加载 carsmall 数据集。

load carsmall
rng 'default'  % For reproducibility

%% 指定马力和重量作为预测变量 (X)，指定 MPG 作为响应变量 (Y)。
% Specify Horsepower and Weight as the predictor variables (X) 
% and MPG as the response variable (Y).

X = [Horsepower Weight];
Y = MPG;

%% 使用 5 折交叉验证交叉验证两个 SVM 回归模型。对于这两个模型，指定对预测变量进行标准化。
% 对于其中一个模型，指定使用默认线性内核进行训练，并为另一个模型指定使用高斯内核。
% Cross-validate two SVM regression models using 5-fold cross-validation. 
% For both models, specify to standardize the predictors.
% For one of the models, specify to train using the default linear kernel,
% and the Gaussian kernel for the other model.

MdlLin = fitrsvm(X,Y,'Standardize',true,'KFold',5)
MdlGau = fitrsvm(X,Y,'Standardize',true,'KFold',5,'KernelFunction','gaussian')
% MdlLin 和 MdlGau 是 RegressionPartitionedSVM 交叉验证模型。
% 每个模型的 Trained 属性是 CompactRegressionSVM 模型的 5×1 元胞数组。
% 单元格中的模型存储 4 次观察的训练结果，并保留 1 次观察结果。
% 比较模型的泛化误差。在这种情况下，泛化误差是样本外均方误差。
% MdlLin and MdlGau are RegressionPartitionedSVM cross-validated models. 
% The Trained property of each model is a 5-by-1 cell array of 
% CompactRegressionSVM models. The models in the cell store the results of training on
% 4 folds of observations, and leaving one fold of observations out.
% 
% Compare the generalization error of the models. In this case, 
% the generalization error is the out-of-sample mean-squared error.

mseLin = kfoldLoss(MdlLin)
% mseLin = 17.4417
mseGau = kfoldLoss(MdlGau)
% mseGau = 16.7355

%% 使用高斯核的 SVM 回归模型比使用线性核的模型表现更好。
% 通过将整个数据集传递给 fitrsvm 来创建适合进行预测的模型，
% 并指定产生性能更好的模型的所有名称-值对参数。但是，不要指定任何交叉验证选项。
% 
% The SVM regression model using the Gaussian kernel performs better than 
% the one using the linear kernel.
% Create a model suitable for making predictions by passing the entire data set 
% to fitrsvm, and specify all name-value pair arguments 
% that yielded the better-performing model. However, 
% do not specify any cross-validation options.

MdlGau = fitrsvm(X,Y,'Standardize',true,'KernelFunction','gaussian');
% 要预测一组汽车的 MPG，请传递 Mdl 和一个包含要预测的汽车的马力和重量测量值的表。
% To predict the MPG of a set of cars, pass Mdl and a table containing the horsepower and weight measurements of the cars to predict.