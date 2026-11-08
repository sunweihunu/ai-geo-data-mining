# SVM_C4.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 25.4 KB · 代码 20 行 · 图窗 1

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_C4.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/SVM_V1/SVM_C4.mlx" download>下载 SVM_C4.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

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

<img src="../SVM_C4_media/figure_0.png" alt="图窗 1" loading="lazy" />

## 使用调整后的 sigmoid 核训练另一个 SVM 分类器。

```matlab
Mdl2 = fitcsvm(X,Y,'KernelFunction','mysigmoid2','Standardize',true);
[~,scores2] = predict(Mdl2,xGrid);
```

<pre class="mlx-out">Unrecognized function or variable 'xGrid'.</pre>

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
