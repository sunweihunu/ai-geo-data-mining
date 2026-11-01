# SVM_C4.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 25.4 KB · 代码 20 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_C4.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/SVM_V1/SVM_C4.mlx" download>下载 SVM_C4.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**使用自定义核训练 SVM 分类器**

## 脚本内容

```matlab
% 使用自定义核训练 SVM 分类器
```

## 导入数据

```matlab
clear
SVM_Data1
```

## 使用调整后的 sigmoid 核训练另一个 SVM 分类器。

```matlab
Mdl2 = fitcsvm(X,Y,'KernelFunction','mysigmoid2','Standardize',true);
[~,scores2] = predict(Mdl2,xGrid);
```

## 绘制数据和决策区域，

```matlab
figure;
h(1:2) = gscatter(X(:,1),X(:,2),Y);
hold on
h(3) = plot(X(Mdl2.IsSupportVector,1),...
    X(Mdl2.IsSupportVector,2),'ko','MarkerSize',10);
title('Scatter Diagram with the Decision Boundary')
contour(x1Grid,x2Grid,reshape(scores2(:,2),size(x1Grid)),[0 0],'k');
legend({'-1','1','Support Vectors'},'Location','Best');
hold off
```

## 并确定样本外的误分类率。

```matlab
CVMdl2 = crossval(Mdl2);
misclass2 = kfoldLoss(CVMdl2);
% misclass2 =    0.0450

% 在 sigmoid 斜率调整后，新决策边界似乎提供更好的样本内拟合，
% 交叉验证率收缩 66% 以上。
```
