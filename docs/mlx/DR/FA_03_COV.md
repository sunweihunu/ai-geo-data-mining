# FA_03_COV.mlx

「降维（DR）」目录 · 对应书稿 **第05章 降维** · 46.0 KB · 代码 29 行 · 图窗 3

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DR/FA_03_COV.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/DR/FA_03_COV.mlx" download>下载 FA_03_COV.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**从协方差矩阵出发**

## 脚本内容

```matlab
%从协方差矩阵出发
clear
regions2004                                              %将保存的数据导入内存
X=zscore(data);                                          %原始数据集体标准化
[Lambda,Psi,T,Stats]=factoran(cov(X),2,'Xtype','cov');   %因子模型求解
```

<pre class="mlx-out">Warning: Significance cannot be computed without either raw data or the 'nobs' argument.</pre>

```matlab
Comm=1-Psi;                                              %计算公因子方差
figure(1)
plot(Lambda(:,1),Lambda(:,2),'r+');                      %绘制载荷图
```

<img src="../FA_03_COV_media/figure_0.png" alt="图窗 1" loading="lazy" />

```matlab
%自由度(不能为负。故本例提取的最大因子数为1)
m=8;M=2;                                                  %变量数和因子数
dfe=((m-M)^2-(m+M))/2;                                    %自由度

%二维图
figure(2)
% [coefs,score] = princomp(zscore(X));
[coefs,score] = pca(zscore(X));
biplot(coefs(:,1:2), 'scores',score(:,1:2), 'varlabels',varname);
```

<img src="../FA_03_COV_media/figure_1.png" alt="图窗 2" loading="lazy" />

```matlab
%三维图
figure(3)
% [coefs,score] = princomp(zscore(X));
[coefs,score] = pca(zscore(X));
biplot(coefs(:,1:3), 'scores',score(:,1:3), 'varlabels',varname);
```

<img src="../FA_03_COV_media/figure_2.png" alt="图窗 3" loading="lazy" />

```matlab
%基于最大似然解的其他因子旋转方式
[Lambda, Psi, T, Stats,F]=factoran(X,2,'Score','wls','Rotate','none');      %不旋转
```

<pre class="mlx-out">Warning: Some unique variances are zero: cannot compute significance.</pre>

```matlab
[Lambda, Psi, T, stats, F] = factoran(X, 1, 'scores', 'regr');              %回归法旋转
[Lambda, Psi, T, Stats,F]=factoran(X,1,'Delta',0.001,'Display','off','MaxFunEvals',400,'MaxIter',100);%限制性旋转
```
