# DA_3C_02_KC.mlx

「判别分析（LDA）」目录 · 对应书稿 **第06章 线性模型** · 3.4 KB · 代码 7 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/LDA/DA_3C_02_KC.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/LDA/DA_3C_02_KC.mlx" download>下载 DA_3C_02_KC.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**快速聚类与判别**

## 脚本内容

```matlab
%快速聚类与判别
UNDP3                                               %调入数据
T=[C1;C2;C3];                                       %将三个子样本的数据合并为训练样本
G=kmeans(T,3);                                      %快速聚类
[Class,E]=classify(S,T,G);                          %基于快速聚类结果对待判样品分类
CT=classify(T,T,G);                                 %计算训练样本的判别结果
Class,E                                             %输出部分结果
```
