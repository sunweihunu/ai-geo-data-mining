# Chapter4 配套代码与数据 —— 聚类分析

对应书稿《人工智能与地理数据挖掘》**第04章 聚类分析**（原始讲义：《机器学习与地学应用》第四讲）。

## 文件清单

| 文件 | 对应书稿章节 | 内容 |
|------|--------------|------|
| `CLUSTER_exp01_fukuoka_hierarchical.m` | 4.6.1 案例1 | 福冈甜橘引种地点的层次聚类（多函数法）：中心法+标准欧氏距离、最短距离法+基于主成分的距离两种方案，谱系图、Cophenetic 系数、与福冈的距离排序、切 3 类输出 |
| `CLUSTER_exp02_iris_kmeans.m` | 4.6.2 案例2 | Fisher 鸢尾花 K-均值聚类（k=3，Replicates=5）：轮廓图与平均轮廓系数、`crosstab` 与真实品种对照、花瓣长宽平面可视化 |
| `CLUSTER_exp03_iris_hierarchical.m` | 4.6.2 案例2 | 鸢尾花层次聚类：`linkage`（组间平均法）+ 完整谱系图（可人工画线分 2/3/4 类）+ 切 3 类与品种对照 |
| `CLUSTER_exp04_kmeans_1d_2d.m` | 4.3.3、4.3.4 | K-均值教学示例：一维数据 [2,4,10,12,3,20,30,11,25] 的五次迭代（复现表 4-11）与二维 10 点聚类 |
| `gen_figures.py` | 全章插图 | 第 4 章 17 张插图的生成脚本（自实现 k 均值、Lance-Williams 层次聚类、DBSCAN、GMM-EM，numpy + matplotlib） |
| `data/fukuoka_climate.csv` | 4.6.1 | 引种案例 7 城市 × 5 气象指标数据（福冈/合肥/成都三行据课件，其余为按气候常年值整理的示例值），与书稿表 4-18 一致 |
| `04_聚类分析_逐页文本.txt` | — | 原始课件《04 聚类分析 V8.pptx》84 页的逐页文本提取结果 |

## 运行环境与说明

- MATLAB 脚本需要 **MATLAB 及 Statistics and Machine Learning Toolbox**（`pdist`、`linkage`、`dendrogram`、`cophenet`、`cluster`、`kmeans`、`silhouette`、`dbscan`、`pca`、`gscatter`、`crosstab` 均来自该工具箱）。
- 鸢尾花脚本使用 MATLAB **内置数据集** `fisheriris`（`meas` 为 150×4 测量值、`species` 为品种名），无需另行下载。
- 运行前将 MATLAB 当前文件夹切换到本目录（`脚本/Chapter4`）即可直接运行各脚本。
- 引种案例数据为**教学示例值**：福冈、合肥、成都三行取自课件代码，武汉、长沙、桂林、温州四行按气候常年值整理。按示例数据重算的结论（与福冈最近的城市为长沙）与课件一致；换成教材原始数据后具体数值会略有差异，以自己的运行输出为准。
- 插图脚本运行方式：`uv run --no-project --with matplotlib --with numpy python gen_figures.py`，输出至 `书稿/figs/ch04/`（脚本内 `OUT` 为相对路径，可在项目根目录或本目录运行）。
- 课件官方示例（含 k 距离图画法）：`openExample('stats/clusterdemo')` 与 MATLAB 帮助文档 `dbscan-clustering` 页。
