% 使用 createns 函数生成 Kd 树最近邻搜索器对象。
% 将对象和查询数据传递给 knnsearch 函数以查找 k 最近邻。

%%  Step 1 ===> 加载Fisher's 鸢尾花数据集.
load fisheriris

%%  Step 2 ===> 从预测器数据中随机删除五个鸢尾花以用作查询集。 
 
rng(1);                     % 固定随机种子
n = size(meas,1);           % meas总数据集的样本个数
qIdx = randsample(n,5);     % 查询数据集的序号
tIdx = ~ismember(1:n,qIdx); % 去掉查询数据集的序号，生成训练数据集的序号
Q = meas(qIdx,:);           % 根据查询数据集的序号，获得查询数据集
X = meas(tIdx,:);           % 根据训练数据集的序号，获得训练数据集

%%  Step 3 ===>  使用训练数据生成四维 Kd 树。 指定用于查找最近邻的 Minkowski 距离。
Mdl = createns(X,'Distance','minkowski')
% 因为 X 有四列，距离度量是 Minkowski，createns 默认创建一个 KDTreeSearcher 模型对象。
% Minkowski 距离指数默认为 2。


%%  Step 4 ===>  查找作为查询数据 (Q) 中每个点的两个最近邻居的训练数据 (Mdl.X) 的索引。
IdxNN = knnsearch(Mdl,Q,'K',2)
% IdxNN 的每一行对应一个查询数据观察，列顺序对应最近邻的顺序，相对于升序。 
% % 例如，根据闵可夫斯基距离，Q(3,:)的第二近邻是X(12,:)。