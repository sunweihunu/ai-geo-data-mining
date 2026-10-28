# -*- coding: utf-8 -*-
"""第22章 地学应用二：气象篇 插图生成脚本。

运行方式（Windows，python 不可直接用）：
    uv run --no-project --with matplotlib --with numpy python tmp_fig22/gen_figures.py
输出：书稿/figs/ch22/fig22_01_*.png ... fig22_14_*.png
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

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

rng = np.random.default_rng(42)

OUT = r"C:\20260905\项目 人工智能与地理数据挖掘\书稿\figs\ch22"
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print("saved:", name)


def new_canvas(figsize=(10, 6)):
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


def smooth_field(rng_, n=48, corr=6.0, amp=1.0):
    """FFT 高斯平滑随机场（不依赖 scipy）。"""
    noise = rng_.standard_normal((n, n))
    k = np.fft.fftfreq(n)
    KX, KY = np.meshgrid(k, k)
    filt = np.exp(-2.0 * (np.pi ** 2) * (corr ** 2) * (KX ** 2 + KY ** 2))
    f = np.fft.ifft2(np.fft.fft2(noise) * filt).real
    f = (f - f.mean()) / (f.std() + 1e-12)
    return f * amp


# ================================================================ fig22_01
def fig22_01_objects():
    """气象的研究对象、内涵与问题（分层框图/表）。"""
    fig, ax = new_canvas(figsize=(10.5, 5.6))
    x0, x1, x2, x3 = 1.0, 16.0, 60.0, 99.0
    ytop, ybot = 97.0, 4.0
    rows = [
        ("化学成分", "二氧化碳、臭氧、水汽、PM2.5、PM10", "时空分布"),
        ("物理要素", "降雨、温度、辐射、湿度、气压、风", "天气预报"),
        ("大气运动", "气压场、驱动力、特殊风、大气环流", "分类、预测"),
        ("天气系统", "气团、锋、气旋与反气旋、副热带高压", "分类、预测"),
        ("气象灾害", "寒潮、霜冻、干旱、洪涝、台风、雾霾、沙尘暴", "分类、极值预测"),
        ("气候", "类型、变化、特殊信号或现象、影响因素", "特征识别、气候预测"),
    ]
    hh = 8.0                                   # 表头高
    rh = (ytop - hh - ybot) / len(rows)
    # 表头
    for xe0, xe1, txt in ((x0, x1, "对象"), (x1, x2, "内涵"),
                          (x2, x3, "问题（对应的机器学习功能）")):
        ax.add_patch(Rectangle((xe0, ytop - hh), xe1 - xe0, hh,
                               fc=C_BLUE, ec="white", lw=1.2))
        ax.text((xe0 + xe1) / 2, ytop - hh / 2, txt, ha="center", va="center",
                fontsize=12, color="white", fontweight="bold")
    # 数据行
    for i, (a, b, c) in enumerate(rows):
        yb = ytop - hh - (i + 1) * rh
        fc = GRAY_L if i % 2 == 0 else "#ffffff"
        ax.add_patch(Rectangle((x0, yb), x1 - x0, rh, fc=BLUE_L,
                               ec=C_GRAY, lw=0.8))
        ax.add_patch(Rectangle((x1, yb), x2 - x1, rh, fc=fc,
                               ec=C_GRAY, lw=0.8))
        ax.add_patch(Rectangle((x2, yb), x3 - x2, rh, fc=ORANGE_L,
                               ec=C_GRAY, lw=0.8))
        ax.text((x0 + x1) / 2, yb + rh / 2, a, ha="center", va="center",
                fontsize=11, fontweight="bold")
        ax.text((x1 + x2) / 2, yb + rh / 2, b, ha="center", va="center",
                fontsize=10.5)
        ax.text((x2 + x3) / 2, yb + rh / 2, c, ha="center", va="center",
                fontsize=10.5, color=C_BLUE, fontweight="bold")
    save(fig, "fig22_01_objects.png")


# ================================================================ fig22_02
def fig22_02_ml_views():
    """从机器学习角度看应用：独立模型 / 与物理模型集成。"""
    fig, ax = new_canvas(figsize=(10.5, 6.2))
    box(ax, 28, 89, 44, 8, "机器学习的气象应用：两条路径",
        fc=C_BLUE, ec=C_BLUE, tc="white", fontsize=12.5, weight="bold")
    arrow(ax, 38, 88.5, 26, 80, color=C_GRAY)
    arrow(ax, 62, 88.5, 74, 80, color=C_GRAY)
    # 左：独立模型
    box(ax, 4, 72, 44, 8, "ML 作为独立模型",
        fc=BLUE_L, ec=C_BLUE, fontsize=12, weight="bold")
    left_items = [
        "处理多类型气象数据、构建基础数据集",
        "近似气象过程",
        "生成有关气象过程的新知识",
        "天气预报",
        "气候预测",
    ]
    y = 61
    for it in left_items:
        box(ax, 6, y, 40, 7.6, it, fc="#ffffff", ec=C_BLUE, fontsize=10.5)
        y -= 10.2
    # 右：与物理模型集成
    box(ax, 52, 72, 44, 8, "ML 与物理模型（数值模式）集成",
        fc=ORANGE_L, ec=C_ORANGE, fontsize=12, weight="bold")
    right_items = [
        "帮助基于过程的模型参数化",
        "开发快速代理",
        "纠正物理模型（数值模式）的偏差",
        "将物理知识与 ML 相结合",
    ]
    y = 61
    for it in right_items:
        box(ax, 54, y, 40, 7.6, it, fc="#ffffff", ec=C_ORANGE, fontsize=10.5)
        y -= 10.2
    # 底注
    ax.text(26, 4.5, "把 ML 当作通用工具，直接求解气象问题",
            ha="center", va="center", fontsize=10.5, color=C_BLUE)
    ax.text(74, 5.8, "前三项：ML 支持物理模型",
            ha="center", va="center", fontsize=10.5, color=C_ORANGE)
    ax.text(74, 2.2, "第四项：物理知识反哺 ML（方向相反）",
            ha="center", va="center", fontsize=10.5, color=C_ORANGE)
    save(fig, "fig22_02_ml_views.png")


# ================================================================ fig22_03
def fig22_03_nwp_def():
    """数值天气预报的定义：输入—求解—输出。"""
    fig, ax = new_canvas(figsize=(10.5, 5.8))
    box(ax, 4, 62, 26, 15, "初始条件\n（初始时刻的大气状态，\n时间上的条件）",
        fc=BLUE_L, ec=C_BLUE, fontsize=10.5)
    box(ax, 4, 40, 26, 15, "边界条件\n（区域边界上的大气状态，\n空间上的条件）",
        fc=BLUE_L, ec=C_BLUE, fontsize=10.5)
    box(ax, 38, 42, 28, 32,
        "数值求解\n大气运动方程组\n\n模式方程：\n大气动力学＋物理过程\n\n数值方法：\n资料同化＋数值求解",
        fc="#ffffff", ec=C_RED, lw=1.6, fontsize=10.5)
    box(ax, 74, 52, 23, 14, "未来时刻的\n大气状态（预报）",
        fc=GREEN_L, ec=C_GREEN, fontsize=11, weight="bold")
    arrow(ax, 30.5, 69.5, 37.5, 64)
    arrow(ax, 30.5, 47.5, 37.5, 52)
    arrow(ax, 66.5, 58, 73.5, 58)
    # 底部：从 ML 视角看输入 / 训练 / 预测
    box(ax, 4, 10, 26, 12, "输入\n（X）", fc=GRAY_L, ec=C_GRAY, fontsize=11)
    box(ax, 38, 6, 28, 20,
        "训练 / 验证\n通常不做训练：\n参数按物理意义由观测\n与实验直接给定",
        fc=RED_L, ec=C_RED, fontsize=10)
    box(ax, 74, 10, 23, 12, "预测\n（未来状态 Y）",
        fc=GRAY_L, ec=C_GRAY, fontsize=11)
    ax.plot([17, 17], [39, 22.5], color=C_GRAY, lw=1.0, ls=":")
    ax.plot([52, 52], [41.5, 26.5], color=C_GRAY, lw=1.0, ls=":")
    ax.plot([85.5, 85.5], [51.5, 22.5], color=C_GRAY, lw=1.0, ls=":")
    save(fig, "fig22_03_nwp_def.png")


# ================================================================ fig22_04
def fig22_04_equations():
    """模式方程组成：网格尺度显式计算 vs 次网格参数化。"""
    fig, ax = new_canvas(figsize=(11, 6.0))
    # 左面板：大气动力学
    box(ax, 2, 8, 46, 86, "", fc=BLUE_L, ec=C_BLUE, lw=1.4)
    ax.text(25, 88.5, "大气动力学：网格尺度过程", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=C_BLUE)
    # 画网格
    gx0, gx1, gy0, gy1 = 7, 43, 60, 82
    for xx in np.linspace(gx0, gx1, 8):
        ax.plot([xx, xx], [gy0, gy1], color=C_BLUE, lw=0.8, alpha=0.55)
    for yy in np.linspace(gy0, gy1, 5):
        ax.plot([gx0, gx1], [yy, yy], color=C_BLUE, lw=0.8, alpha=0.55)
    ax.text(25, 54, "把空间划分成网格，网格尺度（可分辨尺度）\n"
                    "动力过程可由模式动力框架显式计算",
            ha="center", va="center", fontsize=10.2)
    box(ax, 6, 30, 38, 16,
        "运动方程、连续方程、热力学能量方程、\n状态方程、水汽方程",
        fc="#ffffff", ec=C_BLUE, fontsize=10.5)
    ax.text(25, 20, "物理依据：牛顿第二定律、质量守恒、\n能量守恒、水汽守恒定律",
            ha="center", va="center", fontsize=10.2)
    # 右面板：物理过程
    box(ax, 52, 8, 46, 86, "", fc=ORANGE_L, ec=C_ORANGE, lw=1.4)
    ax.text(75, 88.5, "物理过程：次网格参数化", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=C_ORANGE)
    # 粗网格 + 芯片
    gx0, gx1, gy0, gy1 = 57, 93, 66, 84
    for xx in np.linspace(gx0, gx1, 4):
        ax.plot([xx, xx], [gy0, gy1], color=C_ORANGE, lw=1.0, alpha=0.6)
    for yy in np.linspace(gy0, gy1, 3):
        ax.plot([gx0, gx1], [yy, yy], color=C_ORANGE, lw=1.0, alpha=0.6)
    chips = ["积云对流", "边界层湍流混合", "长短波辐射", "地形作用",
             "云与水文过程", "海洋与陆面过程"]
    cx = [65.5, 84.5]
    cy = [79, 72.5, 66]
    k = 0
    for yy in cy:
        for xx in cx:
            box(ax, xx - 8.2, yy - 2.6, 16.4, 5.2, chips[k],
                fc="#ffffff", ec=C_ORANGE, fontsize=9.6)
            k += 1
    ax.text(75, 54, "次网格尺度过程不能被显式分辨，\n"
                    "用可分辨尺度的参数化表示",
            ha="center", va="center", fontsize=10.2)
    box(ax, 56, 30, 38, 16,
        "积云对流、行星边界层的湍流混合、\n长短波辐射、地形等",
        fc="#ffffff", ec=C_ORANGE, fontsize=10.5)
    ax.text(75, 20, "参数化 = 用少量参数近似表达\n次网格物理过程的整体效应",
            ha="center", va="center", fontsize=10.2)
    save(fig, "fig22_04_equations.png")


# ================================================================ fig22_05
def fig22_05_da():
    """资料同化：观测 + 预报 → 分析场（初值）。"""
    fig, ax = new_canvas(figsize=(11, 5.4))
    # 左上：观测
    box(ax, 2, 52, 24, 42, "", fc="#ffffff", ec=C_BLUE, lw=1.3)
    ax.text(14, 90.5, "观测资料（站点）", ha="center", va="center",
            fontsize=11, fontweight="bold", color=C_BLUE)
    axo = fig.add_axes([0.035, 0.585, 0.195, 0.27])
    n = 26
    xs = rng.uniform(0, 1, n)
    ys = rng.uniform(0, 1, n)
    vals = rng.uniform(0.4, 1.0, n)
    axo.scatter(xs, ys, s=42, c=vals, cmap="Blues", vmin=0, vmax=1.2,
                edgecolors=C_BLUE, linewidths=0.6)
    axo.set_xticks([])
    axo.set_yticks([])
    # 左下：背景场
    box(ax, 2, 5, 24, 42, "", fc="#ffffff", ec=C_ORANGE, lw=1.3)
    ax.text(14, 43.5, "模式预报场（背景场）", ha="center", va="center",
            fontsize=11, fontweight="bold", color=C_ORANGE)
    axb = fig.add_axes([0.035, 0.115, 0.195, 0.27])
    fld = smooth_field(rng, n=48, corr=7.0)
    axb.imshow(fld, cmap="RdBu_r", vmin=-2, vmax=2, origin="lower")
    axb.set_xticks([])
    axb.set_yticks([])
    # 中：资料同化
    box(ax, 33, 18, 32, 62,
        "资料同化\n（求解数值预报的反问题）\n\n函数拟合、逐步订正（SC）、\n最优插值（OI）、\n"
        "三维变分、四维变分 /\n增量四维变分、卡尔曼滤波\n\n利用现有的所有信息\n（观测与预测值），\n"
        "定义最大可能精确的\n大气（海洋）运动状态",
        fc=GRAY_L, ec=C_PURPLE, lw=1.5, fontsize=10.3)
    arrow(ax, 26.5, 73, 32.5, 62)
    arrow(ax, 26.5, 26, 32.5, 36)
    # 右上：分析场
    box(ax, 70, 52, 24, 42, "", fc="#ffffff", ec=C_GREEN, lw=1.3)
    ax.text(82, 90.5, "分析场", ha="center", va="center",
            fontsize=11, fontweight="bold", color=C_GREEN)
    axa = fig.add_axes([0.715, 0.585, 0.195, 0.27])
    fld2 = smooth_field(rng, n=48, corr=7.0)
    axa.imshow(0.6 * fld + 0.4 * fld2, cmap="RdBu_r", vmin=-2, vmax=2,
               origin="lower")
    axa.set_xticks([])
    axa.set_yticks([])
    arrow(ax, 65.5, 49, 72, 60)
    # 右下：模式积分
    box(ax, 70, 8, 24, 22, "作为预报模式的初值\n进入模式积分",
        fc=GREEN_L, ec=C_GREEN, fontsize=10.8, weight="bold")
    arrow(ax, 82, 51.5, 82, 31)
    save(fig, "fig22_05_da.png")


# ================================================================ fig22_06
def fig22_06_history():
    """数值天气预报的发展时间线。"""
    fig, ax = new_canvas(figsize=(11.5, 5.6))
    # 主时间轴
    ax.annotate("", xy=(97, 60), xytext=(3, 60),
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=2.2))
    nodes = [
        (8, "20 世纪初", "Abbe 与 Bjerknes：\n天气预报＝数学物理\n中的初值问题", True),
        (24, "1916—1918", "Richardson\n第一次尝试\n数值天气预报", False),
        (39, "1922", "出版专著：首次简化\n数值计算，降低\n方程组复杂度", True),
        (55, "1950", "Charney、Fjortoft、Neumann\n用计算机制作 24 小时\n天气形势预报\n——现代数值天气预报开始", False),
        (73, "1960—1970 年代", "中期预报试验与业务化；\n超算可求解整套方程组", True),
        (89, "今天", "天气—气候无缝隙对接\n与集合预报", False),
    ]
    for x, yr, txt, above in nodes:
        ax.plot([x], [60], marker="o", ms=9, color=C_BLUE, zorder=5)
        if above:
            ax.plot([x, x], [60, 72], color=C_GRAY, lw=1.0)
            ax.text(x, 73.5, yr, ha="center", va="bottom", fontsize=11,
                    fontweight="bold", color=C_RED)
            ax.text(x, 76, txt, ha="center", va="bottom", fontsize=9.4,
                    linespacing=1.4)
        else:
            ax.plot([x, x], [60, 48], color=C_GRAY, lw=1.0)
            ax.text(x, 46.5, yr, ha="center", va="top", fontsize=11,
                    fontweight="bold", color=C_RED)
            ax.text(x, 44, txt, ha="center", va="top", fontsize=9.4,
                    linespacing=1.4)
    # 底部：模式演化
    ax.text(3, 24, "模式演化", ha="left", va="center", fontsize=11.5,
            fontweight="bold", color=C_PURPLE)
    stages = ["数值天气预报模式", "大气环流模式", "海气耦合模式", "地球系统模式"]
    x = 3
    ws = [20, 18, 18, 20]
    for i, (s, w) in enumerate(zip(stages, ws)):
        box(ax, x, 6, w, 11, s, fc=PURPLE_L, ec=C_PURPLE, fontsize=10.6)
        if i < 3:
            arrow(ax, x + w + 0.4, 11.5, x + w + 5.2, 11.5, color=C_PURPLE)
        x += w + 5.6
    save(fig, "fig22_06_history.png")


# ================================================================ fig22_07
def fig22_07_timescale():
    """预报分类的时间尺度轴。"""
    fig = plt.figure(figsize=(11.5, 4.8))
    ax = fig.add_axes([0.05, 0.12, 0.90, 0.78])
    ax.set_xscale("log")
    ax.set_xlim(0.9, 40000)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    bands = [
        (0.9, 2, "临近预报\n0~2 h", "#aec7e8"),
        (2, 12, "短时预报\n0~12 h", "#aec7e8"),
        (12, 72, "短期预报\n0~3 d", "#98df8a"),
        (72, 240, "中期预报\n3~10 d", "#98df8a"),
        (240, 720, "延伸期预报\n10~30 d", "#ffbb78"),
        (720, 40000, "气候预测\n30 d 以上", "#ff9896"),
    ]
    for xa, xb, txt, fc in bands:
        ax.add_patch(Rectangle((xa, 0.42), xb - xa, 0.22, fc=fc,
                               ec="white", lw=1.2))
        xm = np.sqrt(xa * xb) if xb < 30000 else 9000
        ax.text(xm, 0.53, txt, ha="center", va="center", fontsize=10.0,
                linespacing=1.4)
    # 主刻度
    ticks = [2, 12, 72, 240, 720]
    labels = ["2 h", "12 h", "3 d", "10 d", "30 d"]
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, fontsize=10.5)
    ax.minorticks_off()
    for t in ticks:
        ax.plot([t, t], [0.40, 0.42], color=C_GRAY, lw=1.2)
    ax.set_xlabel("预报时效（对数尺度）", fontsize=11)
    ax.tick_params(axis="x", length=0)
    # 顶部分组
    ax.plot([0.9, 720], [0.88, 0.88], color=C_BLUE, lw=2.0)
    ax.plot([0.9, 0.9], [0.84, 0.88], color=C_BLUE, lw=2.0)
    ax.plot([720, 720], [0.84, 0.88], color=C_BLUE, lw=2.0)
    ax.text(30, 0.905, "天气预报（30 天以内）", ha="center", va="bottom",
            fontsize=11.5, fontweight="bold", color=C_BLUE)
    ax.annotate("", xy=(40000, 0.88), xytext=(740, 0.88),
                arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=2.0))
    ax.plot([740, 740], [0.84, 0.88], color=C_RED, lw=2.0)
    ax.text(9500, 0.905, "气候预测（30 天以上）", ha="center", va="bottom",
            fontsize=11.5, fontweight="bold", color=C_RED)
    # 底部：极端预报
    ax.plot([0.9, 720], [0.30, 0.30], color=C_GREEN, lw=1.6, ls="--")
    ax.text(30, 0.20, "极端天气预报：强降雨雪、空气质量、冰雹",
            ha="center", va="center", fontsize=10.2, color=C_GREEN)
    ax.annotate("", xy=(40000, 0.30), xytext=(740, 0.30),
                arrowprops=dict(arrowstyle="-", color=C_PURPLE, lw=1.6,
                                linestyle="--"))
    ax.text(9500, 0.20, "极端气候预测：极端降雨、极端温度、厄尔尼诺",
            ha="center", va="center", fontsize=10.2, color=C_PURPLE)
    # 薄弱区
    ax.add_patch(Rectangle((240, 0.05), 8760 - 240, 0.07, fc=RED_L,
                           ec=C_RED, lw=0.8, ls=":"))
    ax.text(np.sqrt(240 * 8760), 0.085, "延伸期—季节—年尺度：相对薄弱区",
            ha="center", va="center", fontsize=9.6, color=C_RED)
    # 气候预测细分
    ax.text(720, 0.365, "次季节 / 季节 / 年度 / 气候变化预测；可外推数年至数十年以上",
            ha="left", va="center", fontsize=9.2, color=C_GRAY)
    save(fig, "fig22_07_timescale.png")


# ================================================================ fig22_08
def fig22_08_compare():
    """机器学习与数值天气预报的比较。"""
    fig, ax = new_canvas(figsize=(10.5, 6.4))
    box(ax, 8, 85, 84, 12,
        "相同点：根据已知先验信息预测未知；数据都具有高维、海量、异构的特点；\n"
        "可完成同样的预测功能；都可以以规律和知识的获取为目标",
        fc=GRAY_L, ec=C_GRAY, fontsize=10.8)
    # 左：机器学习
    box(ax, 4, 38, 44, 40, "", fc=BLUE_L, ec=C_BLUE, lw=1.5)
    ax.text(26, 71.5, "机器学习", ha="center", va="center", fontsize=13,
            fontweight="bold", color=C_BLUE)
    ax.text(7, 42, "· 数据驱动，隐式表达规律\n"
                   "· 规律的表达较为晦涩，\n   可解释性不足\n"
                   "· 但能够自动、快速地实现，\n   是普适的通用框架",
            ha="left", va="bottom", fontsize=10.8, linespacing=1.75)
    # 右：数值天气预报
    box(ax, 52, 38, 44, 40, "", fc=ORANGE_L, ec=C_ORANGE, lw=1.5)
    ax.text(74, 71.5, "数值天气预报模式", ha="center", va="center",
            fontsize=13, fontweight="bold", color=C_ORANGE)
    ax.text(55, 42, "· 理论知识驱动，将气象规律\n   以数学物理公式显式表达\n"
                   "· 规律的表达更加清晰、准确\n"
                   "· 但认识过程缓慢，是针对\n   特定规律的特殊表达",
            ha="left", va="bottom", fontsize=10.8, linespacing=1.75)
    arrow(ax, 26, 84.5, 26, 79)
    arrow(ax, 74, 84.5, 74, 79)
    # 底：殊途同归
    box(ax, 8, 10, 84, 16,
        "殊途同归：相互借鉴、相互融合\n"
        "大型深度学习模型的预报效果已能与数值天气模式媲美，且推理速度更快",
        fc=GREEN_L, ec=C_GREEN, lw=1.5, fontsize=11)
    arrow(ax, 26, 37.5, 26, 26.5)
    arrow(ax, 74, 37.5, 74, 26.5)
    save(fig, "fig22_08_compare.png")


# ================================================================ fig22_09
def fig22_09_three():
    """机器学习发展三要素：算法、算力、数据。"""
    fig, ax = new_canvas(figsize=(10.8, 6.2))
    box(ax, 24, 88, 52, 9, "机器学习发展的三要素",
        fc=C_BLUE, ec=C_BLUE, tc="white", fontsize=13, weight="bold")
    cols = [
        (3, "算法（方法）", C_BLUE, BLUE_L,
         "· 可解释性研究：模型结构或参数\n  的可视化分析、因果网络开发\n"
         "· 模型迁移：微调、基于样本 /\n  特征 / 模型的迁移\n"
         "· 鲁棒性分析：多采用样本攻击\n"
         "· 自动超参数寻优：AutoML 框架、\n  网络结构搜索、强化学习"),
        (35.5, "算力（软硬件）", C_ORANGE, ORANGE_L,
         "· 软件框架：Scikit-learn、\n  Keras、TensorFlow、PyTorch\n"
         "· GPU 计算库：CUDA、CuDNN\n"
         "· 硬件：神经网络芯片、专用\n  加速硬件（TPU）、GPU / FPGA\n"
         "· 异构超级计算机：Summit 等"),
        (68, "数据（数据集）", C_GREEN, GREEN_L,
         "· 标准数据集的建立与公开发布\n"
         "· 经典数据集：mnist、\n  cifar10 / cifar100、imagenet\n"
         "· 支撑算法研发与客观比较\n"
         "· 地学数据保守、不公开——\n  当前短板，大有可为"),
    ]
    for x, title, ec, fc, body in cols:
        box(ax, x, 14, 29, 70, "", fc=fc, ec=ec, lw=1.5)
        ax.text(x + 14.5, 76, title, ha="center", va="center", fontsize=12.5,
                fontweight="bold", color=ec)
        ax.text(x + 1.8, 66, body, ha="left", va="top", fontsize=10.0,
                linespacing=1.8)
        arrow(ax, x + 14.5, 87.5, x + 14.5, 85)
    save(fig, "fig22_09_three.png")


# ================================================================ fig22_10
def fig22_10_pipeline():
    """机器学习在气象预报中的常规应用步骤。"""
    fig, ax = new_canvas(figsize=(11, 4.9))
    box(ax, 1.5, 55, 22, 30,
        "输入\n二维 / 三元多元时空\n观测资料\n（地面站、卫星、雷达、\n再分析资料等）",
        fc=BLUE_L, ec=C_BLUE, fontsize=10.2)
    box(ax, 27.5, 55, 20, 30,
        "预处理\n质量控制、缺测填补、\n归一化、时空配准",
        fc="#ffffff", ec=C_GRAY, fontsize=10.2)
    box(ax, 51.5, 55, 22, 30,
        "模型\n全连接网络、CNN、\nLSTM 等\n机器学习 / 深度学习模型",
        fc=ORANGE_L, ec=C_ORANGE, fontsize=10.2)
    box(ax, 77.5, 55, 21, 30,
        "输出\n网格化的类别、\n数值或概率",
        fc=GREEN_L, ec=C_GREEN, fontsize=10.2)
    arrow(ax, 24, 70, 27, 70)
    arrow(ax, 48, 70, 51, 70)
    arrow(ax, 74, 70, 77, 70)
    box(ax, 12, 10, 76, 24,
        "独立于传统的数值预报过程：以观测资料为输入、直接输出预报结果；\n"
        "自动捕捉输入资料中的时空特征并快速推理；\n"
        "预报精度与数值天气预报模式相近甚至更高，推理速度优势明显",
        fc=GRAY_L, ec=C_GRAY, fontsize=10.8)
    save(fig, "fig22_10_pipeline.png")


# ================================================================ fig22_11
def fig22_11_xai():
    """可解释性研究的五类方法。"""
    fig, ax = new_canvas(figsize=(11.5, 6.4))
    ax.text(50, 96.5, "两大挑战：① 弱解释性（规律晦涩、知识发现困难）；"
                      "② 理论知识指导下的模型设计",
            ha="center", va="center", fontsize=11, fontweight="bold",
            color=C_RED)
    box(ax, 38, 44, 24, 14, "可解释性研究\n（打开黑盒）",
        fc=PURPLE_L, ec=C_PURPLE, lw=1.8, fontsize=12, weight="bold")
    items = [
        (2, 74, "① 特征分析\n特征选择量化输入对降水的贡献（Manandhar 等）；\n"
                "打开卷积层分析特征图与冰雹生成过程（Gagne 等）", "left"),
        (2, 47, "② 样本权重差异化\n预报点附近样本赋予更大权重（Karevan 等）；\n"
                "利用多观测点相关性（Qiu 等）", "left"),
        (2, 20, "③ 注意力机制\n双因素注意力的多变量编码—解码模型，\n"
                "识别关键变量与区域（Yuan 等）", "left"),
        (66, 60, "④ 基于物理机制定制化目标函数\nSSIM 与 MSE / MAE 结合作训练目标"
                 "（Prasetya 等）；\n预报员损失函数（Tan 等）", "left"),
        (66, 28, "⑤ 本身可解释性好的模型\n决策树、贝叶斯网络等，\n"
                 "直接选用而无需打开黑盒", "left"),
    ]
    for x, y, txt, al in items:
        box(ax, x, y, 32, 17, txt, fc="#ffffff", ec=C_PURPLE,
            fontsize=9.8, align=al)
    arrows = [((34, 80), (46, 57)), ((34, 55), (39, 53)),
              ((34, 30), (44, 45)), ((66, 68), (61, 57)),
              ((66, 38), (61, 47))]
    for (x1, y1), (x2, y2) in arrows:
        arrow(ax, x1, y1, x2, y2, color=C_PURPLE, lw=1.3)
    ax.text(50, 4, "目标：引入气象知识，改善模型的鲁棒性、增强可解释性、减小不确定性",
            ha="center", va="center", fontsize=11, color=C_GREEN,
            fontweight="bold")
    save(fig, "fig22_11_xai.png")


# ================================================================ fig22_12
def fig22_12_ensemble():
    """集合预报与概率预报：成员差异 → 概率分布。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.8),
                                   gridspec_kw={"width_ratios": [1.5, 1]},
                                   constrained_layout=True)
    t = np.linspace(0, 48, 97)
    m = 12
    steps = rng.standard_normal((m, len(t) - 1))
    devs = np.cumsum(steps, axis=1) * 0.16
    devs = np.hstack([np.zeros((m, 1)), devs])
    members = 8.0 + 0.05 * t + devs * np.sqrt(1 + t / 12.0)
    for i in range(m):
        ax1.plot(t, members[i], color=C_BLUE, lw=0.9, alpha=0.55)
    ax1.plot(t, members.mean(axis=0), color=C_RED, lw=2.4, label="集合均值")
    tstar = 42
    ax1.axvline(tstar, color=C_GRAY, lw=1.4, ls="--")
    ax1.fill_between(t,
                     members.mean(axis=0) - 1.65 * members.std(axis=0),
                     members.mean(axis=0) + 1.65 * members.std(axis=0),
                     color=C_BLUE, alpha=0.12, label="约 90% 区间")
    ax1.set_xlabel("预报时间（h）", fontsize=11)
    ax1.set_ylabel("预报要素（如降水量，mm）", fontsize=11)
    ax1.set_title("集合成员：初始与模式不确定性随时间放大", fontsize=11.5)
    ax1.legend(fontsize=9.5, loc="upper left")
    vals = members[:, np.argmin(np.abs(t - tstar))]
    ax2.hist(vals, bins=8, density=True, orientation="horizontal",
             color=BLUE_L, edgecolor=C_BLUE)
    grid = np.linspace(vals.min() - 1.5, vals.max() + 1.5, 200)
    mu, sd = vals.mean(), vals.std()
    pdf = np.exp(-0.5 * ((grid - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
    ax2.plot(pdf, grid, color=C_RED, lw=2.0, label="概率分布")
    ax2.axhline(mu, color=C_RED, lw=1.2, ls=":")
    q10, q90 = np.percentile(vals, [10, 90])
    ax2.axhspan(q10, q90, color=C_ORANGE, alpha=0.18)
    ax2.set_xlabel("概率密度", fontsize=11)
    ax2.set_ylabel("预报要素取值", fontsize=11)
    ax2.set_title("$t=%d$ h 时刻：概率预报" % tstar, fontsize=11.5)
    ax2.legend(fontsize=9.5, loc="upper right")
    save(fig, "fig22_12_ensemble.png")


# ================================================================ fig22_13
def fig22_13_integration():
    """机器学习与数值模式的集成：前处理、耦合、后处理。"""
    fig, ax = new_canvas(figsize=(11.5, 6.2))
    # 图例
    ax.add_patch(Rectangle((24, 93), 3.2, 4, fc=BLUE_L, ec=C_BLUE, lw=1.2))
    ax.text(28.5, 95, "数值天气预报业务环节", ha="left", va="center",
            fontsize=10.5)
    ax.add_patch(Rectangle((52, 93), 3.2, 4, fc="#ffffff", ec=C_ORANGE,
                           lw=1.6))
    ax.text(56.5, 95, "机器学习融入点", ha="left", va="center", fontsize=10.5)
    box(ax, 1, 38, 11, 28, "观测\n（多源观测\n资料）",
        fc=BLUE_L, ec=C_BLUE, fontsize=10)
    blocks = [
        (16, "前处理\n（初值生成）",
         ["观测资料预处理与质量控制：\n偏差纠正、雷达卫星图像预处理、\n缺测填补、云检测分割",
          "资料同化：同化算法参数优化、\n部分替代同化、聚焦观测区域"]),
        (44, "预报模式积分",
         ["耦合：模式代理\n（局部替代 / 全局替代）",
          "替代物理过程参数化方案",
          "参数校正"]),
        (72, "产品应用",
         ["后处理：确定性及集合\n预报结果订正",
          "替代集合预报"]),
    ]
    for x, title, chips in blocks:
        box(ax, x, 6, 24, 78, "", fc=BLUE_L, ec=C_BLUE, lw=1.4)
        ax.text(x + 12, 78.5, title, ha="center", va="center", fontsize=11.5,
                fontweight="bold", color=C_BLUE)
        y = 68
        for c in chips:
            nlines = c.count("\n") + 1
            hh = 4.5 + 3.4 * nlines
            box(ax, x + 1.6, y - hh, 20.8, hh, c, fc="#ffffff",
                ec=C_ORANGE, lw=1.4, fontsize=9.0)
            y -= hh + 2.6
    arrow(ax, 12.5, 52, 15.5, 52)
    arrow(ax, 40.5, 52, 43.5, 52)
    arrow(ax, 68.5, 52, 71.5, 52)
    box(ax, 97.2, 42, 2.6, 20, "产\n品", fc=GREEN_L, ec=C_GREEN, fontsize=9)
    arrow(ax, 96.5, 52, 97.4, 52, lw=1.2)
    save(fig, "fig22_13_integration.png")


# ================================================================ fig22_14
def fig22_14_proxy():
    """DNN 代理 GCM：500 hPa 位势高度的均值 / 方差 / 30 天方差对比。"""
    fig, axs = plt.subplots(3, 2, figsize=(8.6, 9.2), constrained_layout=True)
    rng14 = np.random.default_rng(2022)
    base1 = smooth_field(rng14, n=48, corr=8.0)
    base2 = smooth_field(rng14, n=48, corr=8.0)
    base3a = smooth_field(rng14, n=48, corr=5.0)
    base3b = smooth_field(rng14, n=48, corr=9.0)
    rows = [
        ("均值", base1, base1 + 0.04 * rng14.standard_normal((48, 48)),
         "几乎无差别"),
        ("方差", base2, base2 + 0.10 * rng14.standard_normal((48, 48)),
         "差别不大"),
        ("30 天方差", base3a, base3b, "差异明显"),
    ]
    for r, (lab, fa, fb, note) in enumerate(rows):
        im = axs[r, 0].imshow(fa, cmap="RdBu_r", vmin=-2.2, vmax=2.2,
                              origin="lower")
        axs[r, 1].imshow(fb, cmap="RdBu_r", vmin=-2.2, vmax=2.2,
                         origin="lower")
        axs[r, 0].set_ylabel(lab, fontsize=12)
        axs[r, 0].set_xticks([])
        axs[r, 0].set_yticks([])
        axs[r, 1].set_xticks([])
        axs[r, 1].set_yticks([])
        axs[r, 1].set_ylabel(note, fontsize=10.5, color=C_RED)
        cb = fig.colorbar(im, ax=[axs[r, 0], axs[r, 1]], shrink=0.9,
                          fraction=0.046)
        cb.ax.tick_params(labelsize=8)
    axs[0, 0].set_title("GCM（气候模式）", fontsize=12.5)
    axs[0, 1].set_title("DNN（深度学习代理）", fontsize=12.5)
    fig.supxlabel("标准化 500 hPa 位势高度场（示意）：均值与方差几乎无差别，"
                  "30 天方差才显现差异", fontsize=11.5)
    save(fig, "fig22_14_proxy.png")


# ================================================================ main
if __name__ == "__main__":
    fig22_01_objects()
    fig22_02_ml_views()
    fig22_03_nwp_def()
    fig22_04_equations()
    fig22_05_da()
    fig22_06_history()
    fig22_07_timescale()
    fig22_08_compare()
    fig22_09_three()
    fig22_10_pipeline()
    fig22_11_xai()
    fig22_12_ensemble()
    fig22_13_integration()
    fig22_14_proxy()
    print("all figures done.")
