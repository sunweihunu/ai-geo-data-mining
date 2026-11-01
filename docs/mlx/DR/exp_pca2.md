# exp_pca2.mlx

「降维（DR）」目录 · 对应书稿 **第05章 降维** · 28.1 KB · 代码 28 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DR/exp_pca2.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DR/exp_pca2.mlx" download>下载 exp_pca2.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**==  加权 PCA  ==**

## 脚本内容

```matlab
%  ==  加权 PCA  ==
clear all
% 执行主成分分析时，使用变量的逆方差作为权重。
% == Step1  加载样本数据集。
load hald

%== Step2  使用原料数据的逆方差作为变量权重执行主成分分析。
 [wcoeff,score,latent,~,explained] = pca(ingredients,'VariableWeights','variance')

% 请注意，系数矩阵 wcoeff 不是正交矩阵。

% == Step3  计算正交系数矩阵。
coefforth = inv(diag(std(ingredients)))* wcoeff
% 检查新系数矩阵 coefforth 的正交性。
% 正交矩阵和自己转制相乘以后对角线为1
 coefforth*coefforth'

 % == Step4 画图
biplot(wcoeff(:,1:2),'scores',score(:,1:2),'varlabels',{'v_1','v_2','v_3','v_4'});

% figure;
% biplot(coefforth(:,1:2),'scores',score(:,1:2),'varlabels',{'v_1','v_2','v_3','v_4'});

figure;
scatter(score(:,1),score(:,2))
axis equal
xlabel('1st Principal Component')
ylabel('2nd Principal Component')
```
