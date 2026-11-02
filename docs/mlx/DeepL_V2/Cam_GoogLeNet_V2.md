# Cam_GoogLeNet_V2.mlx

「深度学习（DeepL）」目录 · 对应书稿 **第11章 深度学习** · 3.6 KB · 代码 22 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DeepL_V2/Cam_GoogLeNet_V2.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DeepL_V2/Cam_GoogLeNet_V2.mlx" download>下载 Cam_GoogLeNet_V2.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**此示例说明如何使用预训练的深度卷积神经网络**

GoogLeNet 实时对来自网络摄像头的图像进行分类。

## 脚本内容

```matlab
% 此示例说明如何使用预训练的深度卷积神经网络
% GoogLeNet 实时对来自网络摄像头的图像进行分类。
```

## 注意：该示例需要 MATLAB Support Package for USB Webcams，

以及 Deep Learning Toolbox™ Model for GoogLeNet Network。 如果没有安装所需的支持包，软件会提供下载链接。

## 连续对相机图像进行分类

要连续对相机图像进行分类，请将前面的步骤放入一个循环。在图窗打开时运行该循环。 要停止实时预测，只需关闭图窗。在每次迭代结束时使用 drawnow 更新图窗。

```matlab
clear camera
camera = webcam;
net = googlenet;
% 如果要再次运行该示例，请先运行命令 clear camera，
% 其中 camera 是与网络摄像头的连接。否则将出现错误，
% 因为您不能创建与同一网络摄像头的另一连接。
%
```

## 对相机连续输入图像进行分类

要对图像进行分类，必须将其大小调整为网络的输入大小。 获取网络的图像输入层的 InputSize 属性的前两个元素。 图像输入层是网络的第一层。

```matlab
inputSize = net.Layers(1).InputSize(1:2)
h = figure;

while ishandle(h)
    im = snapshot(camera);
    image(im)
    im = imresize(im,inputSize);
    [label,score] = classify(net,im);
    title({char(label), num2str(max(score),2)});
    drawnow
end

% 关掉图像即停止。
```
