
% 训练支持向量机回归模型
% 使用来自 UCI 机器学习库的鲍鱼数据训练支持向量机回归模型。
% 下载数据并将其保存在名为“abalone.csv”的当前文件夹中。
% Train Support Vector Machine Regression Model
% Train a support vector machine regression model using the abalone data 
% from the UCI Machine Learning Repository.
% Download the data and save it in your current folder with the name 'abalone.csv'.

url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data';
websave('abalone.csv',url);

% 将数据读入表中。指定变量名称。
% Read the data into a table. Specify the variable names.
varnames = {'Sex'; 'Length'; 'Diameter'; 'Height'; 'Whole_weight';...
    'Shucked_weight'; 'Viscera_weight'; 'Shell_weight'; 'Rings'};
Tbl = readtable('abalone.csv','Filetype','text','ReadVariableNames',false);
Tbl.Properties.VariableNames = varnames;

% 样本数据包含 4177 个观测值。除了性别之外，所有预测变量都是连续的，
% 性别是一个分类变量，可能的值是“M”（对于男性）、“F”（对于女性）和“I”（对于婴儿）。
% 目标是预测鲍鱼上环的数量（存储在环中）并使用物理测量确定其年龄。
% 
% 使用具有自动核尺度的高斯核函数训练 SVM 回归模型。标准化数据。
% The sample data contains 4177 observations. All the predictor variables are
% continuous except for Sex, which is a categorical variable with possible values 
% 'M' (for males), 'F' (for females), and 'I' (for infants). 
% The goal is to predict the number of rings (stored in Rings) on the abalone 
% and determine its age using physical measurements.
% 
% Train an SVM regression model, using a Gaussian kernel function 
% with an automatic kernel scale. Standardize the data.

rng default  % For reproducibility
Mdl = fitrsvm(Tbl,'Rings','KernelFunction','gaussian','KernelScale','auto',...
    'Standardize',true)

% 命令行窗口显示 Mdl 是经过训练的 RegressionSVM 模型并显示属性列表。
% 使用点表示法显示 Mdl 的属性。例如，检查以确认模型是否收敛以及完成了多少次迭代。
% The Command Window shows that Mdl is a trained RegressionSVM model 
% and displays a property list.
% Display the properties of Mdl using dot notation. 
% For example, check to confirm whether the model converged and 
% how many iterations it completed.

conv = Mdl.ConvergenceInfo.Converged
iter = Mdl.NumIterations  % iter = 2759
% 返回结果表明模型在 2759 次迭代后收敛。
% The returned results indicate that the model converged after 2759 iterations.