# Img_GoogLeNet_V1.mlx

「深度学习（DeepL）」目录 · 对应书稿 **第11章 深度学习** · 3.6 KB · 代码 19 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DeepL_V2/Img_GoogLeNet_V1.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DeepL_V2/Img_GoogLeNet_V1.mlx" download>下载 Img_GoogLeNet_V1.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**使用预训练网络对图像进行分类**

此示例使用： Deep Learning Toolbox

## 脚本内容

```matlab
% 使用预训练网络对图像进行分类
% 此示例使用：
% Deep Learning Toolbox
% Deep Learning Toolbox Model for GoogLeNet Network
% 此示例说明如何使用预训练的深度卷积神经网络 GoogLeNet 对图像进行分类。

% GoogLeNet 已经对超过一百万个图像进行了训练，可以将图像分为 1000 个对象类别
% （例如键盘、咖啡杯、铅笔和多种动物）。该网络已基于大量图像学习了丰富的特征表示。
% 网络以图像作为输入，然后输出图像中对象的标签以及每个对象类别的概率。
```

## 加载预训练网络

加载预训练的 GoogLeNet 网络。您还可以选择加载不同的预训练网络进行图像分类。 此步骤需要 Deep Learning Toolbox™ Model for GoogLeNet Network 支持包。 如果没有安装所需的支持包，软件会提供下载链接。

```matlab
net = googlenet;
```

## 读取图像并调整图像大小

要分类的图像的大小必须与网络的输入大小相同。对于 GoogLeNet， 网络输入大小是图像输入层的 InputSize 属性。

```matlab
% 读取要分类的图像，并将其大小调整为网络的输入大小。调整大小会略微更改图像的纵横比。

I = imread("peppers.png");
inputSize = net.Layers(1).InputSize;
I = imresize(I,inputSize(1:2));
```

## 分类并显示图像

对图像进行分类并显示图像及预测标签。

```matlab
label = classify(net,I);
figure
imshow(I)
title(string(label))
```
