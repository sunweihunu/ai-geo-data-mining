# kNN_exp11_Reg.mlx

「k 最近邻（kNN）」目录 · 对应书稿 **第07章 k最近邻（kNN）模型** · 18.3 KB · 代码 30 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/kNN/kNN_exp11_Reg.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/kNN/kNN_exp11_Reg.mlx" download>下载 kNN_exp11_Reg.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**根据病人的年龄和身高预测血压最高值**

采用kNN解决回归问题 具体使用knnsearch和mean

## 脚本内容

```matlab
% 根据病人的年龄和身高预测血压最高值
% 采用kNN解决回归问题
% 具体使用knnsearch和mean
```

## 导入医院数据集

```matlab
load hospital;

disp(hospital)  % 展示一下hospital的内容
X = [hospital.Age hospital.Weight];
Y= hospital.BloodPressure(:,1);
```

## Case 1 对5个病人进行预测，没有高血压的真值

```matlab
X_new = [20 162; 30 169; 40 168; 50 170; 60 171];   % 5个新病人

% 默认的knnsearch
Idx = knnsearch(X,X_new);
% Find the patients in X closest in age and weight to those in Y.
X(Idx,:)
Y_pre1=mean(Y(Idx),2)  %最近邻的Y的平均值

% 改变knnsearch参数
Idx2 = knnsearch(X,X_new,'K',2,'Distance','minkowski','P',5);
X(Idx2(:,1),:)  % 第1个最近邻的X
X(Idx2(:,2),:)  % 第2个最近邻的X
Y_pre2=mean(Y(Idx2),2)  %最近邻的Y的平均值
% 比较一下结果
[Y_pre1 Y_pre2]
```

## Case 2 对所有数据集进行预测

采用knnsearch和自取平均值方法

```matlab
kk=2
Idx3 = knnsearch(X,X,'K',kk);
Y_pre3=mean(Y(Idx3),2)

% 比较结果
figure;
plot(Y,Y_pre3,'*');
```
