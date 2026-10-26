# Chapter2 配套代码与数据 —— 编程环境与语言

对应书稿《人工智能与地理数据挖掘》**第02章 编程环境与语言**（原始讲义：《机器学习与地学应用》第二讲，课件分 P1\_3 与 P4\_5 两册）。

## 文件清单

| 文件 | 对应书稿章节 | 内容 |
|------|--------------|------|
| `gen_figures.py` | 全章插图 | 本章 14 幅插图的生成脚本（matplotlib，全示意类图、无随机数据），输出到 `书稿/figs/ch02/` |
| `demo02_compare.m` | 2.8.10、2.8.11 | MATLAB 侧对照演示：`z = x + y` 逐元素相加、切片 `a(2:5)`、Python range 的 MATLAB 等价写法、`end` 与循环体归属、sin/cos 曲线图 |
| `demo02_compare.py` | 2.8.10、2.8.11 | Python 侧对照演示：列表拼接 vs NumPy 逐元素相加、切片 `a[1:5]` 与负下标、range 五例、缩进决定循环体、matplotlib 画同一幅 sin/cos 图 |
| `02_编程环境和语言_P1_3_逐页文本.txt` | — | 课件《02 编程环境和语言 P1_3 V2.pptx》（77 页）的逐页文本提取结果（Linux、Shell、使用场景、Git、VS Code） |
| `02_编程环境和语言_P4_5_逐页文本.txt` | — | 课件《02 编程环境和语言 P4_5 V5.pptx》（64 页）的逐页文本提取结果（隔离环境、UV、Anaconda、MATLAB/Python 对比与互调） |

## 运行环境与说明

- **插图脚本**：`uv run --no-project --with matplotlib --with numpy python gen_figures.py`（脚本内 `OUT` 为绝对路径，换机器运行时按需修改；本组插图为示意图，不含随机数，无需固定种子）。
- **Python 演示**：`uv run --no-project --with numpy --with matplotlib python demo02_compare.py`。
- **MATLAB 演示**：基础 MATLAB 即可运行，未用到任何工具箱函数；`demo02_compare.m` 与 `demo02_compare.py` 输出一一对应，适合并排运行、对照体会两种语言的差异。
- **本章无外部数据文件**：所有演示数据均为脚本内生成的简单序列，`data/` 目录从缺。
- 提取逐页文本所用方法：unzip 解包 pptx 后对 `ppt/slides/slideN.xml` 以 `<a:t>` 标签逐页提取（表格单元格按 `<a:tc>` 坐标核对）。
