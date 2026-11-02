# MLX 实时脚本总览

这里收录课程配套的 **MATLAB 实时脚本（Live Script，.mlx）**：代码、文字说明与运行结果在同一文档中交替呈现，适合边看边运行。每个脚本有单独页面展示其代码与说明，并提供「在 MATLAB Online 中打开」「复制代码」「下载」三种操作。

| 目录 | 对应章节 | 脚本数 | 打包下载 |
|------|----------|-------:|----------|
| [降维（DR）](./DR/index.md) | 第05章 降维 | 12 | [MLX_DR.zip](downloads/MLX_DR.zip) |
| [判别分析（LDA）](./LDA/index.md) | 第06章 线性模型 | 9 | [MLX_LDA.zip](downloads/MLX_LDA.zip) |
| [k 最近邻（kNN）](./kNN/index.md) | 第07章 k最近邻（kNN）模型 | 12 | [MLX_kNN.zip](downloads/MLX_kNN.zip) |
| [决策树（CART）](./DecisionTree_v2/index.md) | 第08章 决策树 | 11 | [MLX_DecisionTree_v2.zip](downloads/MLX_DecisionTree_v2.zip) |
| [人工神经网络（ANN）](./ANN/index.md) | 第09章 人工神经网络 | 46 | [MLX_ANN.zip](downloads/MLX_ANN.zip) |
| [支持向量机（SVM）](./SVM_V1/index.md) | 第10章 支持向量机 | 24 | [MLX_SVM_V1.zip](downloads/MLX_SVM_V1.zip) |
| [深度学习（DeepL）](./DeepL_V2/index.md) | 第11章 深度学习 | 19 | [MLX_DeepL_V2.zip](downloads/MLX_DeepL_V2.zip) |

## 使用说明

1. **运行环境**：实时脚本需 MATLAB R2016a 及以上版本；多数脚本依赖 Statistics and Machine Learning Toolbox，第09章 `ANN_01–27` 使用较旧的神经网络工具箱函数（`newff`、`trainlm` 等），较新版本中仍可用。第11章（DeepL_V2）需 **Deep Learning Toolbox**，`Cam_*` / `Img_*` 首次运行会提示安装预训练网络与摄像头支持包；`seq_LSTM_Reg_V2_seq` 需 C-MAPSS 数据集（可在「参考代码」板块第11章页面下载 CMAPSSData.zip）。
2. **三种操作**：「在 MATLAB Online 中打开」在本站仓库推送 GitHub 后生效（需登录 MathWorks 账号）；「复制代码」把脚本全部代码复制到剪贴板；「下载」保存原始 .mlx 文件，在本地 MATLAB 中直接打开。
3. **网页摘录说明**：页面展示脚本中的代码与文字说明；运行输出（命令行结果与图窗）保存在 .mlx 内部，不随网页展示，打开原文件即可看到。早期脚本中的中文注释在网页展示时已做编码还原，原始文件未做任何改动。
4. **与「参考代码」板块的关系**：本板块的实时脚本与[参考代码](../refcode/)中的 .m 脚本同源（如 `ANN_01_Lin.mlx` 与 `ANN_01_Lin.m`），.mlx 版本保留原讲义排版，适合对照书稿阅读。