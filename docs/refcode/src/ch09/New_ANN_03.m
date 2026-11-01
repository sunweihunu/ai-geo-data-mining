% 此例子用来展示plotfit的主要功能

% plotfit(net,inputs,targets)
% 在输入输入范围内绘制网络的输出函数，
% 并绘制与输入值相关联的目标目标和输出数据点。
% 误差条显示输出和目标之间的差异。
% 
% 该图仅针对具有一个输入(X) 的网络出现。% 
% 如果网络有多个输出(Y) ，则仅展示第一个输出/目标。

% plotfit(net,inputs,targets) plots the output function of a network across the range of the inputs
% inputs and also plots target targets and output data points associated with values in inputs. 
% Error bars show the difference between outputs and targets.

% The plot appears only for networks with one input.
% Only the first output/targets appear if the network has more than one output.


clear;
[x,t] = simplefit_dataset;
net = feedforwardnet(10);
net = train(net,x,t);
plotfit(net,x,t)