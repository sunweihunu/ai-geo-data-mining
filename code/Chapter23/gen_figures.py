# -*- coding: utf-8 -*-
"""第23章 地学应用三：土地篇 插图生成脚本。

运行方式（Windows，python 不可直接用）：
    uv run --no-project --with matplotlib --with numpy python tmp_fig23/gen_figures.py
输出：书稿/figs/ch23/fig23_01_*.png ... fig23_10_*.png
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Patch, Rectangle
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.lines import Line2D

# ---------------------------------------------------------------- 全局风格
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["figure.facecolor"] = "white"

C_BLUE = "#1f77b4"
C_ORANGE = "#ff7f0e"
C_GREEN = "#2ca02c"
C_RED = "#d62728"
C_PURPLE = "#9467bd"
C_GRAY = "#7f7f7f"
BLUE_L = "#dce9f7"
ORANGE_L = "#fde8cf"
GREEN_L = "#ddf0dd"
RED_L = "#fadcdc"
PURPLE_L = "#e9e2f3"
GRAY_L = "#f2f2f2"

# 五级易感性色带（非常低 -> 非常高）
RAMP5 = ["#2c7bb6", "#abd9e9", "#ffffbf", "#fdae61", "#d7191c"]
LAB5 = ["非常低", "低", "中", "高", "非常高"]

rng = np.random.default_rng(42)

OUT = r"C:\20260905\项目 人工智能与地理数据挖掘\书稿\figs\ch23"
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print("saved:", name)


def new_canvas(figsize=(12, 6.4)):
    """返回一个占满整图的坐标轴（数据坐标 0~100），用于手工框图。"""
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc="#ffffff", ec=C_GRAY, lw=1.2,
        fontsize=10.5, tc="black", weight="normal", align="center", ls="-"):
    """圆角矩形 + 居中（或左对齐）文本。"""
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.35,rounding_size=1.2",
                                fc=fc, ec=ec, lw=lw, linestyle=ls,
                                mutation_aspect=1.0))
    if text:
        if align == "center":
            ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                    fontsize=fontsize, color=tc, fontweight=weight,
                    linespacing=1.45)
        else:
            ax.text(x + 1.8, y + h / 2, text, ha="left", va="center",
                    fontsize=fontsize, color=tc, fontweight=weight,
                    linespacing=1.45)


def arrow(ax, x1, y1, x2, y2, color=C_GRAY, lw=1.6, style="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                shrinkA=1.0, shrinkB=1.0))


# ---------------------------------------------------------- 合成空间数据
def smooth_field(rng_local, n=90, k=6, smin=0.10, smax=0.30):
    """若干高斯斑叠加而成的平滑空间场，取值归一到 0~1。"""
    xs = np.linspace(0.0, 1.0, n)
    X, Y = np.meshgrid(xs, xs)
    Z = np.zeros_like(X)
    for _ in range(k):
        A = rng_local.uniform(0.4, 1.0)
        cx, cy = rng_local.uniform(0.05, 0.95, 2)
        s = rng_local.uniform(smin, smax)
        Z += A * np.exp(-(((X - cx) ** 2) + ((Y - cy) ** 2)) / (2 * s ** 2))
    Z -= Z.min()
    if Z.max() > 0:
        Z /= Z.max()
    return Z


def class_field(rng_local, n=90, k=9, ncls=5):
    """由平滑场分割出的类别（面状）图。"""
    Z = smooth_field(rng_local, n=n, k=k, smin=0.06, smax=0.18)
    edges = np.linspace(0.15, 0.85, ncls - 1)
    return np.digitize(Z, edges)


def cls_norm(ncls):
    """类别 imshow 的固定归一化：保证类别 k 恰好取色带第 k 色。"""
    return BoundaryNorm(np.arange(ncls + 1) - 0.5, ncls)


# ================================================================ 图 23-1
def fig01_lsm_concept():
    """LSM 问题概念框图：X 因子图层（全域已知）+ 局部 Y 真值 -> 模型 -> 全域易感性图。"""
    fig, ax = new_canvas(figsize=(12.4, 6.6))

    # --- 左列：条件因子 X（四个小图层）
    ax.text(12, 96.5, "影响因素 X（滑坡调节因子 LCF）", ha="center", va="center",
            fontsize=11, fontweight="bold")
    ax.text(12, 92, "地形与环境变量 · 空间图层 · 全域已知",
            ha="center", va="center", fontsize=9, color=C_GRAY)

    z_slope = smooth_field(rng, n=70, k=6, smin=0.10, smax=0.30)
    z_soil = class_field(rng, n=70, k=9, ncls=5)
    z_rain = smooth_field(rng, n=70, k=3, smin=0.25, smax=0.55)
    z_lith = class_field(rng, n=70, k=5, ncls=4)

    mini = [(4, 79, z_slope, "YlGnBu", None, "坡度"),
            (4, 65.5, z_soil, "Set2", 5, "土壤类型"),
            (4, 52, z_rain, "Blues", None, "降雨量"),
            (4, 38.5, z_lith, "Pastel1", 4, "岩性类型")]
    for x0, y0, Z, cmap, ncls, lab in mini:
        axm = fig.add_axes([x0 / 100, y0 / 100, 16 / 100, 11 / 100])
        if ncls is None:
            axm.imshow(Z, cmap=cmap, extent=[0, 1, 0, 1], origin="lower")
        else:
            axm.imshow(Z, cmap=ListedColormap(
                plt.get_cmap(cmap).colors[:ncls]), extent=[0, 1, 0, 1],
                origin="lower", interpolation="nearest", norm=cls_norm(ncls))
        axm.set_xticks([])
        axm.set_yticks([])
        for sp in axm.spines.values():
            sp.set_color(C_GRAY)
        ax.text(x0 + 1.2, y0 + 9.3, lab, fontsize=8.5, ha="left", va="center",
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.2))

    # --- 中列：兴趣变量 Y（局部真值）
    ax.text(40, 96.5, "兴趣变量 Y：滑坡可能性", ha="center", va="center",
            fontsize=11, fontweight="bold")
    ax.text(40, 92, "真值 · 仅局部已知", ha="center", va="center",
            fontsize=9, color=C_GRAY)

    z_terr = smooth_field(rng, n=70, k=5, smin=0.15, smax=0.35)
    axm = fig.add_axes([30 / 100, 52 / 100, 20 / 100, 32 / 100])
    axm.imshow(z_terr, cmap="Greys", extent=[0, 1, 0, 1], origin="lower",
               alpha=0.75)
    flat = z_terr.ravel()
    top = np.argsort(flat)[-80:]
    pick = rng.choice(top, 12, replace=False)
    py, px = np.unravel_index(pick, z_terr.shape)
    axm.scatter(px / 69, py / 69, marker="^", s=42, c=C_RED, ec="black",
                lw=0.5, zorder=5)
    axm.set_xticks([])
    axm.set_yticks([])
    for sp in axm.spines.values():
        sp.set_color(C_GRAY)
    ax.text(40, 47.6, "Y 真值来源：现场考察 / 影像判读 / 监测",
            ha="center", va="center", fontsize=8.8)
    ax.text(40, 43.2, "样本点往往仅占全域约 10%~20%", ha="center",
            va="center", fontsize=8.8)

    # --- 模型框
    box(ax, 34, 16, 32, 14, "机器学习模型\n学习 X 与 Y 的空间关系",
        fc=BLUE_L, ec=C_BLUE, lw=1.4, fontsize=10.5, weight="bold")

    # --- 右列：输出易感性图
    ax.text(84, 96.5, "滑坡易感性图（全域）", ha="center", va="center",
            fontsize=11, fontweight="bold")
    ax.text(84, 92, "逐像元滑坡概率与分级", ha="center", va="center",
            fontsize=9, color=C_GRAY)

    z_out = smooth_field(rng, n=70, k=6, smin=0.12, smax=0.30)
    cls = np.digitize(z_out, [0.2, 0.4, 0.6, 0.8])
    axm = fig.add_axes([74 / 100, 52 / 100, 20 / 100, 32 / 100])
    axm.imshow(cls, cmap=ListedColormap(RAMP5), extent=[0, 1, 0, 1],
               origin="lower", interpolation="nearest", norm=cls_norm(5))
    axm.set_xticks([])
    axm.set_yticks([])
    for sp in axm.spines.values():
        sp.set_color(C_GRAY)
    # 图例色带
    w = 20 / 5
    for i in range(5):
        ax.add_patch(Rectangle((74 + i * w, 40), w, 3.4, fc=RAMP5[i],
                               ec="white", lw=0.8))
        ax.text(74 + (i + 0.5) * w, 37.2, LAB5[i], ha="center", va="center",
                fontsize=7.2)

    # --- 连接箭头
    arrow(ax, 20.8, 47, 35, 30.5, color=C_BLUE, lw=1.8)
    ax.text(27.5, 44.5, "X（全域）", fontsize=8.6, color=C_BLUE, ha="center")
    arrow(ax, 40, 51.2, 45, 30.8, color=C_RED, lw=1.8)
    ax.text(46.8, 36, "Y（局部样本）", fontsize=8.6, color=C_RED,
            ha="left")
    arrow(ax, 61, 30.8, 76.5, 50.8, color=C_GREEN, lw=1.8)
    ax.text(61.5, 43.5, "预测全域", fontsize=8.6, color=C_GREEN, ha="left")

    # --- 底部结论
    box(ax, 14, 2, 72, 9,
        "问题本质：X 全域已知而 Y 仅局部已知 —— 用已知 X–Y 关系外推全域（空间预测问题）",
        fc=GRAY_L, ec=C_GRAY, fontsize=10)
    ax.text(98.5, 6, "示意", ha="right", va="center", fontsize=8.5,
            color=C_GRAY)

    save(fig, "fig23_01_lsm_concept.png")


# ================================================================ 图 23-2
def fig02_conditioning_factors():
    """常用滑坡条件因子示例（六面板阵列，合成数据）。"""
    fig, axes = plt.subplots(2, 3, figsize=(10.4, 6.8))
    fig.subplots_adjust(left=0.03, right=0.99, top=0.95, bottom=0.07,
                        hspace=0.16, wspace=0.10)

    z_slope = smooth_field(rng, n=90, k=6, smin=0.10, smax=0.30)
    z_asp = smooth_field(rng, n=90, k=5, smin=0.12, smax=0.28)
    gy, gx = np.gradient(z_asp)
    asp = np.degrees(np.arctan2(-gy, gx)) % 360.0
    z_soil = class_field(rng, n=90, k=9, ncls=5)
    z_rain = np.clip(0.25 + 0.45 * smooth_field(rng, n=90, k=2, smin=0.35,
                                                smax=0.7), 0, 1)
    z_twi = smooth_field(rng, n=90, k=7, smin=0.07, smax=0.20)
    z_lith = class_field(rng, n=90, k=4, ncls=4)

    panels = [
        (z_slope, "YlGnBu", "(a) 坡度（坡角）"),
        (asp, "hsv", "(b) 坡向"),
        (z_soil, "Set2", "(c) 土壤类型"),
        (z_rain, "Blues", "(d) 年降雨量（mm）"),
        (z_twi, "BuPu", "(e) 地形湿度指数"),
        (z_lith, "Pastel1", "(f) 岩性类型"),
    ]
    for ax, (Z, cmap, title) in zip(axes.ravel(), panels):
        if cmap in ("Set2", "Pastel1"):
            ncls = 5 if cmap == "Set2" else 4
            ax.imshow(Z, cmap=ListedColormap(
                plt.get_cmap(cmap).colors[:ncls]), extent=[0, 1, 0, 1],
                origin="lower", interpolation="nearest", norm=cls_norm(ncls))
        else:
            ax.imshow(Z, cmap=cmap, extent=[0, 1, 0, 1], origin="lower")
        ax.set_title(title, fontsize=11)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.text(0.5, 0.015,
             "示意：条件因子是覆盖研究区全域的空间图层（连续变量或类别变量），研究区内逐像元都有取值",
             ha="center", va="center", fontsize=9.5, color=C_GRAY)
    save(fig, "fig23_02_conditioning_factors.png")


# ================================================================ 图 23-3
def fig03_binary_vs_fiveclass():
    """同一滑坡可能性的两种表达：二分类 vs 五分类。"""
    fig = plt.figure(figsize=(9.8, 4.9))

    # --- 上：二分类
    ax1 = fig.add_axes([0.07, 0.60, 0.86, 0.30])
    ax1.set_xlim(0, 1)
    ax1.set_ylim(-0.35, 1.85)
    ax1.axis("off")
    ax1.text(0.5, 1.62, "表达方式一：二分类 —— 滑坡还是不滑坡",
             ha="center", va="center", fontsize=11.5, fontweight="bold")
    ax1.add_patch(Rectangle((0.0, 0.15), 0.5, 0.7, fc=BLUE_L, ec=C_BLUE, lw=1.2))
    ax1.add_patch(Rectangle((0.5, 0.15), 0.5, 0.7, fc=RED_L, ec=C_RED, lw=1.2))
    ax1.text(0.25, 0.5, "类别 0\n不滑坡", ha="center", va="center",
             fontsize=10.5)
    ax1.text(0.75, 0.5, "类别 1\n滑坡", ha="center", va="center", fontsize=10.5)
    ax1.plot([0.5, 0.5], [0.05, 1.25], ls="--", color="black", lw=1.2)
    ax1.text(0.51, 1.13, "判别阈值（如 0.5）", ha="left", va="center",
             fontsize=9)
    for x, lab in [(0.0, "0"), (0.5, "0.5"), (1.0, "1")]:
        ax1.plot([x, x], [0.15, 0.08], color="black", lw=0.9)
        ax1.text(x, -0.06, lab, ha="center", va="center", fontsize=9)
    ax1.text(0.5, -0.28, "模型输出的滑坡可能性 P", ha="center", va="center",
             fontsize=9.5, color=C_GRAY)

    # --- 中间说明
    fig.text(0.5, 0.47,
             "同一个“滑坡可能性 P”，两种表达（多分类本质是概率区间分级；也可以不分级、直接输出概率）",
             ha="center", va="center", fontsize=9.8, color=C_GRAY)

    # --- 下：五分类
    ax2 = fig.add_axes([0.07, 0.08, 0.86, 0.30])
    ax2.set_xlim(0, 1)
    ax2.set_ylim(-0.55, 1.85)
    ax2.axis("off")
    ax2.text(0.5, 1.62, "表达方式二：五分类 —— 按可能性区间分级",
             ha="center", va="center", fontsize=11.5, fontweight="bold")
    for i in range(5):
        ax2.add_patch(Rectangle((i * 0.2, 0.15), 0.2, 0.7, fc=RAMP5[i],
                                ec="white", lw=1.0))
        tc = "white" if i in (0, 4) else "black"
        ax2.text(i * 0.2 + 0.1, 0.5, LAB5[i], ha="center", va="center",
                 fontsize=10, color=tc)
        rng_lab = "{:.0f}~{:.0f}%".format(i * 20, (i + 1) * 20)
        ax2.text(i * 0.2 + 0.1, -0.16, rng_lab, ha="center", va="center",
                 fontsize=8.5, color=C_GRAY)
        ax2.plot([i * 0.2, i * 0.2], [0.15, 0.08], color="black", lw=0.9)
    ax2.plot([1.0, 1.0], [0.15, 0.08], color="black", lw=0.9)
    ax2.text(0.0, -0.16, "0%", ha="center", va="center", fontsize=8.5,
             color=C_GRAY)
    ax2.text(1.0, -0.16, "100%", ha="center", va="center", fontsize=8.5,
             color=C_GRAY)
    ax2.text(0.5, -0.45, "模型输出的滑坡可能性 P：预测值落在哪个区间，就归为哪一类",
             ha="center", va="center", fontsize=9.5, color=C_GRAY)

    save(fig, "fig23_03_binary_vs_fiveclass.png")


# ================================================================ 图 23-4
def fig04_research_trends():
    """研究热度：逐年文章数（示意）与常用模型份额（示意）。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.4))
    fig.subplots_adjust(left=0.06, right=0.985, top=0.88, bottom=0.20,
                        wspace=0.24)

    ax = axes[0]
    years = np.arange(2006, 2020)
    counts = np.array([5, 6, 8, 11, 14, 18, 23, 29, 36, 45, 56, 69, 84, 102])
    ax.bar(years, counts, color=C_BLUE, ec="white", lw=0.6, width=0.72)
    ax.set_title("(a) 基于机器学习的 LSM 研究文章数量", fontsize=11.5)
    ax.set_xlabel("年份")
    ax.set_ylabel("文章数量（篇）")
    ax.set_xticks(years[::2])
    ax.set_xticklabels([str(y) for y in years[::2]], fontsize=9)
    ax.tick_params(axis="y", labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.annotate("逐年增长", xy=(years[-1], counts[-1]),
                xytext=(years[-4], counts[-1] * 0.86), fontsize=9.5,
                color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.2))

    ax = axes[1]
    models = ["逻辑回归", "人工神经网络", "支持向量机", "决策树", "随机森林"]
    share = np.array([100, 85, 78, 62, 58])
    colors = [C_BLUE, C_ORANGE, C_GREEN, C_RED, C_PURPLE]
    ypos = np.arange(len(models))[::-1]
    ax.barh(ypos, share, color=colors, ec="white", lw=0.6, height=0.62)
    ax.set_yticks(ypos)
    ax.set_yticklabels(models, fontsize=10.5)
    ax.set_xlabel("相对使用份额（最高者 = 100，示意）")
    ax.set_title("(b) LSM 常用机器学习模型（前五）", fontsize=11.5)
    ax.set_xlim(0, 118)
    for y, v in zip(ypos, share):
        ax.text(v + 2.5, y, str(v), va="center", fontsize=9)
    ax.tick_params(axis="x", labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)

    fig.text(0.5, 0.03,
             "数据为示意（趋势与排序参照 Merghadi et al., 2020 综述的文献计量结果；"
             "模糊神经网络、二次判别分析、朴素贝叶斯等亦有使用）",
             ha="center", va="center", fontsize=9.3, color=C_GRAY)
    save(fig, "fig23_04_research_trends.png")


