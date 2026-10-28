# -*- coding: utf-8 -*-
"""第24章 地学应用四：地球系统篇 插图生成脚本"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (Rectangle, Circle, Ellipse, Polygon,
                                FancyArrowPatch, FancyBboxPatch)

OUT = r"C:\20260905\项目 人工智能与地理数据挖掘\书稿\figs\ch24"
os.makedirs(OUT, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["savefig.bbox"] = "tight"

rng = np.random.default_rng(42)

C_BLUE = "#1f77b4"; C_ORANGE = "#ff7f0e"; C_GREEN = "#2ca02c"
C_RED = "#d62728"; C_PURPLE = "#9467bd"; C_GRAY = "#7f7f7f"
C_LBLUE = "#aec7e8"; C_LORANGE = "#ffbb78"; C_LGREEN = "#98df8a"
C_LRED = "#ff9896"; C_LPURPLE = "#c5b0d5"; C_LYELLOW = "#fff2cc"
BG_PANEL = "#f7f7f7"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight")
    plt.close(fig)
    print("saved:", name)


def new_ax(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def rbox(ax, x, y, w, h, fc, ec, lw=1.2, ls="-", zorder=2, pad=0.04, rs=0.06):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad={pad},rounding_size={rs}",
                       facecolor=fc, edgecolor=ec, linewidth=lw,
                       linestyle=ls, zorder=zorder)
    ax.add_patch(p)
    return p


def box(ax, x, y, w, h, fc, ec, lw=1.0, ls="-", zorder=2, alpha=1.0):
    r = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw,
                  linestyle=ls, zorder=zorder, alpha=alpha)
    ax.add_patch(r)
    return r


def tx(ax, x, y, s, fs=10, color="black", ha="center", va="center",
       weight="normal", zorder=6, style="normal", lh=1.35):
    ax.text(x, y, s, fontsize=fs, color=color, ha=ha, va=va,
            fontweight=weight, zorder=zorder, style=style, linespacing=lh)


def arrow(ax, x1, y1, x2, y2, color=C_GRAY, lw=1.4, zorder=4, style="-|>",
          shrinkA=2, shrinkB=2, rad=0.0, ls="-", ms=12):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, color=color,
                        linewidth=lw, mutation_scale=ms, zorder=zorder,
                        shrinkA=shrinkA, shrinkB=shrinkB, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a)
    return a


def circled(ax, x, y, n, r=0.24, fc=C_ORANGE, fs=11):
    c = Circle((x, y), r, facecolor=fc, edgecolor="none", zorder=7)
    ax.add_patch(c)
    tx(ax, x, y, str(n), fs=fs, color="white", weight="bold", zorder=8)


def mini_grid(ax, x, y, cell, nr, nc, fc="#dce9f5", ec=C_GRAY, lw=0.5, z=3):
    for i in range(nr):
        for j in range(nc):
            box(ax, x + j * cell, y + (nr - 1 - i) * cell, cell, cell,
                fc, ec=ec, lw=lw, zorder=z)


# ======================================================================
# fig24_01 地学大数据特点：4V 与从叶片到全球的多尺度
# ======================================================================
def fig24_01():
    fig, ax = new_ax(10.5, 6.6, (0, 12), (0, 7))

    # 顶部：数据来源
    srcs = [("遥感数据", 0.9), ("实地观测", 4.75), ("实地观察", 8.6)]
    for name, x0 in srcs:
        rbox(ax, x0, 6.05, 2.5, 0.8, C_LBLUE, C_BLUE, lw=1.2)
        tx(ax, x0 + 1.25, 6.45, name, fs=11, weight="bold")
        arrow(ax, x0 + 1.25, 6.0, x0 + 1.25, 5.55, color=C_GRAY)

    rbox(ax, 0.9, 4.7, 10.2, 0.8, C_LYELLOW, C_ORANGE, lw=1.2)
    tx(ax, 6.0, 5.1, "地球系统数据激增：存储量已远远超过几十 PB，传输速率迅速增加",
       fs=11, weight="bold")

    # 左下：4V
    rbox(ax, 0.5, 0.3, 5.3, 3.9, BG_PANEL, C_GRAY, lw=1.0, ls="--")
    tx(ax, 3.15, 3.85, "大数据四大特征（4V）", fs=11.5, weight="bold")
    vs = [("Volume 体积", "海量规模（遥感、观测数据激增）", C_BLUE),
          ("Velocity 速度", "获取与传输速率迅速增加", C_GREEN),
          ("Variety 多样性", "数据源丰富，多元、多类型", C_ORANGE),
          ("Veracity 准确性", "数据质量与可信度参差", C_RED)]
    pos = [(0.85, 2.0), (3.35, 2.0), (0.85, 0.55), (3.35, 0.55)]
    for (name, desc, c), (x0, y0) in zip(vs, pos):
        rbox(ax, x0, y0, 2.25, 1.2, "white", c, lw=1.2)
        tx(ax, x0 + 1.125, y0 + 0.86, name, fs=9.5, weight="bold", color=c)
        tx(ax, x0 + 1.125, y0 + 0.36, desc, fs=7.8, color="#444444")

    # 右下：多尺度
    rbox(ax, 6.2, 0.3, 5.3, 3.9, BG_PANEL, C_GRAY, lw=1.0, ls="--")
    tx(ax, 8.85, 3.85, "数据源：从器官层次到全球层次", fs=11.5, weight="bold")
    tx(ax, 8.85, 3.38, "一维到四维、空间集成、多元多尺度", fs=8.5, color="#555555")

    # 叶片
    leaf = Ellipse((7.15, 2.35), 0.85, 0.42, angle=-28,
                   facecolor=C_LGREEN, edgecolor=C_GREEN, lw=1.2, zorder=3)
    ax.add_patch(leaf)
    ax.plot([6.83, 7.5], [2.2, 2.52], color=C_GREEN, lw=0.9, zorder=4)
    tx(ax, 7.15, 1.62, "叶片\n（器官层次）", fs=8.5)
    # 样地
    box(ax, 8.05, 2.1, 0.75, 0.6, "#e8f4e8", C_GREEN, lw=1.0, zorder=3)
    ax.plot([8.13, 8.35, 8.55], [2.2, 2.5, 2.2], color=C_GREEN, lw=1.0, zorder=4)
    tx(ax, 8.43, 1.62, "样地\n（局地）", fs=8.5)
    # 区域
    mini_grid(ax, 9.25, 1.95, 0.3, 3, 3, fc="#dceefc", ec=C_BLUE)
    tx(ax, 9.7, 1.62, "区域", fs=8.5)
    # 全球
    globe = Circle((10.85, 2.4), 0.42, facecolor="#eaf3fb",
                   edgecolor=C_BLUE, lw=1.3, zorder=3)
    ax.add_patch(globe)
    ax.add_patch(Ellipse((10.85, 2.4), 0.34, 0.84, facecolor="none",
                         edgecolor=C_BLUE, lw=0.9, zorder=4))
    ax.plot([10.43, 11.27], [2.4, 2.4], color=C_BLUE, lw=0.9, zorder=4)
    tx(ax, 10.85, 1.62, "全球层次", fs=8.5)
    for x1, x2 in [(7.5, 8.0), (8.85, 9.2), (10.2, 10.4)]:
        arrow(ax, x1, 2.4, x2, 2.4, color=C_GRAY, lw=1.2)

    save(fig, "fig24_01_bigdata_features.png")


# ======================================================================
# fig24_02 关键挑战、典型问题、两大任务与解决途径
# ======================================================================
def fig24_02():
    fig, ax = new_ax(10.5, 6.8, (0, 12), (0, 7.4))

    rbox(ax, 1.0, 6.1, 10.0, 1.0, C_LRED, C_RED, lw=1.3)
    tx(ax, 6.0, 6.75, "关键的挑战", fs=11.5, weight="bold", color=C_RED)
    tx(ax, 6.0, 6.35,
       "从可能实时的、跨学科整合的大数据中提取可解释的信息和知识——这正是数据挖掘的本义",
       fs=10)

    # 典型问题
    tx(ax, 0.62, 5.05, "典\n型\n问\n题", fs=10, weight="bold", color="#555555")
    probs = [("分类 / 异常检测", 1.55), ("回归 / 状态预测", 4.75), ("动态建模", 7.95)]
    for name, x0 in probs:
        rbox(ax, x0, 4.45, 2.5, 1.0, C_LBLUE, C_BLUE, lw=1.2)
        tx(ax, x0 + 1.25, 4.95, name, fs=10.5, weight="bold", color=C_BLUE)
        arrow(ax, 6.0, 6.05, x0 + 1.25, 5.5, color=C_GRAY, rad=0.0)

    # 两大任务 → 解决方法
    tasks = [
        ("任务一：提取海量激增数据中的有用信息",
         "机器学习和人工智能的许多工具可以使用，\n但需要进一步发展，并适应地球科学分析",
         C_BLUE, 1.0),
        ("任务二：遵循物理定律，从数值模式中获取更多有效特征",
         "相比传统的同化方法获取更多有效特征，\n将机器学习与物理建模相结合",
         C_GREEN, 6.4),
    ]
    for title, desc, c, x0 in tasks:
        rbox(ax, x0, 1.55, 4.6, 2.2, "white", c, lw=1.4)
        box(ax, x0 + 0.15, 2.85, 4.3, 0.75, c, ec="none", alpha=0.12, zorder=3)
        tx(ax, x0 + 2.3, 3.22, title, fs=9.8, weight="bold", color=c)
        tx(ax, x0 + 2.3, 2.25, desc, fs=9)
        arrow(ax, x0 + 2.3, 4.4, x0 + 2.3, 3.85, color=C_GRAY)

    tx(ax, 6.0, 0.85, "两类途径相互补充：机器学习独立建模，或与物理建模深度耦合",
       fs=9.5, color="#555555")
    arrow(ax, 3.3, 1.5, 3.3, 1.15, color=C_GRAY, ls="--")
    arrow(ax, 8.7, 1.5, 8.7, 1.15, color=C_GRAY, ls="--")

    save(fig, "fig24_02_challenge_tasks_ways.png")


# ======================================================================
# fig24_03 深度学习与地球科学的相似性映射
# ======================================================================
def fig24_03():
    fig, ax = new_ax(11, 7.4, (0, 13), (0, 8.6))

    rbox(ax, 0.5, 7.75, 5.6, 0.65, C_LBLUE, C_BLUE, lw=1.2)
    tx(ax, 3.3, 8.07, "深度学习：图像、视频、语言", fs=11, weight="bold", color=C_BLUE)
    rbox(ax, 6.9, 7.75, 5.6, 0.65, C_LGREEN, C_GREEN, lw=1.2)
    tx(ax, 9.7, 8.07, "地球科学：模式、时空过程", fs=11, weight="bold", color=C_GREEN)

    rows_y = [5.65, 3.45, 1.25]      # 每行内容框的下缘
    bh = 1.85                        # 内容框高

    def row_frame(y0):
        rbox(ax, 0.5, y0, 5.6, bh, "white", "#999999", lw=1.0, ls="--")
        rbox(ax, 6.9, y0, 5.6, bh, "white", "#999999", lw=1.0, ls="--")
        arrow(ax, 6.2, y0 + bh / 2, 6.8, y0 + bh / 2, color=C_RED, lw=1.8,
              style="<|-|>", ms=14)

    # 行1：图像 vs 二维数据矩阵
    row_frame(rows_y[0])
    for k, c in enumerate([C_RED, C_GREEN, C_BLUE]):
        box(ax, 1.35 + k * 0.95, 6.35, 0.85, 0.85, c, ec="#555555",
            lw=0.8, alpha=0.65, zorder=3)
    tx(ax, 3.3, 5.98, "图像（RGB 三通道照片）", fs=9.5, weight="bold")
    for k, (c, lab) in enumerate([(C_RED, "R"), (C_GREEN, "G"), (C_BLUE, "B")]):
        x0 = 7.6 + k * 0.55
        gy = 6.05 + k * 0.12
        mini_grid(ax, x0, gy, 0.30, 3, 3,
                  fc="white", ec=c, lw=0.9)
        tx(ax, x0 + 0.05, gy + 0.90 + 0.13, lab, fs=8, color=c, weight="bold")
    tx(ax, 9.7, 5.98, "二维数据矩阵（多变量栅格层）", fs=9.5, weight="bold")

    # 行2：视频 vs 时空序列
    row_frame(rows_y[1])
    for k in range(3):
        box(ax, 1.35 + k * 1.15, 4.15, 1.0, 0.75, "#dce9f5", C_BLUE,
            lw=0.9, zorder=3)
        mini_grid(ax, 1.44 + k * 1.15, 4.24, 0.19, 2, 3, fc="white",
                  ec=C_GRAY, lw=0.5, z=4)
    arrow(ax, 1.35, 3.92, 4.75, 3.92, color=C_GRAY, lw=1.0)
    tx(ax, 4.98, 3.92, "时间", fs=8, color=C_GRAY)
    tx(ax, 3.3, 3.70, "视频：随时间演变的图像序列", fs=9.5, weight="bold")
    arrow(ax, 7.2, 3.92, 12.1, 3.92, color=C_GRAY, lw=1.0)
    tx(ax, 12.32, 3.92, "时间", fs=8, color=C_GRAY)
    for k in range(3):
        mini_grid(ax, 7.9 + k * 1.35, 4.1 + k * 0.18, 0.24, 3, 3,
                  fc="white", ec=C_GREEN, lw=0.9)
    tx(ax, 9.7, 5.0 - bh + 0.35, "", fs=8)
    tx(ax, 9.7, 3.45 + 0.16, "随时间演变的二维矩阵序列", fs=9.5, weight="bold")

    # 行3：语言/语音 vs 动态时间序列
    row_frame(rows_y[2])
    xw = np.linspace(0, 4.4, 400)
    yw = (0.35 * np.sin(2.6 * xw) * np.sin(0.7 * xw)
          + 0.06 * rng.standard_normal(xw.size))
    ax.plot(0.95 + xw, 2.45 + yw, color=C_PURPLE, lw=1.3, zorder=3)
    ax.plot([0.95, 5.35], [2.02, 2.02], color=C_GRAY, lw=0.9)
    tx(ax, 3.3, 1.62, "自然语言 / 语音信号（多分辨率特征）", fs=9.5, weight="bold")
    xt = np.linspace(0, 4.4, 500)
    yt = (0.5 * np.sin(1.7 * xt) + 0.22 * np.sin(5.1 * xt)
          + 0.3 * xt / 4.4 + 0.07 * rng.standard_normal(xt.size))
    ax.plot(7.35 + xt, 2.45 + yt, color=C_GREEN, lw=1.3, zorder=3)
    ax.plot([7.35, 11.75], [2.02, 2.02], color=C_GRAY, lw=0.9)
    tx(ax, 9.7, 1.62, "地球系统变量的动态时间序列", fs=9.5, weight="bold")

    rbox(ax, 0.5, 0.1, 12.0, 0.75, C_LYELLOW, C_ORANGE, lw=1.2)
    tx(ax, 6.5, 0.48,
       "共同的典型问题：分类、回归、异常检测、动态建模——深度学习方法可在两类问题之间迁移",
       fs=10.5, weight="bold")

    save(fig, "fig24_03_similarity_map.png")


# ======================================================================
# fig24_04 计算机视觉与地球科学的差异性
# ======================================================================
def fig24_04():
    fig, ax = new_ax(11.5, 4.9, (0, 13.4), (0, 5.2))
    panels = [(0.25, "差异一：统计特性"), (4.75, "差异二：数量级"),
              (9.25, "差异三：标签")]
    for x0, title in panels:
        rbox(ax, x0, 0.25, 3.9, 4.7, BG_PANEL, C_GRAY, lw=1.0, ls="--")
        tx(ax, x0 + 1.95, 4.6, title, fs=11, weight="bold")

    # 面板1：通道
    x0 = 0.25
    tx(ax, x0 + 1.0, 4.05, "计算机视觉", fs=9, weight="bold", color=C_BLUE)
    for k, c in enumerate([C_RED, C_GREEN, C_BLUE]):
        box(ax, x0 + 0.45 + k * 0.42, 3.0, 0.36, 0.36, c, ec="#555555",
            lw=0.7, alpha=0.7, zorder=3)
    tx(ax, x0 + 1.0, 2.62, "3 通道", fs=8.5)
    tx(ax, x0 + 2.9, 4.05, "地球科学", fs=9, weight="bold", color=C_GREEN)
    for k in range(8):
        box(ax, x0 + 2.15 + k * 0.17, 2.95 + k * 0.06, 0.62, 0.14,
            plt.cm.viridis(k / 7.0), ec=C_GRAY, lw=0.5, alpha=0.9, zorder=3)
    tx(ax, x0 + 2.9, 2.62, "数百个光谱通道（高光谱）", fs=8.5)
    tx(ax, x0 + 1.95, 1.62,
       "变量具有空间依赖与相互依赖，\n违背独立同分布假设；多传感器\n几何、时空统计特征不同；\n噪声源、缺失差距各异",
       fs=8.3)

    # 面板2：数量级
    x0 = 4.75
    tx(ax, x0 + 1.0, 4.05, "计算机视觉", fs=9, weight="bold", color=C_BLUE)
    mini_grid(ax, x0 + 0.55, 2.75, 0.22, 5, 5, fc="white", ec=C_BLUE, lw=0.7)
    tx(ax, x0 + 1.0, 2.32, "$512 \\times 512$ 像素", fs=8.5)
    tx(ax, x0 + 2.9, 4.05, "地球科学", fs=9, weight="bold", color=C_GREEN)
    mini_grid(ax, x0 + 2.1, 2.75, 0.29, 4, 6, fc="white", ec=C_GREEN, lw=0.7)
    tx(ax, x0 + 2.9, 2.32, "约 $40000 \\times 20000$ 像素", fs=8.5)
    tx(ax, x0 + 1.95, 1.55,
       "等分辨率（约 1 公里）的全球域；\n单景数据量、算力需求大几个数量级",
       fs=8.3)

    # 面板3：标签
    x0 = 9.25
    tx(ax, x0 + 1.0, 4.05, "计算机视觉", fs=9, weight="bold", color=C_BLUE)
    for k in range(24):
        xx = x0 + 0.35 + (k % 6) * 0.24 + 0.04 * (k // 6)
        yy = 3.55 - (k // 6) * 0.22
        box(ax, xx, yy, 0.15, 0.15,
            [C_RED, C_GREEN, C_BLUE][k % 3], ec="none", alpha=0.85, zorder=3)
    tx(ax, x0 + 1.0, 2.55, "ImageNet：\n大规模带标签数据集", fs=8.5)
    tx(ax, x0 + 2.9, 4.05, "地球科学", fs=9, weight="bold", color=C_GREEN)
    for k in range(24):
        xx = x0 + 2.25 + (k % 6) * 0.24 + 0.04 * (k // 6)
        yy = 3.55 - (k // 6) * 0.22
        box(ax, xx, yy, 0.15, 0.15, "#dddddd", ec="none", zorder=3)
    for k, c in enumerate([C_RED, C_GREEN, C_ORANGE]):
        box(ax, x0 + 2.32 + k * 0.35, 3.06, 0.15, 0.15, c, ec="none", zorder=4)
    tx(ax, x0 + 2.9, 2.55, "带标签训练集有限", fs=8.5)
    tx(ax, x0 + 1.95, 1.62,
       "现象复杂、难以打标签；\n气候变化使历史出现“没有先例”\n的时段，外推超出有效范围",
       fs=8.3)

    save(fig, "fig24_04_cv_geoscience_differences.png")


# ======================================================================
# fig24_05 五大挑战总览
# ======================================================================
def fig24_05():
    fig, ax = new_ax(10.5, 6.4, (0, 12), (0, 7))
    ell = Ellipse((6.0, 3.6), 3.6, 1.7, facecolor=C_LYELLOW,
                  edgecolor=C_ORANGE, lw=1.6, zorder=3)
    ax.add_patch(ell)
    tx(ax, 6.0, 3.85, "地学中成功应用深度学习", fs=11.5, weight="bold", zorder=5)
    tx(ax, 6.0, 3.35, "（DL）的五大挑战", fs=10, zorder=5)

    items = [
        (4.2, 5.5, 3.6, 1.35, "可解释性", "Interpretability",
         "提高精度重要但还不够；\n远未实现自解释模型与因果发现", C_BLUE, 0),
        (0.15, 3.0, 3.6, 1.5, "物理一致性", "Physical consistency",
         "与观测吻合仍可能物理不一致；\n学习支配物理规律，提供强理论约束", C_RED, 1),
        (8.25, 3.0, 3.6, 1.5, "复杂不确定的数据", "Complex and uncertain data",
         "复杂统计量、多输出、多噪声源；\n需兼顾局部邻近与遥相关的拓扑", C_GREEN, 2),
        (0.55, 0.25, 3.6, 1.5, "有限标签", "Limited labels",
         "少量标记 + 无标记数据；\n半监督学习、领域自适应", C_PURPLE, 3),
        (7.85, 0.25, 3.6, 1.5, "计算需求", "Computational demand",
         "地学问题计算成本高，\n面临巨大的技术挑战", C_ORANGE, 4),
    ]
    centers = []
    for x0, y0, w, h, name, en, desc, c, k in items:
        rbox(ax, x0, y0, w, h, "white", c, lw=1.4)
        box(ax, x0 + 0.12, y0 + h - 0.62, w - 0.24, 0.5, c, ec="none",
            alpha=0.12, zorder=3)
        tx(ax, x0 + w / 2, y0 + h - 0.37, name, fs=10.5, weight="bold", color=c)
        tx(ax, x0 + w / 2, y0 + h - 0.86, en, fs=7.5, style="italic",
           color="#888888")
        tx(ax, x0 + w / 2, y0 + 0.42, desc, fs=8.3)
        centers.append((x0 + w / 2, y0 + h / 2, k))
    # 从中心向外画短箭头（置于连线之下）
    for cx, cy, k in centers:
        arrow(ax, 6.0, 3.6, cx, cy, color="#aaaaaa", lw=1.1,
              shrinkA=95, shrinkB=38, zorder=2, style="-|>")

    save(fig, "fig24_05_five_challenges.png")


# ======================================================================
# fig24_06 五种耦合方式总览（圈1—圈5）
# ======================================================================
def fig24_06():
    fig, ax = new_ax(12.5, 8.0, (0, 14), (0, 8.8))
    cols = [0.3, 4.85, 9.4]
    rows = [4.55, 0.2]
    pw, ph = 4.3, 3.95

    def panel(x0, y0, title, num):
        rbox(ax, x0, y0, pw, ph, BG_PANEL, "#aaaaaa", lw=1.0, ls="--", pad=0.02)
        circled(ax, x0 + 0.52, y0 + ph - 0.4, num, r=0.24)
        tx(ax, x0 + pw / 2 + 0.2, y0 + ph - 0.4, title, fs=10.5, weight="bold")

    def phys(x0, y0, w, h):
        rbox(ax, x0, y0, w, h, C_LBLUE, C_BLUE, lw=1.3)

    def ml(x0, y0, w, h, dashed=False):
        rbox(ax, x0, y0, w, h, C_LORANGE, C_ORANGE, lw=1.3,
             ls="--" if dashed else "-")

    # ---- 圈1 ML 改进参数化 ----
    x0, y0 = cols[0], rows[0]
    panel(x0, y0, "ML 改进参数化", 1)
    phys(x0 + 0.25, y0 + 0.55, 2.35, 2.55)
    tx(ax, x0 + 1.42, y0 + 2.7, "物理模式\n（数值模式）", fs=9, weight="bold")
    rbox(ax, x0 + 0.45, y0 + 0.75, 1.95, 1.0, "white", C_BLUE, lw=1.0, ls="--")
    tx(ax, x0 + 1.42, y0 + 1.42, "参数 $p$", fs=9)
    tx(ax, x0 + 1.42, y0 + 1.02, "难以由第一性原理推导", fs=7.2, color="#555555")
    ml(x0 + 3.05, y0 + 1.5, 1.0, 1.0)
    tx(ax, x0 + 3.55, y0 + 2.0, "机器\n学习", fs=8.5)
    arrow(ax, x0 + 3.05, y0 + 1.7, x0 + 2.42, y0 + 1.35, color=C_ORANGE, lw=1.5)
    tx(ax, x0 + 3.55, y0 + 2.72, "学习参数", fs=7.5, color=C_ORANGE)

    # ---- 圈2 用 ML 取代“物理”子模型 ----
    x0, y0 = cols[1], rows[0]
    panel(x0, y0, "用 ML 取代“物理”子模型", 2)
    phys(x0 + 0.25, y0 + 0.55, 2.95, 2.55)
    tx(ax, x0 + 1.72, y0 + 2.72, "物理模式", fs=9, weight="bold")
    rbox(ax, x0 + 0.45, y0 + 1.95, 1.1, 0.6, "white", C_BLUE, lw=1.0)
    tx(ax, x0 + 1.0, y0 + 2.25, "子模型 A", fs=8)
    rbox(ax, x0 + 1.85, y0 + 1.95, 1.1, 0.6, "#e8e8e8", C_RED, lw=1.0, ls="--")
    tx(ax, x0 + 2.4, y0 + 2.25, "子模型 B", fs=8)
    tx(ax, x0 + 2.78, y0 + 2.42, "×", fs=12, color=C_RED, weight="bold")
    ml(x0 + 1.85, y0 + 0.85, 1.1, 0.75, dashed=True)
    tx(ax, x0 + 2.4, y0 + 1.22, "ML\n子模型", fs=8)
    arrow(ax, x0 + 2.4, y0 + 1.65, x0 + 2.4, y0 + 1.9, color=C_ORANGE, lw=1.5)
    tx(ax, x0 + 2.95, y0 + 1.72, "替代", fs=7.5, color=C_ORANGE)
    tx(ax, x0 + 1.1, y0 + 1.2, "混合模型：\n物理（可解释）\n+ ML（数据适应）", fs=8,
       color="#444444")

    # ---- 圈3 模型—观测不匹配分析 ----
    x0, y0 = cols[2], rows[0]
    panel(x0, y0, "模型—观测不匹配分析", 3)
    phys(x0 + 0.2, y0 + 2.5, 1.85, 0.85)
    tx(ax, x0 + 1.12, y0 + 2.92, "物理模式", fs=8.5, weight="bold")
    rbox(ax, x0 + 2.25, y0 + 2.5, 1.85, 0.85, C_LGREEN, C_GREEN, lw=1.3)
    tx(ax, x0 + 3.17, y0 + 2.92, "观测", fs=8.5, weight="bold")
    ml(x0 + 0.55, y0 + 0.85, 1.95, 1.05)
    tx(ax, x0 + 1.52, y0 + 1.55, "机器学习", fs=8.5, weight="bold")
    tx(ax, x0 + 1.52, y0 + 1.16, "识别、可视化误差模式", fs=7.2)
    arrow(ax, x0 + 0.95, y0 + 2.45, x0 + 1.3, y0 + 1.95, color=C_BLUE, lw=1.3)
    arrow(ax, x0 + 3.35, y0 + 2.45, x0 + 1.85, y0 + 1.95, color=C_GREEN, lw=1.3)
    rbox(ax, x0 + 2.85, y0 + 0.9, 1.25, 0.95, "white", C_GRAY, lw=1.0)
    tx(ax, x0 + 3.47, y0 + 1.55, "修正输出", fs=8)
    tx(ax, x0 + 3.47, y0 + 1.2, "偏差校正\n降尺度", fs=7.2, color="#555555")
    arrow(ax, x0 + 2.55, y0 + 1.38, x0 + 2.8, y0 + 1.38, color=C_ORANGE, lw=1.3)
    arrow(ax, x0 + 0.55, y0 + 1.0, x0 + 0.35, y0 + 2.45, color=C_GRAY,
          ls="--", rad=0.35, lw=1.1)
    tx(ax, x0 + 0.28, y0 + 1.75, "改进\n模式", fs=7, color=C_GRAY)

    # ---- 圈4 约束子模型 ----
    x0, y0 = cols[0], rows[1]
    panel(x0, y0, "约束子模型", 4)
    phys(x0 + 0.25, y0 + 1.45, 3.7, 1.95)
    tx(ax, x0 + 2.1, y0 + 3.08, "物理模式", fs=9, weight="bold")
    rbox(ax, x0 + 0.5, y0 + 2.0, 1.3, 0.8, "white", C_BLUE, lw=1.0)
    tx(ax, x0 + 1.15, y0 + 2.4, "子模型 A", fs=8.5)
    rbox(ax, x0 + 2.45, y0 + 2.0, 1.3, 0.8, "white", C_BLUE, lw=1.0)
    tx(ax, x0 + 3.1, y0 + 2.4, "子模型 B", fs=8.5)
    arrow(ax, x0 + 1.85, y0 + 2.4, x0 + 2.4, y0 + 2.4, color=C_GRAY, lw=1.2,
          ls="--")
    ml(x0 + 1.4, y0 + 0.3, 1.7, 0.75)
    tx(ax, x0 + 2.25, y0 + 0.67, "机器学习输出", fs=8)
    arrow(ax, x0 + 3.1, y0 + 1.05, x0 + 3.1, y0 + 1.95, color=C_ORANGE, lw=1.6)
    tx(ax, x0 + 3.62, y0 + 1.5, "直接驱动", fs=7.5, color=C_ORANGE)
    arrow(ax, x0 + 1.15, y0 + 1.95, x0 + 1.38, y0 + 0.85, color=C_GRAY,
          ls="--", rad=0.3, lw=1.1)
    tx(ax, x0 + 0.72, y0 + 1.15, "离线驱动\n（可能有偏差）", fs=6.8, color=C_GRAY)

    # ---- 圈5 替代建模或模仿 ----
    x0, y0 = cols[1], rows[1]
    panel(x0, y0, "替代建模或模仿（仿真器）", 5)
    rbox(ax, x0 + 0.2, y0 + 1.85, 0.85, 0.85, "white", C_GRAY, lw=1.0)
    tx(ax, x0 + 0.62, y0 + 2.27, "输入", fs=8)
    phys(x0 + 1.4, y0 + 2.5, 1.7, 0.95)
    tx(ax, x0 + 2.25, y0 + 3.12, "物理模式", fs=8.5, weight="bold")
    tx(ax, x0 + 2.25, y0 + 2.75, "慢、计算昂贵", fs=7, color=C_RED)
    ml(x0 + 1.4, y0 + 0.85, 1.7, 0.95)
    tx(ax, x0 + 2.25, y0 + 1.47, "ML 仿真器", fs=8.5, weight="bold")
    tx(ax, x0 + 2.25, y0 + 1.1, "快、近似替代", fs=7, color=C_ORANGE)
    rbox(ax, x0 + 3.45, y0 + 1.85, 0.85, 0.85, "white", C_GRAY, lw=1.0)
    tx(ax, x0 + 3.87, y0 + 2.27, "输出", fs=8)
    arrow(ax, x0 + 1.05, y0 + 2.27, x0 + 1.35, y0 + 2.85, color=C_GRAY, lw=1.1)
    arrow(ax, x0 + 1.05, y0 + 2.15, x0 + 1.35, y0 + 1.45, color=C_ORANGE, lw=1.6)
    arrow(ax, x0 + 3.1, y0 + 2.85, x0 + 3.4, y0 + 2.35, color=C_GRAY, lw=1.1)
    arrow(ax, x0 + 3.1, y0 + 1.45, x0 + 3.4, y0 + 2.1, color=C_ORANGE, lw=1.6)
    arrow(ax, x0 + 2.4, y0 + 2.45, x0 + 2.4, y0 + 1.85, color=C_GRAY, lw=1.1,
          ls="--", rad=-0.5)
    tx(ax, x0 + 3.05, y0 + 2.14, "采样\n训练", fs=7, color=C_GRAY)

    # ---- 图例 ----
    x0, y0 = cols[2], rows[1]
    panel(x0, y0, "图例", 6)
    rbox(ax, x0 + 0.35, y0 + 2.95, 0.9, 0.5, C_LBLUE, C_BLUE, lw=1.2)
    tx(ax, x0 + 2.55, y0 + 3.2, "物理建模（物理模式）", fs=8.5, ha="center")
    ml(x0 + 0.35, y0 + 2.3, 0.9, 0.5)
    tx(ax, x0 + 2.55, y0 + 2.55, "机器学习 / 深度学习", fs=8.5)
    rbox(ax, x0 + 0.35, y0 + 1.65, 0.9, 0.5, C_LGREEN, C_GREEN, lw=1.2)
    tx(ax, x0 + 2.55, y0 + 1.9, "观测数据", fs=8.5)
    rbox(ax, x0 + 0.35, y0 + 1.0, 0.9, 0.5, "white", C_GRAY, lw=1.0, ls="--")
    tx(ax, x0 + 2.55, y0 + 1.25, "可替换 / 虚拟组件", fs=8.5)
    arrow(ax, x0 + 0.4, y0 + 0.6, x0 + 1.2, y0 + 0.6, color=C_GRAY, lw=1.4)
    tx(ax, x0 + 2.55, y0 + 0.6, "实线：数据流 / 驱动", fs=8.5)
    arrow(ax, x0 + 0.4, y0 + 0.25, x0 + 1.2, y0 + 0.25, color=C_GRAY, lw=1.2,
          ls="--")
    tx(ax, x0 + 2.55, y0 + 0.25, "虚线：训练 / 被替代", fs=8.5)

    save(fig, "fig24_06_five_coupling_ways.png")


# ======================================================================
# fig24_07 方式1：ML 改进参数化
# ======================================================================
def fig24_07():
    fig, ax = new_ax(10.5, 6.2, (0, 12), (0, 6.6))

    rbox(ax, 0.4, 4.35, 3.1, 1.7, C_LBLUE, C_BLUE, lw=1.3)
    tx(ax, 1.95, 5.6, "环境变量 $e$", fs=10.5, weight="bold", color=C_BLUE)
    tx(ax, 1.95, 4.95, "降水量、地表坡度、\n温度、土壤属性 ……", fs=9)

    rbox(ax, 4.55, 4.5, 2.9, 1.4, C_LORANGE, C_ORANGE, lw=1.4)
    tx(ax, 6.0, 5.55, "机器学习映射", fs=10.5, weight="bold", color=C_ORANGE)
    tx(ax, 6.0, 4.95, "$\\hat{p} = f(e;\\, w)$", fs=11)

    rbox(ax, 8.5, 4.35, 3.1, 1.7, C_LBLUE, C_BLUE, lw=1.3)
    tx(ax, 10.05, 5.6, "集水区参数 $p$", fs=10.5, weight="bold", color=C_BLUE)
    tx(ax, 10.05, 4.95, "平均流量、最小流量、\n最大流量 ……", fs=9)

    arrow(ax, 3.5, 5.2, 4.5, 5.2, color=C_ORANGE, lw=1.6)
    arrow(ax, 7.45, 5.2, 8.45, 5.2, color=C_ORANGE, lw=1.6)

    # 真值来源
    rbox(ax, 0.4, 1.7, 11.2, 1.7, BG_PANEL, C_GRAY, lw=1.0, ls="--", pad=0.02)
    tx(ax, 6.0, 3.05, "训练真值（以最佳描述真实值为目标）的两种来源", fs=10,
       weight="bold", color="#444444")
    rbox(ax, 1.2, 1.95, 4.2, 0.75, C_LGREEN, C_GREEN, lw=1.2)
    tx(ax, 3.3, 2.32, "观测数据（如数千个集水区的实测）", fs=9)
    rbox(ax, 6.6, 1.95, 4.2, 0.75, C_LPURPLE, C_PURPLE, lw=1.2)
    tx(ax, 8.7, 2.42, "高分辨率物理模式（第一性原理）", fs=9)
    tx(ax, 8.7, 2.1, "过于昂贵、无法直接运行", fs=7.5, color="#555555")
    arrow(ax, 3.3, 2.45, 5.6, 4.45, color=C_GREEN, lw=1.4, ls="--", rad=-0.15)
    arrow(ax, 8.7, 2.45, 6.5, 4.45, color=C_PURPLE, lw=1.4, ls="--", rad=0.15)

    tx(ax, 6.0, 0.75,
       "应用：植被参数不按植物功能类型硬分配，而从统计协变量集学习；"
       "全球大气模式学习对流的有效粗尺度参数（如对流中云析出水的比例）",
       fs=8.5, color="#555555")
    tx(ax, 6.0, 0.3, "可学习的参数带来更好的热带对流表示", fs=8.5,
       color="#555555", style="italic")

    save(fig, "fig24_07_way1_parameterization.png")


# ======================================================================
# fig24_08 方式2：混合模型
# ======================================================================
def fig24_08():
    fig, ax = new_ax(10.5, 5.6, (0, 12), (0, 6.2))

    tx(ax, 6.0, 5.7,
       "$\\dfrac{\\partial s}{\\partial t}"
       " = \\mathcal{P}(s, \\nabla s, \\ldots)"
       " + f_{\\mathrm{ML}}(x;\\, w)$", fs=13)

    rbox(ax, 0.5, 2.7, 4.7, 2.3, C_LBLUE, C_BLUE, lw=1.4)
    tx(ax, 2.85, 4.5, "物理骨架", fs=11, weight="bold", color=C_BLUE)
    tx(ax, 2.85, 3.7, "植物水分传输的（微分）扩散方程\n遵循公认的质量守恒、能量守恒定律\n理论基础扎实、可解释", fs=9)

    rbox(ax, 6.8, 2.7, 4.7, 2.3, C_LORANGE, C_ORANGE, lw=1.4)
    tx(ax, 9.15, 4.5, "机器学习项", fs=11, weight="bold", color=C_ORANGE)
    tx(ax, 9.15, 3.7, "对水分传输的生物调节了解甚少\n调节部分灵活、不作硬性规定\n从数据中学习", fs=9)

    circ = Circle((6.0, 3.85), 0.32, facecolor="white", edgecolor="#555555",
                  lw=1.4, zorder=5)
    ax.add_patch(circ)
    tx(ax, 6.0, 3.85, "+", fs=16, weight="bold", zorder=6)

    rbox(ax, 2.5, 0.45, 7.0, 1.55, C_LGREEN, C_GREEN, lw=1.4)
    tx(ax, 6.0, 1.6, "混合模型（hybrid model）", fs=11, weight="bold", color=C_GREEN)
    tx(ax, 6.0, 0.95, "更“物理”的模型，且调节项可从数据中学习", fs=9.5)

    arrow(ax, 2.85, 2.65, 3.6, 2.05, color=C_BLUE, lw=1.4)
    arrow(ax, 9.15, 2.65, 8.4, 2.05, color=C_ORANGE, lw=1.4)

    tx(ax, 6.0, 0.05, "", fs=8)
    tx(ax, 6.0, -0.25, "", fs=8)

    save(fig, "fig24_08_way2_hybrid_model.png")


# ======================================================================
# fig24_09 方式3：模型—观测不匹配分析
# ======================================================================
def fig24_09():
    fig, ax = new_ax(10.5, 5.8, (0, 13), (0, 6.4))

    rbox(ax, 0.4, 4.55, 3.0, 1.3, C_LBLUE, C_BLUE, lw=1.3)
    tx(ax, 1.9, 5.45, "物理模式输出", fs=10, weight="bold", color=C_BLUE)
    tx(ax, 1.9, 4.95, "动态变量的模拟结果", fs=8.5)

    rbox(ax, 0.4, 2.6, 3.0, 1.3, C_LGREEN, C_GREEN, lw=1.3)
    tx(ax, 1.9, 3.5, "观测", fs=10, weight="bold", color=C_GREEN)
    tx(ax, 1.9, 3.0, "（假设观测无偏差）", fs=8.5)

    rbox(ax, 4.4, 3.55, 2.6, 1.35, "white", C_GRAY, lw=1.2)
    tx(ax, 5.7, 4.5, "偏差", fs=10, weight="bold")
    tx(ax, 5.7, 3.95, "不完善知识导致的\n模型误差", fs=8)

    rbox(ax, 8.0, 3.5, 2.7, 1.45, C_LORANGE, C_ORANGE, lw=1.4)
    tx(ax, 9.35, 4.55, "机器学习", fs=10.5, weight="bold", color=C_ORANGE)
    tx(ax, 9.35, 3.95, "识别、可视化、理解\n模型错误的模式", fs=8.5)

    rbox(ax, 11.3, 4.55, 1.55, 1.3, "white", C_BLUE, lw=1.2)
    tx(ax, 12.07, 5.45, "修正输出", fs=9.5, weight="bold", color=C_BLUE)
    tx(ax, 12.07, 4.95, "偏差校正\n精细降尺度", fs=8)

    rbox(ax, 11.3, 1.6, 1.55, 1.3, "white", C_GREEN, lw=1.2)
    tx(ax, 12.07, 2.5, "改进理论", fs=9.5, weight="bold", color=C_GREEN)
    tx(ax, 12.07, 2.0, "改进物理模型\n与理论本身", fs=8)

    arrow(ax, 3.4, 5.0, 4.55, 4.55, color=C_BLUE, lw=1.4)
    arrow(ax, 3.4, 3.45, 4.55, 3.9, color=C_GREEN, lw=1.4)
    arrow(ax, 7.0, 4.22, 7.95, 4.22, color=C_ORANGE, lw=1.6)
    arrow(ax, 10.7, 4.6, 11.25, 5.0, color=C_ORANGE, lw=1.5)
    arrow(ax, 10.7, 3.85, 11.25, 2.45, color=C_ORANGE, lw=1.5)
    arrow(ax, 11.9, 1.55, 2.5, 4.5, color=C_GRAY, lw=1.2, ls="--", rad=-0.25)
    tx(ax, 6.2, 1.35, "反馈：自动提取物理模型未显式表示的模式，改进模型与理论",
       fs=9, color="#555555")
    tx(ax, 6.2, 0.75, "替代单调、手工设计的降尺度方法", fs=8.5, color="#777777",
       style="italic")

    save(fig, "fig24_09_way3_mismatch_analysis.png")


# ======================================================================
# fig24_10 方式5：替代建模或模仿（仿真器）
# ======================================================================
def fig24_10():
    fig, ax = new_ax(10.5, 5.8, (0, 13), (0, 6.4))

    rbox(ax, 0.4, 4.45, 1.9, 1.2, "white", C_GRAY, lw=1.1)
    tx(ax, 1.35, 5.05, "输入 $x$", fs=10)

    rbox(ax, 3.1, 4.0, 3.7, 2.1, C_LBLUE, C_BLUE, lw=1.4)
    tx(ax, 4.95, 5.6, "物理模式", fs=11, weight="bold", color=C_BLUE)
    tx(ax, 4.95, 4.85, "完整（或部分）模拟\n计算昂贵、耗时长", fs=9)
    rbox(ax, 5.35, 5.75, 1.6, 0.5, C_LRED, C_RED, lw=1.1)
    tx(ax, 6.15, 6.0, "慢", fs=10, weight="bold", color=C_RED)

    rbox(ax, 7.7, 4.45, 2.0, 1.2, "white", C_GRAY, lw=1.1)
    tx(ax, 8.7, 5.05, "输出 $y$", fs=10)

    arrow(ax, 2.35, 5.05, 3.05, 5.05, color=C_GRAY, lw=1.4)
    arrow(ax, 6.85, 5.05, 7.65, 5.05, color=C_GRAY, lw=1.4)

    arrow(ax, 4.95, 3.95, 4.95, 3.15, color=C_GRAY, lw=1.4, ls="--")
    tx(ax, 6.35, 3.5, "采样（输入, 输出）对，训练仿真器", fs=9, color="#555555")

    rbox(ax, 0.4, 1.55, 1.9, 1.2, "white", C_GRAY, lw=1.1)
    tx(ax, 1.35, 2.15, "输入 $x$", fs=10)
    rbox(ax, 3.1, 1.1, 3.7, 2.1, C_LORANGE, C_ORANGE, lw=1.4)
    tx(ax, 4.95, 2.7, "ML 仿真器", fs=11, weight="bold", color=C_ORANGE)
    tx(ax, 4.95, 1.95, "训练后高速仿真\n不牺牲太多精度", fs=9)
    rbox(ax, 5.35, 2.85, 1.6, 0.5, C_LGREEN, C_GREEN, lw=1.1)
    tx(ax, 6.15, 3.1, "快", fs=10, weight="bold", color=C_GREEN)
    rbox(ax, 7.7, 1.55, 2.6, 1.2, "white", C_GRAY, lw=1.1)
    tx(ax, 9.0, 2.15, "输出 $\\hat{y} \\approx y$", fs=10)

    arrow(ax, 2.35, 2.15, 3.05, 2.15, color=C_ORANGE, lw=1.6)
    arrow(ax, 6.85, 2.15, 7.65, 2.15, color=C_ORANGE, lw=1.6)
    arrow(ax, 10.35, 2.15, 11.0, 2.15, color=C_ORANGE, lw=1.6)

    rbox(ax, 11.0, 1.0, 1.85, 2.35, C_LYELLOW, C_ORANGE, lw=1.2)
    tx(ax, 11.92, 2.95, "典型用途", fs=9.5, weight="bold", color=C_ORANGE)
    tx(ax, 11.92, 1.9, "快速敏感性\n分析\n参数校准\n置信区间推导", fs=8.5)

    tx(ax, 6.5, 0.45,
       "例：替代昂贵的辐射传输模型（辐射—植被—大气相互作用）；"
       "气候模型、植被动态模型的状态演变仿真", fs=8.5, color="#555555")
    tx(ax, 6.5, 0.05,
       "物理模型的复杂性使仿真成为检验 ML / DL 外推潜力的优秀测试平台",
       fs=8.5, color="#555555", style="italic")

    save(fig, "fig24_10_way5_emulator.png")


# ======================================================================
# fig24_11 NLP 文本分析五步流程
# ======================================================================
def fig24_11():
    fig, ax = new_ax(12.5, 5.6, (0, 13.4), (0, 6.0))

    steps = [
        ("导入与可视化",
         "导入 PDF、HTML、Excel、\n设备日志、新闻提要、\n调查报告、社交媒体、\n论文（可含表情符号）；\n词云图、散点图观察词频",
         C_BLUE),
        ("预处理",
         "清理 HTML 等特殊符号；\n停用词过滤：and、of、\nthe、to 等虚词与低频词；\nn-gram 拆分",
         C_GREEN),
        ("转换为数值",
         "词频统计；\n独热编码向量；\n预训练编码 / 词向量模型\n（文本 → 向量 / 数字）",
         C_ORANGE),
        ("浅层模型",
         "主题建模；情感分析\n（正面 / 中立 / 负面）；\n文本降维、文档摘要、\n关键词提取、文档打分",
         C_PURPLE),
        ("深度学习与大模型",
         "Transformer、GPT 系列；\n高级情感分类、自动摘要\n与文本生成；\n文本到文本：读一部小说，\n生成同风格的新小说",
         C_RED),
    ]
    x0s = [0.3, 2.95, 5.6, 8.25, 10.9]
    w, h = 2.3, 3.3
    y0 = 1.5
    for (title, desc, c), x0 in zip(steps, x0s):
        rbox(ax, x0, y0, w, h, "white", c, lw=1.4)
        box(ax, x0 + 0.1, y0 + h - 0.72, w - 0.2, 0.6, c, ec="none",
            alpha=0.12, zorder=3)
        tx(ax, x0 + w / 2, y0 + h - 0.42, title, fs=9.8, weight="bold", color=c)
        tx(ax, x0 + w / 2, y0 + 1.28, desc, fs=7.6)
        circled(ax, x0 + w / 2, y0 + h + 0.42, steps.index((title, desc, c)) + 1,
                r=0.26, fc=c, fs=11)

    for i in range(4):
        arrow(ax, x0s[i] + w + 0.04, y0 + h / 2, x0s[i + 1] - 0.04,
              y0 + h / 2, color=C_GRAY, lw=1.6)

    rbox(ax, 0.3, 0.15, 12.9, 0.85, C_LYELLOW, C_ORANGE, lw=1.2)
    tx(ax, 6.75, 0.57,
       "文本向量化之后，即回归本书的机器学习 / 深度学习框架——"
       "NLP 是“把语言变成数据”的数据挖掘", fs=10.5, weight="bold")

    save(fig, "fig24_11_nlp_five_steps.png")


# ======================================================================
if __name__ == "__main__":
    import warnings
    with warnings.catch_warnings(record=True) as wlist:
        warnings.simplefilter("always")
        fig24_01(); fig24_02(); fig24_03(); fig24_04(); fig24_05()
        fig24_06(); fig24_07(); fig24_08(); fig24_09(); fig24_10()
        fig24_11()
        if wlist:
            print("\n===== WARNINGS =====")
            for w in wlist:
                print(w.category.__name__, "-", w.message)
        else:
            print("NO WARNINGS")
    print("ALL DONE")
