# Chapter23 绘图脚本归档（第23章 地学应用三：土地篇）

## 文件清单

| 文件 | 说明 |
|------|------|
| `gen_figures.py` | 本章全部 10 张插图的 matplotlib 绘图脚本（图 23-1 ~ 图 23-10） |
| `23_土地_逐页文本.txt` | 第 23 讲 PPT（23 页）逐页文本提取（`<a:t>` 文本流），章节结构与表格的权威来源 |

## 对应书稿小节与插图

输出图片目录：`书稿/figs/ch23/`（文件名 `fig23_NN_语义名.png`）。

| 图号 | 文件 | 书稿小节 | 内容 |
|------|------|----------|------|
| 图 23-1 | `fig23_01_lsm_concept.png` | 23.1.2 | LSM 问题概念框图：X 因子图层（全域已知）+ 局部 Y 真值 → 模型 → 全域易感性图 |
| 图 23-2 | `fig23_02_conditioning_factors.png` | 23.1.2 | 常用滑坡条件因子示例（坡度/坡向/土壤类型/降雨/地形湿度/岩性，六面板） |
| 图 23-3 | `fig23_03_binary_vs_fiveclass.png` | 23.1.3 | 同一滑坡可能性的两种表达：二分类 vs 五分类（概率区间分级） |
| 图 23-4 | `fig23_04_research_trends.png` | 23.2.2 | 研究热度：逐年文章数柱状图 + 常用模型前五份额（数据示意） |
| 图 23-5 | `fig23_05_decision_tree.png` | 23.3.1 | 滑坡预测决策树示例（坡度/高程/NDVI/土壤深度/降雨阈值，仅作示意） |
| 图 23-6 | `fig23_06_random_forest.png` | 23.3.2 | 随机森林流程：Bootstrap 重抽样 → 多棵决策树 → 平均/投票集成 |
| 图 23-7 | `fig23_07_six_steps.png` | 23.4 | 基于 ML 的 LSM 六步建模总流程（蛇形布局） |
| 图 23-8 | `fig23_08_feature_selection.png` | 23.4.2 | 特征选择：VIF 检验多重共线性 + 信息增益评估因子贡献 |
| 图 23-9 | `fig23_09_cv_grid.png` | 23.4.3/23.4.4 | 五折交叉验证切割 + 网格搜索超参数（SVM 的 C–γ 网格） |
| 图 23-10 | `fig23_10_multi_model_maps.png` | 23.5 | 多模型五级易感性图对比（LR/NB/NNET/QDA/RF/SVM，合成数据） |

## 运行环境与方式

Windows 下不直接调用 python（商店占位符），用 uv 拉取依赖运行：

```bash
uv run --no-project --with matplotlib --with numpy python gen_figures.py
# 网络超时可改用缓存：uv run --offline --no-project --with matplotlib --with numpy python gen_figures.py
```

脚本内 `OUT` 为输出目录的绝对路径（指向 `书稿\figs\ch23`），换机器运行前请相应修改。

风格约定：Microsoft YaHei / SimHei 中文字体；配色 C_BLUE=#1f77b4 等；五级易感性色带 RAMP5（#2c7bb6 → #d7191c）；savefig dpi=150、bbox_inches="tight"；`rng = np.random.default_rng(42)` 固定随机种子；公式一律 mathtext（如 `$\gamma$`），不用 Unicode 上下标。运行输出零 Warning；新增图函数请追加到 `__main__` 列表末尾（rng 顺序消耗，追加不影响已有图）。

## 备注

- 空间示意图（图 23-1、23-2、23-10）均为固定种子的合成高斯混合场，图上已注明"示意"；图 23-4、23-8、23-9 的数值同为示意，正文与图注均已说明。
- 类别图 imshow 必须配 `BoundaryNorm`（脚本内 `cls_norm`）：整数类别数组直接配 ListedColormap 会按数据 min/max 归一化，导致色带错位、个别等级缺色。
- 逐字稿来源（供内容溯源）：20221228151731 的后半（LSM 问题定义、二分类/五分类、综述文献计量、决策树与随机森林例子、六步流程）；20221230100104 的"土地方面"部分（平行班重复讲授，用于互补：Y 真值的现场观测来源、几十到上百个珍贵样本、X 多 Y 少的空间外推逻辑、决策树"越靠近根节点的因子越重要"、广东粤北山区应用背景、土地利用与变化检测背景）。两个逐字稿中的气象部分归第 22 章、地球系统/NLP 部分归第 24 章，均未写入本章。