# ================================================================ 图 23-5
def fig05_decision_tree():
    """滑坡预测的决策树示例（阈值仅作示意）。"""
    fig, ax = new_canvas(figsize=(12.4, 6.9))

    nw = dict(fc="#ffffff", ec=C_BLUE, lw=1.3)
    leaf_fc = RAMP5
    leaf_tc = ["white", "black", "black", "black", "white"]

    # 节点：(x_center, y_center, w, h, text, kind)
    root = (50, 90, 22, 8, "坡度 > 25°？", "node")
    n_h = (27, 68, 24, 8, "高程 > 1000 m？", "node")
    n_s = (73, 68, 26, 8, "土壤深度 > 10 m？", "node")
    n_n = (15, 46, 20, 8, "NDVI > 0.4？", "node")
    n_r = (62.5, 46, 22, 8, "降雨 > 1000 mm？", "node")
    leaves = [(7.5, 22, 14, 8, "非常高", 4),
              (23, 22, 14, 8, "高", 3),
              (39, 22, 14, 8, "中", 2),
              (55, 22, 14, 8, "中", 2),
              (70.5, 22, 14, 8, "低", 1),
              (86.5, 22, 14, 8, "非常低", 0)]

    def draw_node(t):
        x, y, w, h, text, kind = t
        if kind == "node":
            box(ax, x - w / 2, y - h / 2, w, h, text, fontsize=10.5, **nw)
        else:
            k = t[5]
            box(ax, x - w / 2, y - h / 2, w, h, text, fontsize=10.5,
                fc=leaf_fc[k], ec=C_GRAY, lw=1.0, tc=leaf_tc[k],
                weight="bold")

    def edge(p, c, lab, lx, ly):
        arrow(ax, p[0], p[1] - p[3] / 2 - 0.4, c[0], c[1] + c[3] / 2 + 0.4,
              color=C_GRAY, lw=1.4)
        ax.text(lx, ly, lab, fontsize=9.5, ha="center", va="center",
                color=C_GREEN if lab == "是" else C_ORANGE, fontweight="bold")

    draw_node(root)
    draw_node(n_h)
    draw_node(n_s)
    draw_node(n_n)
    draw_node(n_r)
    for t in leaves:
        draw_node(t)

    edge(root, n_h, "是", 36, 80)
    edge(root, n_s, "否", 64, 80)
    edge(n_h, n_n, "是", 19, 58)
    edge(n_h, leaves[2], "否", 35, 44)
    edge(n_s, n_r, "是", 66, 58)
    edge(n_s, leaves[5], "否", 82, 44)
    edge(n_n, leaves[0], "是", 9.5, 35)
    edge(n_n, leaves[1], "否", 20.5, 35)
    edge(n_r, leaves[3], "是", 57, 35)
    edge(n_r, leaves[4], "否", 68.5, 35)

    ax.text(50, 8.5,
            "树形结构把 X 与 Y 的关系显式表达出来（可解释性最佳）；"
            "越靠近根节点的因子影响越大 —— 本例中坡度是首要指标",
            ha="center", va="center", fontsize=10)
    ax.text(50, 3.2, "（叶节点为易感性等级；阈值数值仅作示意）",
            ha="center", va="center", fontsize=9, color=C_GRAY)

    save(fig, "fig23_05_decision_tree.png")


