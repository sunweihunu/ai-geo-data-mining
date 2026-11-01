# mysigmoid.mlx

「支持向量机（SVM）」目录 · 对应书稿 **第10章 支持向量机** · 3.5 KB · 代码 10 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/SVM_V1/mysigmoid.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/SVM_V1/mysigmoid.mlx" download>下载 mysigmoid.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**编写一个函数，该函数接受特征空间中的两个矩阵作为输入，并使用 sigmoid 核将它们转换为 Gram 矩阵。**

## 脚本内容

```matlab
% 编写一个函数，该函数接受特征空间中的两个矩阵作为输入，并使用 sigmoid 核将它们转换为 Gram 矩阵。

function G = mysigmoid(U,V)
% Sigmoid kernel function with slope gamma and intercept c
gamma = 1;
c = -1;
G = tanh(gamma*U*V' + c);
end

% 将此代码保存为您的 MATLAB® 路径上名为 mysigmoid 的文件。
```
