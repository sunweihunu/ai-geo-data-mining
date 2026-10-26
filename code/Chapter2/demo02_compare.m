%% demo02_compare.m —— 第02章 MATLAB/Python 对照演示（MATLAB 侧）
% 对应书稿 2.8.10 两个经典对照实验与 2.8.11 画图对照
% 运行环境：基础 MATLAB 即可，无需工具箱

clear; clc;

%% 1) 实验一：一切皆矩阵 —— z = x + y 逐元素相加
x = [1, 2, 3];
y = [4, 5, 6];
z = x + y          % 期望：5 7 9（Python 列表相加则是拼接 [1,2,3,4,5,6]）

%% 2) 索引与切片：从 1 起、前闭后闭
a = 1:10;
a(1:10)            % 全部
a(2:5)             % 期望：2 3 4 5（Python 等价写法是 a[1:5]）

%% 3) Python range 的 MATLAB 等价写法
0:4                % range(5)：从 0 开始、到不了 5
1:4                % range(1,5)
1:2:10             % range(1,11,2)：步长 2
2:2:2466           % range(2,2468,2)
100:-2:82          % range(100,80,-2)：前大后小用负步长

%% 4) 实验二对照要点：块以 end 收尾（缩进不改变结构）
for i = 1:5
    disp(i);
end
disp('end');       % 无论缩进多少，end 都在循环外（Python 则由缩进决定）

%% 5) sin/cos 曲线图（与 Python 版逐行对应）
x  = 0 : 0.2 : 8.0;
y1 = sin(x);
y2 = cos(x);
figure(3);
plot(x, y1, 'rx-'); hold on
plot(x, y2, 'bo-'); hold off
title('Function', 'fontsize', 20);
legend({'sin', 'cos'}, 'fontsize', 15);
text(1.6, 0.5, 'y > 0', 'fontsize', 18); grid on
xlabel('x', 'fontsize', 18); ylabel('y', 'fontsize', 18);
xlim([0 6.3]); ylim([-1.2 1.2]);
