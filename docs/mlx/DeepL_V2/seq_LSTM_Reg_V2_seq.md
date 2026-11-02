# seq_LSTM_Reg_V2_seq.mlx

「深度学习（DeepL）」目录 · 对应书稿 **第11章 深度学习** · 6.3 KB · 代码 176 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DeepL_V2/seq_LSTM_Reg_V2_seq.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DeepL_V2/seq_LSTM_Reg_V2_seq.mlx" download>下载 seq_LSTM_Reg_V2_seq.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**使用深度学习进行“序列到序列”回归**

https://ww2.mathworks.cn/help/deeplearning/ug/sequence-to-sequence-regression-using-deep-learning.html 此示例说明如何使用深度学习预测发动机的剩余使用寿命 (RUL)。

## 脚本内容

```matlab
% 使用深度学习进行“序列到序列”回归
% https://ww2.mathworks.cn/help/deeplearning/ug/sequence-to-sequence-regression-using-deep-learning.html
% 此示例说明如何使用深度学习预测发动机的剩余使用寿命 (RUL)。
%
% 要训练深度神经网络以根据时序数据或序列数据预测数值，可以使用长短期记忆 (LSTM) 网络。
%
% 此示例使用 [1] 中所述的涡轮风扇发动机退化仿真数据集。该示例训练一个 LSTM 网络，
% 旨在根据表示发动机中各种传感器的时序数据来预测发动机的剩余使用寿命（预测性维护，以周期为单位度量）。
% 训练数据包含 100 台发动机的仿真时序数据。每个序列的长度各不相同，对应于完整的运行至故障 (RTF) 实例。
% 测试数据包含 100 个不完整序列，每个序列的末尾为相应的剩余使用寿命值。
%
% 该数据集包含 100 个训练观测值和 100 个测试观测值。

% 下载数据
% 从 https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/ [2]
% 下载并解压缩涡轮风扇发动机退化仿真数据集。

% 涡轮风扇发动机退化仿真数据集的每个时序表示一个发动机。每台发动机启动时的初始磨损程度和制造变差均未知。
% 发动机在每个时序开始时运转正常，在到达序列中的某一时刻时出现故障。
% 在训练集中，故障的规模不断增大，直到出现系统故障。

% 数据是 ZIP 压缩的文本文件，其中包含 26 列以空格分隔的数值。
% 每一行是在一个运转周期中截取的数据快照，每一列代表一个不同的变量。这些列分别对应于以下数据：
% 第 1 列 - 单元编号
% 第 2 列 - 周期时间
% 第 3-5 列 - 操作设置
% 第 6-26 列 - 传感器测量值 1-21

% 创建一个目录来存储涡轮风扇发动机退化仿真数据集。
dataFolder = fullfile(tempdir,"turbofan");
if ~exist(dataFolder,'dir')
    mkdir(dataFolder);
end
% 从 https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/
% 下载并提取涡轮风扇发动机退化仿真数据集。

% 从文件 CMAPSSData.zip 中解压缩数据。

filename = "CMAPSSData.zip";
unzip(filename,dataFolder)
```

## 准备训练数据

使用此示例附带的函数 processTurboFanDataTrain 加载数据。 函数 processTurboFanDataTrain 从 filenamePredictors 中提取数据并返回元胞数组 XTrain 和 YTrain， 其中包含训练预测变量和响应序列。

```matlab
filenamePredictors = fullfile(dataFolder,"train_FD001.txt");
[XTrain,YTrain] = processTurboFanDataTrain(filenamePredictors);
% 删除具有常量值的特征

% 在所有时间步都保持不变的特征可能对训练产生负面影响。找到最小值和最大值相同的数据行，
% 然后删除这些行。

m = min([XTrain{:}],[],2);
M = max([XTrain{:}],[],2);
idxConstant = M == m;

for i = 1:numel(XTrain)
    XTrain{i}(idxConstant,:) = [];
end
% 查看序列中其余特征的数量。

numFeatures = size(XTrain{1},1)
% numFeatures = 17
```

## 归一化训练预测变量

```matlab
% 将训练预测变量归一化为具有零均值和单位方差。要计算所有观测值的均值和标准差，请水平串联序列数据。

mu = mean([XTrain{:}],2);
sig = std([XTrain{:}],0,2);

for i = 1:numel(XTrain)
    XTrain{i} = (XTrain{i} - mu) ./ sig;
end
```

## 裁剪响应

要更多地从发动机快要出现故障时的序列数据中进行学习，请以阈值 150 对响应进行裁剪。 这会使网络将具有更高 RUL 值的实例视为等同。

```matlab
thr = 150;
for i = 1:numel(YTrain)
    YTrain{i}(YTrain{i} > thr) = thr;
end
% 下图显示了第一个观测值及其对应的裁剪响应。
```

## 准备要填充的数据

要最大程度地减少添加到小批量的填充量，请按序列长度对训练数据进行排序。 然后，选择可均匀划分训练数据的小批量大小，并减少小批量中的填充量。 按序列长度对训练数据进行排序。

