# -*- coding: utf-8 -*-
"""第21章 地学应用一：水文篇 插图生成脚本（共 14 张，图 21-1 ~ 图 21-14）"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Rectangle, Polygon, Circle

# ---------- 全局风格 ----------
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["savefig.bbox"] = "tight"

OUT = r"C:\20260905\项目 人工智能与地理数据挖掘\书稿\figs\ch21"
rng = np.random.default_rng(42)

C_BLUE = "#1f77b4"
C_ORANGE = "#ff7f0e"
C_GREEN = "#2ca02c"
C_RED = "#d62728"
C_PURPLE = "#9467bd"
C_GRAY = "#7f7f7f"
C_LIGHTBLUE = "#dbe9f8"
C_LIGHTORANGE = "#fdebd7"
C_LIGHTGREEN = "#e2f2e2"
C_LIGHTGRAY = "#eeeeee"
C_LIGHTPURPLE = "#ece2f4"
C_LIGHTYELL = "#fff6df"


def box(ax, cx, cy, w, h, text, fc=C_LIGHTBLUE, ec=C_BLUE, fs=9.5, tc="#1a1a1a",
        lw=1.3, weight=None, rounding=0.06):
    p = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                       boxstyle="round,pad=0.02,rounding_size=%.3f" % rounding,
                       fc=fc, ec=ec, lw=lw)
    ax.add_patch(p)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=tc,
            linespacing=1.45, weight=weight)


def arr(ax, x1, y1, x2, y2, color=C_GRAY, lw=1.6, both=False, ls="-", cs=None, ms=13):
    style = "<|-|>" if both else "-|>"
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                linestyle=ls, mutation_scale=ms,
                                connectionstyle=cs if cs else "arc3,rad=0.0"))


def blank_ax(fig, rect, xlim, ylim):
    ax = fig.add_axes(rect)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return ax


# ----------------------------------------------------------------
# 图 21-1 两圈交集思考框架
# ----------------------------------------------------------------
def fig21_01():
    fig = plt.figure(figsize=(9.2, 6.0))
    ax = blank_ax(fig, [0.02, 0.0, 0.96, 1.0], (0, 9.6), (0, 6.6))
    e1 = Ellipse((3.0, 3.95), 5.4, 4.2, fc=C_BLUE, alpha=0.12, ec=C_BLUE, lw=1.6)
    e2 = Ellipse((6.6, 3.95), 5.4, 4.2, fc=C_ORANGE, alpha=0.14, ec=C_ORANGE, lw=1.6)
    ax.add_patch(e1)
    ax.add_patch(e2)
    ax.text(2.45, 5.42, "水文中的问题", ha="center", fontsize=11.5, weight="bold", color=C_BLUE)
    ax.text(7.15, 5.42, "机器学习的功能", ha="center", fontsize=11.5, weight="bold", color=C_ORANGE)
    ax.text(2.35, 3.85, "要素与关系形成的问题：\n预报 · 模拟 · 监测\n归因 · 情景分析……",
            ha="center", va="center", fontsize=9.5, linespacing=1.7)
    ax.text(7.25, 3.85, "聚类 · 降维\n回归 · 分类\n优化……",
            ha="center", va="center", fontsize=9.5, linespacing=1.7)
    ax.text(4.8, 3.95, "机器学习\n的水文应用", ha="center", va="center", fontsize=10.5,
            weight="bold", linespacing=1.6,
            bbox=dict(fc="white", ec="none", alpha=0.85, boxstyle="round,pad=0.3"))
    ax.text(4.8, 1.52, "应用研究前要回答的三个基本问题", ha="center",
            fontsize=10, weight="bold", color=C_GRAY)
    qs = ["问题 1：领域中有哪些问题\n可以用机器学习解决？",
          "问题 2：这些问题原有的\n方法 / 模型是什么？",
          "问题 3：这些应用研究\n进展到什么程度？"]
    for x, q in zip([1.75, 4.8, 7.85], qs):
        box(ax, x, 0.72, 2.9, 0.86, q, fc="#f5f5f5", ec=C_GRAY, fs=8.6)
    fig.savefig(f"{OUT}/fig21_01_two_circle_framework.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 图 21-2 机器学习水文应用总图
# ----------------------------------------------------------------
def fig21_02():
    fig = plt.figure(figsize=(9.6, 6.8))
    ax = blank_ax(fig, [0.02, 0.0, 0.96, 1.0], (0, 10), (0, 7))
    box(ax, 5, 3.5, 2.5, 1.2, "机器学习\n（以多层感知机为代表）", fs=10.5, weight="bold",
        fc="#cfe3f5", ec=C_BLUE, lw=1.8)
    box(ax, 5, 6.3, 2.6, 0.78, "水文事件和变量", fc=C_LIGHTORANGE, ec=C_ORANGE)
    box(ax, 1.55, 5.1, 2.5, 0.78, "遥感和其它数据", fc=C_LIGHTORANGE, ec=C_ORANGE)
    box(ax, 8.45, 5.1, 2.4, 0.78, "水文过程", fc=C_LIGHTORANGE, ec=C_ORANGE)
    box(ax, 1.55, 1.9, 2.4, 0.78, "参数化", fc=C_LIGHTGREEN, ec=C_GREEN)
    box(ax, 8.45, 1.9, 2.4, 0.78, "物理模型", fc=C_LIGHTGREEN, ec=C_GREEN)
    box(ax, 5, 0.7, 2.2, 0.78, "预测", fc=C_LIGHTPURPLE, ec=C_PURPLE)
    arr(ax, 2.75, 4.75, 3.8, 3.95, both=True)          # 遥感数据 <-> ML
    arr(ax, 5, 5.9, 5, 4.15, both=True)                # 事件和变量 <-> ML
    arr(ax, 6.3, 3.95, 7.3, 4.8, both=True)            # 水文过程 <-> ML
    arr(ax, 6.3, 3.05, 7.3, 2.35, both=True)           # 物理模型 <-> ML
    arr(ax, 3.8, 3.05, 2.7, 2.35)                      # ML -> 参数化
    arr(ax, 5, 2.85, 5, 1.15, color=C_PURPLE)          # ML -> 预测
    fig.savefig(f"{OUT}/fig21_02_ml_hydro_overview.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 图 21-3 土壤水分遥感反演框图
# ----------------------------------------------------------------
def fig21_03():
    fig = plt.figure(figsize=(10, 5.6))
    ax = blank_ax(fig, [0.02, 0.0, 0.96, 1.0], (0, 10), (0, 6))
    ax.text(1.9, 5.55, "输  入", ha="center", fontsize=11, weight="bold", color=C_GRAY)
    ax.text(5.4, 5.55, "模  型", ha="center", fontsize=11, weight="bold", color=C_BLUE)
    ax.text(8.5, 5.55, "输  出", ha="center", fontsize=11, weight="bold", color=C_GREEN)
    box(ax, 1.9, 4.05, 3.3, 1.85,
        "影响因素\n土壤特征：质地、粗糙度等\n植被特征：覆盖、冠层等\n气象特征：降雨、风速、蒸散等",
        fs=8.6, fc="#f5f5f5", ec=C_GRAY)
    box(ax, 1.9, 1.75, 3.3, 1.55,
        "电磁波谱特征\n光学反射率特征\n热红外特征\n微波后向散射系数特征\n微波亮度温度特征",
        fs=8.6, fc="#f5f5f5", ec=C_GRAY)
    box(ax, 5.4, 2.9, 2.3, 1.45, "反演模型\n（机器学习的\n回归方法）", fs=9.5,
        fc="#cfe3f5", ec=C_BLUE, lw=1.8)
    box(ax, 8.5, 2.9, 2.6, 1.45, "不同时空分辨率\n下的土壤水分", fs=9.5,
        fc=C_LIGHTGREEN, ec=C_GREEN, lw=1.6)
    arr(ax, 3.6, 4.0, 4.5, 3.3)
    arr(ax, 3.6, 1.8, 4.5, 2.5)
    arr(ax, 6.6, 2.9, 7.15, 2.9, color=C_GREEN)
    ax.text(5.0, 5.0, "（输出的土壤水分又反过来影响植被与气象过程）",
            ha="center", fontsize=8.2, color=C_GRAY)
    fig.savefig(f"{OUT}/fig21_03_soil_moisture_retrieval.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 图 21-4 降雨-径流滞后关系与 LSTM 建模
# ----------------------------------------------------------------
def fig21_04():
    fig = plt.figure(figsize=(11.4, 4.6))
    # ---- (a) 滞后关系 ----
    ax = fig.add_axes([0.07, 0.13, 0.40, 0.76])
    t = np.linspace(0, 60, 241)
    rain = 24 * np.exp(-((t - 12) ** 2) / (2 * 4.5 ** 2))
    flow = 3 + 26 * np.exp(-((t - 26) ** 2) / (2 * 8 ** 2)) \
             + 14 * np.exp(-np.maximum(t - 26, 0) / 22) * (t >= 26)
    ax.bar(t[::4], rain[::4], width=1.4, color=C_BLUE, alpha=0.65, label="降雨 $P$")
    ax.plot(t, flow, color=C_ORANGE, lw=2.2, label="出口断面流量 $Q$")
    ax.axvline(12, color=C_GRAY, ls="--", lw=0.9, alpha=0.7)
    ax.axvline(26, color=C_GRAY, ls="--", lw=0.9, alpha=0.7)
    arr(ax, 13, 40.5, 25, 40.5, color=C_RED, lw=1.4)
    ax.text(19, 41.6, "滞后", ha="center", fontsize=9, color=C_RED)
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 46)
    ax.set_xlabel("时间（天）")
    ax.set_ylabel("强度（示意）")
    ax.set_title("(a) 降雨—径流的滞后关系", fontsize=11)
    ax.legend(loc="upper right", fontsize=8.5)
    # ---- (b) LSTM 门结构 ----
    ax = blank_ax(fig, [0.53, 0.04, 0.45, 0.90], (0, 10), (0, 7.6))
    box(ax, 1.35, 4.3, 1.95, 0.75, "$h_{t-1}$\n（前一时刻输出）", fs=8.4)
    box(ax, 1.35, 2.0, 1.95, 0.75, "$x_t$\n（当前输入）", fs=8.4)
    ax.plot([2.34, 3.05], [4.3, 4.3], color=C_GRAY, lw=1.4)
    ax.plot([2.34, 3.05], [2.15, 4.24], color=C_GRAY, lw=1.4)
    ax.plot([3.05, 3.05], [2.55, 6.85], color=C_GRAY, lw=1.4)
    ax.plot(3.05, 4.3, "o", color=C_GRAY, ms=4)
    gate_ys = [6.0, 4.85, 3.7, 2.55]
    gate_txt = ["遗忘门（σ）", "输入门（σ）", "输出门（σ）", "候选状态（tanh）"]
    for gy, gt in zip(gate_ys, gate_txt):
        box(ax, 4.75, gy, 2.5, 0.6, gt, fs=8.8, fc="#eef3f9", ec=C_BLUE)
        arr(ax, 3.05, gy, 3.42, gy, lw=1.2, ms=10)
    ax.set_title("(b) LSTM：用门结构刻画滞后依赖", fontsize=11)
    arr(ax, 3.05, 6.85, 8.7, 6.85, color=C_BLUE, lw=1.8)
    ax.text(5.6, 7.22, "细胞状态 $C_{t-1}\\rightarrow C_t$（长期记忆）",
            ha="center", fontsize=9.2, color=C_BLUE)
    arr(ax, 4.75, 6.32, 4.75, 6.76, lw=1.2, ms=10, color=C_BLUE)
    ax.text(4.9, 6.52, "保留 / 遗忘", fontsize=7.8, color=C_GRAY, ha="left")
    arr(ax, 6.05, 4.9, 6.9, 6.78, lw=1.2, ms=10, color=C_BLUE, cs="arc3,rad=-0.3")
    ax.text(7.0, 5.75, "输入门控制写入", fontsize=7.8, color=C_GRAY, ha="left")
    arr(ax, 6.05, 3.7, 7.35, 3.7, lw=1.4)
    box(ax, 8.4, 3.7, 1.9, 0.78, "$h_t$（输出）", fs=8.8, fc=C_LIGHTORANGE, ec=C_ORANGE)
    arr(ax, 8.55, 6.76, 8.55, 4.15, lw=1.2, ms=10, color=C_BLUE)
    ax.text(8.72, 5.4, "输出门\n控制输出", fontsize=7.8, color=C_GRAY, ha="left",
            va="center", linespacing=1.4)
    ax.text(5.0, 0.95, "门结构恰好可以刻画滞后的气象水文变量\n（时间序列）之间的长期依赖关系",
            ha="center", fontsize=8.8, color=C_GRAY, linespacing=1.6)
    fig.savefig(f"{OUT}/fig21_04_rainfall_runoff_lstm.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 图 21-5 SWAT 代理模型
# ----------------------------------------------------------------
def fig21_05():
    fig = plt.figure(figsize=(10.6, 5.8))
    ax = blank_ax(fig, [0.02, 0.0, 0.96, 1.0], (0, 10.6), (0, 6))
    ax.plot([0.15, 10.45], [3.1, 3.1], color=C_GRAY, ls="--", lw=0.9, alpha=0.6)
    ax.text(0.45, 4.35, "训练阶段", rotation=90, ha="center", va="center",
            fontsize=10.5, weight="bold", color=C_BLUE)
    ax.text(0.45, 1.5, "应用阶段", rotation=90, ha="center", va="center",
            fontsize=10.5, weight="bold", color=C_GREEN)
    box(ax, 1.75, 4.35, 2.35, 1.15, "代表性气候情景\n＋灌溉方案等输入", fs=8.8,
        fc="#f5f5f5", ec=C_GRAY)
    box(ax, 4.45, 4.35, 2.5, 1.15, "SWAT 流域模型\n（分布式物理模型，\n运行慢）", fs=8.6,
        fc=C_LIGHTORANGE, ec=C_ORANGE)
    box(ax, 7.15, 4.35, 2.35, 1.15, "输入—输出样本对\n（几百至几千次\n模拟运行）", fs=8.6,
        fc="#f5f5f5", ec=C_GRAY)
    box(ax, 9.75, 4.35, 1.85, 1.15, "SVM\n代理模型", fs=9.5, weight="bold",
        fc="#cfe3f5", ec=C_BLUE, lw=1.8)
    arr(ax, 2.95, 4.35, 3.18, 4.35)
    arr(ax, 5.72, 4.35, 5.95, 4.35)
    arr(ax, 8.35, 4.35, 8.6, 4.35)
    box(ax, 2.4, 1.5, 3.1, 1.0, "新情景\n（未模拟过的气候/灌溉组合）", fs=8.6,
        fc=C_LIGHTGREEN, ec=C_GREEN)
    box(ax, 7.0, 1.5, 2.8, 1.0, "快速预测输出\n（径流、水质、产量等）", fs=8.6,
        fc=C_LIGHTGREEN, ec=C_GREEN)
    arr(ax, 3.98, 1.78, 8.6, 3.72, color=C_GREEN, cs="arc3,rad=-0.22")
    ax.text(6.3, 2.35, "新情景作为代理模型的输入", fontsize=8.4, color=C_GREEN,
            ha="center", rotation=8)
    arr(ax, 9.75, 3.74, 7.45, 2.05, color=C_GREEN, cs="arc3,rad=0.22")
    ax.text(9.35, 2.9, "替代 SWAT 运行，\n计算量大大降低", fontsize=8.4, color=C_GREEN,
            ha="center", rotation=-14, linespacing=1.5)
    fig.savefig(f"{OUT}/fig21_05_swat_surrogate.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 图 21-6 LSTM 偏差校正三种输入组合
# ----------------------------------------------------------------
def fig21_06():
    fig = plt.figure(figsize=(10.6, 6.6))
    ax = blank_ax(fig, [0.02, 0.0, 0.96, 1.0], (0, 10.6), (0, 7))
    rows = [
        (5.7, "情形 1", ["大气强迫", "流域属性"],
         "径流模拟\n（纯数据驱动）", C_BLUE),
        (3.6, "情形 2", ["NWM 物理模型输出", "流域属性"],
         "径流预报\n（校正 NWM 的偏差）", C_BLUE),
        (1.5, "情形 3", ["大气强迫", "NWM 物理模型输出", "流域属性"],
         "径流预报\n（结合信息最多，通常最优）", C_RED),
    ]
    for cy, tag, inputs, out_txt, oec in rows:
        ax.text(0.32, cy, tag, ha="center", va="center", fontsize=10,
                weight="bold", color=C_GRAY)
        n = len(inputs)
        if n == 2:
            ys = [cy + 0.4, cy - 0.4]
        else:
            ys = [cy + 0.78, cy, cy - 0.78]
        for it, iy in zip(inputs, ys):
            box(ax, 1.75, iy, 2.35, 0.6, it, fs=8.6, fc="#f5f5f5", ec=C_GRAY)
            arr(ax, 2.95, iy, 3.75, cy + (iy - cy) * 0.28, lw=1.3, ms=11)
        box(ax, 4.6, cy, 1.6, 0.85, "LSTM", fs=10.5, weight="bold",
            fc="#cfe3f5", ec=C_BLUE, lw=1.6)
        arr(ax, 5.42, cy, 6.05, cy, lw=1.4)
        box(ax, 7.85, cy, 3.4, 0.8, out_txt, fs=8.8, fc=C_LIGHTORANGE, ec=oec,
            lw=1.6 if oec == C_RED else 1.2)
    ax.text(5.3, 0.28,
            "NWM：美国国家水模型（基于过程的物理模型）。LSTM 以物理模型输出等为输入，"
            "对径流预报做偏差校正；输入组合包含的信息越多，校正效果通常越好。",
            ha="center", fontsize=8.2, color=C_GRAY)
    fig.savefig(f"{OUT}/fig21_06_lstm_bias_correction.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 图 21-7 径流形成过程示意
# ----------------------------------------------------------------
def fig21_07():
    fig = plt.figure(figsize=(10.4, 7.0))
    ax = blank_ax(fig, [0.01, 0.0, 0.98, 1.0], (0, 10), (0, 7.5))
    ax.add_patch(Rectangle((0, 4.2), 10, 3.3, fc="#eef6fd", ec="none"))
    # 分层剖面
    ax.add_patch(Polygon([(0, 5.3), (7.0, 4.35), (7.0, 4.3), (0, 4.3)],
                         fc="#e6d3ae", ec="none"))
    ax.add_patch(Polygon([(0, 4.3), (7.0, 4.3), (7.0, 3.5), (0, 3.5)],
                         fc="#d9bf93", ec="none"))
    ax.add_patch(Polygon([(0, 3.5), (7.0, 3.5), (7.0, 2.7), (0, 2.7)],
                         fc="#c9a97e", ec="none"))
    ax.add_patch(Polygon([(0, 2.7), (7.0, 2.7), (7.0, 0), (0, 0)],
                         fc="#b3a89a", ec="none"))
    ax.plot([0, 7.0], [5.3, 4.35], color="#6d8a3e", lw=2.4)   # 地面线
    # 河道与海洋
    ax.add_patch(Rectangle((7.0, 0), 0.9, 4.35, fc="#a6d2ef", ec=C_BLUE, lw=1.2))
    ax.add_patch(Rectangle((8.1, 0), 1.9, 4.35, fc="#a6d2ef", ec=C_BLUE, lw=1.2))
    ax.text(9.05, 2.3, "海洋", ha="center", fontsize=11.5, weight="bold",
            color="white")
    ax.text(7.45, 4.62, "河道", ha="center", fontsize=9.5, weight="bold",
            color="#0d4f86")
    arr(ax, 7.45, 4.05, 7.45, 1.45, color="#0d4f86", lw=1.8)
    ax.plot([7.45, 7.45], [1.0, 3.9], color="white", ls="--", lw=1.2)
    ax.text(7.45, 0.55, "出口断面", ha="center", fontsize=7.8, color="white")
    arr(ax, 7.92, 3.9, 8.24, 3.9, color="#0d4f86", lw=1.6)
    # 层名
    ax.text(0.25, 4.62, "土壤水（包气带）", fontsize=8.6, color="#6b5a3e", ha="left")
    ax.text(0.25, 3.92, "浅层地下水", fontsize=8.6, color="#6b5a3e", ha="left")
    ax.text(0.25, 3.12, "深层地下水", fontsize=8.6, color="#6b5a3e", ha="left")
    ax.text(0.25, 1.55, "基岩", fontsize=8.6, color="#57503f", ha="left")
    ax.text(0.3, 6.95, "大气", fontsize=9, color=C_GRAY, ha="left")
    # 植物
    for tx in [1.0, 1.7]:
        sy = 5.3 - 0.95 * tx / 7.0
        ax.plot([tx, tx], [sy, sy + 0.45], color="#8a6642", lw=2)
        ax.add_patch(Circle((tx, sy + 0.64), 0.24, fc="#4c9a4c", ec="none"))
    ax.text(1.55, 6.3, "植物截留 $I_s$", ha="center", fontsize=9.6, color="#2c6b2c")
    arr(ax, 1.25, 6.18, 1.05, 5.95, color="#4c9a4c", lw=1.0, ms=9)
    arr(ax, 1.7, 6.18, 1.74, 5.95, color="#4c9a4c", lw=1.0, ms=9)
    # 降雨
    ax.add_patch(Ellipse((2.9, 6.6), 1.9, 0.68, fc="#d6d6d6", ec=C_GRAY, lw=1.1))
    for rx in [2.3, 2.65, 3.0, 3.35, 3.7]:
        sy = 5.3 - 0.95 * rx / 7.0
        arr(ax, rx, 6.2, rx, sy + 0.07, color=C_BLUE, lw=1.1, ms=9)
    ax.text(3.85, 5.85, "$P$（降雨）", ha="left", fontsize=10.5, color=C_BLUE)
    # 蒸发与水汽输送
    arr(ax, 4.9, 4.85, 4.9, 6.35, color=C_ORANGE, lw=1.8)
    ax.text(4.9, 6.58, "蒸发 $E$", ha="center", fontsize=10, color=C_ORANGE)
    arr(ax, 9.05, 4.45, 9.05, 6.35, color=C_ORANGE, lw=1.8)
    ax.text(9.05, 6.58, "蒸发", ha="center", fontsize=10, color=C_ORANGE)
    arr(ax, 8.6, 7.0, 3.5, 7.0, color=C_GRAY, lw=1.4, ls="--", cs="arc3,rad=-0.08")
    ax.text(6.05, 7.28, "水汽输送（大循环）", ha="center", fontsize=9, color=C_GRAY)
    # 下渗
    for dx in [4.25, 4.55]:
        sy = 5.3 - 0.95 * dx / 7.0
        arr(ax, dx, sy - 0.06, dx, sy - 0.36, color=C_GREEN, lw=1.3, ms=10)
    ax.text(4.85, 4.42, "下渗", fontsize=9, color=C_GREEN, ha="left")
    # 三种径流
    arr(ax, 2.5, 5.12, 6.75, 4.42, color=C_RED, lw=2.2)
    ax.text(3.95, 5.05, "地表径流 $Q_s$", ha="center", fontsize=10.2,
            color=C_RED, weight="bold")
    arr(ax, 2.3, 3.92, 6.75, 3.92, color=C_GREEN, lw=2.2)
    ax.text(4.3, 4.06, "浅层地下径流 $Q_{g1}$", ha="center", fontsize=9.6,
            color="#1e6b1e", weight="bold")
    arr(ax, 2.3, 3.12, 6.75, 3.12, color=C_PURPLE, lw=2.2)
    ax.text(4.3, 3.26, "深层地下径流 $Q_{g2}$", ha="center", fontsize=9.6,
            color=C_PURPLE, weight="bold")
    fig.savefig(f"{OUT}/fig21_07_runoff_formation.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 图 21-8 蓄满产流 vs 超渗产流
# ----------------------------------------------------------------
def fig21_08():
    fig = plt.figure(figsize=(11.4, 4.4))
    # ---- (a) 蓄满产流 ----
    ax = fig.add_axes([0.08, 0.14, 0.38, 0.74])
    t = np.linspace(0, 100, 201)
    P = 0.35 * t
    W0 = 18.0
    t1 = W0 / 0.35
    ax.fill_between(t[t <= t1], 0, P[t <= t1], color=C_GREEN, alpha=0.28,
                    label="下渗补足土壤缺水")
    ax.fill_between(t[t >= t1], W0, P[t >= t1], color=C_BLUE, alpha=0.32,
                    label="蓄满后形成净雨")
    ax.plot(t, P, color=C_BLUE, lw=1.8, label="累积降雨 $P$")
    ax.axhline(W0, color=C_GRAY, ls="--", lw=1.4, label="土壤缺水量 $W'$（不大）")
    ax.axvline(t1, color=C_GRAY, ls=":", lw=1.0)
    ax.annotate("蓄满时刻 $t_1$", xy=(t1, W0), xytext=(60, 6.5), fontsize=9,
                color="#333333",
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 40)
    ax.set_xlabel("时间")
    ax.set_ylabel("累积量（示意）")
    ax.set_title("(a) 蓄满产流（湿润地区，土壤缺水量不大）", fontsize=10.5)
    ax.legend(loc="upper left", fontsize=7.8)
    # ---- (b) 超渗产流 ----
    ax = fig.add_axes([0.57, 0.14, 0.38, 0.74])
    tc = np.arange(5, 100, 10)
    i_bar = np.array([16, 9, 19, 6, 14, 20, 8, 5, 17, 10], dtype=float)
    tt = np.linspace(0, 100, 201)
    f_cap = 14 * np.exp(-tt / 60) + 4
    f_c = 14 * np.exp(-tc / 60) + 4
    colors = [C_ORANGE if iv > fv else C_BLUE for iv, fv in zip(i_bar, f_c)]
    ax.bar(tc, i_bar, width=8.4, color=colors, alpha=0.75,
           label="雨强 $i$")
    ax.plot(tt, f_cap, color=C_RED, lw=2.2, label="下渗能力 $f$")
    ax.annotate("$i>f$ 的时段\n产生超渗地面径流", xy=(65, 20), xytext=(40, 23.2),
                fontsize=8.8, color=C_ORANGE, linespacing=1.5,
                arrowprops=dict(arrowstyle="-|>", color=C_ORANGE, lw=1.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 26)
    ax.set_xlabel("时间")
    ax.set_ylabel("强度（示意）")
    ax.set_title("(b) 超渗产流（干旱地区，雨强大于下渗能力）", fontsize=10.5)
    ax.legend(loc="upper right", fontsize=8.5)
    fig.savefig(f"{OUT}/fig21_08_runoff_generation.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 图 21-9 自然流域 vs 城市化流域径流过程线
# ----------------------------------------------------------------
def fig21_09():
    fig = plt.figure(figsize=(8.0, 4.6))
    ax = fig.add_axes([0.11, 0.13, 0.85, 0.76])
    t = np.linspace(0, 48, 481)
    nat = 3 + 55 * np.exp(-((t - 21) ** 2) / (2 * 9.5 ** 2))
    urb = 3 + 95 * np.exp(-((t - 16) ** 2) / (2 * 4.6 ** 2))
    ax.plot(t, nat, color=C_BLUE, lw=2.2, label="自然流域")
    ax.plot(t, urb, color=C_ORANGE, lw=2.2, label="城市化流域")
    ax.axhline(3, color=C_GRAY, lw=0.8, alpha=0.6)
    ax.annotate("洪峰增大", xy=(16.2, 96), xytext=(26, 92), fontsize=9.5,
                color=C_ORANGE,
                arrowprops=dict(arrowstyle="-|>", color=C_ORANGE, lw=1.3))
    ax.annotate("峰现时间提前", xy=(16.4, 48), xytext=(27, 55), fontsize=9.5,
                color=C_ORANGE,
                arrowprops=dict(arrowstyle="-|>", color=C_ORANGE, lw=1.3))
    ax.text(1.5, 82, "城市化：不透水地面增加、雨水排水系统完善、\n"
                     "热岛 / 雨岛效应使降水增多，\n"
                     "入渗率下降、地下径流与枯水径流减小", fontsize=8.6,
            color="#333333", linespacing=1.6,
            bbox=dict(fc="#fdf3e7", ec=C_ORANGE, lw=0.8, boxstyle="round,pad=0.35"))
    ax.set_xlim(0, 48)
    ax.set_ylim(0, 108)
    ax.set_xlabel("时间（小时）")
    ax.set_ylabel("流量（示意）")
    ax.set_title("城市化对径流过程的影响（示意）", fontsize=11)
    ax.legend(loc="upper right", fontsize=9)
    fig.savefig(f"{OUT}/fig21_09_urbanization_hydrograph.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 图 21-10 中长期预报的两个时间点与时间尺度
# ----------------------------------------------------------------
def fig21_10():
    fig = plt.figure(figsize=(10.2, 5.4))
    ax = blank_ax(fig, [0.02, 0.0, 0.96, 1.0], (0, 15.6), (0, 7.6))
    # 时间轴
    arr(ax, 0, 0.9, 15.45, 0.9, color="#333333", lw=1.4)
    ticks = [(0, "10月"), (2, "12月"), (4, "2月"), (6, "4月"), (8, "6月"),
             (10, "8月"), (12, "10月"), (14, "12月")]
    for x, lab in ticks:
        ax.plot([x, x], [0.8, 0.98], color="#333333", lw=1.1)
        ax.text(x, 0.42, lab, ha="center", fontsize=8.8, color="#333333")
    # 两个时间点
    ax.plot([3, 3], [0.9, 6.9], color=C_RED, ls="--", lw=1.4)
    ax.plot([15, 15], [0.9, 6.9], color=C_RED, ls="--", lw=1.4)
    ax.text(3, 7.2, "发布时刻 T（如 12 月 31 日做预报）", ha="center",
            fontsize=9.6, color=C_RED, weight="bold")
    ax.text(15.2, 7.2, "次年 12 月 31 日", ha="right", fontsize=9, color=C_RED)
    # 三级预报尺度
    def seg(y, x0, x1, color, lw):
        ax.plot([x0, x1], [y, y], color=color, lw=lw)
        for xx in (x0, x1):
            ax.plot([xx, xx], [y - 0.09, y + 0.09], color=color, lw=lw)
    seg(5.7, 3, 15, C_BLUE, 2.6)
    ax.text(9, 6.0, "未来一年总量预报", ha="center", fontsize=9.8, color=C_BLUE)
    for k in range(4):
        seg(4.7, 3 + 3 * k, 6 + 3 * k, C_GREEN, 2.0)
    ax.text(9, 5.02, "各季（或汛期 / 枯期）预报", ha="center", fontsize=9.8, color=C_GREEN)
    for k in range(12):
        seg(3.7, 3 + k, 4 + k, C_ORANGE, 1.5)
    ax.text(9, 4.0, "各月（或各旬）预报", ha="center", fontsize=9.8, color=C_ORANGE)
    # 均值与极值示意
    tt = np.linspace(3.2, 14.8, 300)
    q = 2.05 + 0.42 * np.exp(-((tt - 9.6) ** 2) / (2 * 1.5 ** 2)) + 0.08 * np.sin(2 * tt)
    ax.plot(tt, q, color=C_GRAY, lw=1.5)
    ax.plot([3.2, 8.2], [2.16, 2.16], color=C_BLUE, ls="--", lw=1.4)
    ax.text(5.7, 2.3, "均值（如某月平均水位）", ha="center", fontsize=8.2, color=C_BLUE)
    qm = 2.05 + 0.42 + 0.08 * np.sin(2 * 9.6)
    ax.plot(9.6, qm, "o", color=C_RED, ms=6)
    ax.annotate("极值（如年度最高水位 / 流量）", xy=(9.6, qm), xytext=(10.7, 2.95),
                fontsize=8.6, color=C_RED,
                arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.1))
    # 预见期
    arr(ax, 3.05, 1.4, 14.95, 1.4, both=True, color=C_PURPLE, lw=1.5)
    ax.text(9, 1.62, "预见期：3 天以上、一年以内", ha="center", fontsize=9.4,
            color=C_PURPLE)
    fig.savefig(f"{OUT}/fig21_10_forecast_timeline.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 图 21-11 预报因子体系
# ----------------------------------------------------------------
def fig21_11():
    fig = plt.figure(figsize=(11.4, 6.2))
    ax = blank_ax(fig, [0.02, 0.0, 0.96, 1.0], (0, 12.6), (0, 7.4))
    ax.text(3.0, 6.7, "遥相关因子（大尺度信号）", ha="center", fontsize=11,
            weight="bold", color=C_BLUE)
    ax.text(9.3, 6.7, "本地相关因子（当地观测）", ha="center", fontsize=11,
            weight="bold", color=C_GREEN)
    box(ax, 3.0, 5.5, 4.9, 0.95,
        "大气环流特征：74 项环流指数（逐月）\n来源：中国国家气候中心", fs=8.5,
        fc="#f2f7fd", ec=C_BLUE)
    box(ax, 3.0, 4.3, 4.9, 0.95,
        "高空气压场：北半球 100/500 hPa 逐月平均高度场\n来源：NCEP/NCAR（1956 年起，10°×10° 格点）",
        fs=8.2, fc="#f2f7fd", ec=C_BLUE)
    box(ax, 3.0, 3.1, 4.9, 0.95,
        "海表温度：北太平洋逐月 SST 场\n来源：NOAA（1956 年起，5°×5° 格点）", fs=8.5,
        fc="#f2f7fd", ec=C_BLUE)
    box(ax, 9.3, 5.5, 4.9, 0.8, "前期降雨、气温、蒸发、日照资料", fs=8.8,
        fc="#f2fbf2", ec=C_GREEN)
    box(ax, 9.3, 4.45, 4.9, 0.9,
        "前期径流、水位（自相关）\n用 $Y_{T-1},\\ldots,Y_{T-i}$ 预报 $Y_T$ 或 $Y_{T+i}$",
        fs=8.5, fc="#f2fbf2", ec=C_GREEN)
    box(ax, 9.3, 3.4, 4.9, 0.8, "自然地理、地形资料", fs=8.8,
        fc="#f2fbf2", ec=C_GREEN)
    box(ax, 9.3, 2.35, 4.9, 0.8, "水利工程特征参数及调度运行资料", fs=8.8,
        fc="#f2fbf2", ec=C_GREEN)
    arr(ax, 3.0, 2.6, 4.3, 1.82, color=C_BLUE, lw=1.4)
    arr(ax, 9.3, 1.93, 7.0, 1.82, color=C_GREEN, lw=1.4)
    box(ax, 5.65, 1.35, 5.3, 0.9,
        "因子筛选：相关性分析 ＋ 物理成因分析\n（从众多候选因子中挑选输入变量）", fs=9,
        fc=C_LIGHTYELL, ec=C_ORANGE)
    arr(ax, 8.32, 1.35, 9.15, 1.35, color=C_ORANGE, lw=1.5)
    box(ax, 10.75, 1.35, 3.0, 0.9, "预报模型\n输入 $X$", fs=9.5, weight="bold",
        fc="#cfe3f5", ec=C_BLUE, lw=1.6)
    ax.text(6.3, 7.05,
            "气压场、海温场等格点场数据，既可筛选格点值作为因子，也可把整个场作为图像输入 CNN",
            ha="center", fontsize=8.4, color=C_GRAY,
            bbox=dict(fc="#f7f7f7", ec="none", boxstyle="round,pad=0.3"))
    fig.savefig(f"{OUT}/fig21_11_predictors.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 图 21-12 天气分类决策树示例
# ----------------------------------------------------------------
def fig21_12():
    fig = plt.figure(figsize=(8.6, 5.4))
    ax = blank_ax(fig, [0.02, 0.0, 0.96, 1.0], (0, 10), (0, 7))
    ax.add_patch(Circle((5, 6.1), 0.62, fc="#fde2d0", ec=C_ORANGE, lw=1.6))
    ax.text(5, 6.1, "节点 1\n气温", ha="center", va="center", fontsize=8.8,
            linespacing=1.4)
    ax.add_patch(Circle((2.7, 4.4), 0.62, fc="#fde2d0", ec=C_ORANGE, lw=1.6))
    ax.text(2.7, 4.4, "节点 2\n气压", ha="center", va="center", fontsize=8.8,
            linespacing=1.4)
    ax.plot([4.62, 3.05], [5.62, 4.95], color=C_GRAY, lw=1.4)
    ax.plot([5.38, 7.6], [5.62, 3.12], color=C_GRAY, lw=1.4)
    ax.plot([2.45, 1.4], [3.85, 3.12], color=C_GRAY, lw=1.4)
    ax.plot([2.95, 4.2], [3.85, 3.12], color=C_GRAY, lw=1.4)
    ax.text(3.25, 5.42, "气温 < 20°C", fontsize=9, color="#444444")
    ax.text(6.9, 4.62, "气温 ≥ 20°C", fontsize=9, color="#444444")
    ax.text(1.35, 3.62, "气压 < 500 hPa", fontsize=8.6, color="#444444")
    ax.text(4.0, 3.62, "气压 ≥ 500 hPa", fontsize=8.6, color="#444444")
    box(ax, 1.4, 2.7, 1.7, 0.85, "类别 1\n（晴）", fs=9, fc=C_LIGHTBLUE, ec=C_BLUE)
    box(ax, 4.2, 2.7, 1.7, 0.85, "类别 3\n（阴）", fs=9, fc=C_LIGHTGRAY, ec=C_GRAY)
    box(ax, 7.6, 2.7, 1.7, 0.85, "类别 2\n（雨）", fs=9, fc=C_LIGHTORANGE, ec=C_ORANGE)
    ax.text(8.15, 6.35, "圆：内部节点（属性值比较）\n方框：叶节点（类别）",
            ha="center", fontsize=8.4, color=C_GRAY, linespacing=1.6)
    ax.text(5, 1.15, "训练集：预报因子（气温、气压）的观测样本；预报变量：晴 / 阴 / 雨\n"
                     "决策树把判别规则表达得非常直观，可解释性好（图中数值仅作示意）",
            ha="center", fontsize=8.8, color="#444444", linespacing=1.7,
            bbox=dict(fc="#f7f7f7", ec=C_GRAY, lw=0.8, boxstyle="round,pad=0.4"))
    fig.savefig(f"{OUT}/fig21_12_decision_tree.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 图 21-13 HEPEX 水文集合预报流程
# ----------------------------------------------------------------
def fig21_13():
    fig = plt.figure(figsize=(11.0, 5.6))
    ax = blank_ax(fig, [0.02, 0.0, 0.96, 1.0], (0, 12.2), (0, 6.8))
    box(ax, 1.55, 5.5, 2.4, 1.0, "实测值\n（地面 / 遥感观测）", fs=8.6,
        fc="#f5f5f5", ec=C_GRAY)
    box(ax, 4.25, 5.5, 2.4, 1.0, "地面资料\n同化器", fs=9)
    box(ax, 6.95, 5.5, 2.4, 1.0, "天气与气候预报\n（数值天气预报产品）", fs=8.4,
        fc=C_LIGHTORANGE, ec=C_ORANGE)
    box(ax, 9.65, 5.5, 2.4, 1.0, "天气集合\n预处理器", fs=9,
        fc=C_LIGHTORANGE, ec=C_ORANGE)
    arr(ax, 2.77, 5.5, 3.03, 5.5)
    arr(ax, 5.47, 5.5, 5.73, 5.5)
    arr(ax, 8.17, 5.5, 8.43, 5.5)
    arr(ax, 9.65, 4.98, 9.65, 4.17, color=C_ORANGE)
    ax.text(10.0, 4.6, "集合预报", ha="left", fontsize=8.4, color=C_ORANGE)
    box(ax, 9.65, 3.55, 3.0, 1.2, "水文集合（预报）处理器\n（水文模型、集合初始条件）",
        fs=8.4, fc=C_LIGHTGREEN, ec=C_GREEN, lw=1.5)
    box(ax, 6.15, 3.55, 2.5, 1.0, "输出生产器", fs=9)
    box(ax, 2.65, 3.55, 2.5, 1.0, "成果与服务", fs=9,
        fc=C_LIGHTPURPLE, ec=C_PURPLE)
    arr(ax, 8.13, 3.55, 7.42, 3.55, color=C_GREEN)
    arr(ax, 4.88, 3.55, 3.92, 3.55, color=C_PURPLE)
    ax.text(7.78, 3.82, "单值或集合预报", ha="center", fontsize=7.8, color=C_GREEN)
    ax.text(4.4, 3.82, "可靠的水文成果", ha="center", fontsize=7.8, color=C_PURPLE)
    ax.text(4.25, 4.82, "可靠的水文输入", ha="center", fontsize=7.8, color=C_GRAY)
    box(ax, 6.1, 1.25, 10.8, 1.15,
        "核心思想：应用未来数值天气预报产品，作为水文模型的输入\n"
        "——把气象部门的“预判”作为水文预报的输入，即“我预判了你的预判”",
        fs=9.2, fc=C_LIGHTYELL, ec=C_ORANGE, lw=1.4)
    fig.savefig(f"{OUT}/fig21_13_hepex_workflow.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 图 21-14 多预报成果综合（等权平均与 BMA）
# ----------------------------------------------------------------
def fig21_14():
    fig = plt.figure(figsize=(11.2, 4.4))
    lead = np.arange(1, 31)
    base = 130 * np.exp(-lead / 11) + 35
    biases = [8, -6, 14, -12]
    colors = [C_BLUE, C_ORANGE, C_GREEN, C_PURPLE]
    models = []
    for b in biases:
        noise = np.cumsum(rng.normal(0, 1.8, lead.size))
        models.append(base + b + noise - noise[0])
    models = np.array(models)
    weights = np.array([0.40, 0.28, 0.20, 0.12])
    # ---- (a) 等权平均 ----
    ax = fig.add_axes([0.075, 0.13, 0.38, 0.75])
    for m, c in zip(models, colors):
        ax.plot(lead, m, color=c, lw=1.4, alpha=0.85)
    ax.plot(lead, models.mean(axis=0), color="#222222", lw=2.4, ls="--",
            label="等权平均（综合结果）")
    ax.set_xlim(1, 30)
    ax.set_xlabel("预见期（天）")
    ax.set_ylabel("流量（示意）")
    ax.set_title("(a) 多模型预报成果与等权平均", fontsize=10.5)
    ax.legend(["模型 1", "模型 2", "模型 3", "模型 4", "等权平均（综合结果）"],
              loc="upper right", fontsize=7.8)
    # ---- (b) BMA 加权 ----
    ax = fig.add_axes([0.565, 0.13, 0.38, 0.75])
    labs = ["模型 1（w=%.2f）" % weights[0], "模型 2（w=%.2f）" % weights[1],
            "模型 3（w=%.2f）" % weights[2], "模型 4（w=%.2f）" % weights[3]]
    for m, c, lb in zip(models, colors, labs):
        ax.plot(lead, m, color=c, lw=1.3, alpha=0.55, label=lb)
    bma = (weights[:, None] * models).sum(axis=0)
    ax.plot(lead, bma, color=C_RED, lw=2.6, label="BMA 加权综合")
    ax.set_xlim(1, 30)
    ax.set_xlabel("预见期（天）")
    ax.set_ylabel("流量（示意）")
    ax.set_title("(b) 基于贝叶斯理论（BMA）的自动赋权综合", fontsize=10.5)
    ax.legend(loc="upper right", fontsize=7.4)
    fig.savefig(f"{OUT}/fig21_14_ensemble_combination.png")
    plt.close(fig)


if __name__ == "__main__":
    for fn in [fig21_01, fig21_02, fig21_03, fig21_04, fig21_05, fig21_06,
               fig21_07, fig21_08, fig21_09, fig21_10, fig21_11, fig21_12,
               fig21_13, fig21_14]:
        fn()
        print("done", fn.__name__)
