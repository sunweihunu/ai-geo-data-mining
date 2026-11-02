% 针对回归训练卷积神经网络
% https://ww2.mathworks.cn/help/deeplearning/ug/train-a-convolutional-neural-network-for-regression.html
% 此示例使用：
% Image Processing Toolbox
% Deep Learning Toolbox
% Statistics and Machine Learning Toolbox
% 此示例说明如何使用卷积神经网络拟合回归模型来预测手写数字的旋转角度。

% 卷积神经网络（CNN 或 ConvNet）是深度学习的基本工具，尤其适用于分析图像数据。例如，您可以使用 CNN 对图像进行分类。要预测连续数据（例如角度和距离），可以在网络末尾包含回归层。

% 该示例构造一个卷积神经网络架构，训练网络，并使用经过训练的网络预测手写数字的旋转角度。这些预测对于光学字符识别很有用。

% 此外，您可以选择使用 imrotate (Image Processing Toolbox™) 旋转图像，并可选择使用 boxplot (Statistics and Machine Learning Toolbox™) 创建残差箱线图。

%% 加载数据
% 数据集包含手写数字的合成图像以及每个图像的旋转角度（以度为单位）。

% 使用 digitTrain4DArrayData 和 digitTest4DArrayData 以四维数组的形式加载训练图像和验证图像。输出 YTrain 和 YValidation 是以度为单位的旋转角度。训练数据集和验证数据集各包含 5000 个图像。

[XTrain,~,YTrain] = digitTrain4DArrayData;
[XValidation,~,YValidation] = digitTest4DArrayData;
% 使用 imshow 显示 20 个随机训练图像。

numTrainImages = numel(YTrain);
figure
idx = randperm(numTrainImages,20);
for i = 1:numel(idx)
    subplot(4,5,i)    
    imshow(XTrain(:,:,:,idx(i)))
end


%% 检查数据归一化
% 在训练神经网络时，最好确保数据在网络的所有阶段均归一化。
% 对于使用梯度下降的网络训练，归一化有助于训练的稳定和加速。
% 如果您的数据比例不佳，则损失可能会变为 NaN，并且网络参数在训练过程中可能发生偏离。
% 归一化数据的常用方法包括重新缩放数据，使其范围变为 [0,1]，或使其均值为 0 且标准差为 1。
% 您可以归一化以下数据：

% 1）输入数据。在将预测变量输入到网络之前对其进行归一化。在此示例中，输入图像已归一化到范围 [0,1]。
% 2）层输出。您可以使用批量归一化层来归一化每个卷积层和全连接层的输出。
% 3）响应。如果使用批量归一化层来归一化网络末尾的层输出，则网络的预测值在训练开始时就被归一化。
%    如果响应的比例与这些预测值完全不同，则网络训练可能无法收敛。
%    如果您的响应比例不佳，则尝试对其进行归一化，并查看网络训练是否有所改善。
%    如果在训练之前将响应归一化，则必须变换经过训练网络的预测值，以获得原始响应的预测值。

% 绘制响应的分布。响应（以度为单位的旋转角度）大致均匀地分布在 -45 和 45 之间，效果很好，无需归一化。
% 在分类问题中，输出是类概率，始终需要归一化。

figure
histogram(YTrain)
axis tight
ylabel('Counts')
xlabel('Rotation Angle')

% 通常，数据不必完全归一化。但是，如果在此示例中训练网络来预测 100*YTrain 或 YTrain+500 而不是 YTrain，
% 则损失将变为 NaN，并且网络参数在训练开始时会发生偏离。
% 即使预测 aY + b 的网络与预测 Y 的网络之间的唯一差异是对最终全连接层的权重和偏置的简单重新缩放，
% 也会出现这些结果。

% 如果输入或响应的分布非常不均匀或偏斜，您还可以在训练网络之前对数据执行非线性变换（例如，取其对数）。

%% 创建网络层
% 要求解回归问题，请创建网络层并在网络末尾包含一个回归层。

% 第一层定义输入数据的大小和类型。输入图像的大小为 28×28×1。创建与训练图像大小相同的图像输入层。
% 网络的中间层定义网络的核心架构，大多数计算和学习都在此处进行。
% 最终层定义输出数据的大小和类型。对于回归问题，全连接层必须位于网络末尾的回归层之前。
% 创建一个大小为 1 的全连接输出层以及一个回归层。
% 在 Layer 数组中将所有层组合在一起。

