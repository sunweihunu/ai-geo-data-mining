# cart_exp06.mlx

「决策树（CART）」目录 · 对应书稿 **第08章 决策树** · 156.8 KB · 代码 25 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DecisionTree_v2/cart_exp06.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DecisionTree_v2/cart_exp06.mlx" download>下载 cart_exp06.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**Load the carsmall data set. Consider Horsepower and Weight as predictor variables.**

因变量MPG意思是miles per gallon 每加仑英里数，反映发动机的效率

## 脚本内容

```matlab
% Load the carsmall data set. Consider Horsepower and Weight as predictor variables.
% 因变量MPG意思是miles per gallon 每加仑英里数，反映发动机的效率

load carsmall;
X = [Weight Horsepower];
varNames = {'Weight' 'Horsepower'};
% Grow a regression tree using the entire data set. View the tree.

Mdl = fitrtree(X,MPG,'PredictorNames',varNames)

view(Mdl,'Mode','graph');
% Figure Regression tree viewer contains an axes object and other objects of
% type uimenu, uicontrol. The axes object contains 60 objects of type line, text.

% The regression tree has 16 pruning levels.

% Prune the regression tree to pruning-level 10. View the pruned tree.

MdlPruned = prune(Mdl,'Level',10);
view(MdlPruned,'Mode','graph');
% Figure Regression tree viewer contains an axes object and other objects of type uimenu, uicontrol. The axes object contains 24 objects of type line, text.
%
% The pruned tree has six pruning levels.
%
% Alternatively, you can use the pruning-level field in the Regression tree viewer to prune the tree.
```
