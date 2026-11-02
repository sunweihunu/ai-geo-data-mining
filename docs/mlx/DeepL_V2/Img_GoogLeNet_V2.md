# Img_GoogLeNet_V2.mlx

「深度学习（DeepL）」目录 · 对应书稿 **第11章 深度学习** · 4.7 KB · 代码 72 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DeepL_V2/Img_GoogLeNet_V2.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DeepL_V2/Img_GoogLeNet_V2.mlx" download>下载 Img_GoogLeNet_V2.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**使用 GoogLeNet 对图像进行分类**

https://ww2.mathworks.cn/help/deeplearning/ug/classify-image-using-googlenet.html 此示例使用：

## 脚本内容

```matlab
% 使用 GoogLeNet 对图像进行分类
% https://ww2.mathworks.cn/help/deeplearning/ug/classify-image-using-googlenet.html
% 此示例使用：
% Deep Learning Toolbox
% Deep Learning Toolbox Model for GoogLeNet Network
% 此示例说明如何使用预训练的深度卷积神经网络 GoogLeNet 对图像进行分类。

% GoogLeNet 已经对超过一百万个图像进行了训练，
% 可以将图像分为 1000 个对象类别（例如键盘、咖啡杯、铅笔和多种动物）。
% 该网络已基于大量图像学习了丰富的特征表示。
% 网络以图像作为输入，然后输出图像中对象的标签以及每个对象类别的概率。
```

## 加载预训练网络

加载预训练的 GoogLeNet 网络。此步骤需要 Deep Learning Toolbox™ Model for GoogLeNet Network 支持包。如果没有安装所需的支持包，软件会提供下载链接。

```matlab
% 您还可以选择加载不同的预训练网络进行图像分类。要尝试不同的预训练网络，请在 MATLAB® 中打开此示例并选择其他网络。例如，您可以尝试 squeezenet，这是一个比 googlenet 还要快的网络。您可以使用其他预训练网络运行此示例。有关所有可用网络的列表，请参阅加载预训练网络。

net = googlenet;
% 要分类的图像的大小必须与网络的输入大小相同。对于 GoogLeNet，网络的 Layers 属性的第一个元素是图像输入层。网络输入大小是图像输入层的 InputSize 属性。

inputSize = net.Layers(1).InputSize
% inputSize = 1×3     224   224     3

% Layers 属性的最后一个元素是分类输出层。
% 该层的 ClassNames 属性包含网络学习的类的名称。
% 查看总共 1000 个类名称中的 10 个随机类名称。

classNames = net.Layers(end).ClassNames;
numClasses = numel(classNames);
disp(classNames(randperm(numClasses,10)))
%     'papillon'
%     'eggnog'
%     'jackfruit'
%     'castle'
%     'sleeping bag'
%     'redshank'
%     'Band Aid'
%     'wok'
%     'seat belt'
%     'orange'
```

## 读取图像并调整图像大小

读取并显示要分类的图像。

```matlab
I = imread('peppers.png');
figure
imshow(I)

% 显示图像的大小。图像为 384×512 像素，并且具有三个颜色通道 (RGB)。
size(I)
% ans = 1×3   384   512     3

% 使用 imresize 将图像大小调整为网络的输入大小。调整大小会略微更改图像的纵横比。
I = imresize(I,inputSize(1:2));
figure
imshow(I)

% 根据您的应用，您可能希望以不同方式调整图像大小。
% 例如，您可以使用 I(1:inputSize(1),1:inputSize(2),:) 剪去图像的左上角。
% 如果您有 Image Processing Toolbox™，则可以使用 imcrop 函数。
```

## 对图像进行分类

使用 classify 对图像进行分类并计算类概率。网络正确地将图像分类为甜椒。 用于分类的网络训练为针对每个输入图像输出单个标签，即使图像包含多个对象时也是如此。

```matlab
[label,scores] = classify(net,I);
label
% label = categorical
%      bell pepper

% 显示图像及预测的标签，以及具有该标签的图像的预测概率。
figure
imshow(I)
title(string(label) + ", " + num2str(100*scores(classNames == label),3) + "%");
```

## 显示排名靠前的预测值

显示排名前五的预测标签，并以直方图形式显示它们的相关概率。 由于网络将图像分类为如此多的对象类别，并且许多类别是相似的， 因此在评估网络时通常会考虑准确度排名前五的几个类别。网络以高概率将图像分类为甜椒。

```matlab
[~,idx] = sort(scores,'descend');
idx = idx(5:-1:1);
classNamesTop = net.Layers(end).ClassNames(idx);
scoresTop = scores(idx);

figure
barh(scoresTop)
xlim([0 1])
title('Top 5 Predictions')
xlabel('Probability')
yticklabels(classNamesTop)
```
