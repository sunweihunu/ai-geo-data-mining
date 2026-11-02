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