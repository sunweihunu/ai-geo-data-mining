# -*- coding: utf-8 -*-
"""第1章 绪论 插图生成脚本（全部为概念示意图，matplotlib 重绘）"""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Rectangle
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "书稿" / "figs" / "ch01"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

C_BLUE = "#1f77b4"
C_ORANGE = "#ff7f0e"
C_GREEN = "#2ca02c"
C_RED = "#d62728"
C_PURPLE = "#9467bd"
C_GRAY = "#7f7f7f"
C_LIGHT = "#eef3fb"

rng = np.random.default_rng(42)


def _box(ax, x, y, w, h, text, fc=C_LIGHT, ec=C_BLUE, fs=10, tc="black", lw=1.4, style="round,pad=0.02,rounding_size=0.06", bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style, fc=fc, ec=ec, lw=lw, mutation_aspect=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", linespacing=1.4)


def _arrow(ax, x1, y1, x2, y2, color=C_GRAY, lw=1.6, style="-|>", ms=14, ls="-", rad=0.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}"))


def _save(fig, name):
    fig.savefig(OUT / name, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved:", name)


# ---------------------------------------------------------------- fig1_01
def fig1_01_ai_ml_dl():
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.2)
    ax.axis("off")
    ax.add_patch(Ellipse((5, 3.6), 9.6, 6.8, fc="#dbe9f6", ec=C_BLUE, lw=1.8))
    ax.add_patch(Ellipse((5, 3.3), 6.6, 4.6, fc="#bad4ee", ec=C_BLUE, lw=1.6))
    ax.add_patch(Ellipse((5, 3.0), 3.6, 2.4, fc="#f6d9c0", ec=C_ORANGE, lw=1.6))
    ax.text(5, 6.55, "人工智能（AI）", ha="center", va="center", fontsize=13, fontweight="bold", color=C_BLUE)
    ax.text(5, 5.1, "机器学习（ML）", ha="center", va="center", fontsize=12, fontweight="bold", color="#1a5c96")
    ax.text(5, 3.0, "深度学习\n（DL）", ha="center", va="center", fontsize=11, fontweight="bold", color="#a85a12")
    ax.text(5, 0.42, "机器学习是实现人工智能的主流途径，深度学习是机器学习的一个分支",
            ha="center", va="center", fontsize=9.5, color=C_GRAY)
    _save(fig, "fig1_01_ai_ml_dl.png")


# ---------------------------------------------------------------- fig1_02
def fig1_02_four_functions():
    """四大功能的“横切竖切”直觉：对二维表格做行/列的不同切割"""
    fig, axes = plt.subplots(2, 2, figsize=(9.6, 7.2))
    for ax in axes.flat:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.axis("off")

    def cell(ax, x, y, w, h, s, fc="white", ec=C_GRAY, fs=8.5):
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.0))
        ax.text(x + w / 2, y + h / 2, s, ha="center", va="center", fontsize=fs)

    xs = [1.0, 2.6, 4.2, 5.8, 7.4]
    ys = [6.3, 5.2, 4.1, 3.0, 1.9]
    head = ["$X_1$", "$X_2$", "$X_3$", "$X_4$", "$Y$"]
    labels = [["0.2", "1.6", "31", "105", "1"], ["0.5", "3.6", "28", "96", "1"],
              ["0.9", "4.8", "22", "75", "0"], ["1.0", "5.9", "18", "60", "0"],
              ["0.7", "4.1", "20", "70", "0"]]

    def draw_table(ax, row_colors=None, col_colors=None):
        for j, x in enumerate(xs):
            cell(ax, x, 7.2, 1.6, 0.7, head[j], fc="#e8edf3", fs=9)
        for i, y in enumerate(ys):
            for j, x in enumerate(xs):
                fc = "white"
                if row_colors is not None and row_colors[i] is not None:
                    fc = row_colors[i]
                if col_colors is not None and col_colors[j] is not None:
                    fc = col_colors[j]
                cell(ax, x, y, 1.6, 0.9, labels[i][j], fc=fc)

    # (a) 聚类：横着切行
    ax = axes[0, 0]
    rc = ["#cfe3f5", "#cfe3f5", "#fde2c8", "#fde2c8", "#d9ecd3"]
    draw_table(ax, row_colors=rc)
    ax.set_title("(a) 聚类：横着切（按行分组）\n只有 X，把相近的数据点（行）分成簇", fontsize=10)
    ax.plot([0.7, 9.3], [6.15, 6.15], color=C_RED, lw=2.2, ls="--")
    ax.plot([0.7, 9.3], [2.85, 2.85], color=C_RED, lw=2.2, ls="--")

    # (b) 降维：竖着切列（相关性高的 X 合并）
    ax = axes[0, 1]
    cc = [None, "#cfe3f5", "#cfe3f5", None, "#f2f2f2"]
    draw_table(ax, col_colors=cc)
    ax.set_title("(b) 降维：竖着切（按列合并）\n只有 X，把相关的属性（列）合并成少数几个", fontsize=10)
    ax.annotate("", xy=(2.7, 8.4), xytext=(5.6, 8.4),
                arrowprops=dict(arrowstyle="<->", lw=2.5, color=C_RED))

    # (c) 特征选取：看着 Y 挑 X
    ax = axes[1, 0]
    cc = [None, "#f2f2f2", "#f2f2f2", None, "#fde2c8"]
    draw_table(ax, col_colors=cc)
    ax.set_title("(c) 特征选取：看着 Y 竖着挑\n有 X 和 Y，把与 Y 无关或重复的 X 删去", fontsize=10)
    ax.annotate("", xy=(9.4, 7.55), xytext=(9.4, 1.9),
                arrowprops=dict(arrowstyle="-", lw=2.5, color=C_RED))
    ax.text(9.75, 4.7, "Y", ha="center", va="center", fontsize=11, color=C_RED, fontweight="bold")

    # (d) 分类/回归：用 X 预测 Y
    ax = axes[1, 1]
    draw_table(ax)
    ax.set_title("(d) 分类/回归：由 X 预测 Y\nY 为类别→分类；Y 为实数→回归", fontsize=10)
    for i, y in enumerate(ys):
        ax.annotate("", xy=(8.05, y + 0.45), xytext=(7.25, y + 0.45),
                    arrowprops=dict(arrowstyle="-|>", lw=1.4, color=C_RED, mutation_scale=11))

    fig.suptitle("对同一张二维表格做不同的“切割”，就得到机器学习的四大功能", fontsize=12, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _save(fig, "fig1_02_four_functions.png")


# ---------------------------------------------------------------- fig1_03
def fig1_03_table_data():
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    cols = ["站点", "$X_1$ 云量", "$X_2$ 温度", "$X_3$ 风速", "$Y$ 雨量"]
    data = [["G1", "1.4", "21", "123", "11.2"],
            ["G2", "2.1", "22", "546", "22.4"],
            ["G3", "9.1", "33", "432", "144.6"],
            ["G4", "4.6", "24", "231", "66.3"],
            ["…", "…", "…", "…", "…"],
            ["G9", "8.3", "16", "367", "120.2"]]
    xs = [1.2, 3.0, 4.8, 6.6, 8.4]
    w, h = 1.7, 0.75
    ys = [5.0, 4.15, 3.3, 2.45, 1.6, 0.75]
    for j, x in enumerate(xs):
        fc = "#e8edf3" if j < 4 else "#fde2c8"
        ax.add_patch(Rectangle((x, 5.85), w, h, fc=fc, ec=C_GRAY, lw=1.0))
        ax.text(x + w / 2, 6.22, cols[j], ha="center", va="center", fontsize=9.5)
    for i, y in enumerate(ys):
        for j, x in enumerate(xs):
            fc = "white" if j < 4 else "#fff4ea"
            ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=C_GRAY, lw=1.0))
            ax.text(x + w / 2, y + h / 2, data[i][j], ha="center", va="center", fontsize=9.5)
    # 行标注
    ax.annotate("", xy=(0.95, 5.85), xytext=(0.95, 0.75),
                arrowprops=dict(arrowstyle="<->", lw=1.6, color=C_BLUE))
    ax.text(0.55, 3.3, "行：数据对象、样本、实例、数据点", rotation=90, ha="center", va="center",
            fontsize=10, color=C_BLUE)
    # X 列标注
    ax.annotate("", xy=(3.0, 6.85), xytext=(8.25, 6.85),
                arrowprops=dict(arrowstyle="<->", lw=1.6, color=C_GREEN))
    ax.text(5.6, 7.15, "列：数据属性、变量、特征（X：容易获得）", ha="center", va="bottom", fontsize=10, color=C_GREEN)
    # Y 列标注（表格右侧竖排）
    ax.annotate("", xy=(10.35, 6.6), xytext=(10.35, 0.75),
                arrowprops=dict(arrowstyle="<->", lw=1.6, color=C_ORANGE))
    ax.text(10.9, 3.7, "标签（Y：难获得但想要）", rotation=90, ha="center", va="center", fontsize=10, color=C_ORANGE)
    ax.text(6.0, 0.18, "二维表格（关系数据库）：每行一个样本，每列一个属性；X 与 Y 一起进入数据集",
            ha="center", fontsize=10, color=C_GRAY)
    ax.set_ylim(-0.2, 7.9)
    ax.set_xlim(-0.2, 11.8)
    _save(fig, "fig1_03_table_data.png")


