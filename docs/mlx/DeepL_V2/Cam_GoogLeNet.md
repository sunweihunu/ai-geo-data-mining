# Cam_GoogLeNet.mlx

「深度学习（DeepL）」目录 · 对应书稿 **第11章 深度学习** · 4.0 KB · 代码 42 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DeepL_V2/Cam_GoogLeNet.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DeepL_V2/Cam_GoogLeNet.mlx" download>下载 Cam_GoogLeNet.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**使用深度学习对网络摄像头图像进行分类**

此示例说明如何使用预训练的深度卷积神经网络GoogLeNet 摄像头只抓取一张图像进行分类。

## 脚本内容

```matlab
% 使用深度学习对网络摄像头图像进行分类
% 此示例说明如何使用预训练的深度卷积神经网络GoogLeNet
% 摄像头只抓取一张图像进行分类。
```

## 注意：该示例需要 MATLAB Support Package for USB Webcams，

以及 Deep Learning Toolbox™ Model for GoogLeNet Network。 如果没有安装所需的支持包，软件会提供下载链接。

```matlab
% 此示例使用：
% Deep Learning Toolbox Model for GoogLeNet Network
% Deep Learning Toolbox
% 使用 MATLAB®、普通的网络摄像头和深度神经网络来识别周围环境中的对象。
% 此示例使用 GoogLeNet，它是预训练的深度卷积神经网络（CNN 或 ConvNet），
% 已基于超过一百万个图像进行训练，
% 可以将图像分为 1000 个对象类别（例如键盘、咖啡杯、铅笔和多种动物）。
% 您可以下载 GoogLeNet 并使用 MATLAB 实时连续处理相机图像。

% GoogLeNet 已基于大量图像学习了丰富的特征表示。它以图像作为输入，
% 然后输出图像中对象的标签以及每个对象类别的概率。
% 您可以用周围的物品进行试验，以了解 GoogLeNet 对图像进行分类的准确程度。
% 要了解有关网络对象分类的详细信息，可以实时显示排名前五的类的分数，而不是只显示最终的类决策。
```

## 对相机快照进行分类

如果要再次运行该示例，请先运行命令 clear camera， 其中 camera 是与网络摄像头的连接。否则将出现错误， 因为您不能创建与同一网络摄像头的另一连接。

```matlab
clear camera


% 加载相机和预训练网络
% 连接到相机并加载预训练的 GoogLeNet 网络。
% 您可以在此步骤使用任何预训练网络。
camera = webcam;
net = googlenet;

%

% 要对图像进行分类，必须将其大小调整为网络的输入大小。
% 获取网络的图像输入层的 InputSize 属性的前两个元素。
% 图像输入层是网络的第一层。

inputSize = net.Layers(1).InputSize(1:2)
% inputSize =    224   224
% 显示来自相机的图像以及预测的标签及其概率。
% 在调用 classify 之前，必须将图像大小调整为网络的输入大小。

figure
im = snapshot(camera);
image(im)
im = imresize(im,inputSize);
[label,score] = classify(net,im);
title({char(label),num2str(max(score),2)});
```
