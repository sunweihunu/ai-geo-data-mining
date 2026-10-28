# Chapter21 绘图脚本归档（第21章 地学应用一：水文篇）

## 文件清单

| 文件 | 说明 |
|------|------|
| `gen_figures.py` | 本章全部 14 张插图的 matplotlib 绘图脚本（图 21-1 ~ 图 21-14） |
| `21_水文_逐页文本.txt` | 第 21 讲 PPT（54 页）逐页文本提取（`<a:t>` 文本流），章节结构与表格的权威来源 |

## 对应书稿小节与插图

输出图片目录：`书稿/figs/ch21/`（文件名 `fig21_NN_语义名.png`）。

| 图号 | 文件 | 书稿小节 | 内容 |
|------|------|----------|------|
| 图 21-1 | `fig21_01_two_circle_framework.png` | 21.1.1 | 应用研究思考框架：水文问题与机器学习功能的交集 |
| 图 21-2 | `fig21_02_ml_hydro_overview.png` | 21.2.1 | 机器学习的水文应用总览（中心 ML + 信息流） |
| 图 21-3 | `fig21_03_soil_moisture_retrieval.png` | 21.2.2 | 土壤水分的遥感反演问题框图 |
| 图 21-4 | `fig21_04_rainfall_runoff_lstm.png` | 21.2.2 | 降雨—径流滞后关系与 LSTM 门结构 |
| 图 21-5 | `fig21_05_swat_surrogate.png` | 21.2.3 | 用 SVM 构建 SWAT 的快速代理模型 |
| 图 21-6 | `fig21_06_lstm_bias_correction.png` | 21.2.3 | LSTM 偏差校正三种输入组合 |
| 图 21-7 | `fig21_07_runoff_formation.png` | 21.3.1 | 径流形成过程示意（P/Is/E/Qs/Qg1/Qg2） |
| 图 21-8 | `fig21_08_runoff_generation.png` | 21.3.2 | 蓄满产流 vs 超渗产流 |
| 图 21-9 | `fig21_09_urbanization_hydrograph.png` | 21.3.3 | 自然流域与城市化流域径流过程线对比 |
| 图 21-10 | `fig21_10_forecast_timeline.png` | 21.3.4 | 中长期预报的两个时间点与时间尺度 |
| 图 21-11 | `fig21_11_predictors.png` | 21.3.6 | 中长期预报因子体系（遥相关 + 本地） |
| 图 21-12 | `fig21_12_decision_tree.png` | 21.4.5 | 天气分类决策树示例 |
| 图 21-13 | `fig21_13_hepex_workflow.png` | 21.4.6 | 水文集合预报系统流程图（HEPEX） |
| 图 21-14 | `fig21_14_ensemble_combination.png` | 21.4.7 | 多预报成果综合（等权平均与 BMA） |

## 运行环境与方式

Windows 下不直接调用 python（商店占位符），用 uv 拉取依赖运行：

```bash
uv run --no-project --with matplotlib --with numpy python gen_figures.py
# 网络超时可改用缓存：uv run --offline --no-project --with matplotlib --with numpy python gen_figures.py
```

脚本内 `OUT` 为输出目录的绝对路径（指向 `书稿\figs\ch21`），换机器运行前请相应修改。

风格约定：Microsoft YaHei / SimHei 中文字体；配色 C_BLUE=#1f77b4 等；savefig dpi=150、bbox_inches="tight"；`rng = np.random.default_rng(42)` 固定随机种子；公式一律 mathtext（如 `$Q_{g1}$`），不用 Unicode 上下标。运行输出应零 Warning；新增图函数请追加到 `__main__` 列表末尾（rng 顺序消耗，追加不影响已有图）。