# ================================================================ 图 23-6
def fig06_random_forest():
    """随机森林流程：Bootstrap 重抽样 -> 多棵决策树 -> 平均/投票集成。"""
    fig, ax = new_canvas(figsize=(12.4, 6.4))

    ax.text(50, 95.5, "随机森林：用 Bootstrap 重抽样把一棵树变成一片森林",
            ha="center", va="center", fontsize=12, fontweight="bold")

    # 原始数据集
    box(ax, 3, 42, 19, 16, "原始训练集\n（样本：X ＋ Y）", fc=GRAY_L,
        ec=C_GRAY, fontsize=10.5)

    rows = [(74, "训练集 1"), (44.5, "训练集 2"), (15, "训练集 3")]
    tree_ys = []
    for yc, name in rows:
        box(ax, 30, yc, 20, 11, name, fc=ORANGE_L, ec=C_ORANGE, fontsize=10)
        arrow(ax, 22.4, 50, 29.6, yc + 5.5, color=C_ORANGE, lw=1.5)
        box(ax, 58, yc, 18, 11, "", fc="white", ec=C_GREEN, lw=1.3)
        ax.text(59.6, yc + 5.5, "决策树", fontsize=9.6, ha="left",
                va="center")
        # 迷你树形图标
        x0 = 70.0
        yb, yt = yc + 2.0, yc + 9.0
        ymid = (yb + yt) / 2
        pts_root = [(x0 + 2.2, yt)]
        pts_mid = [(x0, ymid), (x0 + 4.4, ymid)]
        pts_leaf = [(x0 - 1.2, yb), (x0 + 1.2, yb), (x0 + 3.2, yb),
                    (x0 + 5.6, yb)]
        for (x1, y1) in pts_root:
            for (x2, y2) in pts_mid:
                ax.plot([x1, x2], [y1, y2], color=C_GREEN, lw=1.0)
        for (x1, y1) in pts_mid:
            for (x2, y2) in pts_leaf:
                ax.plot([x1, x2], [y1, y2], color=C_GREEN, lw=1.0)
        for (x1, y1) in pts_root + pts_mid + pts_leaf:
            ax.plot(x1, y1, "o", ms=2.6, color=C_GREEN)
        arrow(ax, 50.4, yc + 5.5, 57.6, yc + 5.5, color=C_GREEN, lw=1.5)
        tree_ys.append(yc + 5.5)

    ax.text(40, 34.5, "Bootstrap 重抽样\n（有放回随机抽样）", fontsize=8.8,
            ha="center", va="center", color=C_ORANGE)

    # 集成
    box(ax, 84, 42, 14.5, 16, "集成\n平均 / 投票", fc=GREEN_L, ec=C_GREEN,
        fontsize=10.5, weight="bold")
    arrow(ax, 76.4, tree_ys[0], 85.5, 56.5, color=C_GREEN, lw=1.5)
    arrow(ax, 76.4, tree_ys[1], 83.6, 50, color=C_GREEN, lw=1.5)
    arrow(ax, 76.4, tree_ys[2], 85.5, 43.5, color=C_GREEN, lw=1.5)

    ax.text(50, 5,
            "多棵树的平均（回归）或投票（分类）通常比单棵树精度更高；"
            "但可解释性下降 —— 用哪棵树解释？可考察各棵树的共性，共性因子影响更大",
            ha="center", va="center", fontsize=9.8)

    save(fig, "fig23_06_random_forest.png")


