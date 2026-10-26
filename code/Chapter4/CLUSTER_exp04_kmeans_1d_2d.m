%% K-均值教学示例：一维数据与二维数据
% 对应书稿 4.3.3 节（表 4-11 迭代过程）与 4.3.4 节（二维 10 点）
clear; clc;

%% 1) 一维数据：[2,4,10,12,3,20,30,11,25]，k=2，前两个点作初始中心
x = [2 4 10 12 3 20 30 11 25]';     % 列向量
c = x(1:2)';                        % 初始中心 m1=2, m2=4
for it = 1:5
    lab = abs(x - c(1)) <= abs(x - c(2));   % 距离最近原则（并列归第 1 类）
    newc = [mean(x(lab)), mean(x(~lab))];   % 重算各类均值作新中心
    fprintf('第 %d 次迭代: m1=%.2f, m2=%.2f, K1=[%s]\n', ...
        it, newc(1), newc(2), num2str(sort(x(lab))'));
    if isequal(newc, c)             % 中心不再变化 → 收敛
        fprintf('中心稳定，聚类收敛。\n');
        break;
    end
    c = newc;
end

% 用 kmeans 函数验证（多次重复取最好）
[idx1, C1] = kmeans(x, 2, 'Replicates', 5);
fprintf('kmeans 结果中心: %.2f 与 %.2f\n', sort(C1));

%% 2) 二维数据：10 个点，k=2（前 6 点与后 4 点大体分属两团）
X = [3 4; 3 6; 3 8; 4 5; 4 7; 5 1; 5 5; 7 3; 7 4; 8 5];
[idx2, C2] = kmeans(X, 2, 'Replicates', 5);
figure; gscatter(X(:,1), X(:,2), idx2, 'br'); hold on;
plot(C2(:,1), C2(:,2), 'kp', 'MarkerSize', 14, 'MarkerFaceColor', 'y');
title('二维数据 K-均值聚类（k=2）'); xlabel('x_1'); ylabel('x_2');
legend('类 1', '类 2', '类中心', 'Location', 'best');

s = silhouette(X, idx2);
fprintf('二维示例平均轮廓值 = %.3f\n', mean(s));
