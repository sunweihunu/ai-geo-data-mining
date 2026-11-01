# UNDP2.mlx

「判别分析（LDA）」目录 · 对应书稿 **第06章 线性模型** · 3.2 KB · 代码 20 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/LDA/UNDP2.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/LDA/UNDP2.mlx" download>下载 UNDP2.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**二分类判别分析**

UNDP2.m

## 脚本内容

```matlab
%二分类判别分析
%UNDP2.m
C1=[79.1	99.0 	23582
76.8	99.0 	29605
80.0	99.0 	23257
78.7	99.0 	25512
73.1	96.7 	12013
75.0	74.6 	17719];                             %第一类训练样本矩阵
C2=[75.8	96.4 	3967
66.7	99.5 	6460
71.3	98.2 	4809
70.7	91.2 	6006
72.9	99.0 	3353
69.8	92.8 	4288
69.4	77.8 	4036
66.7	53.7 	3041];                              %第二类训练样本矩阵
S=[78.7	99.0 	20659
78.2	96.9 	13943
70.2	97.9 	5648
68.0	82.8 	3105];                              %待判样本矩阵
```