layers = [
    imageInputLayer([28 28 1])
    convolution2dLayer(3,8,'Padding','same')
    batchNormalizationLayer
    reluLayer
    averagePooling2dLayer(2,'Stride',2)
    convolution2dLayer(3,16,'Padding','same')
    batchNormalizationLayer
    reluLayer
    averagePooling2dLayer(2,'Stride',2)
    convolution2dLayer(3,32,'Padding','same')
    batchNormalizationLayer
    reluLayer
    convolution2dLayer(3,32,'Padding','same')
    batchNormalizationLayer
    reluLayer
    dropoutLayer(0.2)
    fullyConnectedLayer(1)
    regressionLayer];

%% 训练网络
% 创建网络训练选项。进行 30 轮训练。将初始学习率设置为 0.001，
% 并在 20 轮训练后降低学习率。通过指定验证数据和验证频率，
% 监控训练过程中的网络准确度。
% 软件基于训练数据训练网络，并在训练过程中按固定时间间隔计算基于验证数据的准确度。
% 验证数据不用于更新网络权重。打开训练进度图，关闭命令行窗口输出。

miniBatchSize  = 128;
validationFrequency = floor(numel(YTrain)/miniBatchSize);
options = trainingOptions('sgdm', ...
    'MiniBatchSize',miniBatchSize, ...
    'MaxEpochs',30, ...
    'InitialLearnRate',1e-3, ...
    'LearnRateSchedule','piecewise', ...
    'LearnRateDropFactor',0.1, ...
    'LearnRateDropPeriod',20, ...
    'Shuffle','every-epoch', ...
    'ValidationData',{XValidation,YValidation}, ...
    'ValidationFrequency',validationFrequency, ...
    'Plots','training-progress', ...
    'Verbose',false);
% 使用 trainNetwork 创建网络。如果存在兼容的 GPU，此命令会使用 GPU。
% 使用 GPU 需要 Parallel Computing Toolbox™ 和支持的 GPU 设备。
% 有关受支持设备的信息，请参阅GPU Support by Release (Parallel Computing Toolbox)。
% 否则，trainNetwork 将使用 CPU。

net = trainNetwork(XTrain,YTrain,layers,options);


% 检查 net 的 Layers 属性中包含的网络架构的详细信息。

net.Layers

%% 测试网络
% 基于验证数据评估准确度来测试网络性能。
% 使用 predict 预测验证图像的旋转角度。

YPredicted = predict(net,XValidation);
%% 评估性能

% 通过计算以下值来评估模型性能：
% 在可接受误差界限内的预测值的百分比
% 预测旋转角度和实际旋转角度的均方根误差 (RMSE)
% 计算预测旋转角度和实际旋转角度之间的预测误差。

predictionError = YValidation - YPredicted;
% 计算在实际角度的可接受误差界限内的预测值的数量。将阈值设置为 10 度。
% 计算此阈值范围内的预测值的百分比。

thr = 10;
numCorrect = sum(abs(predictionError) < thr);
numValidationImages = numel(YValidation);

accuracy = numCorrect/numValidationImages
% accuracy = 0.9690
% 使用均方根误差 (RMSE) 来衡量预测旋转角度和实际旋转角度之间的差异。

squares = predictionError.^2;
rmse = sqrt(mean(squares))
% rmse = single      4.6062
%% 可视化预测
% 在散点图中可视化预测。绘制预测值对真实值的图。

figure
scatter(YPredicted,YValidation,'+')
xlabel("Predicted Value")
ylabel("True Value")

hold on
plot([-60 60], [-60 60],'r--')


%% 校正数字旋转
% 您可以使用 Image Processing Toolbox 中的函数来摆正数字并将它们显示在一起。
% 使用 imrotate (Image Processing Toolbox) 根据预测的旋转角度旋转 49 个样本数字。

idx = randperm(numValidationImages,49);
for i = 1:numel(idx)
    image = XValidation(:,:,:,idx(i));
    predictedAngle = YPredicted(idx(i));  
    imagesRotated(:,:,:,i) = imrotate(image,predictedAngle,'bicubic','crop');
end
% 显示原始数字以及校正旋转后的数字。您可以使用 montage (Image Processing Toolbox) 将数字显示在同一个图像上。

figure
subplot(1,2,1)
montage(XValidation(:,:,:,idx))
title('Original')

subplot(1,2,2)
montage(imagesRotated)
% title('Corrected')