# ================================================================ 图 23-7
def fig07_six_steps():
    """基于 ML 的 LSM 六步建模总流程（蛇形）。"""
    fig, ax = new_canvas(figsize=(12.6, 6.2))

    steps = [
        ("1", "构建空间数据库", "滑坡库存图 Y ＋\n滑坡条件因子 X", 4, 62),
        ("2", "数据分析与优化", "特征选择（模型前处理）：\nVIF ／ 信息增益 IG", 37, 62),
        ("3", "构建重采样数据集", "交叉验证 CV 切割训练／验证，\n优化模型超参数", 70, 62),
        ("4", "模型训练、配置与实现", "参数估计：网格搜索、随机搜索、\n基于梯度和智能搜索（如 PSO）", 70, 14),
        ("5", "模型训练、验证与比较", "总体准确性 ACC、\nAUC、Cohen's kappa", 37, 14),
        ("6", "生成滑坡易感性图", "概率格网重新分类为类别\n（如按百分位数分五类）", 4, 14),
    ]
    w, h = 26, 24

    for k, (num, title, desc, x, y) in enumerate(steps):
        fc = BLUE_L if k < 5 else ORANGE_L
        ec = C_BLUE if k < 5 else C_ORANGE
        box(ax, x, y, w, h, "", fc=fc, ec=ec, lw=1.5)
        ax.add_patch(Circle((x + 4.2, y + h - 4.2), 2.7, fc=ec, ec="none"))
        ax.text(x + 4.2, y + h - 4.2, num, ha="center", va="center",
                fontsize=11, color="white", fontweight="bold")
        ax.text(x + 8.2, y + h - 4.2, "第 {} 步".format(num), ha="left",
                va="center", fontsize=10.5, fontweight="bold")
        ax.text(x + w / 2, y + h - 9.0, title, ha="center", va="center",
                fontsize=10.5, fontweight="bold")
        ax.text(x + w / 2, y + (h - 10) / 2 - 0.5, desc, ha="center",
                va="center", fontsize=8.8, color="#333333", linespacing=1.5)

    # 蛇形箭头：1->2->3（上排向右），3->4（向下），4->5->6（下排向左）
    arrow(ax, 30.6, 74, 36.6, 74, color=C_GRAY, lw=2.0)                      # 1->2
    arrow(ax, 63.6, 74, 69.6, 74, color=C_GRAY, lw=2.0)                      # 2->3
    arrow(ax, 83, 61.4, 83, 38.6, color=C_GRAY, lw=2.0)                      # 3->4
    arrow(ax, 69.6, 26, 63.6, 26, color=C_GRAY, lw=2.0)                      # 4->5
    arrow(ax, 36.6, 26, 30.6, 26, color=C_GRAY, lw=2.0)                      # 5->6

    ax.text(50, 4.5,
            "核心线索：Y 稀缺而珍贵（现场观测真值），X 全域已知（空间图层）——"
            "第 2~5 步都是围绕“如何用好珍贵样本”展开的",
            ha="center", va="center", fontsize=9.6, color=C_GRAY)

    save(fig, "fig23_07_six_steps.png")


