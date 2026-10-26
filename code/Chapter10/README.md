# Chapter10 配套代码与数据 —— 支持向量机（SVM）

对应书稿《人工智能与地理数据挖掘》**第10章 支持向量机**（原始讲义：《机器学习与地学应用》第十讲 支持向量机）。

## 文件清单

| 文件 | 对应书稿章节 | 内容 |
|------|--------------|------|
| `gen_figures.py` | 全章插图 | 生成书稿图 10-1 ~ 图 10-14 共 14 张插图（matplotlib + numpy；内置简化 SMO 求解器与核岭回归，不依赖 scikit-learn） |
| `SVM_exp01_iris_svc.m` | 10.8.1 案例一 | 鸢尾花二分类：去掉 setosa，花瓣长度/宽度两特征，标准化后 `fitcsvm`（RBF 核）训练、`predict` 回代、可视化决策边界与支持向量（图 10-14） |
| `SVM_exp02_svr_sine.m` | 10.8.2 案例二 | 一元非线性回归：正弦+噪声数据，标准化后 `fitrsvm`（高斯核）拟合、预测后**反标准化**再算相关系数与 RMSE |
| `data/iris.csv` | 10.8.1 / 图 10-14 | Fisher 鸢尾花数据集（150 样本 × 4 特征 + 品种，UCI iris.data 整理），供 `gen_figures.py` 画案例插图用；MATLAB 案例脚本用内置 `fisheriris`，不依赖此文件 |
| `10_支持向量机_逐页文本.txt` | — | 原始课件《10. 支持向量机 V5.pptx》（54 页）逐页文本提取结果（`<a:t>` 标签），供内容核对 |

## 运行环境与说明

- **MATLAB 脚本**：需要 MATLAB R2018a+ 及 Statistics and Machine Learning Toolbox（`fitcsvm`、`fitrsvm`、`predict`、`gscatter`）；案例一用 MATLAB 内置 `fisheriris` 数据集，无需另行下载数据。运行前把当前文件夹切到本目录直接运行即可。
- **绘图脚本**：`uv run --no-project --with matplotlib --with numpy python gen_figures.py`（Windows 无系统 python 时统一用 `uv run`；PyPI 超时可加 `--offline` 用缓存）。输出目录为 `../../书稿/figs/ch10/`，固定随机种子 42，可整体复跑；如需新增插图，把新函数**追加**到 `MAIN` 列表末尾，避免改变已有图的随机数流。
- `gen_figures.py` 内含：简化 SMO 软间隔对偶求解器（线性/多项式/RBF 核）、核岭回归（用于示意不同核函数的回归曲线形状）、图 10-2/10-5/10-9 为解析构造的几何示意图。
- 插图与书稿图号的对应关系：`fig10_01_margin_idea` → 图 10-1、`fig10_02_margin_geometry` → 图 10-2、`fig10_03_normalization` → 图 10-3、`fig10_04_hyperplane_dims` → 图 10-4、`fig10_05_kernel_mapping` → 图 10-5、`fig10_06_kernels_classification` → 图 10-6、`fig10_07_svr_kernels` → 图 10-7、`fig10_08_history` → 图 10-8、`fig10_09_convex_qp` → 图 10-9、`fig10_10_kernel_functions` → 图 10-10、`fig10_11_soft_margin` → 图 10-11、`fig10_12_effect_of_C` → 图 10-12、`fig10_13_svr_epsilon` → 图 10-13、`fig10_14_case_iris` → 图 10-14。
