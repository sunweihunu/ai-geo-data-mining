%% 训练残差网络进行图像分类
% https://ww2.mathworks.cn/help/deeplearning/ug/train-residual-network-for-image-classification.html

% 此示例说明如何创建包含残差连接的深度学习神经网络，并针对 CIFAR-10 数据对其进行训练。
% 残差连接是卷积神经网络架构中的常见元素。使用残差连接可以改善网络中的梯度流，从而可以训练更深的网络。
% 
% 对于许多应用来说，使用由一个简单的层序列组成的网络就已足够。
% 但是，某些应用要求网络具有更复杂的层次图结构，其中的层可接收来自多个层的输入，也可以输出到多个层。
% 这些类型的网络通常称为有向无环图 (DAG) 网络。残差网络就是一种 DAG 网络，
% 其中的残差（或快捷）连接会绕过主网络层。
% 残差连接让参数梯度可以更轻松地从输出层传播到较浅的网络层，从而能够训练更深的网络。
% 增加网络深度可在执行更困难的任务时获得更高的准确度。
% 
%% 要创建和训练具有层次图结构的网络，请按照以下步骤操作。

% 使用 layerGraph 创建一个 LayerGraph 对象。层次图指定网络架构。
% 您可以创建一个空的层次图，然后向其中添加层。
% 还可以直接从一组网络层创建一个层次图。这种情况下，layerGraph 会依次连接这些层。
% 使用 addLayers 向层次图中添加层，使用 removeLayers 从层次图中删除层。
% 使用 connectLayers 在不同层之间建立层连接，使用 disconnectLayers 断开层连接。
% 使用 plot 绘制网络架构。
% 使用 trainNetwork 训练网络。经过训练的网络是一个 DAGNetwork 对象。
% 使用 classify 和 predict 对新数据执行分类和预测。
% 您还可以加载预训练网络进行图像分类。有关详细信息，请参阅预训练的深度神经网络。

%% 准备数据
% 下载 CIFAR-10 数据集 [1]。该数据集包含 60,000 个图像。每个图像为 32×32 大小，
% 并且具有三个颜色通道 (RGB)。数据集的大小为 175 MB。根据您的 Internet 连接，下载过程可能需要一些时间。

datadir = tempdir; 
downloadCIFARData(datadir);
% 将 CIFAR-10 训练和测试图像作为四维数组加载。训练集包含 50,000 个图像，测试集包含 10,000 个图像。
% 使用 CIFAR-10 测试图像进行网络验证。

[XTrain,YTrain,XValidation,YValidation] = loadCIFARData(datadir);
% 您可以使用以下代码显示训练图像的随机样本。

figure;
idx = randperm(size(XTrain,4),20);
im = imtile(XTrain(:,:,:,idx),'ThumbnailSize',[96,96]);
imshow(im)
% 创建一个 augmentedImageDatastore 对象以用于网络训练。
% 在训练过程中，数据存储会沿垂直轴随机翻转训练图像，并在水平方向和垂直方向上将图像随机平移最多四个像素。
% 数据增强有助于防止网络过拟合和记忆训练图像的具体细节。

imageSize = [32 32 3];
pixelRange = [-4 4];
imageAugmenter = imageDataAugmenter( ...
    'RandXReflection',true, ...
    'RandXTranslation',pixelRange, ...
    'RandYTranslation',pixelRange);
augimdsTrain = augmentedImageDatastore(imageSize,XTrain,YTrain, ...
    'DataAugmentation',imageAugmenter, ...
    'OutputSizeMode','randcrop');

%% 定义网络架构
% 残差网络架构由以下组件构成：

% 主分支 - 顺序连接的卷积层、批量归一化层和 ReLU 层。
% 残差连接 - 绕过主分支的卷积单元。残差连接和卷积单元的输出按元素相加。
% 当激活区域的大小变化时，残差连接也必须包含 1×1 卷积层。
% 残差连接让参数梯度可以更轻松地从输出层流到较浅的网络层，从而能够训练更深的网络。

%% 创建主分支

% 首先创建网络的主分支。主分支包含五部分。
% 初始部分 - 包含图像输入层和带激活函数的初始卷积层。
% 三个卷积层阶段 - 分别具有不同的特征大小（32×32、16×16 和 8×8）。
% 每个阶段包含 N 个卷积单元。在示例的这一部分中，N = 2。
% 每个卷积单元包含两个带激活函数的 3×3 卷积层。
% netWidth 参数是网络宽度，定义为网络第一卷积层阶段中的滤波器数目。
% 第二阶段和第三阶段中的前几个卷积单元会将空间维度下采样二分之一。
% 为了使整个网络中每个卷积层所需的计算量大致相同，每次执行空间下采样时，都将滤波器的数量增加一倍。
% 最后部分 - 包含全局平均池化层、全连接层、softmax 层和分类层。

