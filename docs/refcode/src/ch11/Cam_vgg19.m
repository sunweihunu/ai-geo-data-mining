% 使用深度学习实时对来自摄像头图像进行分类
% 使用了预训练的深度卷积神经网络GoogLeNet 
% 连续分类图像并显示排名靠前的预测值
clear
clear camera
camera = webcam;
net = vgg19;
inputSize = net.Layers(1).InputSize(1:2)

% 要连续对来自相机的图像进行分类并显示排名靠前的预测值，请将前面的步骤放入一个循环。
% 在图窗打开时运行该循环。要停止实时预测，只需关闭图窗。
% 在每次迭代结束时使用 drawnow 更新图窗。
% 

% 创建图窗窗口。首先调整窗口大小以使宽度增加一倍，并创建两个子图。
% 要防止坐标区大小改变，请将 PositionConstraint 属性设置为 'innerposition'。

h = figure;
h.Position(3) = 2*h.Position(3);
ax1 = subplot(1,2,1);
ax2 = subplot(1,2,2);
ax2.PositionConstraint = 'innerposition';
% 连续显示并分类图像，同时显示排名前五的预测值的直方图。

while ishandle(h)
    % Display and classify the image
    im = snapshot(camera);
    image(ax1,im)
    im = imresize(im,inputSize);
    [label,score] = classify(net,im);
    title(ax1,{char(label),num2str(max(score),2)});

    % Select the top five predictions
    [~,idx] = sort(score,'descend');
    idx = idx(5:-1:1);
    classes = net.Layers(end).Classes; % added by SW
    scoreTop = score(idx);
    classNamesTop = string(classes(idx));

    % Plot the histogram
    barh(ax2,scoreTop)
    title(ax2,'Top 5')
    xlabel(ax2,'Probability')
    xlim(ax2,[0 1])
    yticklabels(ax2,classNamesTop)
    ax2.YAxisLocation = 'right';

    drawnow
end