# ---------------------------------------------------------------- fig1_04
def fig1_04_uncertainty():
    fig, axes = plt.subplots(2, 2, figsize=(9.6, 6.4))
    for ax in axes.flat:
        ax.set_ylim(-1.5, 2.2)
        ax.set_yticks([])
        ax.spines[["left", "right", "top"]].set_visible(False)
        ax.axhline(0, color="black", lw=1.0)
        ax.set_xticks([])

    ax = axes[0, 0]
    ax.set_xlim(0, 40)
    ax.plot([25], [0], "o", ms=10, color=C_BLUE)
    ax.annotate("25", (25, 0), xytext=(25, 0.55), ha="center", fontsize=11, color=C_BLUE)
    ax.set_title("(a) 确定数：一个明确的数值", fontsize=11)

    ax = axes[0, 1]
    ax.set_xlim(0, 40)
    ax.plot([20, 35], [0, 0], lw=6, color=C_ORANGE, solid_capstyle="butt")
    ax.annotate("20", (20, 0), xytext=(20, 0.55), ha="center", fontsize=11)
    ax.annotate("35", (35, 0), xytext=(35, 0.55), ha="center", fontsize=11)
    ax.set_title("(b) 区间数：只知道下限与上限\n（如明天气温 20~35 $^\\circ$C）", fontsize=11)

    ax = axes[1, 0]
    ax.set_xlim(0, 24)
    x1 = np.array([5, 9, 15, 19])
    y1 = np.array([0, 1, 1, 0])
    ax.plot(x1, y1, lw=2, color=C_GREEN)
    ax.fill_between(x1, 0, y1, color=C_GREEN, alpha=0.15)
    ax.annotate("7", (7, 0), xytext=(7, -0.62), ha="center", fontsize=10)
    ax.annotate("10", (10, 0), xytext=(10, 1.28), ha="center", fontsize=10)
    ax.annotate("15", (15, 0), xytext=(15, 1.28), ha="center", fontsize=10)
    ax.annotate("17", (17, 0), xytext=(17, -0.62), ha="center", fontsize=10)
    ax.set_title("(c) 模糊数：核 [10,15] 隶属度为 1，\n两翼隶属度逐渐下降", fontsize=11)
    ax.text(12, -1.25, "隶属度", ha="center", fontsize=9, color=C_GRAY)

    ax = axes[1, 1]
    ax.set_xlim(0, 44)
    ax.plot([15, 20], [0.0, 0.0], lw=6, color=C_PURPLE, solid_capstyle="butt")
    ax.plot([30, 35], [0.9, 0.9], lw=6, color=C_PURPLE, solid_capstyle="butt")
    ax.plot([15, 30], [0.0, 0.9], lw=1.2, ls=":", color=C_PURPLE)
    ax.plot([20, 35], [0.0, 0.9], lw=1.2, ls=":", color=C_PURPLE)
    ax.annotate("最低温 [15,20]", (17.5, 0), xytext=(17.5, -0.75), ha="center", fontsize=10)
    ax.annotate("最高温 [30,35]", (32.5, 0.9), xytext=(32.5, 1.55), ha="center", fontsize=10)
    ax.set_title("(d) 粗糙数：每个端点又各有一个区间\n（下限与上限都不确定）", fontsize=11)

    fig.suptitle("数据属性的不确定性：同一物理量可以用不同“数”来表达（随机变量见正文）", fontsize=12, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _save(fig, "fig1_04_uncertainty.png")


# ---------------------------------------------------------------- fig1_05
def fig1_05_kdd_process():
    fig, ax = plt.subplots(figsize=(10.5, 2.9))
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    steps = ["数据筛选", "数据预处理", "数据变换", "数据挖掘 /\n机器学习", "解释与评价"]
    xs = [0.4, 4.4, 8.4, 12.4, 16.4]
    for x, s in zip(xs, steps):
        _box(ax, x, 1.3, 3.4, 1.6, s, fs=11, bold=(s.startswith("数据挖掘")))
    for a, b in zip(xs[:-1], xs[1:]):
        _arrow(ax, a + 3.4, 2.1, b, 2.1, lw=2.0)
    _box(ax, 16.4, 3.1, 3.4, 0.9, "知识", fc="#fde2c8", ec=C_ORANGE, fs=11, bold=True)
    _arrow(ax, 18.1, 2.9, 18.1, 2.4, color=C_ORANGE, lw=2.0)
    _arrow(ax, 18.1, 0.5, 2.1, 0.5, color=C_RED, lw=1.6, ls="--", rad=0.06)
    _arrow(ax, 2.1, 0.5, 2.1, 1.3, color=C_RED, lw=1.6, ls="--")
    ax.text(10.0, 0.05, "解释与评价不通过：回到前面的步骤重新调整（虚线反馈）", ha="center", fontsize=9.5, color=C_RED)
    ax.set_ylim(-0.4, 4.4)
    _save(fig, "fig1_05_kdd_process.png")


# ---------------------------------------------------------------- fig1_06
def fig1_06_geo_methods():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.6))
    for ax in axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis("off")

    ax = axes[0]
    ax.set_title("传统地理学方法", fontsize=12, color=C_BLUE, fontweight="bold")
    steps = ["实地考察、收集资料", "根据已有概念体系条理化", "比较、归纳、概括", "地理解释", "建立理论与法则"]
    y = 8.4
    for i, s in enumerate(steps):
        _box(ax, 1.2, y, 7.6, 1.15, s, fs=10.5)
        if i < len(steps) - 1:
            _arrow(ax, 5.0, y, 5.0, y - 0.5, lw=1.8)
        y -= 1.65

    ax = axes[1]
    ax.set_title("现代地理学方法（四个步骤）", fontsize=12, color=C_ORANGE, fontweight="bold")
    steps = ["观察实践，发现先期模式", "资料筛选", "构造假设", "建立模型", "验证模型"]
    y = 8.4
    ys_box = []
    for i, s in enumerate(steps):
        _box(ax, 0.8, y, 7.2, 1.15, s, fc="#fff4ea", ec=C_ORANGE, fs=10.5)
        if i < len(steps) - 1:
            _arrow(ax, 4.4, y, 4.4, y - 0.5, lw=1.8, color=C_ORANGE)
        ys_box.append(y)
        y -= 1.65
    # 不成立：从“验证模型”右侧出发，绕到“构造假设”右侧（明确的三段折线）
    yv = ys_box[-1] + 0.575
    yh = ys_box[2] + 0.575
    xr = 9.3
    ax.plot([8.0, xr], [yv, yv], color=C_RED, lw=1.8)
    ax.plot([xr, xr], [yv, yh], color=C_RED, lw=1.8)
    _arrow(ax, xr, yh, 8.0, yh, color=C_RED, lw=1.8)
    ax.text(9.75, (yv + yh) / 2, "不\n成\n立", ha="center", va="center", fontsize=10, color=C_RED)
    # 成立：向下进入“发展理论与法则”
    _arrow(ax, 4.4, ys_box[-1], 4.4, ys_box[-1] - 0.5, lw=1.8, color=C_ORANGE)
    ax.text(5.0, ys_box[-1] - 0.28, "成立", ha="left", va="center", fontsize=9.5, color=C_GREEN)
    _box(ax, 0.8, ys_box[-1] - 1.75, 7.2, 1.15, "发展理论与法则", fc="#d9ecd3", ec=C_GREEN, fs=10.5, bold=True)
    ax.set_xlim(0, 10.6)
    ax.set_ylim(-0.3, 10)
    fig.suptitle("无论传统还是现代方法，每个步骤都离不开地理数据的收集、处理与分析", fontsize=11.5, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    _save(fig, "fig1_06_geo_methods.png")


# ---------------------------------------------------------------- fig1_07
def fig1_07_time_order():
    fig, ax = plt.subplots(figsize=(10.6, 3.6))
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 6)
    ax.axis("off")
    steps = [("了解问题", "研究什么、\n假设是什么"),
             ("数据", "有无 Y、\n无监督/有监督"),
             ("选择模型", "浅层/深层、\n候选方法"),
             ("构建模型", "结构、参数、\n功能"),
             ("后模型分析", "性能达标？\n机理分析")]
    xs = [0.3, 4.35, 8.4, 12.45, 16.5]
    for (name, sub), x in zip(steps, xs):
        _box(ax, x, 3.2, 3.85, 1.5, name, fs=11.5, bold=True)
        _box(ax, x, 0.9, 3.85, 1.6, sub, fc="white", ec=C_GRAY, fs=9.5, lw=1.0)
        _arrow(ax, x + 1.925, 2.5, x + 1.925, 3.2, lw=1.4)
    for a, b in zip(xs[:-1], xs[1:]):
        _arrow(ax, a + 3.85, 3.95, b, 3.95, lw=2.0)
    ax.annotate("", xy=(8.4, 5.55), xytext=(18.4, 5.55),
                arrowprops=dict(arrowstyle="-|>", lw=1.8, color=C_RED, connectionstyle="arc3,rad=0.12"))
    ax.text(13.4, 5.9, "不理想：回到数据与假设重新迭代", ha="center", fontsize=9.5, color=C_RED)
    _save(fig, "fig1_07_time_order.png")


