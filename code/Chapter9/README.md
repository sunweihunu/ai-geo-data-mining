# Chapter9 配套代码与数据 —— 人工神经网络

对应书稿《人工智能与地理数据挖掘》**第09章 人工神经网络**（原始讲义：《机器学习与地学应用》第九讲）。

## 文件清单

| 文件 | 对应书稿章节 | 内容 |
|------|--------------|------|
| `gen_figures.py` | 全章插图 | 第九章全部 15 张插图（图 9-1~图 9-15）的 matplotlib 生成脚本，输出至 `书稿/figs/ch09/`（fig9_01~fig9_15）。固定随机种子 42（案例数值实验另用固定种子 2022），改参重跑可复现 |
| `09_神经网络_逐页文本.txt` | — | 《09 神经网络 V6.pptx》93 页逐页文本提取（unzip + sed 解析 `<a:t>`），书稿撰写时的原始参考数据 |
| `ANN_exp01_regression.m` | 9.9.1 案例1 | 一元非线性函数回归：`rng(42)` 生成与插图一致的模拟数据，`fitnet(8)` + `trainlm` + `train` + `sim`，评估 MSE 与相关系数并绘图 |
| `ANN_exp02_iris_patternnet.m` | 9.9.2 案例2 | Fisher 鸢尾花多分类：`ind2vec` 构造 one-hot 目标，`patternnet(10)` + `trainscg` + `train` + `sim`，`vec2ind` 取概率最大类，`plotconfusion` 混淆矩阵 |

## 运行环境与说明

- 绘图脚本运行方式：`uv run --no-project --with matplotlib --with numpy python gen_figures.py`（PyPI 网络超时时加 `--offline` 使用本地缓存）；需系统安装中文字体 Microsoft YaHei 或 SimHei。
- MATLAB 案例需要 **Deep Learning Toolbox**（`fitnet`、`patternnet`、`train`、`sim`、`plotconfusion`）；案例 2 另用到 Statistics and Machine Learning Toolbox 的 `grp2idx`。
- 案例 2 训练数据为 MATLAB 内置数据集 `fisheriris`，无需另行下载。
- 神经网络训练含随机初始化（MATLAB 中 `rng` 控制数据生成，网络初始权重仍随机），每次运行结果会略有不同——这正是书稿 9.7.9 节"多组不同初始参数"策略的体现。
- 讲师课堂示例取自 MATLAB 官网（书稿 9.12 节附链接），本目录两个脚本为按课程口径整理的最小示例。
