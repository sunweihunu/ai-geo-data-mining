# Chapter11 深度学习（书稿第11章）配套代码与资料

本章对应书稿《第11章 深度学习》（`书稿/第11章 深度学习.md`），插图 14 张位于
`书稿/figs/ch11/`。

## 文件清单

| 文件 | 说明 | 对应书稿小节 |
|------|------|--------------|
| `gen_figures.py` | 全部 14 张插图的生成脚本（matplotlib + numpy，固定随机种子 42） | 11.2、11.3、11.4、11.5 各节插图 |
| `demo_alexnet_webcam.m` | 摄像头 + AlexNet 预训练网络实时图像分类 | 11.7.1 案例一 |
| `demo_googlenet_top5.m` | 摄像头 + GoogLeNet：实时分类并显示 Top-5 概率条形图 | 11.7.1 案例一 |
| `demo_digit_cnn.m` | 从头构建 CNN 识别手写数字（750 训练 / 250 验证） | 11.7.2 案例二 |
| `demo_lstm_sequence.m` | LSTM 序列分类骨架示例（多对一结构） | 11.7.2 末尾 |
| `11_深度学习_逐页文本.txt` | 课件《11 深度学习 V8.pptx》105 页的逐页文本提取（sed 提取 `<a:t>`） | 全章结构与表格依据 |

## 运行环境

- **gen_figures.py**：Python 3.8+，`matplotlib`、`numpy`。Windows 下 python 为商店占位符时用
  `uv run --no-project --with matplotlib --with numpy python gen_figures.py`；
  输出目录由脚本内 `OUT` 指定（默认指向 `书稿/figs/ch11`），可在本目录重建。
  中文字体使用 Microsoft YaHei / SimHei。
- **MATLAB 演示脚本**：需要深度学习工具箱（Deep Learning Toolbox）。
  - `demo_alexnet_webcam.m` / `demo_googlenet_top5.m`：首次运行会提示安装预训练网络
    支持包与摄像头支持包，按提示链接安装即可；无 GPU 可运行（CPU 即可）。
  - `demo_digit_cnn.m`：优先使用本目录 `DigitDataset/`（按数字 0—9 建子文件夹存放图像，
    本归档未附带图像数据）；不存在时自动改用 MATLAB 自带的手写数字示例数据集。
  - `demo_lstm_sequence.m`：骨架示例，数据部分为注释伪代码，替换为实际序列数据后运行。

## 数据说明

本章课件演示未提供外部数据文件（数字图像数据用 MATLAB 自带示例数据集即可复现），
故本目录无 `data/` 子目录。

## 备注

- 课件封面页写“第十讲 深度学习”系笔误，按课件文件名（11）与全书章节顺序，
  本章书稿编号为第 11 章（第 10 章为支持向量机）。
- 本章书稿依据两轮共四次课的逐字稿（2022-11-23/24 DL part1、2022-11-30/12-01 DL part2）
  与 105 页课件整理；插图全部依据课件内容重绘，未引用课件原图。
