# cart_exp06.mlx

「决策树（CART）」目录 · 对应书稿 **第08章 决策树** · 156.8 KB · 代码 25 行 · 图窗 2

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DecisionTree_v2/cart_exp06.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/DecisionTree_v2/cart_exp06.mlx" download>下载 cart_exp06.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

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
```

<pre class="mlx-out">Mdl = 
  RegressionTree
           PredictorNames: {'Weight'  'Horsepower'}
             ResponseName: 'Y'
    CategoricalPredictors: []
        ResponseTransform: 'none'
          NumObservations: 94

  Properties, Methods</pre>

```matlab
view(Mdl,'Mode','graph');
```

<img src="../cart_exp06_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
% Figure Regression tree viewer contains an axes object and other objects of
% type uimenu, uicontrol. The axes object contains 60 objects of type line, text.

% The regression tree has 16 pruning levels.

% Prune the regression tree to pruning-level 10. View the pruned tree.

MdlPruned = prune(Mdl,'Level',10);
view(MdlPruned,'Mode','graph');
```

<img src="../cart_exp06_media/figure_1.png" alt="图窗 2" loading="lazy" />

```matlab
% Figure Regression tree viewer contains an axes object and other objects of type uimenu, uicontrol. The axes object contains 24 objects of type line, text.
%
% The pruned tree has six pruning levels.
%
% Alternatively, you can use the pruning-level field in the Regression tree viewer to prune the tree.
```
