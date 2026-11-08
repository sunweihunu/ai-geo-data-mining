# kNN_exp12_Reg.mlx

「k 最近邻（kNN）」目录 · 对应书稿 **第07章 k最近邻（kNN）模型** · 14.5 KB · 代码 25 行 · 图窗 1

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/kNN/kNN_exp12_Reg.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/kNN/kNN_exp12_Reg.mlx" download>下载 kNN_exp12_Reg.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**根据病人的年龄和身高预测血压最高值**

采用kNN解决回归问题 具体使用fitcknn和predict函数

## 脚本内容

```matlab
% 根据病人的年龄和身高预测血压最高值
% 采用kNN解决回归问题
% 具体使用fitcknn和predict函数

% 导入医院数据集
load hospital;
X = [hospital.Age hospital.Weight];
Y= hospital.BloodPressure(:,1);

% 5个病人的自变量数据，没有高血压的真值
X_new = [20 162; 30 169; 40 168; 50 170; 60 171];   % 5个新病人


% 采用fitcknn和predict 进行预测
Mdl = fitcknn(X,Y,'NumNeighbors',2);
Y_pre = predict(Mdl,X)
```

<pre class="mlx-out">Y_pre = 100x1
   124
   109
   113
   117
   122
   121
   123
   115
   115
   118</pre>

```matlab
% 对5个病人进行预测
Y_pre_new = predict(Mdl,X_new)
```

<pre class="mlx-out">Y_pre_new = 5x1
   127
   120
   128
   125
   125</pre>

```matlab
% 比较结果
figure;
plot(Y,Y_pre,'o');hold on;
plot(Y_pre_new,Y_pre_new,'*');
```

<img src="../kNN_exp12_Reg_media/figure_0.png" alt="图窗 1" loading="lazy" />