```matlab
for i=1:numel(XTrain)
    sequence = XTrain{i};
    sequenceLengths(i) = size(sequence,2);
end

[sequenceLengths,idx] = sort(sequenceLengths,'descend');
XTrain = XTrain(idx);
YTrain = YTrain(idx);
% 在条形图中查看排序的序列长度。

figure
bar(sequenceLengths)
xlabel("Sequence")
ylabel("Length")
title("Sorted Data")

% 选择可均匀划分训练数据的小批量大小，并减少小批量中的填充量。指定小批量大小为 20。
% 下图显示了未排序序列和已排序序列的填充情况。
miniBatchSize = 20;


% 定义网络架构
% 定义网络架构。创建一个 LSTM 网络，该网络包含一个具有 200 个隐藏单元的 LSTM 层，
% 然后是一个大小为 50 的全连接层和一个丢弃概率为 0.5 的丢弃层。

numResponses = size(YTrain{1},1);
numHiddenUnits = 200;

layers = [ ...
    sequenceInputLayer(numFeatures)
    lstmLayer(numHiddenUnits,'OutputMode','sequence')
    fullyConnectedLayer(50)
    dropoutLayer(0.5)
    fullyConnectedLayer(numResponses)
    regressionLayer];
% 指定训练选项。使用求解器 'adam' 以大小为 20 的小批量进行 60 轮训练。
% 指定学习率为 0.01。要防止梯度爆炸，请将梯度阈值设置为 1。
% 要使序列保持按长度排序，请将 'Shuffle' 设置为 'never'。

maxEpochs = 60;
miniBatchSize = 20;

options = trainingOptions('adam', ...
    'MaxEpochs',maxEpochs, ...
    'MiniBatchSize',miniBatchSize, ...
    'InitialLearnRate',0.01, ...
    'GradientThreshold',1, ...
    'Shuffle','never', ...
    'Plots','training-progress',...
    'Verbose',0);
```

## 训练网络

使用 trainNetwork 训练网络。

```matlab
net = trainNetwork(XTrain,YTrain,layers,options);
```

## 测试网络

使用此示例附带的函数 processTurboFanDataTest 准备测试数据。 函数 processTurboFanDataTest 从 filenamePredictors 和 filenameResponses 中提取数据 并返回元胞数组 XTest 和 YTest，其中分别包含测试预测变量和响应序列。

```matlab
filenamePredictors = fullfile(dataFolder,"test_FD001.txt");
filenameResponses = fullfile(dataFolder,"RUL_FD001.txt");
[XTest,YTest] = processTurboFanDataTest(filenamePredictors,filenameResponses);
% 使用根据训练数据计算出的 idxConstant 删除具有常量值的特征。
% 使用与训练数据相同的参数来归一化测试预测变量。使用与训练数据相同的阈值对测试响应进行裁剪。

for i = 1:numel(XTest)
    XTest{i}(idxConstant,:) = [];
    XTest{i} = (XTest{i} - mu) ./ sig;
    YTest{i}(YTest{i} > thr) = thr;
end
% 使用 predict 对测试数据进行预测。为防止函数向数据添加填充，请指定小批量大小为 1。

YPred = predict(net,XTest,'MiniBatchSize',1);
% LSTM 网络对不完整序列进行预测，一次预测一个时间步。
% 在每个时间步，网络使用此时间步的值进行预测，网络状态仅根据先前的时间步进行计算。
% 网络在各次预测之间更新其状态。predict 函数返回这些预测值的序列。
% 预测值的最后一个元素对应于不完整序列的预测 RUL。

% 您也可以使用 predictAndUpdateState 一次对一个时间步进行预测。
% 这在时间步的值以流的方式到达时非常有用。通常，对完整序列进行预测比一次对一个时间步进行预测更快。
% 有关如何通过在相邻的单个时间步预测之间更新网络来预测将来时间步的示例，请参阅使用深度学习进行时序预测。

% 在绘图中可视化一些预测值。

idx = randperm(numel(YPred),4);
figure
for i = 1:numel(idx)
    subplot(2,2,i)

    plot(YTest{idx(i)},'--')
    hold on
    plot(YPred{idx(i)},'.-')
    hold off

    ylim([0 thr + 25])
    title("Test Observation " + idx(i))
    xlabel("Time Step")
    ylabel("RUL")
end
legend(["Test Data" "Predicted"],'Location','southeast')
% 对于给定的不完整序列，预测的当前 RUL 是预测序列的最后一个元素。
% 计算预测值的均方根误差 (RMSE)，并在直方图中可视化预测误差。

for i = 1:numel(YTest)
    YTestLast(i) = YTest{i}(end);
    YPredLast(i) = YPred{i}(end);
end
figure
rmse = sqrt(mean((YPredLast - YTestLast).^2))
histogram(YPredLast - YTestLast)
title("RMSE = " + rmse)
ylabel("Frequency")
xlabel("Error")
```