% 使用 convolutionalUnit(numF,stride,tag) 创建一个卷积单元。
% numF 是每一层中卷积滤波器的数量，stride 是该单元第一个卷积层的步幅，tag 是添加在层名称前面的字符数组。
% convolutionalUnit 函数在示例末尾定义。

% 为所有层指定唯一名称。卷积单元中的层的名称以 'SjUk' 开头，
% 其中 j 是阶段索引，k 是该阶段内卷积单元的索引。
% 例如，'S2U1' 表示第 2 阶段第 1 单元。

netWidth = 16;
layers = [
    imageInputLayer([32 32 3],'Name','input')
    convolution2dLayer(3,netWidth,'Padding','same','Name','convInp')
    batchNormalizationLayer('Name','BNInp')
    reluLayer('Name','reluInp')
    
    convolutionalUnit(netWidth,1,'S1U1')
    additionLayer(2,'Name','add11')
    reluLayer('Name','relu11')
    convolutionalUnit(netWidth,1,'S1U2')
    additionLayer(2,'Name','add12')
    reluLayer('Name','relu12')
    
    convolutionalUnit(2*netWidth,2,'S2U1')
    additionLayer(2,'Name','add21')
    reluLayer('Name','relu21')
    convolutionalUnit(2*netWidth,1,'S2U2')
    additionLayer(2,'Name','add22')
    reluLayer('Name','relu22')
    
    convolutionalUnit(4*netWidth,2,'S3U1')
    additionLayer(2,'Name','add31')
    reluLayer('Name','relu31')
    convolutionalUnit(4*netWidth,1,'S3U2')
    additionLayer(2,'Name','add32')
    reluLayer('Name','relu32')
    
    averagePooling2dLayer(8,'Name','globalPool')
    fullyConnectedLayer(10,'Name','fcFinal')
    softmaxLayer('Name','softmax')
    classificationLayer('Name','classoutput')
    ];
% 根据层数组创建一个层次图。layerGraph 按顺序连接 layers 中的所有层。绘制层次图。

lgraph = layerGraph(layers);
figure('Units','normalized','Position',[0.2 0.2 0.6 0.6]);
plot(lgraph);


%% 创建残差连接

% 在卷积单元周围添加残差连接。大多数残差连接不执行任何操作，只是简单地按元素与卷积单元的输出相加。

% 创建从 'reluInp' 到 'add11' 层的残差连接。由于您在创建相加层时将其输入数指定为 2，
% 因此该层有两个输入，名为 'in1' 和 'in2'。第一个卷积单元的最终层已连接到 'in1' 输入。
% 因此，相加层将第一个卷积单元的输出和 'reluInp' 层相加。

% 同样，将 'relu11' 层连接到 'add12' 层的第二个输入。通过绘制层次图，确认已正确连接各个层。

lgraph = connectLayers(lgraph,'reluInp','add11/in2');
lgraph = connectLayers(lgraph,'relu11','add12/in2');

figure('Units','normalized','Position',[0.2 0.2 0.6 0.6]);
plot(lgraph);


% 当卷积单元中层激活区域的大小发生变化时（即，当它们在空间维度下采样而在通道维度上采样时），
% 残差连接中激活区域的大小也必须随之变化。通过使用 1×1 卷积层及其批量归一化层，更改残差连接中激活区域的大小。

skip1 = [
    convolution2dLayer(1,2*netWidth,'Stride',2,'Name','skipConv1')
    batchNormalizationLayer('Name','skipBN1')];
lgraph = addLayers(lgraph,skip1);
lgraph = connectLayers(lgraph,'relu12','skipConv1');
lgraph = connectLayers(lgraph,'skipBN1','add21/in2');
% 在网络的第二阶段添加恒等连接。

lgraph = connectLayers(lgraph,'relu21','add22/in2');
% 通过另一个 1×1 卷积层及其批量归一化层，更改第二阶段和第三阶段之间的残差连接中激活区域的大小。

skip2 = [
    convolution2dLayer(1,4*netWidth,'Stride',2,'Name','skipConv2')
    batchNormalizationLayer('Name','skipBN2')];
lgraph = addLayers(lgraph,skip2);
lgraph = connectLayers(lgraph,'relu22','skipConv2');
lgraph = connectLayers(lgraph,'skipBN2','add31/in2');
% 添加最后一个恒等连接，并绘制最终的层次图。

lgraph = connectLayers(lgraph,'relu31','add32/in2');

figure('Units','normalized','Position',[0.2 0.2 0.6 0.6]);
plot(lgraph)


%% 创建更深的网络
% 要为任意深度和宽度的 CIFAR-10 数据创建具有残差连接的层次图，请使用支持函数 residualCIFARlgraph。

lgraph = residualCIFARlgraph(netWidth,numUnits,unitType) 
% 为 CIFAR-10 数据创建具有残差连接的层次图。

