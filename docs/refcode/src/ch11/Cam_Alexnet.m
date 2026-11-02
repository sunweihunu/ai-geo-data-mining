%% 运行以下命令，根据需要获取下载，连接到网络摄像头，并获得预训练的神经网络。
% 如果报错，请点击提示中的"功能资源管理器"，安装Webcam Support Package，详见最下面注释。
% camera = webcam; % Connect to the camera
camera = webcam; % Connect to the camera
net = alexnet;   % Load the neural network
% net =alexnet('Weights','none');
% 如果您需要安装 webcam 和 alexnet 附加功能，对于每个函数都会显示一条带链接的消息，
% 帮助您使用附加功能资源管理器下载免费的附加功能。或者，
% 请参阅 Deep Learning Toolbox Model for AlexNet Network 
% 和 MATLAB Support Package for USB Webcams。

% 安装 Deep Learning Toolbox™ Model for AlexNet Network 后，
% 可以使用它对图像进行分类。AlexNet 是预训练的卷积神经网络 (CNN)，
% 已基于超过一百万个图像进行训练，可以将图像分为 1000 个对象类别
% （例如键盘、鼠标、咖啡杯、铅笔和多种动物）。

% 运行以下代码来显示和分类实时图像。将网络摄像头对准一个对象，
% 神经网络会报告它认为网络摄像头正在显示哪类对象。
% 网络会持续进行图像分类，直到您按下 Ctrl+C 为止。
% 该代码使用 imresize (Image Processing Toolbox) 针对网络调整图像的大小。

while true
    im = snapshot(camera);       % Take a picture
    image(im);                   % Show the picture
    im = imresize(im,[227 227]); % Resize the picture for alexnet
    label = classify(net,im);    % Classify the picture
    title(char(label));          % Show the class label
    drawnow
end
% 在此示例中，网络对咖啡杯进行了正确分类。用您周围的物体进行试验，看看该网络的准确度如何。

%% 如果报错，请点击提示中的"功能资源管理器"，来安装Webcam Support Package
% 错误使用 webcam (第 73 行)
% 尚未安装 MATLAB Support Package for USB Webcams。
% 请打开附加功能资源管理器以安装 Webcam Support Package。
% 
%% 如果报错，错误使用 alexnet (第 61 行)
% alexnet 需要 Deep Learning Toolbox Model for AlexNet Network 支持包以使用预训练的权重。要安装此支持包，请使用附加功能资源管理器。要使用未训练的层，请使用
% alexnet('Weights','none')，这不需要支持包。

% 建议在点开的安装窗口点"安装"；
% 手动安装可以点"下载"，再在Win Shell命令窗口中
% 根据自己电脑上的下载和Matlab安装文件夹，执行类似下面语句进行安装
% cd C:\Program Files\MATLAB\R2021b\bin\win64
% install_supportsoftware.exe -archives C:\Users\sunwei29\Downloads\MathWorks\SupportPackages\R2021b\