# ================================================================ 图 23-8
def fig08_feature_selection():
    """特征选择：VIF 检验多重共线性与信息增益评估因子贡献。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.6))
    fig.subplots_adjust(left=0.115, right=0.985, top=0.88, bottom=0.21,
                        wspace=0.42)

    ax = axes[0]
    factors = ["高程", "地形湿度指数", "坡度", "NDVI", "土壤类型", "降雨量",
               "岩性类型", "坡向"]
    vif = np.array([14.8, 11.3, 3.9, 2.8, 2.2, 1.9, 1.6, 1.3])
    ypos = np.arange(len(factors))[::-1]
    cols = [C_RED if v > 10 else C_BLUE for v in vif]
    ax.barh(ypos, vif, color=cols, ec="white", lw=0.6, height=0.62)
    ax.set_yticks(ypos)
    ax.set_yticklabels(factors, fontsize=10)
    ax.axvline(10, ls="--", color=C_RED, lw=1.3)
    ax.text(10.25, ypos[0] + 0.55, "VIF = 10", fontsize=9, color=C_RED)
    for y, v in zip(ypos, vif):
        ax.text(v + 0.25, y, "{:.1f}".format(v), va="center", fontsize=8.8)
    ax.set_xlim(0, 17.5)
    ax.set_ylim(-0.6, 7.9)
    ax.set_xlabel("方差膨胀因子 VIF")
    ax.set_title("(a) VIF：检验多重共线性（呼应第 6 章）", fontsize=11)
    ax.tick_params(axis="x", labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(15.3, ypos[1], "剔除", fontsize=9.5, color=C_RED, va="center",
            fontweight="bold")

    ax = axes[1]
    factors2 = ["坡度", "岩性类型", "降雨量", "高程", "地形湿度指数", "NDVI",
                "土壤类型", "坡向"]
    ig = np.array([0.42, 0.33, 0.27, 0.22, 0.17, 0.12, 0.08, 0.04])
    ypos2 = np.arange(len(factors2))[::-1]
    ax.barh(ypos2, ig, color=C_GREEN, ec="white", lw=0.6, height=0.62)
    ax.set_yticks(ypos2)
    ax.set_yticklabels(factors2, fontsize=10)
    for y, v in zip(ypos2, ig):
        ax.text(v + 0.008, y, "{:.2f}".format(v), va="center", fontsize=8.8)
    ax.set_xlim(0, 0.5)
    ax.set_xlabel("信息增益 IG")
    ax.set_title("(b) 信息增益：评估因子贡献（呼应第 8 章）", fontsize=11)
    ax.tick_params(axis="x", labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)

    fig.text(0.5, 0.035,
             "数值为示意。常用组合：先用 VIF 剔除高度共线的因子，再用信息增益排序，"
             "保留对分类贡献大的因子进入模型",
             ha="center", va="center", fontsize=9.4, color=C_GRAY)
    save(fig, "fig23_08_feature_selection.png")


# ================================================================ 图 23-9
def fig09_cv_grid():
    """交叉验证切割与网格搜索超参数。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.8),
                             gridspec_kw=dict(width_ratios=[1.05, 1.25]))
    fig.subplots_adjust(left=0.09, right=0.98, top=0.87, bottom=0.19,
                        wspace=0.30)

    # --- (a) 五折交叉验证
    ax = axes[0]
    for r in range(5):
        for c in range(5):
            fc = ORANGE_L if r == c else BLUE_L
            ec = C_ORANGE if r == c else C_BLUE
            ax.add_patch(Rectangle((c + 0.07, 4 - r + 0.07), 0.86, 0.86,
                                   fc=fc, ec=ec, lw=1.1))
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_xticks([c + 0.5 for c in range(5)])
    ax.set_xticklabels(["折 {}".format(i + 1) for i in range(5)], fontsize=9)
    ax.set_yticks([4 - r + 0.5 for r in range(5)])
    ax.set_yticklabels(["迭代 {}".format(i + 1) for i in range(5)],
                       fontsize=9)
    ax.set_title("(a) 交叉验证（CV）：把珍贵样本反复切割", fontsize=11)
    ax.text(0 + 0.5, 4 - 0 + 0.5, "验证", ha="center", va="center",
            fontsize=8.5, color=C_ORANGE, fontweight="bold")
    ax.text(1 + 0.5, 4 - 0 + 0.5, "训练", ha="center", va="center",
            fontsize=8.5, color=C_BLUE, fontweight="bold")
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)

    # --- (b) 网格搜索
    ax = axes[1]
    gammas = [10, 1, 0.1, 0.01]
    cs = [0.1, 1, 10, 100]
    acc = np.array([[0.55, 0.64, 0.70, 0.68],
                    [0.60, 0.72, 0.80, 0.78],
                    [0.62, 0.76, 0.86, 0.83],
                    [0.60, 0.70, 0.79, 0.74]])
    im = ax.imshow(acc, cmap="YlGnBu", vmin=0.5, vmax=0.9, aspect="auto")
    ax.set_xticks(range(4))
    ax.set_xticklabels(["C = {}".format(v) for v in cs], fontsize=9)
    ax.set_yticks(range(4))
    ax.set_yticklabels(["$\\gamma$ = {}".format(v) for v in gammas],
                       fontsize=9)
    ax.set_xlabel("惩罚系数 C", fontsize=10)
    ax.set_ylabel("核参数 $\\gamma$", fontsize=10)
    best = np.unravel_index(np.argmax(acc), acc.shape)
    for i in range(4):
        for j in range(4):
            tc = "white" if acc[i, j] > 0.78 else "black"
            ax.text(j, i, "{:.2f}".format(acc[i, j]), ha="center",
                    va="center", fontsize=9, color=tc)
    ax.add_patch(Rectangle((best[1] - 0.5, best[0] - 0.5), 1, 1, fill=False,
                           ec=C_RED, lw=2.4))
    ax.set_title("(b) 网格搜索超参数（以 SVM 为例，红框为最优）", fontsize=11)
    cb = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.03)
    cb.set_label("CV 平均精度（ACC）", fontsize=9)
    cb.ax.tick_params(labelsize=8.5)

    fig.text(0.5, 0.035,
             "在交叉验证的每一折上评估、取平均精度；除网格搜索外，还有随机搜索、"
             "基于梯度和智能搜索（如粒子群优化 PSO）。数值为示意",
             ha="center", va="center", fontsize=9.4, color=C_GRAY)
    save(fig, "fig23_09_cv_grid.png")


