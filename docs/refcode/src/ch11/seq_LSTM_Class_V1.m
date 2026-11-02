% 使用深度学习进行序列分类
% https://ww2.mathworks.cn/help/deeplearning/ug/classify-sequence-data-using-lstm-networks.html
% 此示例说明如何使用长短期记忆 (LSTM) 网络对序列数据进行分类。
% 
% 要训练深度神经网络以对序列数据进行分类，可以使用 LSTM 网络。LSTM 网络允许您将序列数据输入网络，并根据序列数据的各个时间步进行预测。
% 
% 此示例使用 [1] 和 [2] 中所述的日语元音数据集。此示例训练一个 LSTM 网络，旨在根据表示连续说出的两个日语元音的时序数据来识别说话者。训练数据包含九个说话者的时序数据。每个序列有 12 个特征，且长度不同。该数据集包含 270 个训练观测值和 370 个测试观测值。
% 
% 加载序列数据
% 加载日语元音训练数据。XTrain 是包含 270 个不同长度的 12 维序列的元胞数组。Y 是对应于九个说话者的标签 "1"、"2"、...、"9" 的分类向量。XTrain 中的条目是具有 12 行（每个特征一行）和不同列数（每个时间步一列）的矩阵。

[XTrain,YTrain] = japaneseVowelsTrainData;
XTrain(1:5)
% 在绘图中可视化第一个时序。每行对应一个特征。

figure
plot(XTrain{1}')
xlabel("Time Step")
title("Training Observation 1")
numFeatures = size(XTrain{1},1);
legend("Feature " + string(1:numFeatures),'Location','northeastoutside')


% 准备要填充的数据
% 在训练过程中，默认情况下，软件将训练数据拆分成小批量并填充序列，使它们具有相同的长度。过多填充会对网络性能产生负面影响。

% 为了防止训练过程添加过多填充，您可以按序列长度对训练数据进行排序，并选择合适的小批量大小，以使同一小批量中的序列长度相近。下图显示了对数据进行排序之前和之后填充序列的效果。



% 获取每个观测值的序列长度。

numObservations = numel(XTrain);
for i=1:numObservations
    sequence = XTrain{i};
    sequenceLengths(i) = size(sequence,2);
end
% 按序列长度对数据进行排序。

[sequenceLengths,idx] = sort(sequenceLengths);
XTrain = XTrain(idx);
YTrain = YTrain(idx);
% 在条形图中查看排序的序列长度。

figure
bar(sequenceLengths)
ylim([0 30])
xlabel("Sequence")
ylabel("Length")
title("Sorted Data")


% 选择小批量大小 27 以均匀划分训练数据，并减少小批量中的填充量。下图说明了添加到序列中的填充。

miniBatchSize = 27;


% 定义 LSTM 网络架构
% 定义 LSTM 网络架构。将输入大小指定为序列大小 12（输入数据的维度）。指定具有 100 个隐含单元的双向 LSTM 层，并输出序列的最后一个元素。最后，通过包含大小为 9 的全连接层，后跟 softmax 层和分类层，来指定九个类。

% 如果您可以在预测时访问完整序列，则可以在网络中使用双向 LSTM 层。双向 LSTM 层在每个时间步从完整序列学习。如果您不能在预测时访问完整序列，例如，您正在预测值或一次预测一个时间步时，则改用 LSTM 层。

inputSize = 12;
numHiddenUnits = 100;
numClasses = 9;

layers = [ ...
    sequenceInputLayer(inputSize)
    bilstmLayer(numHiddenUnits,'OutputMode','last')
    fullyConnectedLayer(numClasses)
    softmaxLayer
    classificationLayer]

% 现在，指定训练选项。指定求解器为 'adam'，梯度阈值为 1，最大轮数为 100。要减少小批量中的填充量，请选择 27 作为小批量大小。要填充数据以使长度与最长序列相同，请将序列长度指定为 'longest'。要确保数据保持按序列长度排序的状态，请指定从不打乱数据。

% 由于小批量数据存储较小且序列较短，因此更适合在 CPU 上训练。将 'ExecutionEnvironment' 指定为 'cpu'。要在 GPU（如果可用）上进行训练，请将 'ExecutionEnvironment' 设置为 'auto'（这是默认值）。

maxEpochs = 100;
miniBatchSize = 27;

options = trainingOptions('adam', ...
    'ExecutionEnvironment','cpu', ...
    'GradientThreshold',1, ...
    'MaxEpochs',maxEpochs, ...
    'MiniBatchSize',miniBatchSize, ...
    'SequenceLength','longest', ...
    'Shuffle','never', ...
    'Verbose',0, ...
    'Plots','training-progress');
% 训练 LSTM 网络
% 使用 trainNetwork 以指定的训练选项训练 LSTM 网络。

net = trainNetwork(XTrain,YTrain,layers,options);


% 测试 LSTM 网络
% 加载测试集并将序列分类到不同的说话者。
% 加载日语元音测试数据。XTest 是包含 370 个不同长度的 12 维序列的元胞数组。YTest 是由对应于九个说话者的标签 "1"、"2"、...、"9" 组成的分类向量。

[XTest,YTest] = japaneseVowelsTestData;
XTest(1:3)

% LSTM 网络 net 已使用相似长度的小批量序列进行训练。确保以相同的方式组织测试数据。按序列长度对测试数据进行排序。

numObservationsTest = numel(XTest);
for i=1:numObservationsTest
    sequence = XTest{i};
    sequenceLengthsTest(i) = size(sequence,2);
end
[sequenceLengthsTest,idx] = sort(sequenceLengthsTest);
XTest = XTest(idx);
YTest = YTest(idx);
% 对测试数据进行分类。要减少分类过程中引入的填充量，请将小批量大小设置为 27。要应用与训练数据相同的填充，请将序列长度指定为 'longest'。

miniBatchSize = 27;
YPred = classify(net,XTest, ...
    'MiniBatchSize',miniBatchSize, ...
    'SequenceLength','longest');
% 计算预测值的分类准确度。

acc = sum(YPred == YTest)./numel(YTest)