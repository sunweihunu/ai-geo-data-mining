# SVM_C3.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 58.2 KB · 代码 36 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_C3.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/SVM_V1/SVM_C3.mlx" download>下载 SVM_C3.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**使用自定义核训练 SVM 分类器**

此示例说明如何使用自定义核函数（例如 sigmoid 核）训练 SVM 分类器， 并调整自定义核函数参数。

## 脚本内容

```matlab
% 使用自定义核训练 SVM 分类器
% 此示例说明如何使用自定义核函数（例如 sigmoid 核）训练 SVM 分类器，
% 并调整自定义核函数参数。
```

## 导入数据

```matlab
clear
SVM_Data1
```

## 使用 sigmoid 核函数训练 SVM 分类器。标准化数据是一种良好的做法。

```matlab
Mdl1 = fitcsvm(X,Y,'KernelFunction','mysigmoid','Standardize',true);
% Mdl1 是 ClassificationSVM 分类器，其中包含估计的参数。
% 绘制数据，并确定支持向量和决策边界。

% Compute the scores over a grid
d = 0.02; % Step size of the grid
[x1Grid,x2Grid] = meshgrid(min(X(:,1)):d:max(X(:,1)),...
    min(X(:,2)):d:max(X(:,2)));
xGrid = [x1Grid(:),x2Grid(:)];        % The grid
[~,scores1] = predict(Mdl1,xGrid); % The scores

figure;
h(1:2) = gscatter(X(:,1),X(:,2),Y);
hold on
h(3) = plot(X(Mdl1.IsSupportVector,1),...
    X(Mdl1.IsSupportVector,2),'ko','MarkerSize',10);
% Support vectors
contour(x1Grid,x2Grid,reshape(scores1(:,2),size(x1Grid)),[0 0],'k');
% Decision boundary
title('Scatter Diagram with the Decision Boundary')
legend({'-1','1','Support Vectors'},'Location','Best');
hold off


% 您可以调整核参数，尝试改进决策边界的形状。这也可能降低样本内的误分类率，
% 但您应首先确定样本外的误分类率。
% 使用 10 折交叉验证确定样本外的误分类率。
CVMdl1 = crossval(Mdl1);
misclass1 = kfoldLoss(CVMdl1)
% misclass1 =    0.1350
% 样本外的误分类率为 13.5%。
```
