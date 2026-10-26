# Chapter6 配套代码与数据 —— 线性模型

对应书稿《人工智能与地理数据挖掘》**第06章 线性模型**（原始讲义：《机器学习与地学应用》第六讲）。

## 文件清单

| 文件 | 对应书稿位置 | 内容 |
|------|--------------|------|
| `gen_figures.py` | 全章插图 | 第六章全部 14 张插图（图 6-1~图 6-14）的 matplotlib 生成脚本，输出至 `书稿/figs/ch06/`（fig6_01~fig6_14）。固定随机种子 42，改参重跑可复现 |
| `06_线性模型_逐页文本.txt` | — | 《06 线性模型 V5.pptx》74 页逐页文本提取（unzip + sed 解析 `<a:t>`），书稿撰写时的原始参考数据 |

## 运行环境与说明

- 绘图脚本运行方式：`uv run --no-project --with matplotlib --with numpy python gen_figures.py`（PyPI 网络超时时加 `--offline` 使用本地缓存）；需系统安装中文字体 Microsoft YaHei 或 SimHei。
- 插图数据除标注外均为脚本内固定种子的模拟数据，用于概念示意。
- 书稿 6.8 节 UNDP 案例引用的课程原始 MATLAB 文件（`DA2C_01.m`~`DA_3C_02_KC.m`）未随原始讲稿提供；正文中的代码段为按课程口径（`classify`、`fitcdiscr`+`predict`、`regress`、`polyfit`）整理的最小示例。
