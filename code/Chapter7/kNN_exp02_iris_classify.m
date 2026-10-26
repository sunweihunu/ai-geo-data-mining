%% kNN_exp02_iris_classify.m —— 第7章 案例2：鸢尾花的 kNN 分类
% 对应书稿《第07章 k最近邻（kNN）模型》7.8.2 节
% 数据：MATLAB 内置 fisheriris（150 个标本 × 4 个属性 × 3 个品种），
%       本例只用后两个属性（花瓣长度、花瓣宽度），便于二维作图
% 示例数据文件：data/iris_query_samples.csv（与本脚本中的待测样本取值一致）
% 课件英文原版参考：openExample('stats/ClassifyingQueryDataUsingKnnsearchExample')

clear; clc; close all;

load fisheriris
X = meas(:, 3:4);                    % 训练样本自变量：花瓣长度、花瓣宽度（150×2）

%% 第一部分：1 个待测样本（k=10，闵可夫斯基距离）
y0 = [5.0 1.7];                      % 待测样本（示例数值）
idx0 = knnsearch(X, y0, 'K', 10, 'Distance', 'minkowski', 'P', 2);
fprintf('单个待测样本 10 个近邻的品种构成：\n');
tabulate(species(idx0))
% 课件运行结果：versicolor 8 个（80%）、virginica 2 个（20%）→ 判为 versicolor；
% 注：其中两个 versicolor 标本的两个属性值完全相同，在二维图上重叠显示为一个点。

%% 第二部分：3 个待测样本，两种距离函数对比
Y = [6.0 2.5;                        % 待测样本1（示例数值）
     5.1 1.8;                        % 待测样本2
     2.7 0.9];                       % 待测样本3

% 闵可夫斯基距离（P=2，即欧氏距离），每朵花找 10 个邻居，返回 3×10 索引
Idx1 = knnsearch(X, Y, 'K', 10, 'Distance', 'minkowski', 'P', 2);
% 换用切比雪夫距离再找一次，选中的邻居会有所不同
Idx2 = knnsearch(X, Y, 'K', 10, 'Distance', 'chebychev');

for i = 1:size(Y, 1)
    fprintf('待测样本 %d（闵可夫斯基距离）10 个近邻的品种构成：\n', i);
    tabulate(species(Idx1(i, :)))
end
% 课件运行结果（书稿表 7-5）：样本1 全部 virginica；样本2 virginica 2 + versicolor 8；
% 样本3 versicolor 7 + setosa 3。具体计数取决于查询点位置，请以自己运行的输出为准。

%% 可视化：闵可夫斯基（圆圈）与切比雪夫（五角星）选中的邻居
figure; hold on;
gscatter(X(:,1), X(:,2), species);                        % 训练样本按品种着色
h1 = plot(X(Idx1(:),1), X(Idx1(:),2), 'o', 'MarkerSize', 10, ...
          'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'none', ...
          'LineWidth', 1.5);                              % 闵可夫斯基邻居
h2 = plot(X(Idx2(:),1), X(Idx2(:),2), 'p', 'MarkerSize', 12, ...
          'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'none', ...
          'LineWidth', 1.2);                              % 切比雪夫邻居
plot(Y(:,1), Y(:,2), 'k*', 'MarkerSize', 14);             % 待测样本
xlabel('花瓣长度 (cm)'); ylabel('花瓣宽度 (cm)');
title('鸢尾花 kNN 分类：两种距离函数选中的 10 近邻（k=10）');
legend([h1 h2], '闵可夫斯基(p=2)选中的邻居', '切比雪夫选中的邻居', ...
       'Location', 'best');
hold off;
