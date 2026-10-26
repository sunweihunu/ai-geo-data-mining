# -*- coding: utf-8 -*-
"""第11章 深度学习 插图生成脚本（依据《机器学习与地学应用·第十一讲 深度学习》课件重绘）"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, FancyBboxPatch
from matplotlib.lines import Line2D
import os

OUT = r"C:\20260905\项目 人工智能与地理数据挖掘\书稿\figs\ch11"
os.makedirs(OUT, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["savefig.dpi"] = 150

C_BLUE = "#1f77b4"; C_ORANGE = "#ff7f0e"; C_GREEN = "#2ca02c"
C_RED = "#d62728"; C_PURPLE = "#9467bd"; C_GRAY = "#7f7f7f"
C_LBLUE = "#aec7e8"; C_LORANGE = "#ffbb78"; C_LGREEN = "#98df8a"
C_LRED = "#ff9896"; C_LPURPLE = "#c5b0d5"

rng = np.random.default_rng(42)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight")
    plt.close(fig)
    print("saved:", name)


def box(ax, x, y, w, h, fc, ec="none", lw=1.0, alpha=1.0, zorder=2, ls="-"):
    r = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw,
                  alpha=alpha, zorder=zorder, linestyle=ls)
    ax.add_patch(r)
    return r


def arrow(ax, x1, y1, x2, y2, color=C_GRAY, lw=1.4, zorder=3, style="-|>",
          shrinkA=0, shrinkB=0, rad=0.0, ls="-"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, color=color,
                        linewidth=lw, mutation_scale=12, zorder=zorder,
                        shrinkA=shrinkA, shrinkB=shrinkB, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a)
    return a


def grid(ax, x0, y0, cell, vals, facecolors=None, txtcolors=None, fs=7,
         ec="#555555", lw=0.6, fmt="{:g}"):
    vals = np.asarray(vals)
    n_r, n_c = vals.shape
    for i in range(n_r):
        for j in range(n_c):
            fc = "#ffffff" if facecolors is None else facecolors[i][j]
            box(ax, x0 + j * cell, y0 + (n_r - 1 - i) * cell, cell, cell,
                fc, ec=ec, lw=lw, zorder=2)
            if not isinstance(vals[i, j], str):
                tc = "#333333" if txtcolors is None else txtcolors[i][j]
                ax.text(x0 + j * cell + cell / 2, y0 + (n_r - 1 - i) * cell + cell / 2,
                        fmt.format(vals[i, j]), ha="center", va="center",
                        fontsize=fs, color=tc, zorder=4)


# ======================================================================
def fig11_01_dl_timeline():
    """纵向时间线：17 个事件，左右交替，类别着色"""
    events = [
        ("1943", "M-P 神经元模型：模仿生物神经元的三神经元模型", "trunk"),
        ("1958", "感知机（单层）：在 M-P 模型前加输入节点", "trunk"),
        ("1969", "专著指出感知机局限（不能处理非线性问题），研究陷入低谷", "trunk"),
        ("1986", "反向传播（BP）算法提出，多层感知机可以训练", "trunk"),
        ("1986", "Jordan 网络：每个隐层节点接一个状态单元（延时输入）", "rec"),
        ("1990", "Elman 网络：第一个全连接 RNN；与 Jordan 网络合称 SRN", "rec"),
        ("1994–98", "LeNet-5：卷积、参数共享、池化，字符与数字识别", "conv"),
        ("1997", "LSTM：引入门控，解决 RNN 时间维度的梯度消失", "rec"),
        ("2003", "“深度学习三剑客”组成联盟，悄悄开发 10 层以上网络", "conv"),
        ("2006", "深度信念网络（DBN）：逐层预训练 + 微调", "conv"),
        ("2009", "ImageNet 数据集发布（320 万张，后增至 1500 万张标注图片）", "conv"),
        ("2010", "基于 RNN 的语言模型（自然语言处理）", "rec"),
        ("2012", "AlexNet 以领先第二名 10 个百分点夺得 ImageNet 冠军", "conv"),
        ("2013–15", "编码器-解码器、自注意力层等算法用于机器翻译", "rec"),
        ("2014", "GoogLeNet（Inception 结构）；同年 GRU、GAN、Adam 优化器", "conv"),
        ("2015", "ResNet（152 层）：错误率降至 3.57%，超过人类水平", "conv"),
        ("2017–", "Transformer、BERT 等大型模型，注意力机制广泛应用", "rec"),
    ]
    colors = {"trunk": C_GREEN, "rec": C_BLUE, "conv": C_ORANGE}
    names = {"trunk": "人工神经网络主干", "rec": "循环结构一支（序列/时序）",
             "conv": "卷积与深层结构一支（图像）"}

    n = len(events)
    fig, ax = plt.subplots(figsize=(11.8, 8.6))
    ax.set_xlim(-11.5, 11.5)
    ax.set_ylim(-n * 0.92 - 0.4, 1.4)
    ax.axis("off")

    xs = np.arange(n) * -0.92
    ax.plot([0, 0], [0.4, xs[-1] - 0.4], color="#999999", lw=2.0, zorder=1)
    for k, ((yr, txt, cat), y) in enumerate(zip(events, xs)):
        c = colors[cat]
        left = (k % 2 == 0)
        ax.plot([0], [y], "o", ms=8, color=c, zorder=3,
                markeredgecolor="white", markeredgewidth=1.2)
        s = 1 if left else -1
        ax.plot([0, s * 0.55], [y, y], color=c, lw=1.1, ls=":")
        ax.text(s * 0.75, y, f"{yr}  {txt}", ha="left" if left else "right",
                va="center", fontsize=9.6, color="#222222")
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=colors[c],
                      markersize=9, label=names[c]) for c in ("trunk", "rec", "conv")]
    ax.legend(handles=handles, loc="upper left", fontsize=9.5, frameon=False,
              bbox_to_anchor=(0.0, 1.02))
    ax.set_title("从人工神经网络到深度学习的发展脉络", fontsize=13.5, pad=14)
    save(fig, "fig11_01_dl_timeline.png")


# ======================================================================
def fig11_02_local_connect_share():
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 5.0))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 9.2); ax.axis("off")
    x0, y0, cell = 0.7, 2.2, 0.85

    # (a) 全连接
    ax = axes[0]
    ax.set_title("(a) 全连接", fontsize=11)
    for i in range(4):
        for j in range(4):
            box(ax, x0 + j * cell, y0 + i * cell, cell, cell, C_LBLUE, ec=C_BLUE, lw=0.8)
    nodes = [(8.0, 7.2), (8.0, 5.4), (8.0, 3.6)]
    for nx, ny in nodes:
        for i in range(4):
            for j in range(4):
                sx = x0 + j * cell + cell / 2
                sy = y0 + i * cell + cell / 2
                ax.plot([sx, nx - 0.3], [sy, ny], color="#9ecae1", lw=0.4, zorder=1)
        ax.add_patch(Circle((nx, ny), 0.32, fc=C_ORANGE, ec="none", zorder=3))
    ax.text(2.4, 6.4, "输入图像\n(4×4 = 16 个像素)", ha="center", fontsize=9.5)
    ax.text(4.6, 1.1, "隐层每个节点与全部像素相连\n权重数 = 16 × 3 = 48", ha="center",
            fontsize=9.5, color="#333333")

    # (b) 局部连接
    ax = axes[1]
    ax.set_title("(b) 局部连接", fontsize=11)
    patches_ = [((0, 0), "#fbd9d9", C_RED, 7.2), ((2, 1), "#d9f0d9", C_GREEN, 5.4),
                ((1, 2), "#e8dbf2", C_PURPLE, 3.6)]
    for (pi, pj), fc, ec, ny in patches_:
        sx = x0 + pj * cell + cell
        sy = y0 + pi * cell + cell
        ax.plot([sx, 7.7], [sy, ny], color=ec, lw=1.3, zorder=1)
        ax.add_patch(Circle((8.0, ny), 0.32, fc=C_ORANGE, ec="none", zorder=3))
    for i in range(4):
        for j in range(4):
            box(ax, x0 + j * cell, y0 + i * cell, cell, cell, "none", ec=C_BLUE, lw=0.8)
    for (pi, pj), fc, ec, ny in patches_:
        box(ax, x0 + pj * cell, y0 + pi * cell, 2 * cell, 2 * cell, fc, ec=ec, lw=1.7, zorder=2)
    ax.text(4.6, 1.1, "每个节点只连一个局部窗口（感受野）\n权重数 = 3 × 4 = 12", ha="center",
            fontsize=9.5, color="#333333")

    # (c) 参数共享
    ax = axes[2]
    ax.set_title("(c) 参数（权值）共享", fontsize=11)
    wcols = [C_RED, C_GREEN, C_PURPLE, C_ORANGE]
    wfc = ["#fbd9d9", "#d9f0d9", "#e8dbf2", "#ffe3c2"]
    wins = [(0, 0, 4.9), (2, 1, 3.9), (1, 2, 2.9)]
    for pi, pj, ny in wins:
        sx = x0 + pj * cell + cell
        sy = y0 + pi * cell + cell
        ax.plot([sx, 7.7], [sy, ny], color="#999999", lw=1.0, zorder=1)
        for a in range(2):
            for b in range(2):
                box(ax, x0 + (pj + b) * cell, y0 + (pi + a) * cell, cell, cell,
                    wfc[a * 2 + b], ec=wcols[a * 2 + b], lw=1.5)
    for i in range(4):
        for j in range(4):
            box(ax, x0 + j * cell, y0 + i * cell, cell, cell, "none", ec=C_BLUE, lw=0.8)
    ax.add_patch(Circle((8.0, 3.9), 0.32, fc=C_ORANGE, ec="none", zorder=3))
    # 卷积核图例
    kx, ky, kc = 7.1, 6.2, 0.85
    ax.text(kx + kc, ky + 2 * kc + 0.3, "卷积核（同一组权重）", ha="center", fontsize=9.5)
    for a in range(2):
        for b in range(2):
            box(ax, kx + b * kc, ky + (1 - a) * kc, kc, kc, wfc[a * 2 + b],
                ec=wcols[a * 2 + b], lw=1.5)
            ax.text(kx + b * kc + kc / 2, ky + (1 - a) * kc + kc / 2,
                    f"$w_{a * 2 + b + 1}$", ha="center", va="center", fontsize=8.5)
    ax.text(4.6, 1.1, "同一卷积核从左上到右下扫描全图\n权重数 = 4（各窗口共用）", ha="center",
            fontsize=9.5, color="#333333")
    save(fig, "fig11_02_local_connect_share.png")


# ======================================================================
def fig11_03_layerwise_pretrain():
    fig, ax = plt.subplots(figsize=(11.8, 6.6))
    ax.set_xlim(0, 16); ax.set_ylim(0, 11); ax.axis("off")

    def layer_row(y, n, label, color):
        xs = np.linspace(2.6, 7.0, n)
        for x in xs:
            ax.add_patch(Circle((x, y), 0.26, fc=color, ec="none", zorder=3))
        ax.text(2.1, y, label, ha="right", va="center", fontsize=10.5, color=color)
        return xs

    ys = [1.6, 4.2, 6.8, 9.4]
    xs0 = layer_row(ys[0], 5, "输入层 $x$", C_BLUE)
    xs1 = layer_row(ys[1], 4, "隐层 1 $h_1$", C_ORANGE)
    xs2 = layer_row(ys[2], 4, "隐层 2 $h_2$", C_GREEN)
    xs3 = layer_row(ys[3], 3, "隐层 3 / 输出", C_RED)

    steps = [((ys[0], xs0), (ys[1], xs1), "① 训练第 1 个 RBM（输入层—隐层 1）"),
             ((ys[1], xs1), (ys[2], xs2), "② 以 $h_1$ 的输出为输入，训练第 2 个 RBM"),
             ((ys[2], xs2), (ys[3], xs3), "③ 以 $h_2$ 的输出为输入，训练第 3 个 RBM")]
    for (ya, xa), (yb, xb), txt in steps:
        for x1 in xa:
            for x2 in xb:
                ax.plot([x1, x2], [ya + 0.3, yb - 0.3], color="#cccccc", lw=0.5, zorder=1)
        box(ax, 1.9, min(ya, yb) - 0.6, 5.9, abs(yb - ya) + 1.2, "none",
            ec=C_GRAY, lw=1.7, zorder=2, ls=(0, (4, 3)))
        ax.text(8.4, (ya + yb) / 2, txt, ha="left", va="center", fontsize=10.5,
                color="#222222")

    for x1 in xs0:
        for x2 in xs3:
            ax.plot([x1, x2], [ys[0] + 0.3, ys[3] - 0.3], color="#e2e2e2", lw=0.4, zorder=1)
    ax.text(8.4, 1.9, "④ 各层预训练完成后，再用 BP 算法对整个网络微调：\n"
                      "此时各参数已处于“不那么差”的初始值附近，\n"
                      "比随机初始化直接训练更容易收敛",
            ha="left", va="top", fontsize=10.5, color="#222222",
            bbox=dict(boxstyle="round,pad=0.45", fc="#fff7e6", ec=C_ORANGE, lw=1.2))
    ax.set_title("深度信念网络的逐层预训练 + 微调（2006，Hinton）", fontsize=13, pad=8)
    save(fig, "fig11_03_layerwise_pretrain.png")


# ======================================================================
def fig11_04_alexnet():
    fig, ax = plt.subplots(figsize=(13.4, 6.0))
    ax.set_xlim(0, 26); ax.set_ylim(0, 11.5); ax.axis("off")

    def blk(x, y, w, h, t1, t2, fc, fs=8.5):
        box(ax, x, y, w, h, fc, ec="#666666", lw=0.8)
        ax.text(x + w / 2, y + h * 0.63, t1, ha="center", va="center", fontsize=fs)
        ax.text(x + w / 2, y + h * 0.27, t2, ha="center", va="center", fontsize=fs - 1,
                color="#555555")

    y1 = 6.8
    blk(0.8, y1, 2.6, 2.2, "输入图像", "227×227×3\n(RGB 3 通道)", C_LBLUE)
    arrow(ax, 3.4, y1 + 1.1, 4.2, y1 + 1.1)
    blk(4.2, y1, 2.9, 2.2, "卷积 1", "核 11×11，步幅 4\n输出 55×55×96", C_LORANGE)
    arrow(ax, 7.1, y1 + 1.1, 7.9, y1 + 1.1)
    blk(7.9, y1, 2.4, 2.2, "最大池化 1", "3×3，步幅 2", C_LGREEN)
    arrow(ax, 10.3, y1 + 1.1, 11.1, y1 + 1.1)
    blk(11.1, y1, 2.4, 2.2, "卷积 2", "核 5×5", C_LORANGE)
    arrow(ax, 13.5, y1 + 1.1, 14.3, y1 + 1.1)
    blk(14.3, y1, 2.4, 2.2, "卷积 3、4", "核 3×3", C_LORANGE)
    arrow(ax, 16.7, y1 + 1.1, 17.5, y1 + 1.1)
    blk(17.5, y1, 2.4, 2.2, "卷积 5 +\n最大池化 2", "核 3×3", C_LORANGE, fs=8)

    ax.plot([19.9, 19.9], [y1, 4.4], color=C_GRAY, lw=1.4)
    ax.plot([19.9, 2.6], [4.4, 4.4], color=C_GRAY, lw=1.4)
    arrow(ax, 2.6, 4.4, 2.6, 4.55)

    y2 = 1.4
    blk(17.5, y2, 2.4, 2.2, "特征图展平", "6×6×256", C_LBLUE, fs=8)
    arrow(ax, 17.5, y2 + 1.1, 16.7, y2 + 1.1)
    blk(13.9, y2, 2.8, 2.2, "全连接 1", "4096", C_LPURPLE)
    arrow(ax, 13.9, y2 + 1.1, 13.1, y2 + 1.1)
    blk(10.3, y2, 2.8, 2.2, "全连接 2", "4096", C_LPURPLE)
    arrow(ax, 10.3, y2 + 1.1, 9.5, y2 + 1.1)
    blk(6.7, y2, 2.8, 2.2, "Softmax", "输出 1000 类\n的概率", C_LRED)

    box(ax, 0.8, 10.0, 24.4, 1.15, "#f7f7f7", ec="#bbbbbb", lw=0.8)
    ax.text(13.0, 10.58, "图中前半部分上、下两半对应两块 GPU 并行计算；层间的 ReLU 激活与局部响应归一化未画出",
            ha="center", va="center", fontsize=9.5, color="#444444")
    ax.text(13.0, 0.55, "输入图像经层层卷积与池化不断提取特征，最终展平为 4096 维特征向量，映射到 1000 个类别的概率",
            ha="center", va="center", fontsize=9.5, color="#444444")
    ax.set_title("AlexNet 的结构示意（2012，ImageNet 竞赛冠军）", fontsize=13, pad=4)
    save(fig, "fig11_04_alexnet.png")


# ======================================================================
def fig11_05_residual_block():
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.0), gridspec_kw={"width_ratios": [1.15, 1]})

    ax = axes[0]
    ax.set_xlim(0, 12); ax.set_ylim(0, 8.2); ax.axis("off")
    ax.set_title("(a) ResNet 的捷径连接（残差块）", fontsize=11)
    ax.text(0.9, 4.0, "$x$", fontsize=15, ha="center", va="center")
    ax.add_patch(FancyBboxPatch((2.0, 3.4), 2.4, 1.2, boxstyle="round,pad=0.08",
                                fc=C_LBLUE, ec=C_BLUE, lw=1.2))
    ax.text(3.2, 4.0, "卷积 + ReLU", ha="center", va="center", fontsize=9.5)
    ax.add_patch(FancyBboxPatch((5.4, 3.4), 2.4, 1.2, boxstyle="round,pad=0.08",
                                fc=C_LBLUE, ec=C_BLUE, lw=1.2))
    ax.text(6.6, 4.0, "卷积 (+ReLU)", ha="center", va="center", fontsize=9.5)
    arrow(ax, 1.2, 4.0, 1.95, 4.0)
    arrow(ax, 4.45, 4.0, 5.35, 4.0)
    ax.text(4.9, 4.38, "$F(x)$", fontsize=11, ha="center", color=C_BLUE)
    ax.add_patch(Circle((9.0, 4.0), 0.34, fc="white", ec="#333333", lw=1.2, zorder=3))
    ax.text(9.0, 4.0, "$+$", fontsize=13, ha="center", va="center", zorder=4)
    arrow(ax, 7.85, 4.0, 8.62, 4.0)
    ax.plot([1.0, 1.0, 9.0, 9.0], [4.3, 1.9, 1.9, 3.62], color=C_GREEN, lw=1.6)
    arrow(ax, 9.0, 1.9, 9.0, 3.6, color=C_GREEN, lw=1.6)
    ax.text(5.0, 1.55, "捷径连接：恒等映射，直接把 $x$ 加到输出", ha="center",
            fontsize=9.5, color=C_GREEN)
    arrow(ax, 9.38, 4.0, 10.6, 4.0)
    ax.text(11.05, 4.0, "$H(x)$", fontsize=13, ha="center", va="center")
    ax.text(5.4, 6.9, "学习目标改为残差：$F(x) = H(x) - x$，即 $H(x) = F(x) + x$",
            ha="center", fontsize=10.5, color="#222222",
            bbox=dict(boxstyle="round,pad=0.35", fc="#eef7ee", ec=C_GREEN, lw=1.0))
    ax.text(5.4, 5.9, "梯度可沿捷径“直达”前面的层，缓解梯度消失，网络可加深到上百甚至上千层",
            ha="center", fontsize=9, color="#555555")

    ax = axes[1]
    n = np.arange(1, 21)
    ax.semilogy(n, 0.25 ** n, "o-", color=C_RED, lw=1.6, ms=4,
                label="Sigmoid：每传一层梯度衰减为 0.25")
    ax.semilogy(n, np.ones_like(n, dtype=float), "s-", color=C_GREEN, lw=1.6, ms=4,
                label="ReLU：导数恒为 1（x>0）")
    ax.set_xlabel("向后传递的层数", fontsize=10.5)
    ax.set_ylabel("梯度幅度（对数刻度）", fontsize=10.5)
    ax.set_title("(b) 激活函数与深层网络的梯度衰减", fontsize=11)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=9.5, loc="center left")
    ax.annotate("20 层后仅约 $10^{-12}$", xy=(20, 0.25 ** 20), xytext=(11.5, 3e-7),
                fontsize=9.5, color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.0))
    save(fig, "fig11_05_residual_block.png")


# ======================================================================
def fig11_06_rnn_structure():
    fig, axes = plt.subplots(1, 2, figsize=(13.8, 5.4), gridspec_kw={"width_ratios": [1, 1.75]})

    ax = axes[0]
    ax.set_xlim(0, 10); ax.set_ylim(0, 9.4); ax.axis("off")
    ax.set_title("(a) 折叠形式：隐层节点“自循环”", fontsize=11)
    ax.add_patch(FancyBboxPatch((3.6, 3.4), 2.9, 1.8, boxstyle="round,pad=0.1",
                                fc=C_LORANGE, ec=C_ORANGE, lw=1.4))
    ax.text(5.05, 4.3, "RNN 单元\n$h_t = f(h_{t-1},\\, x_t)$", ha="center",
            va="center", fontsize=9.5)
    arrow(ax, 1.3, 4.3, 3.5, 4.3, lw=1.6)
    ax.text(0.85, 4.3, "$x_t$", fontsize=13, ha="center", va="center")
    ax.text(2.4, 4.75, "$U$", fontsize=11, color=C_BLUE)
    arrow(ax, 6.6, 4.3, 8.6, 4.3, lw=1.6)
    ax.text(9.1, 4.3, "$o_t$", fontsize=13, ha="center", va="center")
    ax.text(7.55, 4.75, "$V$", fontsize=11, color=C_BLUE)
    ax.add_patch(FancyArrowPatch((4.35, 5.35), (5.75, 5.35), arrowstyle="-|>",
                                 color=C_RED, lw=1.6, mutation_scale=13,
                                 connectionstyle="arc3,rad=2.6"))
    ax.text(5.05, 8.0, "$W$", fontsize=11, color=C_RED, ha="center")
    ax.text(5.05, 2.0, "弧线表示 $h_t$ 依赖上一时刻的隐层状态 $h_{t-1}$，\n"
                       "即隐层节点之间（跨时刻）有连接",
            ha="center", fontsize=9.5, color="#444444")

    ax = axes[1]
    ax.set_xlim(0, 18); ax.set_ylim(0, 9.4); ax.axis("off")
    ax.set_title("(b) 按时间展开：同一个单元在各个时刻复用", fontsize=11)
    xs = [2.6, 8.0, 13.4]
    ts = ["t-1", "t", "t+1"]
    for x, t in zip(xs, ts):
        ax.add_patch(FancyBboxPatch((x - 1.1, 3.4), 2.2, 1.6, boxstyle="round,pad=0.08",
                                    fc=C_LORANGE, ec=C_ORANGE, lw=1.3))
        ax.text(x, 4.2, f"${t}$", ha="center", va="center", fontsize=11)
        arrow(ax, x, 1.7, x, 3.35, lw=1.5)
        ax.text(x, 1.15, f"$x_{{{t}}}$", fontsize=12, ha="center", va="center")
        ax.text(x + 0.38, 2.45, "$U$", fontsize=10, color=C_BLUE)
        arrow(ax, x, 5.05, x, 6.85, lw=1.5)
        ax.text(x, 7.35, f"$o_{{{t}}}$", fontsize=12, ha="center", va="center")
        ax.text(x + 0.38, 5.95, "$V$", fontsize=10, color=C_BLUE)
    for k in range(2):
        arrow(ax, xs[k] + 1.15, 4.2, xs[k + 1] - 1.2, 4.2, lw=1.5, color=C_RED)
        ax.text((xs[k] + xs[k + 1]) / 2, 4.55, "$W$", fontsize=10, color=C_RED, ha="center")
    ax.text(9.0, 0.35, "各时刻共用同一组权重 $U$、$W$、$V$（随时间共享）——这正是 RNN 可以“往前看”任意多个输入的原因",
            ha="center", fontsize=9.5, color="#444444")
    save(fig, "fig11_06_rnn_structure.png")


# ======================================================================
def fig11_07_rnn_io_modes():
    fig, axes = plt.subplots(1, 3, figsize=(13.8, 4.8))
    caps = ["(a) 多对多：序列到序列", "(b) 多对一：序列到单个输出",
            "(c) 一对多：单个输入到序列"]
    apps = ["典型应用：语音识别、机器翻译",
            "典型应用：动作识别、行为识别、\n单词量有限的语音识别（如智能手环）",
            "典型应用：文本生成（如“古诗接龙”）、\n看图说话"]
    for ax, cap, app in zip(axes, caps, apps):
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
        ax.set_title(cap, fontsize=10.5)
        ax.text(5.0, 0.8, app, ha="center", fontsize=9.3, color="#444444")

    def cell(ax, x, y):
        ax.add_patch(FancyBboxPatch((x - 0.75, y - 0.55), 1.5, 1.1,
                                    boxstyle="round,pad=0.06",
                                    fc=C_LORANGE, ec=C_ORANGE, lw=1.1))

    ax = axes[0]
    for k in range(3):
        x = 2.0 + k * 3.0
        cell(ax, x, 5.0)
        arrow(ax, x, 2.6, x, 4.4, lw=1.3)
        ax.text(x, 2.1, "$x_%d$" % (k + 1), fontsize=11, ha="center")
        arrow(ax, x, 5.6, x, 7.3, lw=1.3)
        ax.text(x, 7.8, "$y_%d$" % (k + 1), fontsize=11, ha="center")
        if k < 2:
            arrow(ax, x + 0.8, 5.0, x + 2.2, 5.0, lw=1.2, color=C_RED)

    ax = axes[1]
    for k in range(3):
        x = 1.8 + k * 2.1
        cell(ax, x, 5.0)
        arrow(ax, x, 2.6, x, 4.4, lw=1.3)
        ax.text(x, 2.1, "$x_%d$" % (k + 1), fontsize=11, ha="center")
        if k < 2:
            arrow(ax, x + 0.8, 5.0, x + 1.3, 5.0, lw=1.2, color=C_RED)
    arrow(ax, 6.9, 5.0, 8.0, 5.0, lw=1.3)
    ax.text(8.5, 5.0, "$y$", fontsize=13, ha="center", va="center")
    ax.text(4.2, 6.9, "只取最后一个时刻的输出", ha="center", fontsize=9, color="#666666")

    ax = axes[2]
    ax.text(1.3, 5.0, "$x$", fontsize=13, ha="center", va="center")
    for k in range(3):
        x = 3.8 + k * 2.5
        cell(ax, x, 5.0)
        arrow(ax, x, 5.6, x, 7.3, lw=1.3)
        ax.text(x, 7.8, "$y_%d$" % (k + 1), fontsize=11, ha="center")
        if k < 2:
            arrow(ax, x + 0.8, 5.0, x + 1.7, 5.0, lw=1.2, color=C_RED)
    arrow(ax, 1.7, 5.0, 3.0, 5.0, lw=1.3)
    save(fig, "fig11_07_rnn_io_modes.png")


# ======================================================================
def fig11_08_lstm_cell():
    fig, ax = plt.subplots(figsize=(12.8, 7.8))
    ax.set_xlim(0, 15.5); ax.set_ylim(0, 11); ax.axis("off")

    yC = 9.2
    for a, b in [(1.3, 3.0), (3.62, 5.9), (6.55, 13.3)]:
        ax.plot([a, b], [yC, yC], color=C_GREEN, lw=2.4)
    ax.text(0.85, yC, "$C_{t-1}$", fontsize=13, ha="center", va="center", color=C_GREEN)
    ax.text(13.9, yC, "$C_t$", fontsize=13, ha="center", va="center", color=C_GREEN)
    ax.text(9.9, yC + 0.55, "细胞状态（长期状态）", fontsize=10, color=C_GREEN, ha="center")

    def opnode(x, y, sym):
        ax.add_patch(Circle((x, y), 0.32, fc="white", ec="#333333", lw=1.4, zorder=4))
        ax.text(x, y, sym, fontsize=12, ha="center", va="center", zorder=5)

    opnode(3.3, yC, "$\\times$")
    opnode(6.2, yC, "$+$")
    opnode(6.2, 7.3, "$\\times$")
    opnode(11.25, 6.3, "$\\times$")

    def gate(x, y, label, kind):
        fc = "#fde3e3" if kind == "sig" else "#e6f0fa"
        ec = C_RED if kind == "sig" else C_BLUE
        ax.add_patch(FancyBboxPatch((x - 0.9, y - 0.55), 1.8, 1.1,
                                    boxstyle="round,pad=0.06", fc=fc, ec=ec, lw=1.3))
        sym = r"$\sigma$" if kind == "sig" else r"$\tanh$"
        ax.text(x, y + 0.14, sym, fontsize=12, ha="center", va="center")
        ax.text(x, y - 0.32, label, fontsize=8.6, ha="center", va="center",
                color="#444444")

    yG = 5.6
    gate(3.3, yG, "遗忘门 $f_t$", "sig")
    gate(5.3, yG, "输入门 $i_t$", "sig")
    gate(7.1, yG, "即时状态 $\\tilde{C}_t$", "tanh")
    gate(10.6, yG, "输出门 $o_t$", "sig")
    gate(9.0, 6.3, "", "tanh")

    ax.text(0.95, 2.0, "$h_{t-1}$", fontsize=13, ha="center", va="center")
    ax.text(0.95, 3.3, "$x_t$", fontsize=13, ha="center", va="center")
    ax.plot([1.35, 1.8], [2.0, 2.0], color=C_GRAY, lw=1.6)
    ax.plot([1.35, 1.8], [3.3, 3.3], color=C_GRAY, lw=1.6)
    ax.plot([1.8, 1.8], [2.0, 3.3], color=C_GRAY, lw=1.6)
    ax.plot([1.8, 11.45], [2.6, 2.6], color=C_GRAY, lw=1.6)
    for gx in (3.3, 5.3, 7.1, 10.6):
        arrow(ax, gx, 2.6, gx, yG - 0.64, lw=1.2)

    arrow(ax, 3.3, yG + 0.64, 3.3, yC - 0.42, lw=1.4, color=C_RED)
    arrow(ax, 5.3, yG + 0.64, 5.3, 7.3, lw=1.2, color=C_RED)
    ax.plot([5.3, 5.85], [7.3, 7.3], color=C_RED, lw=1.2)
    arrow(ax, 7.1, yG + 0.64, 7.1, 7.05, lw=1.2, color=C_BLUE)
    ax.plot([7.1, 6.57], [7.05, 7.3], color=C_BLUE, lw=1.2)
    arrow(ax, 6.2, 7.66, 6.2, yC - 0.42, lw=1.3, color=C_RED)

    ax.plot([9.0, 9.0], [yC, 6.9], color=C_GREEN, lw=1.6)
    arrow(ax, 9.92, 6.3, 10.9, 6.3, lw=1.3, color=C_BLUE)
    arrow(ax, 10.6, yG + 0.64, 10.6, 6.05, lw=1.2, color=C_RED)
    ax.plot([10.6, 10.95], [6.05, 6.22], color=C_RED, lw=1.2)
    arrow(ax, 11.6, 6.3, 12.7, 6.3, lw=1.5, color=C_GRAY)
    ax.text(13.35, 6.3, "$h_t$", fontsize=13, ha="center", va="center")
    ax.plot([12.9, 12.9, 14.6, 14.6], [6.0, 4.6, 4.6, 3.2], color="#aaaaaa",
            lw=1.1, ls="--")
    arrow(ax, 14.6, 3.2, 14.6, 2.7, color="#aaaaaa", lw=1.1, ls="--")
    ax.text(14.6, 2.2, "$h_t$ 送入\n下一时刻", fontsize=8.5, ha="center", color="#777777")

    handles = [
        Line2D([0], [0], marker="$\\times$", color="w", markerfacecolor="#333333",
               markeredgecolor="#333333", markersize=11, linestyle="none",
               label="乘法门（逐点相乘）：信息选择通过"),
        Line2D([0], [0], marker="$+$", color="w", markerfacecolor="#333333",
               markeredgecolor="#333333", markersize=11, linestyle="none",
               label="加法门（逐点相加）：信息合并通过"),
    ]
    ax.legend(handles=handles, loc="lower left", fontsize=9.5, framealpha=0.95)
    ax.text(2.6, 10.45, "LSTM 单元结构：三道门（$\\sigma$ 输出 0~1 的“闸门”）控制细胞状态的遗忘、写入与输出",
            fontsize=11.5, ha="left", color="#222222")
    save(fig, "fig11_08_lstm_cell.png")


# ======================================================================
def fig11_09_lstm_vs_rnn():
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.6))
    for ax in axes:
        ax.set_xlim(0, 12); ax.set_ylim(0, 10); ax.axis("off")

    ax = axes[0]
    ax.set_title("(a) RNN 单元：两个输入、一个输出", fontsize=11)
    ax.add_patch(FancyBboxPatch((4.6, 4.0), 2.8, 2.0, boxstyle="round,pad=0.1",
                                fc=C_LORANGE, ec=C_ORANGE, lw=1.4))
    ax.text(6.0, 5.0, r"$\tanh$", fontsize=14, ha="center", va="center")
    ax.text(2.0, 7.4, "$h_{t-1}$", fontsize=12, ha="center", va="center")
    ax.text(2.0, 2.6, "$x_t$", fontsize=12, ha="center", va="center")
    arrow(ax, 2.5, 7.1, 4.5, 5.7, lw=1.4)
    arrow(ax, 2.5, 2.9, 4.5, 4.3, lw=1.4)
    arrow(ax, 7.5, 5.0, 9.7, 5.0, lw=1.4)
    ax.text(10.2, 5.0, "$h_t$", fontsize=12, ha="center", va="center")
    ax.text(6.0, 1.9, "把过去状态与当前输入“连环”到一起，经 tanh 变换后输出，\n"
                      "只考虑最近时刻的状态", ha="center", fontsize=9.5, color="#444444")

    ax = axes[1]
    ax.set_title("(b) LSTM 单元：比 RNN 多一路输入和一路输出", fontsize=11)
    ax.add_patch(FancyBboxPatch((4.2, 3.6), 3.6, 3.2, boxstyle="round,pad=0.1",
                                fc=C_LGREEN, ec=C_GREEN, lw=1.4))
    ax.text(6.0, 5.7, "三道门 + tanh", ha="center", fontsize=9.5)
    ax.text(6.0, 4.6, "（内部完整结构见图 11-8）", ha="center", fontsize=9, color="#666666")
    ax.text(2.0, 8.2, "$h_{t-1}$", fontsize=12, ha="center", va="center")
    ax.text(2.0, 6.4, "$x_t$", fontsize=12, ha="center", va="center")
    ax.text(2.0, 2.6, "$C_{t-1}$", fontsize=12, ha="center", va="center", color=C_GREEN)
    arrow(ax, 2.5, 8.0, 4.1, 6.4, lw=1.3)
    arrow(ax, 2.5, 6.4, 4.1, 5.6, lw=1.3)
    arrow(ax, 2.5, 2.8, 4.1, 4.1, lw=1.6, color=C_GREEN)
    arrow(ax, 7.9, 6.0, 9.9, 6.9, lw=1.3)
    arrow(ax, 7.9, 4.3, 9.9, 3.5, lw=1.6, color=C_GREEN)
    ax.text(10.5, 7.1, "$h_t$", fontsize=12, ha="center", va="center")
    ax.text(10.5, 3.1, "$C_t$", fontsize=12, ha="center", va="center", color=C_GREEN)
    ax.text(6.0, 1.4, "细胞状态 $C_t$ 像“传送带”：长期信息直通下游，\n"
                      "由三道门决定哪些留下、哪些遗忘", ha="center",
            fontsize=9.5, color="#444444")
    save(fig, "fig11_09_lstm_vs_rnn.png")


# ======================================================================
def fig11_10_conv_example():
    n = 10
    img = np.full((n, n), 2.0)
    img[:, 5:] = 9.0
    padded = np.pad(img, 1)
    K = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=float)
    fm = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            fm[i, j] = np.sum(padded[i:i + 3, j:j + 3] * K)

    fig, axes = plt.subplots(2, 2, figsize=(11.8, 10.6))

    # (a) 输入（含补零）
    ax = axes[0, 0]
    ax.set_title("(a) 输入图像矩阵（外围补一圈 0）", fontsize=11)
    fc, tc = [], []
    for i in range(12):
        rf, rt = [], []
        for j in range(12):
            v = padded[i, j]
            rf.append("#f0f0f0" if v == 0 else ("#dbe9f6" if v == 2 else "#f6dcd3"))
            rt.append("#777777" if v == 0 else "#333333")
        fc.append(rf); tc.append(rt)
    grid(ax, 0.9, 0.8, 0.86, padded, facecolors=fc, txtcolors=tc, fs=7.5)
    wi, wj = 5, 4
    box(ax, 0.9 + wj * 0.86, 0.8 + (11 - (wi + 2)) * 0.86, 3 * 0.86, 3 * 0.86,
        "none", ec=C_RED, lw=2.0, zorder=5)
    ax.annotate("局部窗口\n（感受野）", xy=(0.9 + (wj + 3) * 0.86, 0.8 + (11 - wi) * 0.86),
                xytext=(12.3, 11.3), fontsize=9.5, color=C_RED, ha="left",
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.2))
    ax.set_xlim(0, 16.5); ax.set_ylim(0, 12.4); ax.axis("off")

    # (b) 卷积核
    ax = axes[0, 1]
    ax.set_title("(b) 卷积核（滤波器）", fontsize=11)
    kf = [["#ffe9e6"] * 3 for _ in range(3)]
    kf[1][1] = "#f6cfb8"
    grid(ax, 1.6, 7.0, 1.15, K, facecolors=kf, fs=12)
    ax.text(3.35, 5.6, "哈达马积（逐元素相乘）\n后求和，得到一个输出值",
            ha="center", fontsize=9.5, color="#444444")
    ax.set_xlim(0, 7); ax.set_ylim(0, 12.4); ax.axis("off")

    # (c) 特征图数值
    ax = axes[1, 0]
    ax.set_title("(c) 输出特征图（数值）", fontsize=11)
    fc2, tc2 = [], []
    for i in range(n):
        rfc, rtc = [], []
        for j in range(n):
            v = fm[i, j]
            if v > 15:
                rfc.append("#f2b8b0"); rtc.append(C_RED)
            elif v < -15:
                rfc.append("#b8d4f2"); rtc.append(C_BLUE)
            else:
                rfc.append("#f2f2f2"); rtc.append("#888888")
        fc2.append(rfc); tc2.append(rtc)
    grid(ax, 0.9, 1.0, 0.86, fm, facecolors=fc2, txtcolors=tc2, fs=7.2)
    ax.text(5.2, 0.35, "0：平坦区域；红/蓝：数值跳变的边界", ha="center",
            fontsize=9, color="#444444")
    ax.set_xlim(0, 10.4); ax.set_ylim(0, 11.0); ax.axis("off")

    # (d) 特征图可视化
    ax = axes[1, 1]
    ax.set_title("(d) 特征图可视化：轮廓被勾勒出来", fontsize=11)
    ax.imshow(fm, cmap="RdBu_r", vmin=-40, vmax=40)
    ax.set_xticks([]); ax.set_yticks([])
    cb = plt.colorbar(ax.imshow(fm, cmap="RdBu_r", vmin=-40, vmax=40), ax=ax,
                      fraction=0.045)
    cb.set_label("特征值", fontsize=9)
    ax.text(4.5, -1.3, "一个 3×3 的小核就把原图中“2 值区/9 值区”的\n边界（轮廓）提取成了高亮竖线",
            ha="center", fontsize=9.5, color="#444444")
    save(fig, "fig11_10_conv_example.png")


# ======================================================================
def fig11_11_stride_padding():
    fig, axes = plt.subplots(2, 2, figsize=(12.4, 11.6))

    def scan_panel(ax, title, inp, wins, outR, outC, note, pad_label=None):
        """wins: list of (i, j, color, out_i, out_j)，(i,j) 为输入坐标（不含 pad）"""
        ax.set_title(title, fontsize=10.8)
        nr, nc = inp.shape
        cell = 0.92
        x0, y0 = 0.9, 1.7
        for i in range(nr):
            for j in range(nc):
                box(ax, x0 + j * cell, y0 + (nr - 1 - i) * cell, cell, cell,
                    "#ffffff", ec="#888888", lw=0.7)
                ax.text(x0 + j * cell + cell / 2, y0 + (nr - 1 - i) * cell + cell / 2,
                        f"{inp[i, j]:g}", ha="center", va="center", fontsize=8)
        for k, (i, j, c, oi, oj) in enumerate(wins):
            wx = x0 + j * cell
            wy = y0 + (nr - 1 - (i + 2)) * cell
            box(ax, wx, wy, 3 * cell, 3 * cell, "none", ec=c, lw=1.8, zorder=5)
            # 左上角编号徽标（白底彩边，不遮挡输入数值）
            bx, by = wx - 0.12, wy + 3 * cell - 0.12
            ax.add_patch(Circle((bx, by), 0.26, fc="white", ec=c, lw=1.5, zorder=7))
            ax.text(bx, by, str(k + 1), ha="center", va="center", fontsize=8.5,
                    color=c, fontweight="bold", zorder=8)
        ox = x0 + nc * cell + 1.4
        out = np.full((outR, outC), np.nan)
        for i in range(outR):
            for j in range(outC):
                box(ax, ox + j * cell, y0 + (outR - 1 - i) * cell, cell, cell,
                    "#f7f7f7", ec="#888888", lw=0.7)
        for k, (i, j, c, oi, oj) in enumerate(wins):
            box(ax, ox + oj * cell, y0 + (outR - 1 - oi) * cell, cell, cell,
                c, ec="#888888", lw=0.7, alpha=0.55)
            ax.text(ox + oj * cell + cell / 2, y0 + (outR - 1 - oi) * cell + cell / 2,
                    str(k + 1), ha="center", va="center", fontsize=8.5)
        ax.text(x0 + nc * cell / 2, y0 + nr * cell + 0.35,
                f"输入 {nr}×{nc}" + (pad_label or ""), ha="center", fontsize=9.5)
        ax.text(ox + outC * cell / 2, y0 + max(outR, 3) * cell + 0.35,
                f"输出 {outR}×{outC}", ha="center", fontsize=9.5)
        ax.text((x0 + nc * cell + ox + outC * cell) / 2, 0.35, note, ha="center",
                fontsize=9, color="#444444")
        ax.set_xlim(0, ox + outC * cell + 0.6)
        ax.set_ylim(0, y0 + nr * cell + 0.8)
        ax.axis("off")

    inp5 = np.full((5, 5), 3.0)
    cols = [C_RED, C_ORANGE, C_GREEN, C_BLUE, C_PURPLE, "#8c564b", "#e377c2",
            "#17becf", "#bcbd22"]
    scan_panel(axes[0, 0], "(a) 步幅 = 1：核 3×3 逐格扫描（示 9 个位置）", inp5,
               [(0, 0, cols[0], 0, 0), (0, 1, cols[1], 0, 1), (0, 2, cols[2], 0, 2),
                (1, 0, cols[3], 1, 0), (1, 1, cols[4], 1, 1), (1, 2, cols[5], 1, 2),
                (2, 0, cols[6], 2, 0), (2, 1, cols[7], 2, 1), (2, 2, cols[8], 2, 2)],
               3, 3, "输出 = (5−3)/1 + 1 = 3，得 3×3 特征图")
    scan_panel(axes[0, 1], "(b) 步幅 = 2：跳着扫描（示 4 个位置）", inp5,
               [(0, 0, cols[0], 0, 0), (0, 2, cols[2], 0, 1),
                (2, 0, cols[6], 1, 0), (2, 2, cols[8], 1, 1)],
               2, 2, "输出 = (5−3)/2 + 1 = 2，得 2×2 特征图")
    inp7 = np.zeros((7, 7))
    inp7[1:6, 1:6] = 3.0
    scan_panel(axes[1, 0], "(c) 填充 = 1 + 核 3×3（示 4 个角位置）", inp7,
               [(0, 0, cols[0], 0, 0), (0, 4, cols[2], 0, 4),
                (4, 0, cols[6], 4, 0), (4, 4, cols[8], 4, 4)],
               5, 5, "输出 = (5+2×1−3)/1 + 1 = 5，与输入同大；边缘数据也被利用",
               pad_label="（外围一圈 0）")

    # (d) 扩张卷积：感受野示意
    ax = axes[1, 1]
    ax.set_title("(d) 扩张卷积（扩张系数 = 2）", fontsize=10.8)
    cell = 0.92
    x0, y0 = 0.9, 2.0
    for i in range(7):
        for j in range(7):
            box(ax, x0 + j * cell, y0 + (6 - i) * cell, cell, cell,
                "#ffffff", ec="#888888", lw=0.7)
            ax.text(x0 + j * cell + cell / 2, y0 + (6 - i) * cell + cell / 2,
                    "3", ha="center", va="center", fontsize=8)
    # 5×5 感受野框（左上角 (0,0)）
    box(ax, x0, y0 + 2 * cell, 5 * cell, 5 * cell, "none", ec=C_RED, lw=1.9, zorder=5)
    for i in range(3):
        for j in range(3):
            ii, jj = i * 2, j * 2
            box(ax, x0 + jj * cell, y0 + (6 - ii) * cell, cell, cell,
                "#fbd9d9", ec=C_RED, lw=1.2, zorder=4)
            ax.text(x0 + jj * cell + cell / 2, y0 + (6 - ii) * cell + cell / 2,
                    "●", ha="center", va="center", fontsize=7, color=C_RED, zorder=5)
    ax.text(x0 + 3.5 * cell, y0 + 7 * cell + 0.45,
            "红框为 5×5 感受野：9 个红色格点为核元素，白色格为“空洞”",
            ha="center", fontsize=8.8, color="#444444")
    ax.text(x0 + 3.5 * cell, 1.0, "核元素间插入空白：3×3 核等效 5×5 感受野，\n"
                                  "不增加参数个数与计算量",
            ha="center", fontsize=9, color="#444444")
    ax.set_xlim(0, x0 + 7 * cell + 0.6)
    ax.set_ylim(0, y0 + 7 * cell + 1.0)
    ax.axis("off")

    fig.suptitle("步幅、填充与扩张卷积（输入格中的编号窗口对应输出格）", fontsize=13, y=0.985)
    fig.tight_layout(rect=[0, 0, 1, 0.965])
    save(fig, "fig11_11_stride_padding.png")


# ======================================================================
def fig11_12_pooling():
    inp = np.array([[2, 3, 8, 6],
                    [4, 1, 5, 9],
                    [7, 2, 3, 4],
                    [1, 6, 8, 2]])
    mx = np.array([[4, 9], [7, 8]])
    av = np.array([[2.5, 7.0], [4.0, 4.25]])
    fig, axes = plt.subplots(1, 3, figsize=(13.4, 5.0))
    wcols = [C_RED, C_GREEN, C_BLUE, C_PURPLE]
    wfc = ["#fdeaea", "#eaf5ea", "#eaf0f8", "#f3edf9"]
    wfc2 = ["#fbd9d9", "#d9f0d9", "#d9e6f7", "#e8dbf2"]
    cell = 1.1

    ax = axes[0]
    ax.set_title("(a) 输入特征图（按 2×2 分窗）", fontsize=11)
    for i in range(4):
        for j in range(4):
            w = (i // 2) * 2 + (j // 2)
            box(ax, 0.8 + j * cell, 1.0 + (3 - i) * cell, cell, cell, wfc[w],
                ec=wcols[w], lw=1.4)
            ax.text(0.8 + j * cell + cell / 2, 1.0 + (3 - i) * cell + cell / 2,
                    f"{inp[i, j]:g}", ha="center", va="center", fontsize=10)
    ax.set_xlim(0, 6.6); ax.set_ylim(0, 6.4); ax.axis("off")

    ax = axes[1]
    ax.set_title("(b) 最大池化：取窗口最大值", fontsize=11)
    for i in range(2):
        for j in range(2):
            w = i * 2 + j
            box(ax, 1.4 + j * cell, 1.8 + (1 - i) * cell, cell, cell, wfc2[w],
                ec=wcols[w], lw=1.6)
            ax.text(1.4 + j * cell + cell / 2, 1.8 + (1 - i) * cell + cell / 2,
                    f"{mx[i, j]:g}", ha="center", va="center", fontsize=11)
    ax.text(2.5, 0.8, "在“池子”里挑最大：4×4 降为 2×2", ha="center",
            fontsize=9.5, color="#444444")
    ax.set_xlim(0, 6.6); ax.set_ylim(0, 6.4); ax.axis("off")

    ax = axes[2]
    ax.set_title("(c) 平均池化：取窗口平均值", fontsize=11)
    for i in range(2):
        for j in range(2):
            w = i * 2 + j
            box(ax, 1.4 + j * cell, 1.8 + (1 - i) * cell, cell, cell, wfc2[w],
                ec=wcols[w], lw=1.6)
            ax.text(1.4 + j * cell + cell / 2, 1.8 + (1 - i) * cell + cell / 2,
                    f"{av[i, j]:g}", ha="center", va="center", fontsize=10.5)
    ax.text(2.5, 0.8, "取窗口平均值：降维、缓解过拟合，\n图像识别中还能提供平移/旋转不变性",
            ha="center", fontsize=9.5, color="#444444")
    ax.set_xlim(0, 6.6); ax.set_ylim(0, 6.4); ax.axis("off")
    save(fig, "fig11_12_pooling.png")


# ======================================================================
def fig11_13_relu_sigmoid():
    x = np.linspace(-4, 4, 401)
    sig = 1 / (1 + np.exp(-x))
    tanh = np.tanh(x)
    relu = np.maximum(0, x)

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8))
    ax = axes[0]
    ax.plot(x, sig, color=C_BLUE, lw=2, label="Sigmoid")
    ax.plot(x, tanh, color=C_GREEN, lw=2, label="Tanh")
    ax.plot(x, relu, color=C_RED, lw=2.2, label="ReLU")
    ax.set_title("(a) 三种激活函数", fontsize=11)
    ax.set_xlabel("$x$", fontsize=11); ax.set_ylabel("$f(x)$", fontsize=11)
    ax.grid(alpha=0.3); ax.legend(fontsize=10, loc="lower right")
    ax.set_ylim(-1.4, 4.3)
    ax.text(2.15, 1.05, r"$f(x)=\max(0,\,x)$", fontsize=11, color=C_RED)

    ax = axes[1]
    ax.plot(x, sig * (1 - sig), color=C_BLUE, lw=2, label="Sigmoid 导数（最大 0.25）")
    ax.plot(x, 1 - tanh ** 2, color=C_GREEN, lw=2, label="Tanh 导数（最大 1）")
    ax.plot(x, (x > 0).astype(float), color=C_RED, lw=2.2, label="ReLU 导数（0 或 1）")
    ax.set_title("(b) 导数对比：梯度消失的关键", fontsize=11)
    ax.set_xlabel("$x$", fontsize=11); ax.set_ylabel("$f'(x)$", fontsize=11)
    ax.grid(alpha=0.3); ax.legend(fontsize=9.5, loc="upper left")
    ax.set_ylim(-0.15, 1.4)
    ax.annotate("峰值仅 0.25：深层连乘后梯度迅速消失", xy=(0, 0.25),
                xytext=(-3.9, 0.95), fontsize=9.5, color=C_BLUE,
                arrowprops=dict(arrowstyle="->", color=C_BLUE))
    ax.text(2.15, 1.08, "x>0 时恒为 1：\n反向传播不衰减", fontsize=9.5, color=C_RED)
    save(fig, "fig11_13_relu_sigmoid.png")


# ======================================================================
def smooth_rand(m):
    q = m.copy()
    for _ in range(4):
        qq = q.copy()
        qq[1:-1, 1:-1] = (q[1:-1, 1:-1] + q[:-2, 1:-1] + q[2:, 1:-1] +
                          q[1:-1, :-2] + q[1:-1, 2:] + q[:-2, :-2] +
                          q[:-2, 2:] + q[2:, :-2] + q[2:, 2:]) / 9
        q = qq
    return q


def fig11_14_multilayer_cnn():
    fig = plt.figure(figsize=(14.2, 5.8))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 20); ax.set_ylim(0, 9); ax.axis("off")

    img = smooth_rand(rng.random((12, 12)))
    fig.add_axes([0.02, 0.36, 0.09, 0.20]).imshow(img, cmap="YlGn")
    for a in fig.axes[1:]:
        a.axis("off")
    ax.text(1.2, 2.85, "输入图像", ha="center", fontsize=10)

    def fmap_stack(x, y, n_maps, size, step, cmap):
        for m in range(n_maps):
            xx = x + m * step
            yy = y - (m % 2) * 0.08
            fm = smooth_rand(rng.random((10, 10)))
            am = fig.add_axes([xx / 20, yy / 9, size / 20, size / 9])
            am.imshow(fm, cmap=cmap)
            am.axis("off")

    # 布局：s1 [3.0,6.01] s2 [6.7,9.95] s3 [10.6,14.15] 圆点 15.05 条形 15.9 起
    arrow(ax, 2.45, 4.1, 2.9, 4.1)
    ax.text(2.65, 4.95, "卷积 + ReLU", ha="center", fontsize=8.5)
    fmap_stack(3.0, 3.3, 4, 1.15, 0.62, "Blues")
    ax.text(4.5, 2.8, "特征图 16×16", ha="center", fontsize=9)

    arrow(ax, 6.15, 4.1, 6.55, 4.1)
    ax.text(6.35, 4.95, "池化", ha="center", fontsize=8.5)
    fmap_stack(6.7, 3.45, 6, 0.95, 0.50, "Greens")
    ax.text(8.3, 2.8, "特征图 8×8", ha="center", fontsize=9)

    arrow(ax, 10.1, 4.1, 10.45, 4.1)
    ax.text(10.28, 4.95, "卷积 + 池化", ha="center", fontsize=8.5)
    fmap_stack(10.6, 3.55, 8, 0.75, 0.40, "Oranges")
    ax.text(12.4, 2.8, "特征图 4×4", ha="center", fontsize=9)

    arrow(ax, 14.3, 4.1, 14.75, 4.1)
    ax.text(14.52, 4.95, "展平", ha="center", fontsize=8.5)
    for yy in [4.9, 4.3, 3.7, 3.1]:
        ax.add_patch(Circle((15.05, yy), 0.16, fc=C_PURPLE, ec="none", zorder=3))
    ax.text(15.05, 2.55, "全连接", ha="center", fontsize=9)
    arrow(ax, 15.3, 4.1, 15.7, 4.1)

    labels = ["羊", "狗", "猫", "狮子"]
    probs = [0.04, 0.09, 0.16, 0.71]
    lcols = ["#c7c7c7", "#c7c7c7", "#c7c7c7", C_RED]
    for k, (lb, pb, cb) in enumerate(zip(labels, probs, lcols)):
        yy = 5.7 - k * 0.8
        ax.add_patch(Rectangle((16.0, yy), pb * 3.4, 0.55, fc=cb, ec="none"))
        ax.text(15.85, yy + 0.27, lb, ha="right", va="center", fontsize=9.5)
        ax.text(16.1 + pb * 3.4, yy + 0.27, f"{pb:.2f}", ha="left", va="center",
                fontsize=8.5, color="#444444")
    ax.text(17.1, 6.75, "Softmax 分类", ha="center", fontsize=9.5)

    ax.text(4.9, 7.9, "层浅：学到边缘、纹理等局部特征", ha="center", fontsize=10, color=C_BLUE)
    ax.text(12.6, 7.9, "层深：特征更全局化（部件 → 整体）", ha="center", fontsize=10, color=C_ORANGE)
    arrow(ax, 3.0, 7.35, 6.6, 7.35, color=C_BLUE, lw=1.2, style="<|-")
    arrow(ax, 8.0, 7.35, 13.4, 7.35, color=C_ORANGE, lw=1.2, style="<|-")
    ax.text(10.0, 1.5, "“卷积 → 激活 → 池化”反复堆叠，低级特征逐层组合成高级特征，最后接全连接层与 Softmax 输出各类别概率",
            ha="center", fontsize=9.5, color="#444444")
    save(fig, "fig11_14_multilayer_cnn.png")


if __name__ == "__main__":
    fig11_01_dl_timeline()
    fig11_02_local_connect_share()
    fig11_03_layerwise_pretrain()
    fig11_04_alexnet()
    fig11_05_residual_block()
    fig11_06_rnn_structure()
    fig11_07_rnn_io_modes()
    fig11_08_lstm_cell()
    fig11_09_lstm_vs_rnn()
    fig11_10_conv_example()
    fig11_11_stride_padding()
    fig11_12_pooling()
    fig11_13_relu_sigmoid()
    fig11_14_multilayer_cnn()
    print("ALL DONE")
