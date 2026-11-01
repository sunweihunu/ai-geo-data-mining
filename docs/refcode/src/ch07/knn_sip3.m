% Search for Nearest Neighbors Using Kd-tree and Exhaustive Search
% knnsearch accepts ExhaustiveSearcher or KDTreeSearcher model objects
% to search the training data for the nearest neighbors to the query data. 
% An ExhaustiveSearcher model invokes the exhaustive searcher algorithm, 
% and a KDTreeSearcher model defines a Kd-tree, which knnsearch uses to search for nearest neighbors.
% 
%% Load Fisher's iris data set. Randomly reserve five observations from the data for query data.

load fisheriris
rng(1); % For reproducibility
n = size(meas,1);
idx = randsample(n,5);  % 随机挑选查询样本
X = meas(~ismember(1:n,idx),:); % Training data  保证训练样本和查询样本不重复
Y = meas(idx,:);                % Query data
% The variable meas contains 4 predictors.

%% Grow a default four-dimensional Kd-tree.

MdlKDT = KDTreeSearcher(X)
% MdlKDT = 
%   KDTreeSearcher with properties:
% 
%        BucketSize: 50
%          Distance: 'euclidean'
%     DistParameter: []
%                 X: [145x4 double]

%% MdlKDT is a KDTreeSearcher model object. 
% You can alter its writable properties using dot notation.
% 
% Prepare an exhaustive nearest neighbor searcher.

MdlES = ExhaustiveSearcher(X)
% MdlES = 
%   ExhaustiveSearcher with properties:
% 
%          Distance: 'euclidean'
%     DistParameter: []
%                 X: [145x4 double]

%% MdlKDT is an ExhaustiveSearcher model object.
% It contains the options, such as the distance metric, to use to find nearest neighbors.
% 
% Alternatively, you can grow a Kd-tree or prepare an exhaustive nearest neighbor searcher using createns.
% 
% Search the training data for the nearest neighbors indices 
% that correspond to each query observation. 
% Conduct both types of searches using the default settings.
% By default, the number of neighbors to search for per query observation is 1.

IdxKDT = knnsearch(MdlKDT,Y);
IdxES = knnsearch(MdlES,Y);
[IdxKDT IdxES]
% ans = 5×2
% 
%     17    17
%      6     6
%      1     1
%     89    89
%    124   124

% In this case, the results of the search are the same.