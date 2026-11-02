# img_CNN_Class_V1.mlx

「深度学习（DeepL）」目录 · 对应书稿 **第11章 深度学习** · 4.5 KB · 代码 51 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DeepL_V2/img_CNN_Class_V1.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DeepL_V2/img_CNN_Class_V1.mlx" download>下载 img_CNN_Class_V1.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**创建简单的图像分类网络**

## 脚本内容

## 创建简单的图像分类网络

https://ww2.mathworks.cn/help/deeplearning/gs/create-simple-deep-learning-classification-network.html 此示例说明如何创建和训练简单的卷积神经网络来进行深度学习分类。卷积神经网络是深度学习的基本工具，尤其适用于图像识别。

该示例演示如何： 加载图像数据。 定义网络架构。 指定训练选项。 训练网络。

```matlab
% 预测新数据的标签并计算分类准确度。

% 有关如何以交互方式创建和训练简单图像分类网络的示例，
% 请参阅使用深度网络设计器创建简单的图像分类网络。
```

## 加载数据

将数字样本数据加载为图像数据存储。imageDatastore 函数根据文件夹名称自动对图像加标签。

```matlab
digitDatasetPath = fullfile(matlabroot,'toolbox','nnet','nndemos', ...
    'nndatasets','DigitDataset');

imds = imageDatastore(digitDatasetPath, ...
    'IncludeSubfolders',true, ...
    'LabelSource','foldernames');
% 将数据划分为训练数据集和验证数据集，以使训练集中的每个类别包含 750 个图像，
% 并且验证集包含对应每个标签的其余图像。
% splitEachLabel 将图像数据存储拆分为两个新的数据存储以用于训练和验证。

numTrainFiles = 750;
[imdsTrain,imdsValidation] = splitEachLabel(imds,numTrainFiles,'randomize');
```

## 定义网络架构

定义卷积神经网络架构。指定网络输入层中图像的大小以及分类层前面的全连接层中类的数量。每个图像为 28×28×1 像素，有 10 个类。

```matlab
inputSize = [28 28 1];
numClasses = 10;

layers = [    imageInputLayer(inputSize)
    convolution2dLayer(5,20)
    batchNormalizationLayer
    reluLayer
    fullyConnectedLayer(numClasses)
    softmaxLayer
    classificationLayer];
% 有关深度学习层的详细信息，请参阅深度学习层列表。
```

## 训练网络

指定训练选项并训练网络。

```matlab
% 默认情况下，trainNetwork 使用 GPU（如果有），否则使用 CPU。
% 在 GPU 上训练需要 Parallel Computing Toolbox™ 和支持的 GPU 设备。
% 有关受支持设备的信息，请参阅GPU Support by Release (Parallel Computing Toolbox)。
% 您还可以使用 trainingOptions 的 'ExecutionEnvironment' 名称-值对组参数指定执行环境。

options = trainingOptions('sgdm', ...
    'MaxEpochs',4, ...
    'ValidationData',imdsValidation, ...
    'ValidationFrequency',30, ...
    'Verbose',false, ...
    'Plots','training-progress');

net = trainNetwork(imdsTrain,layers,options);


% 有关训练选项的详细信息，请参阅设置参数并训练卷积神经网络。
```

## 测试网络

对验证数据进行分类，并计算分类准确度。

```matlab
YPred = classify(net,imdsValidation);
YValidation = imdsValidation.Labels;
accuracy = mean(YPred == YValidation)
% accuracy = 0.9892
% 在深度学习的后续步骤中，您可以尝试将预训练网络用于其他任务。
% 通过迁移学习或特征提取解决新的图像数据分类问题。
% 有关示例，请参阅使用迁移学习更快地开始深度学习和使用从预训练网络中提取的特征训练分类器。
% 要了解有关预训练网络的详细信息，请参阅预训练的深度神经网络。
```