# ---------------------------------------------------------------- fig1_08
def fig1_08_data_split():
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9.8)
    ax.axis("off")
    cols = ["$X_1$ 云量", "$X_2$ 温度", "$X_3$ 风速", "$Y$ 雨量"]
    x0, w, h, gap = 1.5, 1.9, 0.62, 0.72
    xs = [x0 + j * w for j in range(4)]
    ytop = 8.6

    def draw_row(vals, fc, y):
        for j, x in enumerate(xs):
            cfc = fc if j < 3 else "#ffffff"
            ax.add_patch(Rectangle((x, y), w, h, fc=cfc, ec=C_GRAY, lw=1.0))
            ax.text(x + w / 2, y + h / 2, vals[j], ha="center", va="center", fontsize=8.5)

    bands = [
        ("训练集\n60%~80%", "#cfe3f5", C_BLUE,
         [["1.4", "21", "123", "11.2"], ["2.1", "22", "546", "22.4"], ["9.1", "33", "432", "144.6"],
          ["4.6", "24", "231", "66.3"], ["…", "…", "…", "…"], ["…", "…", "…", "…"]]),
        ("验证集\n15%~20%", "#d9ecd3", C_GREEN,
         [["5.7", "25", "224", "99.1"], ["…", "…", "…", "…"]]),
        ("测试集\n15%~20%", "#fde2c8", C_ORANGE,
         [["8.3", "16", "367", "120.2"], ["…", "…", "…", "…"]]),
        ("未知集\n（新数据）", "#f2f2f2", C_GRAY,
         [["6.7", "35", "424", "？"]]),
    ]
    y = ytop
    # 表头
    for j, x in enumerate(xs):
        fc = "#e8edf3" if j < 3 else "#fde2c8"
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=C_GRAY, lw=1.0))
        ax.text(x + w / 2, y + h / 2, cols[j], ha="center", va="center", fontsize=9.5)
    y -= gap
    for name, fc, ec, rows in bands:
        y1 = y
        for vals in rows:
            draw_row(vals, fc, y)
            y -= h
        y2 = y + h
        cy = (y1 + y2) / 2
        ax.text(0.95, cy, name, ha="center", va="center", fontsize=9.5, color=ec, fontweight="bold", linespacing=1.5)
        ax.annotate("", xy=(1.28, y2), xytext=(1.28, y1), arrowprops=dict(arrowstyle="<->", lw=1.5, color=ec))
        y -= 0.30
    ax.text(6.2, 9.5, "行方向划分：X 与 Y 成对进入同一个子集；未知集只有 X，Y 待预测",
            ha="center", fontsize=10, color=C_RED)
    _save(fig, "fig1_08_data_split.png")


