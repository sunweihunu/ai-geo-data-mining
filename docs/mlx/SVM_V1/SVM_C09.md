# SVM_C09.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 34.9 KB · 代码 46 行 · 图窗 1

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/SVM_C09.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/SVM_V1/SVM_C09.mlx" download>下载 SVM_C09.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**使用 SVM 和一类学习检测离群值**

通过将所有鸢尾花分配给同一个类来修改 Fisher 的鸢尾花数据集。 检测修改后的数据集中的离群值，并确认观测值中离群值的预期比例。

## 脚本内容

```matlab
% 使用 SVM 和一类学习检测离群值
% 通过将所有鸢尾花分配给同一个类来修改 Fisher 的鸢尾花数据集。
% 检测修改后的数据集中的离群值，并确认观测值中离群值的预期比例。

% 加载 Fisher 鸢尾花数据集。删除花瓣的长度和宽度。
% 将所有鸢尾花都视为来自同一个类。

load fisheriris
X = meas(:,1:2);
y = ones(size(X,1),1);
% 使用修改后的数据集训练 SVM 分类器。假设 5% 的观测值是离群值。对预测变量进行标准化。

rng(1);
SVMModel = fitcsvm(X,y,'KernelScale','auto','Standardize',true,...
    'OutlierFraction',0.05);
% SVMModel 是经过训练的 ClassificationSVM 分类器。
% 默认情况下，软件使用高斯核进行一类学习。
% 绘制观测值和决策边界。标记支持向量和潜在离群值。

svInd = SVMModel.IsSupportVector;
h = 0.02; % Mesh grid step size
[X1,X2] = meshgrid(min(X(:,1)):h:max(X(:,1)),...
    min(X(:,2)):h:max(X(:,2)));
[~,score] = predict(SVMModel,[X1(:),X2(:)]);
scoreGrid = reshape(score,size(X1,1),size(X2,2));

figure
plot(X(:,1),X(:,2),'k.')
hold on
plot(X(svInd,1),X(svInd,2),'ro','MarkerSize',10)
contour(X1,X2,scoreGrid)
colorbar;
title('{\bf Iris Outlier Detection via One-Class SVM}')
xlabel('Sepal Length (cm)')
ylabel('Sepal Width (cm)')
legend('Observation','Support Vector')
hold off
```

<img src="../SVM_C09_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
% 将离群值与其余数据分隔的边界出现在围道值为 0 的位置。

% 验证交叉验证数据中具有负分数的观测值的比例接近 5%。

CVSVMModel = crossval(SVMModel);
[~,scorePred] = kfoldPredict(CVSVMModel);
outlierRate = mean(scorePred<0)
```

<pre class="mlx-out">outlierRate = 0.0467</pre>

```matlab
% outlierRate = 0.0467
```
