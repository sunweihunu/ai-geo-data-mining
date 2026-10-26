%% exp03_preprocess_demo.m —— 第3章案例：随机表格数据的预处理与可视化
% 对应书稿《人工智能与地理数据挖掘》第03章 3.7 节（练习：了解数据预处理和可视化）
% 流程：生成数据 → 数据污染 → 数据清洗 → 数据集成 → 数据缩减 → 数据变换 → 可视化
% 运行环境：基础 MATLAB 即可（未用到任何工具箱函数）
% 说明：rng(42) 固定随机种子，每次运行结果一致；书中数值以本机实际输出为准

clear; clc; rng(42);

%% 1. 数据生成
Data1 = randperm(10000, 100)';               % 站点 S1：100×1，1~10000 不重复整数

idx  = randperm(100);                        % S2：60 个编号取自 S1（打乱顺序），
pool = setdiff(1:10000, Data1);              % 另 40 个为不与 S1 重叠的新编号，
S2   = [Data1(idx(1:60)); pool(randperm(numel(pool), 40))];   % 模拟“范围相同、
                                                              % 重新生成、存在差异”
T = -10 + 55*rand(100,1);                    % 温度 T ∈ (-10, 45) ℃
P = 1000*rand(100,1);                        % 降雨 P ∈ (0, 1000) mm
Y = 10*T + P;                                % 虚拟变量 Y = 10T + P
Data2 = [S2, T, P, Y];                       % 100×4

%% 2. 数据污染
Data2(randperm(100,20), 2) = NaN;            % T 列 20 行置为 NaN
Data2(randperm(100,40), 3) = NaN;            % P 列 40 行置为 NaN
Data2(randperm(100,60), 4) = NaN;            % Y 列 60 行置为 NaN
fprintf('污染后缺失统计：T 列 %d 个，P 列 %d 个，Y 列 %d 个\n', ...
        sum(isnan(Data2(:,2))), sum(isnan(Data2(:,3))), sum(isnan(Data2(:,4))));

%% 3. 数据清洗：定位空缺，相邻值（前后均值）填充 T、P 列，Y 列重算
Data2(:,2) = fill_adjacent(Data2(:,2));
Data2(:,3) = fill_adjacent(Data2(:,3));
Data2(:,4) = 10*Data2(:,2) + Data2(:,3);
fprintf('清洗后剩余缺失：%d 个\n', sum(sum(isnan(Data2))));

%% 4. 数据集成：按共同站点（相同编号）合并成 Data3
[S3, ~, ib] = intersect(Data1, Data2(:,1));  % 共同站点（约 60 个）
Data3 = [S3, Data2(ib, 2:4)];                % n×4：S、T、P、Y
fprintf('集成后 Data3 规模：%d × %d\n', size(Data3,1), size(Data3,2));

%% 5. 数据缩减：相关分析 + 有放回抽样
rT = corrcoef(Data3(:,2), Data3(:,4));  rT = rT(1,2);   % T 与 Y 的相关系数
rP = corrcoef(Data3(:,3), Data3(:,4));  rP = rP(1,2);   % P 与 Y 的相关系数
fprintf('r(T,Y) = %.3f,  r(P,Y) = %.3f\n', rT, rP);

idx4  = randi(size(Data3,1), 40, 1);        % 有放回抽样 40 个样本
Data4 = Data3(idx4, :);                     % 同一对象可能被重复抽中

%% 6. 数据变换：T、P、Y 列按“本列”的最小-最大规范化到 [0,1]
Data5 = Data3;
for j = 2:4
    lo = min(Data3(:,j));  hi = max(Data3(:,j));
    Data5(:,j) = (Data3(:,j) - lo) / (hi - lo);
end
fprintf('Data5 各列范围：%.3f~%.3f, %.3f~%.3f, %.3f~%.3f\n', ...
        min(Data5(:,2)), max(Data5(:,2)), min(Data5(:,3)), max(Data5(:,3)), ...
        min(Data5(:,4)), max(Data5(:,4)));

%% 7. 可视化
labs = {'站点编号 S','温度 T/℃','降雨 P/mm','虚拟变量 Y'};

figure('Name','Data3 四列分布图');           % (1) Data3 分布图（2×2）
for k = 1:4
    subplot(2,2,k);  histogram(Data3(:,k), 12);
    title(['Data3：', labs{k}]);
end

figure('Name','Data4 四列分布图');           % (2) Data4 分布图（2×2），与 Data3 对比
for k = 1:4
    subplot(2,2,k);  histogram(Data4(:,k), 12);
    title(['Data4：', labs{k}]);
end

[~, ord] = sort(Data3(:,1));  Data3s = Data3(ord,:);   % 按站点编号排序
figure('Name','Data3 排序后序列图');         % (3) 排序后序列图（2×2）
for k = 1:4
    subplot(2,2,k);  plot(Data3s(:,k), '.-');
    title(['Data3（按 S 排序）：', labs{k}]);
end

[~, ord4] = sort(Data4(:,1));  Data4s = Data4(ord4,:);
figure('Name','Data4 排序后序列图');
for k = 1:4
    subplot(2,2,k);  plot(Data4s(:,k), '.-');
    title(['Data4（按 S 排序）：', labs{k}]);
end

figure('Name','Data5 三列分布图');           % (4) Data5 规范化后分布（3×1）
for k = 1:3
    subplot(3,1,k);  histogram(Data5(:,k+1), 12);
    title(['Data5：', labs{k+1}, '（规范化后 0~1）']);
end

%% ---------- 局部函数 ----------
function v = fill_adjacent(col)
% 用相邻的非缺失值（前后均值）填充缺失值；缺失在端点时退化为单侧取值
v = col;  n = numel(v);
for k = find(isnan(v))'
    lo = k;  while lo > 1 && isnan(v(lo)),  lo = lo - 1;  end   % 向左找非缺失
    hi = k;  while hi < n && isnan(v(hi)),  hi = hi + 1;  end   % 向右找非缺失
    if isnan(v(lo))
        v(k) = v(hi);                       % 左端缺失，用右邻
    elseif hi > n || isnan(v(hi))
        v(k) = v(lo);                       % 右端缺失，用左邻
    else
        v(k) = (v(lo) + v(hi)) / 2;         % 前后均值
    end
end
end
