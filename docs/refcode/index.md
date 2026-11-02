# 参考代码总览

这里是随书各章**参考代码**的在线浏览页：每个脚本均展示完整源码与注释说明，可单文件下载，也可整章打包下载。

| 章节 | 文件数 | 页面 | 打包下载 |
|------|-------:|------|----------|
| 第04章 聚类分析 | 24 | [浏览](./ch04.md) | [ch04_聚类分析_参考代码.zip](downloads/ch04_%E8%81%9A%E7%B1%BB%E5%88%86%E6%9E%90_%E5%8F%82%E8%80%83%E4%BB%A3%E7%A0%81.zip) |
| 第05章 降维 | 12 | [浏览](./ch05.md) | [ch05_降维_参考代码.zip](downloads/ch05_%E9%99%8D%E7%BB%B4_%E5%8F%82%E8%80%83%E4%BB%A3%E7%A0%81.zip) |
| 第06章 线性模型 | 9 | [浏览](./ch06.md) | [ch06_线性模型（判别分析）_参考代码.zip](downloads/ch06_%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%EF%BC%88%E5%88%A4%E5%88%AB%E5%88%86%E6%9E%90%EF%BC%89_%E5%8F%82%E8%80%83%E4%BB%A3%E7%A0%81.zip) |
| 第07章 k最近邻（kNN）模型 | 12 | [浏览](./ch07.md) | [ch07_k 最近邻_参考代码.zip](downloads/ch07_k%20%E6%9C%80%E8%BF%91%E9%82%BB_%E5%8F%82%E8%80%83%E4%BB%A3%E7%A0%81.zip) |
| 第08章 决策树 | 11 | [浏览](./ch08.md) | [ch08_决策树_参考代码.zip](downloads/ch08_%E5%86%B3%E7%AD%96%E6%A0%91_%E5%8F%82%E8%80%83%E4%BB%A3%E7%A0%81.zip) |
| 第09章 人工神经网络 | 46 | [浏览](./ch09.md) | [ch09_人工神经网络_参考代码.zip](downloads/ch09_%E4%BA%BA%E5%B7%A5%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C_%E5%8F%82%E8%80%83%E4%BB%A3%E7%A0%81.zip) |
| 第10章 支持向量机 | 25 | [浏览](./ch10.md) | [ch10_支持向量机_参考代码.zip](downloads/ch10_%E6%94%AF%E6%8C%81%E5%90%91%E9%87%8F%E6%9C%BA_%E5%8F%82%E8%80%83%E4%BB%A3%E7%A0%81.zip) |
| 第11章 深度学习 | 20 | [浏览](./ch11.md) | [ch11_深度学习_参考代码.zip](downloads/ch11_%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0_%E5%8F%82%E8%80%83%E4%BB%A3%E7%A0%81.zip) |

## 使用说明

1. **运行环境**：MATLAB R2014b 及以上；多数脚本依赖 Statistics and Machine Learning Toolbox（`pca`、`fitcknn`、`fitcsvm`、`fitctree`、`fitcdiscr`、`linkage`、`kmeans` 等）。第09章 `ANN_01–27` 使用较旧的神经网络工具箱函数（`newff`、`trainlm`），在较新版本中仍可用。第11章需 **Deep Learning Toolbox**：`Cam_*` / `Img_*` 首次运行会提示安装预训练网络与摄像头支持包，按提示操作即可；`seq_LSTM_Reg_V2_seq` 另需先下载 C-MAPSS 数据集（见该章页面）。
2. **运行方法**：下载后把 MATLAB「当前文件夹」切换到脚本所在目录，打开脚本直接运行；需要数据的脚本会自动加载同目录的数据文件（或 `fisheriris` 等内置数据集）。
3. **编码说明**：原始参考代码中 GBK 与 UTF-8 编码各占一半，本站所有文本已统一转为 UTF-8；脚本内容未做任何改动。
4. **按钮说明**：「复制代码」一键复制完整脚本；「在 MATLAB Online 中打开」会在 [MATLAB Online](https://matlab.mathworks.com/) 中克隆本站 GitHub 仓库并打开当前脚本（需登录 MathWorks 账号，仓库发布到 GitHub 后生效）；「下载」保存原文件。
5. **与书稿的关系**：脚本的编号与书稿中的例题、图表对应（如 `ANN_18_BP.m` 对应第09章 BP 网络示例）；各章正文中的「配套代码」指的是经重写注释的 `code/ChapterX` 精选脚本，此处为更完整的原始参考代码。