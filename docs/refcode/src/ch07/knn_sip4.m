% Search for Nearest Neighbors of Query Data Using Minkowski Distance
% Grow a Kd-tree nearest neighbor searcher object by using the createns function.
% Pass the object and query data to the knnsearch function to find k-nearest neighbors.
% 
% Load Fisher's iris data set.

load fisheriris
% Remove five irises randomly from the predictor data to use as a query set.

rng(1)                      % For reproducibility
n = size(meas,1);           % Sample size
qIdx = randsample(n,5);     % Indices of query data
tIdx = ~ismember(1:n,qIdx); % Indices of training data
Q = meas(qIdx,:);
X = meas(tIdx,:);
% Grow a four-dimensional Kd-tree using the training data. 
% Specify the Minkowski distance for finding nearest neighbors.

Mdl = createns(X,'Distance','minkowski')
% Mdl = 
%   KDTreeSearcher with properties:
% 
%        BucketSize: 50
%          Distance: 'minkowski'
%     DistParameter: 2
%                 X: [145x4 double]

% Because X has four columns and the distance metric is Minkowski,
% createns creates a KDTreeSearcher model object by default. 
% The Minkowski distance exponent is 2 by default.

% Find the indices of the training data (Mdl.X) that are the two nearest neighbors 
% of each point in the query data (Q).

IdxNN = knnsearch(Mdl,Q,'K',2)
% IdxNN = 5×2
% 
%     17     4
%      6     2
%      1    12
%     89    66
%    124   100
% 
% Each row of IdxNN corresponds to a query data observation, 
% and the column order corresponds to the order of the nearest neighbors,
% with respect to ascending distance. 
% For example, based on the Minkowski distance, the second nearest neighbor of Q(3,:) is X(12,:).