# ---------------------------------------------------------------- fig1_09
def fig1_09_split_methods():
    fig, axes = plt.subplots(2, 2, figsize=(9.8, 6.2))
    for ax in axes.flat:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6.4)
        ax.axis("off")

    ax = axes[0, 0]
    ax.set_title("(a) 留出法：直接划分两个互斥集合\n训练/测试样本比通常 2:1~4:1", fontsize=10.5)
    ax.add_patch(Rectangle((0.8, 2.2), 5.4, 2.4, fc="#cfe3f5", ec=C_BLUE, lw=1.5))
    ax.add_patch(Rectangle((6.4, 2.2), 2.8, 2.4, fc="#fde2c8", ec=C_ORANGE, lw=1.5))
    ax.text(3.5, 3.4, "训练集", ha="center", va="center", fontsize=11, color=C_BLUE)
    ax.text(7.8, 3.4, "测试集", ha="center", va="center", fontsize=11, color=C_ORANGE)
    ax.text(5.0, 0.9, "适合大数据集；多次随机划分\n重复实验取平均", ha="center", fontsize=9, color=C_GRAY)

    ax = axes[0, 1]
    ax.set_title("(b) k 折交叉验证：k 个大小相似的子集\n轮流做测试集（图中 k=5）", fontsize=10.5)
    for i in range(5):
        fc = "#fde2c8" if i == 2 else "#cfe3f5"
        ec = C_ORANGE if i == 2 else C_BLUE
        ax.add_patch(Rectangle((0.7 + i * 1.75, 2.2), 1.6, 2.4, fc=fc, ec=ec, lw=1.5))
        ax.text(1.5 + i * 1.75, 3.4, f"{i + 1}", ha="center", va="center", fontsize=11)
    ax.text(5.0, 5.45, "第 3 折做测试，其余 4 折合并训练", ha="center", fontsize=9, color=C_GRAY)
    ax.text(5.0, 0.9, "返回 k 个结果的均值；常取 k=10，\n适合中等或小数据集", ha="center", fontsize=9, color=C_GRAY)

    ax = axes[1, 0]
    ax.set_title("(c) 留一法：k = 样本数 m\n每次只留 1 个样本做测试", fontsize=10.5)
    for i in range(10):
        fc = "#fde2c8" if i == 6 else "#cfe3f5"
        ec = C_ORANGE if i == 6 else C_BLUE
        ax.add_patch(Rectangle((0.7 + i * 0.88, 2.2), 0.76, 2.4, fc=fc, ec=ec, lw=1.2))
    ax.text(5.0, 0.9, "不受随机划分影响、结果较准，\n适合小数据集，但计算量大", ha="center", fontsize=9, color=C_GRAY)

    ax = axes[1, 1]
    ax.set_title("(d) 自助法：有放回抽样 m 次\n未被抽到的样本作验证（包外估计）", fontsize=10.5)
    pts = rng.uniform(1.0, 9.0, size=(24, 2)) * [1.0, 2.2] + [0, 1.2]
    picked = rng.integers(0, 24, size=24)
    oo = set(range(24)) - set(picked.tolist())
    for i, (px, py) in enumerate(pts):
        fc = "#cfe3f5" if i in set(picked.tolist()) else "#fde2c8"
        ec = C_BLUE if i in set(picked.tolist()) else C_ORANGE
        ax.plot(px, py, "o", ms=7, mfc=fc, mec=ec)
    ax.text(5.0, 0.6, "约 36.8% 样本从未被抽到（橙色），可作验证集", ha="center", fontsize=9, color=C_GRAY)
    fig.suptitle("数据集划分的四种方法：按数据集规模与划分难度选用", fontsize=12, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _save(fig, "fig1_09_split_methods.png")


# ---------------------------------------------------------------- fig1_10
def fig1_10_method_selection():
    fig, ax = plt.subplots(figsize=(9.8, 6.2))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 13)
    ax.axis("off")
    _box(ax, 6.5, 11.2, 7.0, 1.4, "研究的问题要实现什么功能？", fs=11.5, fc="#fde2c8", ec=C_ORANGE, bold=True)
    _box(ax, 1.0, 8.6, 8.0, 1.5, "数据只有 X（无监督学习）", fs=10.5, fc="#cfe3f5", ec=C_BLUE)
    _box(ax, 11.0, 8.6, 8.0, 1.5, "数据有 X 和 Y（有监督学习）", fs=10.5, fc="#d9ecd3", ec=C_GREEN)
    _arrow(ax, 8.5, 11.2, 5.0, 10.1, lw=1.8)
    _arrow(ax, 11.5, 11.2, 15.0, 10.1, lw=1.8)
    _box(ax, 0.2, 5.2, 3.9, 1.5, "探查分组\n→聚类\n（硬/软聚类）", fs=9.5, fc="white")
    _box(ax, 4.3, 5.2, 3.9, 1.5, "减少维度\n→降维", fs=9.5, fc="white")
    _box(ax, 9.2, 5.2, 3.9, 1.5, "Y 为类别\n→分类", fs=9.5, fc="white")
    _box(ax, 13.3, 5.2, 3.9, 1.5, "Y 为实数\n→回归", fs=9.5, fc="white")
    _arrow(ax, 3.0, 8.6, 2.1, 6.7, lw=1.5)
    _arrow(ax, 6.0, 8.6, 6.2, 6.7, lw=1.5)
    _arrow(ax, 13.0, 8.6, 11.1, 6.7, lw=1.5)
    _arrow(ax, 16.0, 8.6, 15.2, 6.7, lw=1.5)
    _box(ax, 3.0, 2.4, 14.0, 1.5, "在该功能下的若干候选方法中挑选：\n文献怎么选、自己熟悉哪些、数据规模与模型结构是否匹配", fs=10, fc="#fff4ea", ec=C_ORANGE)
    for xc in (2.1, 6.2, 11.1, 15.2):
        _arrow(ax, xc, 5.2, 10.0, 3.9, lw=1.2)
    _box(ax, 3.0, 0.2, 14.0, 1.3, "动手试 1~3 种方法，比较验证集性能后确定", fs=10.5, fc="#d9ecd3", ec=C_GREEN, bold=True)
    _arrow(ax, 10.0, 2.4, 10.0, 1.5, lw=1.8)
    _save(fig, "fig1_10_method_selection.png")


