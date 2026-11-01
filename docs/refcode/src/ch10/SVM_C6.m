% 基于SVM 分类器的分类测试观察样本的

%% 加载电离层数据集。
% Label Test Sample Observations of SVM Classifiers
% Load the ionosphere data set.
load ionosphere
rng(1); % For reproducibility

%% 训练一个 SVM 分类器。 指定一个 15% 的留存样本进行测试，
% 对数据进行标准化，并指定 'g' 是正类。 
% Train an SVM classifier. Specify a 15% holdout sample for testing,
% standardize the data, and specify that 'g' is the positive class.

CVSVMModel = fitcsvm(X,Y,'Holdout',0.15,'ClassNames',{'b','g'},...
    'Standardize',true);
CompactSVMModel = CVSVMModel.Trained{1}; % Extract trained, compact classifier
testInds = test(CVSVMModel.Partition);   % Extract the test indices
XTest = X(testInds,:);
YTest = Y(testInds,:);
% CVSVMModel 是一个 ClassificationPartitionedModel 分类器。
% 它包含受过训练的属性，它是一个 1×1 元胞数组，其中包含一个
% 使用训练集训练的 CompactClassificationSVM 分类器。
% CVSVMModel is a ClassificationPartitionedModel classifier.
% It contains the property Trained, which is a 1-by-1 cell array holding a 
% CompactClassificationSVM classifier that the software trained using the training set.

%% 对测试样本观察值进行分类（标记）。
% 显示测试样本中前 10 个观测值的结果。
% Label the test sample observations. 
% Display the results for the first 10 observations in the test sample.
[label,score] = predict(CompactSVMModel,XTest);
table(YTest(1:10),label(1:10),score(1:10,2),'VariableNames',...
    {'TrueLabel','PredictedLabel','Score'})