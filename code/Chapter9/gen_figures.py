# -*- coding: utf-8 -*-
"""第九章 人工神经网络 插图生成脚本（最终稿）

说明：
- 全部数据由脚本内嵌生成，随机数用固定种子 rng = default_rng(42)，
  重复运行本脚本可得到与书稿插图完全一致的结果；
- 输出目录：书稿/figs/ch09/fig9_XX_*.png（dpi=150，tight bbox）；
- 运行方式（本机 python 为商店占位符，用 uv）：
  uv run --no-project --with matplotlib --with numpy python tmp_fig9/gen_figures.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle, FancyArrowPatch

# ---------- 全局风格 ----------
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3

OUT = r"C:\20260905\项目 人工智能与地理数据挖掘\书稿\figs\ch09"
rng = np.random.default_rng(42)

C_BLUE = "#1f77b4"
C_ORANGE = "#ff7f0e"
C_GREEN = "#2ca02c"
C_RED = "#d62728"
C_PURPLE = "#9467bd"
C_GRAY = "#7f7f7f"


def node(ax, x, y, r=0.16, fc="#eaf2fb", ec="#4a6fa5", lw=1.2, z=3):
    c = Circle((x, y), r, facecolor=fc, edgecolor=ec, lw=lw, zorder=z)
    ax.add_patch(c)
    return c


# ----------------------------------------------------------------
# fig9_01 生物神经元示意
# ----------------------------------------------------------------
def fig9_01():
    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_aspect("equal")

    # 左侧三个相连神经元（突触前）
    pre = [(0.9, 6.9), (0.9, 5.6), (0.9, 4.3)]
    for (x, y) in pre:
        node(ax, x, y, r=0.30, fc="#fbe9e7", ec=C_RED)
        # 树突（带突触小分支的曲线）
        xs = np.linspace(x + 0.32, 4.05, 60)
        ys = y + (5.6 - y) * (xs - x) ** 1.6 / (4.05 - x) ** 1.6
        ax.plot(xs, ys, color=C_RED, lw=1.3, zorder=1)
        # 突触标记
        ax.plot([x + 0.45, x + 0.45], [y - 0.12, y + 0.12], color=C_RED, lw=2.2)

    ax.text(0.9, 3.55, "其他神经元\n（突触前）", ha="center", fontsize=9.5, color=C_RED)
    ax.text(2.35, 7.35, "树突：接收输入信号", fontsize=10, color=C_RED)

    # 细胞体
    soma = Ellipse((5.2, 5.6), 2.4, 1.75, facecolor="#e8f5e9",
                   edgecolor=C_GREEN, lw=1.8, zorder=2)
    ax.add_patch(soma)
    ax.text(5.2, 5.6, "细胞体\n（神经元）", ha="center", va="center",
            fontsize=10.5, color=C_GREEN)
    ax.annotate("电位超过阈值\n→ 神经元被激活",
                xy=(5.2, 6.55), xytext=(4.4, 7.6), fontsize=9.5, color=C_GREEN,
                ha="center", arrowprops=dict(arrowstyle="->", color=C_GREEN))

    # 轴突
    ax.annotate("", xy=(9.6, 5.6), xytext=(6.45, 5.6),
                arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=3.0))
    ax.text(8.0, 5.95, "轴突：传出信号", fontsize=10, color=C_BLUE, ha="center")

    # 轴突末梢 → 突触 → 下一神经元
    for (ex, ey) in [(10.9, 6.9), (10.9, 4.3)]:
        ax.plot([9.55, 10.25], [5.6, ey], color=C_BLUE, lw=1.3)
        ax.plot([10.25, 10.25], [ey - 0.14, ey + 0.14], color=C_PURPLE, lw=2.4)
        node(ax, ex, ey, r=0.30, fc="#f3e5f5", ec=C_PURPLE)
    ax.text(10.15, 7.6, "突触：兴奋时释放化学物质\n（神经递质），改变下一神经元的电位",
            fontsize=9.5, color=C_PURPLE, ha="center")
    ax.text(11.6, 5.6, "下一神经元\n（突触后）", ha="center", fontsize=9.5, color=C_PURPLE)

    ax.set_title("生物神经元：信息的接收、整合与传递", fontsize=12)
    fig.savefig(f"{OUT}/fig9_01_bio_neuron.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig9_02 神经网络做图像识别（模式分类）示意
# ----------------------------------------------------------------
def fig9_02():
    fig = plt.figure(figsize=(10.5, 4.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[0.9, 1.6], wspace=0.05)

    # 左：像素化的猫脸“输入图像”
    img = np.ones((22, 22))
    yy, xx = np.mgrid[0:22, 0:22]
    face = (yy - 13) ** 2 / 49 + (xx - 11) ** 2 / 40 <= 1.05          # 脸
    e1 = ((yy - 3.6) ** 2 + (xx - 6.0) ** 2) <= 9                       # 左耳
    e2 = ((yy - 3.6) ** 2 + (xx - 16.0) ** 2) <= 9                      # 右耳
    cat = face | e1 | e2
    img[~cat] = 0.0
    # 眼睛、嘴留白
    for (cy, cx) in [(10, 7.5), (10, 14.5)]:
        eye = (yy - cy) ** 2 + (xx - cx) ** 2 <= 2.2
        img[eye] = 1.0
    mouth = (np.abs(yy - 16) <= 1.1) & (np.abs(xx - 11) <= 4.0)
    img[mouth] = 1.0

    ax0 = fig.add_subplot(gs[0])
    ax0.imshow(img, cmap="gray_r", interpolation="nearest")
    ax0.set_title("输入图像（像素值展开为输入向量 $x$）", fontsize=10.5)
    ax0.set_xticks([]); ax0.set_yticks([])

    # 右：网络 → 类别
    ax = fig.add_subplot(gs[1])
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.axis("off"); ax.grid(False)

    xin, hid, out = [2.0, 6.0], [5.0], [8.0]
    ny_in, ny_h, ny_o = 5, 4, 2
    ys_in = np.linspace(8.2, 1.8, ny_in)
    ys_h = np.linspace(8.0, 2.0, ny_h)
    ys_o = np.array([6.9, 3.1])
    for yi in ys_in:
        for yh in ys_h:
            ax.plot([xin[0], hid[0]], [yi, yh], color="#b0bec5", lw=0.6, zorder=1)
    for yh in ys_h:
        for yo in ys_o:
            ax.plot([hid[0], out[0]], [yh, yo], color="#b0bec5", lw=0.6, zorder=1)
    for yi in ys_in:
        node(ax, xin[0], yi, r=0.22, fc="#e3f2fd", ec=C_BLUE)
    for yh in ys_h:
        node(ax, hid[0], yh, r=0.22, fc="#e8f5e9", ec=C_GREEN)
    node(ax, out[0], ys_o[0], r=0.26, fc="#fff3e0", ec=C_ORANGE)
    node(ax, out[0], ys_o[1], r=0.26, fc="#fff3e0", ec=C_ORANGE)
    ax.text(2.0, 0.9, "输入层", ha="center", fontsize=10)
    ax.text(5.0, 0.9, "隐含层", ha="center", fontsize=10)
    ax.text(8.0, 0.9, "输出层", ha="center", fontsize=10)

    ax.text(9.0, ys_o[0] + 0.15, "“狗”", fontsize=11, va="bottom")
    ax.text(9.0, ys_o[1] + 0.15, "“猫”", fontsize=11, va="bottom")
    ax.text(9.0, ys_o[0] - 0.65, "0.05", fontsize=10, color=C_GRAY)
    ax.text(9.0, ys_o[1] - 0.65, "0.95", fontsize=10, color=C_RED)
    ax.text(8.0, 9.5, "输出各类别的概率", ha="center", fontsize=9.5, color=C_RED)

    # 从图像到网络的箭头
    ax.annotate("", xy=(0.55, 5.0), xytext=(-1.55, 5.0),
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.8))
    ax.text(5.0, 1.75, "多层网络（权重 + 偏置）", ha="center", fontsize=9.5,
            color=C_GREEN)
    ax.set_title("神经网络用于模式识别（分类）：图像 → 类别", fontsize=12)
    fig.savefig(f"{OUT}/fig9_02_pattern_recognition.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig9_03 多层前馈网络结构（4-5-7-3，线宽∝|权重|）
# ----------------------------------------------------------------
def fig9_03():
    fig, ax = plt.subplots(figsize=(10, 5.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8.6)
    ax.axis("off"); ax.grid(False)

    layers = [4, 5, 7, 3]
    xs = [1.1, 3.7, 6.3, 8.9]
    ys = [np.linspace(6.9, 1.7, n) for n in layers]
    w = [rng.normal(0, 1, (layers[k], layers[k + 1])) for k in range(3)]

    for k in range(3):
        wmax = np.abs(w[k]).max()
        for i, yi in enumerate(ys[k]):
            for j, yj in enumerate(ys[k + 1]):
                wv = w[k][i, j]
                lw = 0.4 + 2.0 * abs(wv) / wmax
                al = 0.30 + 0.65 * abs(wv) / wmax
                col = C_BLUE if wv >= 0 else C_RED
                ax.plot([xs[k], xs[k + 1]], [yi, yj], color=col, lw=lw,
                        alpha=al, zorder=1)

    fcs = ["#e3f2fd", "#e8f5e9", "#e8f5e9", "#fff3e0"]
    ecs = [C_BLUE, C_GREEN, C_GREEN, C_ORANGE]
    for k in range(4):
        for y in ys[k]:
            node(ax, xs[k], y, r=0.21, fc=fcs[k], ec=ecs[k])
    labels = ["输入层\n（4 个输入）", "隐含层 1\n（5 节点）",
              "隐含层 2\n（7 节点）", "输出层\n（3 节点）"]
    for k in range(4):
        ax.text(xs[k], 0.55, labels[k], ha="center", fontsize=10.5)

    # 图例（正/负权重）
    ax.plot([], [], color=C_BLUE, lw=2.2, label="连线：权重 $w>0$")
    ax.plot([], [], color=C_RED, lw=2.2, label="连线：权重 $w<0$")
    ax.legend(loc="upper center", ncol=2, frameon=False, fontsize=9.5)
    ax.text(5.0, 8.35, "连线越粗表示 |权重| 越大：网络的输出主要由强连接通路决定",
            ha="center", fontsize=9.5, color=C_GRAY)
    ax.set_title("一个 4-5-7-3 的多层前馈神经网络（全连接示意）", fontsize=12)
    fig.savefig(f"{OUT}/fig9_03_ann_structure.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig9_04 M-P 神经元模型
# ----------------------------------------------------------------
def fig9_04():
    fig, ax = plt.subplots(figsize=(9.5, 4.4))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    ax.axis("off"); ax.grid(False)

    xs_in = 1.2
    ys_in = [4.9, 3.7, 2.5, 1.3]
    names = ["$x_1$", "$x_2$", "$\\vdots$", "$x_d$"]
    ws = ["$w_1$", "$w_2$", "", "$w_d$"]
    sum_xy = (5.3, 3.1)
    for y, nm, wl in zip(ys_in, names, ws):
        ax.text(0.75, y, nm, fontsize=13, ha="center", va="center")
        ax.annotate("", xy=sum_xy, xytext=(1.65, y),
                    arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.4))
        if wl:
            ax.text(3.1, (y + sum_xy[1]) / 2 + 0.28, wl, fontsize=11,
                    color=C_BLUE, ha="center")
    node(ax, *sum_xy, r=0.46, fc="#e8f5e9", ec=C_GREEN, lw=1.6)
    ax.text(*sum_xy, "$\\Sigma$", fontsize=17, ha="center", va="center")
    ax.text(5.3, 4.15, "加权求和", fontsize=9.5, ha="center", color=C_GREEN)

    # 减阈值 → 激活函数
    ax.annotate("", xy=(7.35, 3.1), xytext=(5.85, 3.1),
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.4))
    ax.text(6.6, 3.42, "$-\\ \\theta$", fontsize=12, ha="center", color=C_RED)
    ax.text(6.6, 2.35, "与阈值比较", fontsize=9, ha="center", color=C_RED)

    box = Rectangle((7.35, 2.45), 2.5, 1.3, facecolor="#fff3e0",
                    edgecolor=C_ORANGE, lw=1.6, zorder=2)
    ax.add_patch(box)
    ax.text(8.6, 3.35, "激活函数", fontsize=11, ha="center", color=C_ORANGE)
    ax.text(8.6, 2.85, "$f(\\cdot)$", fontsize=12, ha="center", color=C_ORANGE)

    ax.annotate("", xy=(11.1, 3.1), xytext=(9.95, 3.1),
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.4))
    ax.text(11.35, 3.1, "$y$", fontsize=14, ha="center", va="center")

    ax.text(6.0, 0.85, "$y=f\\left(\\sum_{i=1}^{d} w_i x_i-\\theta\\right)$",
            fontsize=14, ha="center")
    ax.text(6.0, 0.28, "（等价写法：$y=f\\left(\\sum_i w_i x_i+b\\right)$，$b=-\\theta$ 即偏置）",
            fontsize=10, ha="center", color=C_GRAY)
    ax.set_title("M-P 神经元模型 [McCulloch and Pitts, 1943]", fontsize=12)
    fig.savefig(f"{OUT}/fig9_04_mp_neuron.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig9_05 偏置的两种等价画法
# ----------------------------------------------------------------
def fig9_05():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))

    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 6.4)
        ax.axis("off"); ax.grid(False)

    # 左：偏置直接加在节点内
    ax = axes[0]
    ys_in = [5.0, 3.6, 2.2]
    for y in ys_in:
        ax.annotate("", xy=(4.6, 3.6), xytext=(1.7, y),
                    arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.3))
    ax.text(0.95, 5.0, "$x_1$", fontsize=13, ha="center", va="center")
    ax.text(0.95, 3.6, "$x_2$", fontsize=13, ha="center", va="center")
    ax.text(0.95, 2.2, "$x_3$", fontsize=13, ha="center", va="center")
    ax.text(2.7, 4.72, "$w_1$", fontsize=10, color=C_BLUE, ha="center")
    ax.text(2.7, 3.68, "$w_2$", fontsize=10, color=C_BLUE, ha="center")
    ax.text(2.7, 2.28, "$w_3$", fontsize=10, color=C_BLUE, ha="center")
    # 偏置从上方进入
    ax.annotate("", xy=(4.6, 4.35), xytext=(4.6, 5.9),
                arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.5))
    ax.text(5.1, 5.6, "偏置 $b$", fontsize=11, color=C_RED)
    node(ax, 4.6, 3.6, r=0.42, fc="#e8f5e9", ec=C_GREEN, lw=1.5)
    ax.text(4.6, 3.6, "$f$", fontsize=13, ha="center", va="center")
    ax.annotate("", xy=(7.6, 3.6), xytext=(5.15, 3.6),
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.4))
    ax.text(7.9, 3.6, "$y$", fontsize=13, va="center")
    ax.text(4.9, 1.3, "$y=f(w_1 x_1+w_2 x_2+w_3 x_3+b)$", fontsize=12, ha="center")
    ax.set_title("画法一：偏置写在节点内部", fontsize=11.5)

    # 右：偏置作为恒为 1 的输入
    ax = axes[1]
    ys_in = [5.3, 3.9, 2.5, 1.1]
    labs = ["$x_1$", "$x_2$", "$x_3$", "$1$"]
    wls = ["$w_1$", "$w_2$", "$w_3$", "$b$"]
    for y, nm, wl in zip(ys_in, labs, wls):
        ax.annotate("", xy=(5.2, 3.2), xytext=(1.7, y),
                    arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.3))
        ax.text(0.95, y, nm, fontsize=13, ha="center", va="center",
                color=C_RED if nm == "$1$" else "black")
        ax.text(3.0, (y + 3.2) / 2 + 0.30, wl, fontsize=10, ha="center",
                color=C_RED if wl == "$b$" else C_BLUE)
    node(ax, 1.7, 1.1, r=0.17, fc="#fdecea", ec=C_RED)
    ax.text(1.7, 0.55, "恒为 1 的输入", fontsize=9, ha="center", color=C_RED)
    node(ax, 5.2, 3.2, r=0.42, fc="#e8f5e9", ec=C_GREEN, lw=1.5)
    ax.text(5.2, 3.2, "$f$", fontsize=13, ha="center", va="center")
    ax.annotate("", xy=(8.2, 3.2), xytext=(5.75, 3.2),
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.4))
    ax.text(8.5, 3.2, "$y$", fontsize=13, va="center")
    ax.text(5.35, 5.9, "偏置被“移出”为一个恒为 1、权重为 $b$ 的输入",
            fontsize=10.5, ha="center", color=C_RED)
    ax.set_title("画法二：偏置作为恒为 1 的输入（等价变形）", fontsize=11.5)

    fig.suptitle("偏置的两种等价画法", fontsize=12.5, y=1.02)
    fig.savefig(f"{OUT}/fig9_05_bias_as_input.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig9_06 经典激活函数：阶跃 / Sigmoid / Tanh
# ----------------------------------------------------------------
def fig9_06():
    t = np.linspace(-5, 5, 400)
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))

    ax = axes[0]
    ax.plot(t[t < 0], np.zeros(t[t < 0].size), color=C_BLUE, lw=2.2)
    ax.plot(t[t >= 0], np.ones(t[t >= 0].size), color=C_BLUE, lw=2.2)
    ax.plot(0, 0, "o", mfc="white", mec=C_BLUE, ms=7)
    ax.plot(0, 1, "o", color=C_BLUE, ms=7)
    ax.set_title("阶跃函数（理想激活函数）")
    ax.text(-4.6, 0.62, "0：抑制；1：激活\n不连续、不光滑，\n求导不方便", fontsize=9.5)

    ax = axes[1]
    sg = 1 / (1 + np.exp(-t))
    ax.plot(t, sg, color=C_BLUE, lw=2.2)
    ax.axhline(0, color="gray", lw=0.8, ls=":")
    ax.axhline(1, color="gray", lw=0.8, ls=":")
    ax.set_title("Sigmoid 函数：$\\sigma(x)=1/(1+e^{-x})$")
    ax.text(-4.8, 0.55, "输出 (0,1)，\n可解释为概率", fontsize=9.5)
    ax.annotate("两侧饱和：梯度≈0\n（梯度消失）；输出非零中心",
                xy=(-3.8, 0.022), xytext=(-3.2, 0.36), fontsize=9.5,
                arrowprops=dict(arrowstyle="->", color=C_RED), color=C_RED)

    ax = axes[2]
    ax.plot(t, np.tanh(t), color=C_BLUE, lw=2.2)
    ax.axhline(0, color="gray", lw=0.8, ls=":")
    ax.set_title("Tanh（Tansig）函数")
    ax.text(-4.8, 0.62, "Sigmoid 向下平移，\n零中心，范围 (−1,1)", fontsize=9.5)
    ax.annotate("同样存在饱和区\n（梯度消失）",
                xy=(3.8, 0.999), xytext=(1.15, 0.32), fontsize=9.5,
                arrowprops=dict(arrowstyle="->", color=C_RED), color=C_RED)

    for ax in axes:
        ax.set_xlabel("净输入 $n$")
        ax.set_ylabel("输出 $a$")
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig9_06_activation_functions.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig9_07 MATLAB 中的传递函数：purelin / tansig / softmax
# ----------------------------------------------------------------
def fig9_07():
    n = np.linspace(-2.5, 2.5, 300)
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.4))

    ax = axes[0]
    ax.plot(n, n, color=C_BLUE, lw=2.2)
    ax.set_title("purelin：$a=n$（线性，输出层用）")
    ax.set_xlabel("净输入 $n$"); ax.set_ylabel("输出 $a$")

    ax = axes[1]
    ts = 2 / (1 + np.exp(-2 * n)) - 1
    ax.plot(n, ts, color=C_BLUE, lw=2.2)
    ax.plot(n, np.tanh(n), color=C_GREEN, lw=1.0, ls="--",
            label="$\\tanh(n)$（完全重合）")
    ax.set_title("tansig：$a=2/(1+e^{-2n})-1$")
    ax.set_xlabel("净输入 $n$"); ax.set_ylabel("输出 $a$"); ax.legend(fontsize=8.5)

    ax = axes[2]
    logits = np.array([2.0, 1.0, 0.1])
    p = np.exp(logits) / np.exp(logits).sum()
    bars = ax.bar([1, 2, 3], p, width=0.55,
                  color=[C_BLUE, C_ORANGE, C_GREEN])
    for b, v in zip(bars, p):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.2f}",
                ha="center", fontsize=10)
    ax.set_xticks([1, 2, 3]); ax.set_ylim(0, 0.8)
    ax.set_xticklabels(["类 1", "类 2", "类 3"])
    ax.set_title("softmax：$a_j=e^{n_j}/\\sum_k e^{n_k}$")
    ax.text(2.0, 0.44, "输出各类概率，和为 1\n（多分类输出层用）", ha="center",
            fontsize=9.5, color=C_RED)
    ax.set_xlabel("净输入向量 $n$（3 类）"); ax.set_ylabel("概率")

    fig.tight_layout()
    fig.savefig(f"{OUT}/fig9_07_matlab_transfer_functions.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig9_08 感知机实现“与、或、非”
# ----------------------------------------------------------------
def fig9_08():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))

    def base(ax):
        ax.set_xlim(-0.35, 1.35); ax.set_ylim(-0.35, 1.35)
        ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
        ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")

    ax = axes[0]
    base(ax)
    xs0 = [(0, 0), (0, 1), (1, 0)]
    ax.plot(*zip(*xs0), "o", color=C_RED, ms=11, label="输出 0")
    ax.plot(1, 1, "o", color=C_BLUE, ms=11, label="输出 1")
    xx = np.linspace(-0.35, 1.35, 10)
    ax.plot(xx, 1.5 - xx, "--", color=C_GREEN, lw=1.8)
    ax.text(-0.25, 1.72, "分界线 $x_1+x_2=1.5$", color=C_GREEN, fontsize=9)
    ax.set_title("“与”：$w_1=w_2=1,\\ \\theta=1.5$\n（仅 $x_1=x_2=1$ 时输出 1）")

    ax = axes[1]
    base(ax)
    ax.plot(0, 0, "o", color=C_RED, ms=11, label="输出 0")
    xs1 = [(0, 1), (1, 0), (1, 1)]
    ax.plot(*zip(*xs1), "o", color=C_BLUE, ms=11, label="输出 1")
    ax.plot(xx, 0.5 - xx, "--", color=C_GREEN, lw=1.8)
    ax.text(-0.25, 0.72, "分界线 $x_1+x_2=0.5$", color=C_GREEN, fontsize=9)
    ax.set_title("“或”：$w_1=w_2=1,\\ \\theta=0.5$\n（至少一个为 1 时输出 1）")
    axes[1].legend(loc="lower right", fontsize=8.5)

    ax = axes[2]
    ax.set_xlim(-0.35, 1.35); ax.set_ylim(-0.6, 1.35)
    ax.set_xticks([0, 1]); ax.set_yticks([])
    ax.set_xlabel("$x_1$（只有一个输入）")
    ax.plot(0, 0, "o", color=C_BLUE, ms=11)
    ax.plot(1, 0, "o", color=C_RED, ms=11)
    ax.text(0, 0.14, "输出 1", ha="center", color=C_BLUE, fontsize=10)
    ax.text(1, 0.14, "输出 0", ha="center", color=C_RED, fontsize=10)
    ax.axvline(0.833, ls="--", color=C_GREEN, lw=1.8)
    ax.text(0.86, 0.82, "分界点\n$x_1\\approx 0.83$", color=C_GREEN, fontsize=9)
    ax.set_title("“非”：$w_1=-0.6,\\ \\theta=-0.5$\n（$y=f(-0.6x_1+0.5)$）")

    fig.suptitle("单个 M-P 神经元（感知机）即可实现逻辑“与、或、非”", fontsize=12.5, y=1.04)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig9_08_perceptron_and_or_not.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig9_09 线性可分 vs 异或（线性不可分）
# ----------------------------------------------------------------
def fig9_09():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    xx = np.linspace(-0.35, 1.35, 10)

    ax = axes[0]
    ax.set_xlim(-0.35, 1.35); ax.set_ylim(-0.35, 1.35)
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.plot(0, 0, "o", color=C_RED, ms=11, label="类别 0")
    for p in [(0, 1), (1, 0), (1, 1)]:
        ax.plot(*p, "o", color=C_BLUE, ms=11, label="类别 1" if p == (0, 1) else None)
    ax.plot(xx, 0.5 - xx, "--", color=C_GREEN, lw=2)
    ax.text(-0.28, 0.76, "一条直线即可分开", color=C_GREEN, fontsize=10)
    ax.set_title("线性可分问题（如“或”）")
    ax.legend(loc="lower right", fontsize=9)

    ax = axes[1]
    ax.set_xlim(-0.35, 1.35); ax.set_ylim(-0.35, 1.35)
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    for p in [(0, 0), (1, 1)]:
        ax.plot(*p, "o", color=C_RED, ms=11, label="输出 0" if p == (0, 0) else None)
    for p in [(0, 1), (1, 0)]:
        ax.plot(*p, "s", color=C_BLUE, ms=11, label="输出 1" if p == (0, 1) else None)
    ax.axhline(0.5, ls="--", color=C_GREEN, lw=1.6)
    ax.axvline(0.5, ls="--", color=C_GREEN, lw=1.6)
    ax.text(-0.3, 0.56, "一条直线无论怎么放都无法\n把同类两点与异类两点分开",
            fontsize=9.5, color=C_RED)
    ax.text(0.56, 1.02, "两条直线（两个\n神经元）才能围出\n异或区域", fontsize=9,
            color=C_GREEN)
    ax.set_title("线性不可分问题：异或（XOR）")
    ax.legend(loc="lower right", fontsize=9)

    fig.suptitle("单层感知机只能求解线性可分问题；异或问题需要多层结构",
                 fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig9_09_xor_problem.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig9_10 两层感知机解决异或
# ----------------------------------------------------------------
def fig9_10():
    fig, ax = plt.subplots(figsize=(10, 5.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8.4)
    ax.axis("off"); ax.grid(False)

    # 节点位置
    x1, x2 = (0.9, 5.6), (0.9, 2.4)
    h1, h2 = (4.6, 5.6), (4.6, 2.4)
    y_ = (8.3, 4.0)

    for a, b, wl in [(x1, h1, "1"), (x2, h1, "1"),
                     (x1, h2, "1"), (x2, h2, "1"),
                     (h1, y_, "1"), (h2, y_, "−1")]:
        ax.annotate("", xy=b, xytext=a,
                    arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.5))
        # 标签放在连线 35% 处，避开两条交叉线的中点
        mx, my = a[0] + 0.35 * (b[0] - a[0]), a[1] + 0.35 * (b[1] - a[1])
        dx = 0.24 if a[1] > b[1] else -0.24
        ax.text(mx, my + dx, wl, fontsize=11, color=C_BLUE, ha="center")

    node(ax, *x1, r=0.24, fc="#e3f2fd", ec=C_BLUE)
    node(ax, *x2, r=0.24, fc="#e3f2fd", ec=C_BLUE)
    ax.text(0.9, 6.15, "$x_1$", fontsize=13, ha="center")
    ax.text(0.9, 1.75, "$x_2$", fontsize=13, ha="center")
    ax.text(0.9, 0.85, "输入层", ha="center", fontsize=10)

    node(ax, *h1, r=0.24, fc="#e8f5e9", ec=C_GREEN)
    node(ax, *h2, r=0.24, fc="#e8f5e9", ec=C_GREEN)
    ax.text(4.6, 6.35, "$h_1$：“或”", fontsize=11, ha="center")
    ax.text(4.6, 6.85, "$w_1=w_2=1,\\ \\theta=0.5$", fontsize=9.5, ha="center",
            color=C_GREEN)
    ax.text(4.6, 1.65, "$h_2$：“与”", fontsize=11, ha="center")
    ax.text(4.6, 1.15, "$w_1=w_2=1,\\ \\theta=1.5$", fontsize=9.5, ha="center",
            color=C_GREEN)
    ax.text(4.6, 0.35, "隐含层（新增的一层）", ha="center", fontsize=10)

    node(ax, *y_, r=0.26, fc="#fff3e0", ec=C_ORANGE)
    ax.text(8.3, 4.0, "$y$", fontsize=13, ha="center", va="center")
    ax.text(8.3, 5.05, "$y=f(h_1-h_2-0.5)$", fontsize=10.5, ha="center")
    ax.text(8.3, 5.65, "即 $w_1=1,\\ w_2=-1,\\ \\theta=-0.5$", fontsize=9.5,
            ha="center", color=C_ORANGE)
    ax.text(8.3, 3.35, "输出层", ha="center", fontsize=10)

    # 真值表
    rows = [("$x_1$", "$x_2$", "$h_1$", "$h_2$", "$y$"),
            ("0", "0", "0", "0", "0"),
            ("0", "1", "1", "0", "1"),
            ("1", "0", "1", "0", "1"),
            ("1", "1", "1", "1", "0")]
    tbl = ax.table(cellText=rows[1:], colLabels=rows[0], cellLoc="center",
                   loc="center right", bbox=[0.60, 0.08, 0.38, 0.30])
    tbl.auto_set_font_size(False); tbl.set_fontsize(10.5)
    ax.set_title("两层感知机（含隐含层）解决异或问题", fontsize=12.5)
    fig.savefig(f"{OUT}/fig9_10_xor_two_layer.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig9_11 BP：前向传播与误差反向传播
# ----------------------------------------------------------------
def fig9_11():
    fig, ax = plt.subplots(figsize=(10, 5.8))
    ax.set_xlim(0, 10); ax.set_ylim(-0.4, 6.6)
    ax.axis("off"); ax.grid(False)

    ys_in = [4.4, 3.6, 2.8]
    ys_h = [4.9, 4.1, 3.3, 2.5]
    ys_o = [4.4, 3.0]
    x_in, x_h, x_o = 1.4, 4.6, 7.8

    for yi in ys_in:
        for yh in ys_h:
            ax.plot([x_in, x_h], [yi, yh], color="#b0bec5", lw=0.7, zorder=1)
    for yh in ys_h:
        for yo in ys_o:
            ax.plot([x_h, x_o], [yh, yo], color="#b0bec5", lw=0.7, zorder=1)

    for yi in ys_in:
        node(ax, x_in, yi, r=0.22, fc="#e3f2fd", ec=C_BLUE)
    for yh in ys_h:
        node(ax, x_h, yh, r=0.22, fc="#e8f5e9", ec=C_GREEN)
    for yo in ys_o:
        node(ax, x_o, yo, r=0.22, fc="#fff3e0", ec=C_ORANGE)

    ax.text(x_in, 5.45, "输入层 $x$", ha="center", fontsize=11)
    ax.text(x_h, 5.55, "隐含层 $b$", ha="center", fontsize=11)
    ax.text(x_o, 5.45, "输出层 $\\hat{y}$", ha="center", fontsize=11)
    ax.text(x_o + 1.15, 3.7, "误差\n$E_k=\\frac{1}{2}\\sum_j(\\hat{y}_j-y_j)^2$",
            fontsize=10.5, color=C_RED, ha="center")
    ax.text(x_o + 1.15, 2.2, "真实观测 $y$", fontsize=10, ha="center")

    # 前向大箭头（上）
    ax.annotate("", xy=(7.6, 6.15), xytext=(1.6, 6.15),
                arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=3.2))
    ax.text(4.6, 6.38, "① 前向传播：由输入逐层算出各层输出与预测值 $\\hat{y}$",
            fontsize=11, ha="center", color=C_BLUE)

    # 反向大箭头（下）
    ax.annotate("", xy=(1.6, 0.35), xytext=(7.6, 0.35),
                arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=3.2,
                                linestyle=(0, (5, 3))))
    ax.text(4.6, 0.02, "② 反向传播：由输出层逐层回传误差，算出每个参数的梯度",
            fontsize=11, ha="center", color=C_RED, va="top")

    ax.set_title("误差反向传播算法：先从前往后算输出，再从后往前传误差", fontsize=12.5)
    fig.savefig(f"{OUT}/fig9_11_bp_forward_backward.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig9_12 梯度下降（单参数）
# ----------------------------------------------------------------
def fig9_12():
    v = np.linspace(0.0, 4.0, 300)
    E = (v - 2.0) ** 2 + 0.4
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.plot(v, E, color=C_BLUE, lw=2.2, zorder=2)
    ax.plot(2.0, 0.4, "*", color=C_RED, ms=16, zorder=4)
    ax.text(2.05, 0.52, "最小值（$\\partial E/\\partial v=0$）", fontsize=10,
            color=C_RED)

    # 左坡下降
    v0, v1, v2 = 0.7, 1.25, 1.65
    for a, b in [(v0, v1), (v1, v2)]:
        ax.annotate("", xy=(b, (b - 2) ** 2 + 0.4 + 0.03),
                    xytext=(a, (a - 2) ** 2 + 0.4),
                    arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.8))
    ax.plot([v0, v1, v2], [(vi - 2) ** 2 + 0.4 for vi in [v0, v1, v2]],
            "o", color=C_ORANGE, ms=8, zorder=4)
    # 切线示意
    tg = np.linspace(0.3, 1.3, 10)
    ax.plot(tg, (v0 - 2) ** 2 + 0.4 + 2 * (v0 - 2) * (tg - v0), ":",
            color=C_GREEN, lw=1.6)
    ax.text(0.98, 1.62, "切线斜率 $\\partial E/\\partial v<0$，\n"
            "$-\\eta\\,\\partial E/\\partial v>0$：参数右移",
            fontsize=9.5, color=C_GREEN)

    # 右坡下降
    u0, u1 = 3.6, 2.85
    ax.annotate("", xy=(u1, (u1 - 2) ** 2 + 0.4 + 0.03),
                xytext=(u0, (u0 - 2) ** 2 + 0.4),
                arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.8))
    ax.plot([u0, u1], [(ui - 2) ** 2 + 0.4 for ui in [u0, u1]],
            "o", color=C_PURPLE, ms=8, zorder=4)
    ax.text(2.98, 1.95, "斜率>0：参数左移", fontsize=9.5, color=C_PURPLE)

    ax.text(2.0, 4.15,
            "参数更新：$v \\leftarrow v+\\Delta v,\\quad \\Delta v=-\\eta\\,\\dfrac{\\partial E}{\\partial v}$",
            fontsize=12, ha="center")
    ax.text(2.0, 3.62, "学习率 $\\eta\\in(0,1)$ 控制步长：太大易震荡，太小收敛慢",
            fontsize=10, ha="center", color=C_GRAY)
    ax.set_xlabel("参数 $v$（某个权重或偏置）")
    ax.set_ylabel("误差 $E$")
    ax.set_title("梯度下降：沿误差函数的负梯度方向更新参数")
    fig.savefig(f"{OUT}/fig9_12_gradient_descent.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig9_14 多峰误差曲面：局部极小与全局最小
# ----------------------------------------------------------------
def fig9_14():
    w1 = np.linspace(-2.4, 2.4, 120)
    w2 = np.linspace(-2.4, 2.4, 120)
    W1, W2 = np.meshgrid(w1, w2)

    def well(cx, cy, s, depth):
        return -depth * np.exp(-((W1 - cx) ** 2 + (W2 - cy) ** 2) / s)

    E = (1.1 + 0.08 * W1 + 0.05 * W2
         + well(1.15, 0.95, 1.6, 1.00)     # 全局最小
         + well(-1.25, -0.95, 1.0, 0.62)   # 局部极小
         + well(0.15, -1.55, 0.7, 0.45))   # 局部极小

    g_min = (1.15, 0.95)
    l_min = [(-1.25, -0.95), (0.15, -1.55)]

    fig = plt.figure(figsize=(11.5, 4.6))
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.plot_surface(W1, W2, E, cmap="viridis", alpha=0.92,
                     rcount=70, ccount=70, linewidth=0, antialiased=True)
    for (lx, ly) in l_min:
        lz = (1.1 + 0.08 * lx + 0.05 * ly
              - 0.62 if (lx, ly) == l_min[0] else 0.45)
        ax1.scatter([lx], [ly], [lz + 0.06], color=C_ORANGE, s=55, marker="o",
                    depthshade=False)
    gz = 1.1 + 0.08 * g_min[0] + 0.05 * g_min[1] - 1.00
    ax1.scatter([g_min[0]], [g_min[1]], [gz + 0.06], color=C_RED, s=90,
                marker="*", depthshade=False)
    ax1.set_xlabel("$w_1$"); ax1.set_ylabel("$w_2$"); ax1.set_zlabel("误差 $E$")
    ax1.set_title("误差曲面（两维参数）", fontsize=11)
    ax1.view_init(elev=38, azim=-58)

    ax2 = fig.add_subplot(1, 2, 2)
    cf = ax2.contourf(W1, W2, E, levels=22, cmap="viridis")
    fig.colorbar(cf, ax=ax2, shrink=0.9, label="误差 $E$")
    ax2.plot(*g_min, "*", color=C_RED, ms=17, label="全局最小")
    ax2.plot(*zip(*l_min), "o", color=C_ORANGE, ms=9, mec="white",
             label="局部极小")
    # 一条“下坡轨迹”示意：从某初始点收敛到局部极小
    path_w1 = [1.9, 1.45, 1.0, 0.62, 0.34, 0.20, 0.16]
    path_w2 = [-2.05, -1.85, -1.75, -1.68, -1.62, -1.58, -1.56]
    ax2.plot(path_w1, path_w2, "--", color="white", lw=1.6)
    ax2.plot(path_w1[0], path_w2[0], "s", color="white", ms=7)
    ax2.text(0.42, -1.5, "梯度下降\n可能停在局部极小", color="white", fontsize=9.5)
    ax2.set_xlabel("$w_1$"); ax2.set_ylabel("$w_2$")
    ax2.set_title("等高线与两条下降路径", fontsize=11)
    ax2.legend(loc="upper left", fontsize=9, framealpha=0.9)

    fig.suptitle("梯度为零、误差小于邻点的点即局部极小；全局最小只有一个",
                 fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig9_14_local_minima.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig9_13 早停策略（缓解过拟合）
# ----------------------------------------------------------------
def fig9_13():
    ep = np.arange(1, 61)
    train = 0.92 * np.exp(-ep / 11) + 0.055 + rng.normal(0, 0.004, ep.size)
    valid = (0.96 * np.exp(-ep / 15) + 0.06
             + 0.00085 * np.maximum(ep - 24, 0) ** 1.45
             + rng.normal(0, 0.004, ep.size))
    best = int(ep[np.argmin(valid)])

    fig, ax = plt.subplots(figsize=(7.6, 4.5))
    ax.plot(ep, train, color=C_BLUE, lw=2, label="训练误差")
    ax.plot(ep, valid, color=C_RED, lw=2, label="验证误差")
    ax.axvline(best, color=C_GREEN, ls="--", lw=1.8)
    ax.plot(best, valid.min(), "o", color=C_GREEN, ms=9)
    ax.annotate(f"早停点（第 {best} 轮）：验证误差最小",
                xy=(best, valid.min()), xytext=(best - 26, 0.42),
                fontsize=10, color=C_GREEN,
                arrowprops=dict(arrowstyle="->", color=C_GREEN))
    ax.annotate("继续训练：训练误差仍下降，\n验证误差却上升 → 过拟合",
                xy=(50, valid[ep == 50][0]), xytext=(33, 0.20),
                fontsize=10, color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED))
    ax.set_xlabel("训练轮数（epoch）")
    ax.set_ylabel("误差")
    ax.set_ylim(0, 1.0)
    ax.set_title("早停：在验证误差开始回升时停止训练")
    ax.legend(fontsize=10)
    fig.savefig(f"{OUT}/fig9_13_early_stopping.png")
    plt.close(fig)


# ----------------------------------------------------------------
# 小型 BP 网络数值实验（供 fig9_15 使用，tansig 隐层 + 线性输出）
# ----------------------------------------------------------------
def tansig(z):
    return 2.0 / (1.0 + np.exp(-2.0 * z)) - 1.0


def _mlp_predict(x, y, q, xtarget, iters=12000, lr=0.06, seed=None):
    """训练一维输入、一维输出的 1-q-1 网络（tansig 隐层 + 线性输出，
    梯度下降），返回在 xtarget 上的预测；x、y 均已归一化到 [-1,1]。"""
    r = np.random.default_rng(seed)
    W1 = r.normal(0, 0.6, q); b1 = r.normal(0, 0.2, q)
    W2 = r.normal(0, 0.6, q); b2 = 0.0
    m = x.size
    for _ in range(iters):
        h = tansig(W1[None, :] * x[:, None] + b1[None, :])
        yhat = h @ W2 + b2
        e = (yhat - y) / m
        gW2 = h.T @ e; gb2 = e.sum()
        dh = np.outer(e, W2) * (1 - h ** 2)
        gW1 = (dh * x[:, None]).sum(axis=0); gb1 = dh.sum(axis=0)
        W1 -= lr * gW1; b1 -= lr * gb1
        W2 -= lr * gW2; b2 -= lr * gb2
    ht = tansig(W1[None, :] * xtarget[:, None] + b1[None, :])
    return ht @ W2 + b2


def denorm(zn, zmin, zmax):
    return (zn + 1) / 2 * (zmax - zmin) + zmin


# ----------------------------------------------------------------
# fig9_15 案例一：1-q-1 网络拟合非线性函数 + 隐节点数影响
# ----------------------------------------------------------------
def fig9_15():
    x = np.linspace(0, 6.0, 60)
    y = np.sin(x) + 0.16 * x + rng.normal(0, 0.10, x.size)
    xmin, xmax, ymin, ymax = 0.0, 6.0, y.min() - 0.15, y.max() + 0.15
    xn = (x - xmin) / (xmax - xmin) * 2 - 1
    yn = (y - ymin) / (ymax - ymin) * 2 - 1
    xt = np.linspace(0, 6.0, 240)
    xnt = (xt - xmin) / (xmax - xmin) * 2 - 1

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))

    ax = axes[0]
    ax.scatter(x, y, s=22, color=C_BLUE, alpha=0.8, label="训练样本", zorder=3)
    ax.plot(xt, np.sin(xt) + 0.16 * xt, "--", color=C_GRAY, lw=1.5,
            label="真实关系", zorder=2)
    # 训练 1-8-1 网络并在细网格上预测（固定种子保证可复现）
    predt = _mlp_predict(xn, yn, q=8, xtarget=xnt, seed=2022)
    ax.plot(xt, denorm(predt, ymin, ymax), color=C_RED, lw=2.2,
            label="1-8-1 网络拟合", zorder=4)
    ax.set_xlabel("自变量 $x$")
    ax.set_ylabel("因变量 $y$")
    ax.set_title("案例一：1-8-1 BP 网络拟合非线性函数")
    ax.legend(fontsize=9)

    ax = axes[1]
    ax.scatter(x, y, s=14, color=C_BLUE, alpha=0.45, zorder=2)
    ax.plot(xt, np.sin(xt) + 0.16 * xt, "--", color=C_GRAY, lw=1.5,
            label="真实关系", zorder=3)
    for q, col, note in [(1, C_RED, "q=1：欠拟合"),
                         (3, C_ORANGE, "q=3：基本贴合"),
                         (10, C_GREEN, "q=10：充分逼近")]:
        pq = _mlp_predict(xn, yn, q=q, xtarget=xnt, seed=2022)
        ax.plot(xt, denorm(pq, ymin, ymax), color=col, lw=1.9, label=note,
                zorder=4)
    ax.set_xlabel("自变量 $x$")
    ax.set_ylabel("因变量 $y$")
    ax.set_title("隐节点数 q 的影响（“足够多神经元即可逼近连续函数”）")
    ax.legend(fontsize=9)

    fig.tight_layout()
    fig.savefig(f"{OUT}/fig9_15_ann_fit_case.png")
    plt.close(fig)


if __name__ == "__main__":
    figs = [fig9_01, fig9_02, fig9_03, fig9_04, fig9_05, fig9_06, fig9_07,
            fig9_08, fig9_09, fig9_10, fig9_11, fig9_12, fig9_13, fig9_14,
            fig9_15]
    for f in figs:
        print("生成", f.__name__, "...")
        f()
    print("全部完成，输出目录：", OUT)