# ================================================================ 图 23-10
def fig10_multi_model_maps():
    """多模型五级易感性图对比（合成数据模拟）。"""
    fig, axes = plt.subplots(2, 3, figsize=(11.6, 7.6))
    fig.subplots_adjust(left=0.03, right=0.99, top=0.955, bottom=0.115,
                        hspace=0.14, wspace=0.08)

    base = smooth_field(rng, n=90, k=7, smin=0.10, smax=0.30)
    models = [
        ("逻辑回归（LR）", 0.10, 1.0),
        ("朴素贝叶斯（NB）", 0.18, 1.0),
        ("人工神经网络（NNET）", 0.12, 1.1),
        ("二次判别分析（QDA）", 0.08, 0.95),
        ("随机森林（RF）", 0.09, 1.25),
        ("支持向量机（SVM）", 0.10, 1.2),
    ]
    letters = "abcdef"

    # 观测滑坡点：取基准场高值区中的 14 个点
    flat = base.ravel()
    top = np.argsort(flat)[-90:]
    pick = rng.choice(top, 14, replace=False)
    py, px = np.unravel_index(pick, base.shape)
    px = px / 89
    py = py / 89

    cmap5 = ListedColormap(RAMP5)
    norm5 = cls_norm(5)
    for ax, (name, amp, sharp), letter in zip(axes.ravel(), models, letters):
        pert = smooth_field(rng, n=90, k=3, smin=0.15, smax=0.35) - 0.5
        P = (base + amp * pert - 0.5) * sharp + 0.5
        P = 0.01 + 0.98 * (P - P.min()) / (P.max() - P.min())
        bounds = np.percentile(P, [2.5, 25, 50, 75, 97.5])
        if np.any(np.diff(bounds) <= 0):
            bounds = np.maximum.accumulate(bounds) + np.arange(5) * 1e-3
        # 五个百分位切点把数轴分成六段，两端尾部分别并入最低／最高两级
        cls = np.clip(np.digitize(P, bounds) - 1, 0, 4)
        ax.imshow(cls, cmap=cmap5, extent=[0, 1, 0, 1], origin="lower",
                  interpolation="nearest", norm=norm5)
        ax.scatter(px, py, marker="^", s=26, c="black", lw=0.4)
        ax.set_title("({}) {}".format(letter, name), fontsize=10.5)
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color(C_GRAY)
            sp.set_linewidth(0.8)

    handles = [Patch(fc=RAMP5[i], ec="none", label=LAB5[i]) for i in range(5)]
    handles.append(Line2D([0], [0], marker="^", color="black", ls="none",
                          markersize=7, label="观测滑坡点"))
    fig.legend(handles=handles, loc="lower center", ncol=6, frameon=False,
               fontsize=10, bbox_to_anchor=(0.51, 0.005))
    fig.text(0.995, 0.012, "合成数据，仅作示意", ha="right", va="bottom",
             fontsize=8.5, color=C_GRAY)
    save(fig, "fig23_10_multi_model_maps.png")


# ================================================================ 主流程
if __name__ == "__main__":
    fig01_lsm_concept()
    fig02_conditioning_factors()
    fig03_binary_vs_fiveclass()
    fig04_research_trends()
    fig05_decision_tree()
    fig06_random_forest()
    fig07_six_steps()
    fig08_feature_selection()
    fig09_cv_grid()
    fig10_multi_model_maps()
    print("all done")