# ---------------------------------------------------------------- fig1_11
def fig1_11_modeling_steps():
    fig, ax = plt.subplots(figsize=(11.2, 4.3))
    ax.set_xlim(0, 23)
    ax.set_ylim(0, 8.2)
    ax.axis("off")
    steps = [("数据预处理", "特征选取/降维\n数据标准化"),
             ("数据分割", "留出法/交叉验证/\n留一法/自助法"),
             ("初始化模型", "确定模型结构\n（层数、函数等）"),
             ("训练模型", "选择率定算法\n求解最优参数"),
             ("预测", "训练集预测\n验证集预测"),
             ("性能评估", "分类：错误率、精度\n回归：r、MSE、RMSE\n假设检验"),
             ("数据后处理", "预测值变换回\n原始数量级")]
    xs = [0.25, 3.45, 6.65, 9.85, 13.05, 16.25, 19.85]
    ws = [2.9, 2.9, 2.9, 2.9, 2.9, 3.2, 2.9]
    for (name, sub), x, w in zip(steps, xs, ws):
        _box(ax, x, 4.6, w, 1.4, name, fs=10.5, bold=True)
        _box(ax, x, 1.9, w, 2.0, sub, fc="white", ec=C_GRAY, fs=8.5, lw=1.0)
        _arrow(ax, x + w / 2, 3.9, x + w / 2, 4.6, lw=1.3)
    for i in range(len(steps) - 1):
        _arrow(ax, xs[i] + ws[i], 5.3, xs[i + 1], 5.3, lw=1.8)
    # 验证不理想：从“性能评估”回到“训练模型”（底部三段折线）
    yl = 0.95
    ax.plot([17.85, 17.85], [1.9, yl], color=C_RED, lw=1.6, ls="--")
    ax.plot([17.85, 11.3], [yl, yl], color=C_RED, lw=1.6, ls="--")
    _arrow(ax, 11.3, yl, 11.3, 1.9, color=C_RED, lw=1.6, ls="--")
    ax.text(14.6, 0.55, "验证不理想：调整模型结构或参数，重新训练", ha="center", fontsize=8.5, color=C_RED)
    ax.set_ylim(0, 8.2)
    fig.tight_layout()
    _save(fig, "fig1_11_modeling_steps.png")