% netWidth 是网络宽度，定义为网络的前几个 3×3 卷积层中的滤波器数量。
% 
% numUnits 是网络主分支中的卷积单元数。因为网络由三个阶段组成，其中每个阶段的卷积单元数量都相同，
% 所以 numUnits 必须是 3 的整数倍。
% 
% unitType 是卷积单元的类型，指定为 "standard" 或 "bottleneck"。
% 一个标准卷积单元由两个 3×3 卷积层组成。
% 一个瓶颈卷积单元由三个卷积层组成：一个在通道维度进行下采样的 1×1 层，一个 3×3 卷积层，
% 以及一个在通道维度进行上采样的 1×1 层。
% 因此，瓶颈卷积单元的卷积层数比标准单元多 50%，而其空间 3×3 卷积层数却是标准单元的一半。
% 这两种单元类型的计算复杂度相似，但使用瓶颈单元时，残差连接中传播的特征总数要多四倍。
% 网络的总深度定义为顺序卷积层和全连接层的层数之和。
% 对于由标准单元构成的网络，总深度为 2*numUnits + 2，对于由瓶颈单元构成的网络，总深度为 3*numUnits + 2。

% 创建一个包含九个标准卷积单元（每阶段三个单元）且宽度为 16 的残差网络。网络总深度为 2*9+2 = 20。

numUnits = 9;
netWidth = 16;
lgraph = residualCIFARlgraph(netWidth,numUnits,"standard");
figure('Units','normalized','Position',[0.1 0.1 0.8 0.8]);
plot(lgraph)


% % 训练网络
% 指定训练选项。对网络进行 80 轮训练。
% 选择与小批量大小成正比的学习率，并在 60 轮训练后将学习率降低十分之一。
% 每轮训练后都使用验证数据验证一次网络。

miniBatchSize = 128;
learnRate = 0.1*miniBatchSize/128;
valFrequency = floor(size(XTrain,4)/miniBatchSize);
options = trainingOptions('sgdm', ...
    'InitialLearnRate',learnRate, ...
    'MaxEpochs',80, ...
    'MiniBatchSize',miniBatchSize, ...
    'VerboseFrequency',valFrequency, ...
    'Shuffle','every-epoch', ...
    'Plots','training-progress', ...
    'Verbose',false, ...
    'ValidationData',{XValidation,YValidation}, ...
    'ValidationFrequency',valFrequency, ...
    'LearnRateSchedule','piecewise', ...
    'LearnRateDropFactor',0.1, ...
    'LearnRateDropPeriod',60);
% 要使用 trainNetwork 训练网络，请将 doTraining 标志设置为 true。
% 否则，请加载预训练的网络。在一个较好的 GPU 上训练网络大约需要两小时。
% 如果您没有 GPU，则训练需要更长时间。

doTraining = false;
if doTraining
    trainedNet = trainNetwork(augimdsTrain,lgraph,options);
else
    load('CIFARNet-20-16.mat','trainedNet');
end


%% 评估经过训练的网络
% 基于训练集（无数据增强）和验证集计算网络的最终准确度。

[YValPred,probs] = classify(trainedNet,XValidation);
validationError = mean(YValPred ~= YValidation);
YTrainPred = classify(trainedNet,XTrain);
trainError = mean(YTrainPred ~= YTrain);
disp("Training error: " + trainError*100 + "%")
Training error: 2.862%
disp("Validation error: " + validationError*100 + "%")
Validation error: 9.76%
% 绘制混淆矩阵。使用列汇总和行汇总显示每个类的准确率和召回率。网络最常将猫与狗混淆。

figure('Units','normalized','Position',[0.2 0.2 0.4 0.4]);
cm = confusionchart(YValidation,YValPred);
cm.Title = 'Confusion Matrix for Validation Data';
cm.ColumnSummary = 'column-normalized';
cm.RowSummary = 'row-normalized';


% 您可以使用以下代码显示包含九个测试图像的随机样本，以及它们的预测类和这些类的概率。

figure
idx = randperm(size(XValidation,4),9);
for i = 1:numel(idx)
    subplot(3,3,i)
    imshow(XValidation(:,:,:,idx(i)));
    prob = num2str(100*max(probs(idx(i),:)),3);
    predClass = char(YValPred(idx(i)));
    title([predClass,', ',prob,'%'])
end
convolutionalUnit(numF,stride,tag) 
% 创建一个层数组，其中包含两个卷积层以及对应的批量归一化层和 ReLU 层。
% numF 是卷积滤波器的数量，stride 是第一个卷积层的步幅，tag 是添加在所有层名称前面的标记。

function layers = convolutionalUnit(numF,stride,tag)
layers = [
    convolution2dLayer(3,numF,'Padding','same','Stride',stride,'Name',[tag,'conv1'])
    batchNormalizationLayer('Name',[tag,'BN1'])
    reluLayer('Name',[tag,'relu1'])
    convolution2dLayer(3,numF,'Padding','same','Name',[tag,'conv2'])
    batchNormalizationLayer('Name',[tag,'BN2'])];
end