%% FA_01_PCA.m —— 通过 PCA（正交变换法）求因子分析解
% 对随机变量分布没有要求。对应书稿 5.4.2 节（表 5-12 第 1 种方法）。
% 运行前将 MATLAB 当前文件夹切换到本目录。
% 若中文注释乱码：主页->预设->编辑器，将编码改为 UTF-8。

clear; clc; close all;

X  = Regions2004;                          % 31x8 原始数据
Xz = (X - mean(X)) ./ std(X);              % 1) 标准化，消除量纲影响
names = {'GDP','工业增加值','固定资产投资','职工平均工资', ...
         '城镇居民消费','农村居民消费','居民消费价格指数','商品零售价格指数'};

% 2) 主成分：特征向量（载荷方向）与特征值（投影方差）
[coeff, score, eigv] = pca(Xz);

% 3) pareto 图：特征值百分比（柱）与累计百分比（线），确定因子个数
figure;
pareto(eigv / sum(eigv));
title('主成分方差贡献率与累计贡献率（前两个累计 87.9\%）');

% 4) 前两个特征值开平方，构造主成分法载荷矩阵（未旋转）
C = diag(sqrt(eigv(1:2)));
A = coeff(:,1:2) * C;

% 5) 方差最大正交旋转（rotatefactors 默认 varimax）
%    因子方向约定：每列主导载荷取正，便于解读
A = rotatefactors(A);
[~, lead] = max(abs(A), [], 1);
sgn = sign(A(sub2ind(size(A), lead, 1:2)));
A = A .* sgn;

% 载荷图：旋转前后对比
figure;
subplot(1,2,1);                            % 未旋转载荷（重新计算展示）
A0 = coeff(:,1:2) * C;
plot(A0(:,1), A0(:,2), 'o'); hold on;
line([0 0],[-1 1]); line([-1 1],[0 0]);
text(A0(:,1)+0.03, A0(:,2)+0.03, names, 'FontSize', 8);
axis equal; axis([-1.1 1.1 -1.1 1.1]);
title('旋转前的载荷'); xlabel('F_1'); ylabel('F_2');
subplot(1,2,2);                            % 旋转载荷
plot(A(:,1), A(:,2), 'o'); hold on;
line([0 0],[-1 1]); line([-1 1],[0 0]);
text(A(:,1)+0.03, A(:,2)+0.03, names, 'FontSize', 8);
axis equal; axis([-1.1 1.1 -1.1 1.1]);
title('旋转后的载荷（varimax）'); xlabel('F_1'); ylabel('F_2');

% 6) 回归法因子得分系数与得分：B = R^-1 A，F = Xz*B
B = corr(Xz) \ A;
F = Xz * B;

% 7) 共性方差（应全部小于 1，否则出现 Heywood 现象）
comm = sum(A .^ 2, 2);
disp('旋转载荷矩阵 A（8x2）与共性方差：');
disp([A, comm]);

% 8) 综合得分：按旋转后方差贡献率加权
rate = sum(A .^ 2);                        % 各因子方差贡献
w    = rate / sum(rate);                   % 权重（0.52 / 0.48）
S    = F * w;                              % 综合得分
regions = {'北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江', ...
           '上海','江苏','浙江','安徽','福建','江西','山东','河南','湖北', ...
           '湖南','广东','广西','海南','重庆','四川','贵州','云南','西藏', ...
           '陕西','甘肃','青海','宁夏','新疆'};
[Sorted, idx] = sort(S, 'descend');
figure;
barh(S(idx)); set(gca, 'YTickLabel', regions(idx));
title(sprintf('综合因子得分：S = %.2f F_1 + %.2f F_2', w(1), w(2)));
xlabel('综合得分');