# ---------------------------------------------------------------- fig1_12
def fig1_12_evaluation():
    rng = np.random.default_rng(7)
    n = 80
    t = np.arange(n)
    obs = 20 + 10 * np.sin(2 * np.pi * t / 24) + rng.normal(0, 1.5, n)
    pred = obs + rng.normal(0, 2.5, n) + 0.15 * np.sin(2 * np.pi * t / 12)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    ax = axes[0]
    ax.plot(t, obs, color=C_BLUE, lw=1.6, label="观测值")
    ax.plot(t, pred, color=C_ORANGE, lw=1.4, ls="--", label="预测值")
    ax.set_xlabel("时间（小时）")
    ax.set_ylabel("雨量（mm）")
    ax.set_title("(a) 时间序列对比：两条曲线是否吻合", fontsize=11)
    ax.legend(fontsize=9, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)

    ax = axes[1]
    ax.plot([0, 45], [0, 45], color=C_GRAY, lw=1.2, ls="--", label="1:1 参考线")
    ax.scatter(obs, pred, s=22, color=C_BLUE, alpha=0.7, label="样本点", edgecolors="none")
    ax.set_xlabel("观测值（mm）")
    ax.set_ylabel("预测值（mm）")
    ax.set_xlim(0, 45)
    ax.set_ylim(0, 45)
    ax.set_title("(b) 观测—预测散点：是否落在\n45$^\\circ$ 对角线附近", fontsize=11)
    ax.legend(fontsize=9, frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    _save(fig, "fig1_12_evaluation.png")


# ---------------------------------------------------------------- fig1_13
def fig1_13_geo_apps():
    apps = [("暴雨/降水预报", "冷暖气团、锋面、季风、\n副热带高压、气旋、台风等", "回归（降雨量为实数）"),
            ("径流/洪水预报", "降水、蒸发；大气环流、\n太阳活动、海气相互作用", "回归；洪峰日期为分类"),
            ("河冰/凌汛预报", "天气情况、水流\n和河冰情势", "回归或分类\n（开河日期、文开/武开）"),
            ("空气质量预报", "前期污染物浓度；风速、\n风向、降雨、气温等", "回归或分类\n（PM$_{2.5}$、AQI 等）"),
            ("土壤水分遥感反演", "土壤/植被/气象特征；光学、\n热红外、微波波谱特征", "回归（不同时空分辨率）"),
            ("植被遥感分类", "植被指数、多时相、多源\n数据、纹理与地形信息", "分类（是否植被/类型）")]
    fig, ax = plt.subplots(figsize=(11.2, 7.4))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.axis("off")
    for i, (name, inp, model) in enumerate(apps):
        col, row = i % 2, i // 2
        x0 = 0.4 + col * 10.0
        y0 = 10.6 - row * 3.7
        _box(ax, x0, y0, 9.2, 3.1, "", fc="white", ec=C_GRAY, lw=1.2)
        ax.text(x0 + 0.55, y0 + 2.45, f"{name}", fontsize=11, fontweight="bold", color="#1a5c96", va="center", ha="left")
        ax.text(x0 + 0.55, y0 + 1.05, f"输入：{inp}", fontsize=8.8, va="center", ha="left", linespacing=1.5)
        ax.text(x0 + 0.55, y0 + 0.42, f"模型/输出：{model}", fontsize=8.8, va="center", ha="left", color=C_ORANGE, linespacing=1.5)
    fig.suptitle("地学中的典型预测问题：输入—模型—输出", fontsize=12.5, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    _save(fig, "fig1_13_geo_apps.png")


# ---------------------------------------------------------------- fig1_14
def fig1_14_course_map():
    fig, ax = plt.subplots(figsize=(10.6, 6.4))
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 13)
    ax.axis("off")
    _box(ax, 7.5, 11.0, 6.0, 1.6, "地学问题", fs=13, fc="#fde2c8", ec=C_ORANGE, bold=True)
    domains = ["水文/水资源", "气象/气候", "土地/土壤", "植被/生态/环境", "社会/城市/资源/灾害"]
    xw = 3.8
    for i, d in enumerate(domains):
        _box(ax, 0.6 + i * 4.0, 8.6, xw, 1.2, d, fs=9.5, fc="white")
        _arrow(ax, 2.5 + i * 4.0, 9.8, 10.5, 11.0, lw=1.4)
    _box(ax, 8.0, 5.8, 5.0, 1.5, "机器学习", fs=13, fc="#cfe3f5", ec=C_BLUE, bold=True)
    _arrow(ax, 10.5, 8.6, 10.5, 7.3, lw=2.0)
    parts = [("定义/分类", 1.2), ("典型方法", 6.1), ("结构、特点、评估", 11.4)]
    for name, x in parts:
        _box(ax, x, 3.2, 5.2, 1.3, name, fs=10.5, fc="white", ec=C_BLUE)
        _arrow(ax, x + 2.6, 4.5, 10.5, 5.8, lw=1.2)
    _box(ax, 1.2, 0.6, 18.6, 1.5, "数据挖掘 + 应用研究：把方法用到具体地学问题，揭示规律与机理",
         fs=11.5, fc="#d9ecd3", ec=C_GREEN, bold=True)
    _arrow(ax, 3.8, 3.2, 3.8, 2.1, lw=1.4)
    _arrow(ax, 17.0, 3.2, 17.0, 2.1, lw=1.4)
    _save(fig, "fig1_14_course_map.png")


if __name__ == "__main__":
    for fn in [fig1_01_ai_ml_dl, fig1_02_four_functions, fig1_03_table_data,
               fig1_04_uncertainty, fig1_05_kdd_process, fig1_06_geo_methods,
               fig1_07_time_order, fig1_08_data_split, fig1_09_split_methods,
               fig1_10_method_selection, fig1_11_modeling_steps, fig1_12_evaluation,
               fig1_13_geo_apps, fig1_14_course_map]:
        fn()
    print("ALL DONE")
