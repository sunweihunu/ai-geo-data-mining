# 第8章 决策树 配套脚本

| 文件 | 说明 | 运行方式 |
|------|------|----------|
| `gen_figures.py` | 生成书稿第 8 章全部 14 张插图（`书稿/figs/ch08/`）。内含自实现的 CART 回归树/分类树（基尼指数、平方误差），其中鸢尾花树按 MATLAB `fitctree` 默认参数（MinParentSize=10）生长，复现"错分 3 个、回代误差 0.020"的课程结果 | `uv run --no-project --with matplotlib --with numpy python gen_figures.py`（需与本文件同目录的 iris.csv） |
| `iris.csv` | Fisher 鸢尾花数据集（150×5），fig8_13 / fig8_14 的数据来源 | — |
| `ch08_xigu_gain.py` | 西瓜数据集 2.0（17 样例）信息增益与增益率复算，验证表 8-3 / 表 8-4 数值（色泽 0.109、根蒂 0.143、敲声 0.141、纹理 0.381、脐部 0.289、触感 0.006，纹理最大） | `uv run --no-project --with numpy python ch08_xigu_gain.py` |

说明：修改插图参数后重绘，可直接编辑 `gen_figures.py` 中对应 `fig8_xx()` 函数；固定随机种子 `default_rng(42)`，重跑结果可复现。
