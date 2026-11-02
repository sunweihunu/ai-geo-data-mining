% 使用深度学习进行“序列到序列”分类
% https://ww2.mathworks.cn/help/deeplearning/ug/sequence-to-sequence-classification-using-deep-learning.html
% 此示例说明如何使用长短期记忆 (LSTM) 网络对序列数据的每个时间步进行分类。
% 
% 要训练深度神经网络以对序列数据的每个时间步进行分类，可以使用“序列到序列”LSTM 网络。通过“序列到序列”LSTM 网络，您可以对序列数据的每个时间步进行不同预测。
% 
% 此示例使用从佩戴在身体上的智能手机获得的传感器数据。该示例训练一个 LSTM 网络，旨在根据表示三个不同方向上的加速度计读数的时间序列数据来识别佩戴者的活动。训练数据包含七个人的时序数据。每个序列有三个特征，且长度不同。该数据集包含六个训练观测值和一个测试观测值。
% 
% 加载序列数据
% 加载人体活动识别数据。该数据包含从佩戴在身体上的智能手机获得的七个时序的传感器数据。每个序列有三个特征，且长度不同。这三个特征对应于三个不同方向上的加速度计读数。

load HumanActivityTrain
XTrain
% 在绘图中可视化一个训练序列。绘制第一个训练序列的第一个特征，并按照对应的活动为绘图着色。

X = XTrain{1}(1,:);
classes = categories(YTrain{1});

figure
for j = 1:numel(classes)
    label = classes(j);
    idx = find(YTrain{1} == label);
    hold on
    plot(idx,X(idx))
end
hold off

xlabel("Time Step")
ylabel("Acceleration")
title("Training Sequence 1, Feature 1")
legend(classes,'Location','northwest')


%% 定义 LSTM 网络架构
% 定义 LSTM 网络架构。将输入指定为大小为 3（输入数据的特征数量）的序列。指定包含 200 个隐含单元的 LSTM 层，并输出完整序列。最后，在网络中包含一个大小为 5 的全连接层，后跟 softmax 层和分类层，以此来指定五个类。

numFeatures = 3;
numHiddenUnits = 200;
numClasses = 5;

layers = [ ...
    sequenceInputLayer(numFeatures)
    lstmLayer(numHiddenUnits,'OutputMode','sequence')
    fullyConnectedLayer(numClasses)
    softmaxLayer
    classificationLayer];
% 指定训练选项。将求解器设置为 'adam'。进行 60 轮训练。要防止梯度爆炸，请将梯度阈值设置为 2。

options = trainingOptions('adam', ...
    'MaxEpochs',60, ...
    'GradientThreshold',2, ...
    'Verbose',0, ...
    'Plots','training-progress');
% 使用 trainNetwork 以指定的训练选项训练 LSTM 网络。每个小批量都包含整个训练集，因此每训练一轮便更新一次绘图。序列非常长，因此处理每个小批量并更新绘图可能需要一些时间。

net = trainNetwork(XTrain,YTrain,layers,options);


% 测试 LSTM 网络
% 加载测试数据并对每个时间步的活动进行分类。

% 加载人体活动测试数据。XTest 包含一个维度为 3 的序列。YTest 包含对应于每个时间步的活动的分类标签序列。

load HumanActivityTest
figure
plot(XTest{1}')
xlabel("Time Step")
legend("Feature " + (1:numFeatures))
title("Test Data")


% 使用 classify 对测试数据进行分类。
YPred = classify(net,XTest{1});
% 您也可以使用 classifyAndUpdateState 一次对一个时间步进行预测。这在时间步的值以流的方式到达时非常有用。通常，对完整序列进行预测比一次对一个时间步进行预测更快。有关如何通过在相邻的单个时间步预测之间更新网络来预测将来时间步的示例，请参阅使用深度学习进行时序预测。

% 计算预测的准确度。

acc = sum(YPred == YTest{1})./numel(YTest{1})
% 通过绘图将预测值与测试数据进行比较。

figure
plot(YPred,'.-')
hold on
plot(YTest{1})
hold off

xlabel("Time Step")
ylabel("Activity")
title("Predicted Activities")
legend(["Predicted" "Test Data"])