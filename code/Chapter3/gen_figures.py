# -*- coding: utf-8 -*-
"""第03章 数据预处理与可视化 插图生成脚本"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import matplotlib.gridspec as gridspec

OUT = r"C:\20260905\项目 人工智能与地理数据挖掘\书稿\figs\ch03"

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["figure.dpi"] = 100

C_BLUE = "#1f77b4"
C_ORANGE = "#ff7f0e"
C_GREEN = "#2ca02c"
C_RED = "#d62728"
C_PURPLE = "#9467bd"
C_GRAY = "#7f7f7f"

rng = np.random.default_rng(42)


def save(fig, name):
    fig.savefig(f"{OUT}\\{name}", bbox_inches="tight")
    plt.close(fig)
    print("saved:", name)


# ---------------------------------------------------------------- 3-1 四大任务
def fig3_01_four_tasks():
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.5))
    (a, b), (c, d) = axes

    # (a) 清洗 = 查漏补缺：一行数据格，缺值/错值 → 补好
    a.set_xlim(0, 10); a.set_ylim(0, 4); a.axis("off")
    vals = [28, 30, None, 27, "31", 29, None, 26, 28, 30]   # None=缺失, "31"=错误
    for j, v in enumerate(vals):
        if v is None:
            a.add_patch(Rectangle((j, 2.5), 0.9, 0.9, fc="white", ec=C_RED, ls="--", lw=1.5))
            a.text(j + 0.45, 2.95, "?", ha="center", va="center", color=C_RED, fontsize=13)
        elif isinstance(v, str):
            a.add_patch(Rectangle((j, 2.5), 0.9, 0.9, fc="white", ec=C_RED, lw=1.2))
            a.text(j + 0.45, 2.95, v, ha="center", va="center", color=C_RED, fontsize=10)
            a.text(j + 0.45, 3.7, "×", ha="center", color=C_RED, fontsize=13)
        else:
            a.add_patch(Rectangle((j, 2.5), 0.9, 0.9, fc="#dceefb", ec=C_BLUE, lw=1.2))
            a.text(j + 0.45, 2.95, str(v), ha="center", va="center", fontsize=9)
    fixed = [28, 30, 29, 27, 29, 29, 28, 26, 28, 30]
    for j, v in enumerate(fixed):
        a.add_patch(Rectangle((j, 0.6), 0.9, 0.9, fc="#dceefb", ec=C_BLUE, lw=1.2))
        if vals[j] is None or isinstance(vals[j], str):
            a.text(j + 0.45, 1.05, str(v), ha="center", va="center", fontsize=9, color=C_GREEN, fontweight="bold")
        else:
            a.text(j + 0.45, 1.05, str(v), ha="center", va="center", fontsize=9)
    a.annotate("", xy=(4.6, 0.9), xytext=(4.6, 2.3),
               arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=2))
    a.set_title("(a) 数据清洗 = 查漏补缺：填补缺失、纠正错误、去除离群", fontsize=11)

    # (b) 集成 = 加法：多个数据源 → 一个数据集
    b.set_xlim(0, 10); b.set_ylim(0, 4); b.axis("off")
    srcs = [(0.2, 2.8, C_BLUE, "数据库 A"), (0.2, 0.5, C_ORANGE, "数据库 B"), (3.6, 1.6, C_GREEN, "文件 C")]
    for x, y, col, lab in srcs:
        b.add_patch(FancyBboxPatch((x, y), 2.2, 1.0, boxstyle="round,pad=0.08",
                                   fc="white", ec=col, lw=1.8))
        b.text(x + 1.1, y + 0.5, lab, ha="center", va="center", fontsize=10, color=col)
        b.annotate("", xy=(6.6, 1.75), xytext=(x + 2.4, y + 0.5),
                   arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.6,
                                   connectionstyle="arc3,rad=0.15"))
    b.add_patch(FancyBboxPatch((6.6, 1.0), 3.0, 1.5, boxstyle="round,pad=0.08",
                               fc="#fff3e0", ec=C_RED, lw=2))
    b.text(8.1, 1.75, "集成后的\n统一数据集", ha="center", va="center", fontsize=10, color=C_RED)
    b.set_title("(b) 数据集成 = 加法：多个数据源合并为一个（少变多）", fontsize=11)

    # (c) 缩减 = 减法：大表格去掉若干行、列
    c.set_xlim(0, 10); c.set_ylim(0, 4); c.axis("off")
    drop_cols, drop_rows = {6, 7}, {5, 6}
    for i in range(7):
        for j in range(9):
            bad = (j in drop_cols) or (i in drop_rows)
            c.add_patch(Rectangle((j, 3.2 - i * 0.42), 0.38, 0.36,
                                  fc="white" if bad else "#dceefb",
                                  ec=C_GRAY if bad else C_BLUE, lw=0.8,
                                  hatch="xx" if bad else None))
    c.annotate("", xy=(6.3, 1.9), xytext=(5.8, 1.9),
               arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=2))
    keep = np.array([[3.2 - i * 0.42 for i in range(5)]] * 7)
    for i in range(5):
        for j in range(7):
            c.add_patch(Rectangle((7.1 + j * 0.38, 3.2 - i * 0.42), 0.34, 0.36,
                                  fc="#e8f5e9", ec=C_GREEN, lw=0.9))
    c.text(4.5, 0.05, "去掉冗余列与部分行", ha="center", fontsize=9, color=C_GRAY)
    c.set_title("(c) 数据缩减 = 减法：降维、减少样本量、压缩（多变少）", fontsize=11)

    # (d) 变换 = 乘除法：长轴按比例缩放到短轴
    d.set_xlim(0, 10); d.set_ylim(0, 4); d.axis("off")
    d.add_patch(Rectangle((0.4, 2.5), 8.8, 0.8, fc="#dceefb", ec=C_BLUE, lw=1.5))
    for x, lab in [(0.4, "0"), (4.8, "500"), (9.2, "1000")]:
        d.text(x, 3.45, lab, ha="center", fontsize=9, color=C_BLUE)
    d.annotate("", xy=(4.9, 1.5), xytext=(4.9, 2.4),
               arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=2))
    d.text(5.15, 1.95, "按比例缩放", fontsize=9, color=C_GRAY)
    d.add_patch(Rectangle((0.4, 0.4), 8.8, 0.8, fc="#fff3e0", ec=C_ORANGE, lw=1.5))
    for x, lab in [(0.4, "0"), (4.8, "0.5"), (9.2, "1")]:
        d.text(x, 1.35, lab, ha="center", fontsize=9, color=C_ORANGE)
    d.set_title("(d) 数据变换 = 乘除法：缩放/取对数/线性组合（变形式）", fontsize=11)

    fig.tight_layout()
    save(fig, "fig3_01_four_tasks.png")


# ---------------------------------------------------------------- 3-2 过程
def fig3_02_process():
    fig, ax = plt.subplots(figsize=(11.5, 4.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")

    def box(x, y, w, h, text, fc, ec, fs=10):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                                    fc=fc, ec=ec, lw=1.8))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)

    box(0.15, 3.0, 1.5, 1.0, "原始数据", "#f5f5f5", C_GRAY)
    box(2.05, 3.0, 1.7, 1.0, "数据清理\n（查漏补缺）", "#dceefb", C_BLUE)
    box(4.05, 3.0, 1.7, 1.0, "数据集成\n（加法）", "#dceefb", C_BLUE)
    box(6.05, 3.0, 1.7, 1.0, "数据缩减\n（减法）", "#dceefb", C_BLUE)
    box(8.05, 3.0, 1.7, 1.0, "数据变换\n（乘除法）", "#dceefb", C_BLUE)
    box(10.05, 3.0, 1.8, 1.0, "满足要求的\n干净数据", "#e8f5e9", C_GREEN)
    box(7.6, 0.6, 1.8, 1.0, "机器学习\n建模", "#fff3e0", C_ORANGE)
    box(10.05, 0.6, 1.8, 1.0, "模型评估", "#fff3e0", C_ORANGE)

    arr = dict(arrowstyle="-|>", color=C_GRAY, lw=1.8)
    for x0, x1 in [(1.65, 2.05), (3.75, 4.05), (5.75, 6.05), (7.75, 8.05), (9.75, 10.05)]:
        ax.annotate("", xy=(x1, 3.5), xytext=(x0, 3.5), arrowprops=arr)
    ax.annotate("", xy=(9.7, 1.1), xytext=(10.6, 2.95), arrowprops=arr)
    ax.annotate("", xy=(8.6, 1.1), xytext=(10.0, 1.1), arrowprops=arr)
    # 反馈回路
    fb = dict(arrowstyle="-|>", color=C_RED, lw=1.8, connectionstyle="arc3,rad=-0.35", ls="--")
    ax.annotate("", xy=(2.9, 4.35), xytext=(8.5, 1.3), arrowprops=fb)
    ax.text(5.6, 3.95, "效果不佳？回到数据检查：是不是清洗有误、某些自变量不该放进来",
            ha="center", fontsize=9.5, color=C_RED)
    ax.text(6.0, 4.75, "数据预处理的一般过程（步骤顺序可调整，且往往需要循环往复）",
            ha="center", fontsize=11)
    fig.tight_layout()
    save(fig, "fig3_02_process.png")


# ---------------------------------------------------------------- 3-3 缺失值填充
def fig3_03_missing_value_fill():
    t = np.arange(1, 16)
    temp = np.array([22.0, 23.1, 24.5, 26.2, 27.8, 28.9, 30.2, np.nan, 25.1,
                     24.3, 23.0, 21.8, 22.6, 23.4, 24.0])
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.plot(t, temp, "-o", color=C_BLUE, ms=5, label="日平均温度（含缺失）")
    k = 7  # 第 8 天缺失（0 起）
    ax.plot(t[k], 30.2, "s", color=C_ORANGE, ms=9, zorder=5)
    ax.plot(t[k], 25.1, "s", color=C_ORANGE, ms=9, zorder=5)
    ax.plot([], [], "s", color=C_ORANGE, ms=9, label="相邻值：前一天 30.2 / 后一天 25.1")
    ax.plot(t[k], 27.65, "*", color=C_RED, ms=17, zorder=6,
            label="相邻平均值 27.65（本例采用）")
    ax.axvline(t[k], color=C_GRAY, ls=":", lw=1)
    ax.annotate("缺失（NaN）", xy=(t[k], 22.4), xytext=(t[k] + 1.2, 21.0),
                fontsize=10, color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED))
    ax.set_xlabel("日期（第 n 天）"); ax.set_ylabel("温度（℃）")
    ax.set_title("缺失值的填充：用相邻值或相邻平均值补缺（时间序列常用插值思想）")
    ax.grid(alpha=0.3); ax.legend(fontsize=9, loc="upper right")
    ax.set_ylim(19.5, 32.5)
    fig.tight_layout()
    save(fig, "fig3_03_missing_value_fill.png")


# ---------------------------------------------------------------- 3-4 箱线图
def fig3_04_boxplot():
    data = rng.normal(20, 4, 160)
    data = np.concatenate([data, [38.5, 41.2, 3.5, 1.2, 43.0]])
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    bp = ax.boxplot(data, vert=True, widths=0.35, patch_artist=True,
                    boxprops=dict(facecolor="#dceefb", edgecolor=C_BLUE, lw=1.6),
                    medianprops=dict(color=C_RED, lw=2),
                    whiskerprops=dict(color=C_BLUE, lw=1.6),
                    capprops=dict(color=C_BLUE, lw=1.6),
                    flierprops=dict(marker="o", markerfacecolor=C_ORANGE,
                                    markeredgecolor=C_RED, markersize=7))
    q1, med, q3 = np.percentile(data, [25, 50, 75])
    iqr = q3 - q1
    ax.hlines([q1, med, q3], 0.82, 1.0, color="none")
    for v, lab, dy in [(q1, "下四分位数 Q1", -0.9), (med, "中位数", 0), (q3, "上四分位数 Q3", 0.9)]:
        ax.text(1.2, v + dy, f"{lab} = {v:.1f}", fontsize=9.5, va="center")
        ax.plot([1.18], [v], "o", ms=4, color="k")
    ax.annotate("上须 = Q3 + 1.5×IQR", xy=(1.18, q3 + 1.5 * iqr), xytext=(1.55, q3 + 1.5 * iqr + 3),
                fontsize=9.5, arrowprops=dict(arrowstyle="->", color=C_GRAY))
    ax.annotate("离群点（可疑噪声/极端值）", xy=(1.0, 41.2), xytext=(1.6, 44),
                fontsize=10, color=C_RED, arrowprops=dict(arrowstyle="->", color=C_RED))
    ax.annotate("下须 = Q1 − 1.5×IQR", xy=(1.18, q1 - 1.5 * iqr), xytext=(1.55, q1 - 1.5 * iqr - 4),
                fontsize=9.5, arrowprops=dict(arrowstyle="->", color=C_GRAY))
    ax.set_xticks([])
    ax.set_ylabel("属性取值")
    ax.set_title("箱线图（盒须图）检测离群数据：须以外的点即离群点")
    ax.set_xlim(0.6, 2.6)
    fig.tight_layout()
    save(fig, "fig3_04_boxplot.png")


# ---------------------------------------------------------------- 3-5 冗余相关
def fig3_05_correlation_redundancy():
    x1 = rng.uniform(0, 100, 120)
    x2 = 0.3 + 0.95 * x1 + rng.normal(0, 5, 120)
    x3 = rng.uniform(0, 100, 120)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4))
    r_hi = np.corrcoef(x1, x2)[0, 1]
    axes[0].scatter(x1, x2, s=22, color=C_BLUE, alpha=0.75)
    axes[0].set_xlabel("$X_1$（如：年均降雨量）"); axes[0].set_ylabel("$X_2$（如：年均径流量）")
    axes[0].set_title(f"(a) r = {r_hi:.2f}：高度相关，信息冗余\n两个变量只需保留其一")
    axes[1].scatter(x1, x3, s=22, color=C_GREEN, alpha=0.75)
    axes[1].set_xlabel("$X_1$（如：年均降雨量）"); axes[1].set_ylabel("$X_3$（如：站点高程）")
    r_lo = np.corrcoef(x1, x3)[0, 1]
    axes[1].set_title(f"(b) r = {r_lo:.2f}：几乎不相关\n两个变量各自携带独立信息")
    for ax in axes:
        ax.grid(alpha=0.3)
    fig.tight_layout()
    save(fig, "fig3_05_correlation_redundancy.png")


# ---------------------------------------------------------------- 3-6 抽样
def fig3_06_sampling():
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.2))
    n = 60
    pop = rng.uniform(0, 10, (n, 2))

    sel = rng.choice(n, 12, replace=False)
    axes[0].scatter(pop[:, 0], pop[:, 1], s=26, color=C_GRAY, alpha=0.6)
    axes[0].scatter(pop[sel, 0], pop[sel, 1], s=200, facecolors="none",
                    edgecolors=C_RED, linewidths=1.8)
    axes[0].set_title("(a) 简单随机抽样（不放回）\n抽中即移除，不会重复出现")

    sel2 = rng.choice(n, 12, replace=True)
    uniq, cnt = np.unique(sel2, return_counts=True)
    axes[1].scatter(pop[:, 0], pop[:, 1], s=26, color=C_GRAY, alpha=0.6)
    for k_idx, c in zip(uniq, cnt):
        axes[1].scatter(pop[k_idx, 0], pop[k_idx, 1], s=200, facecolors="none",
                        edgecolors=C_RED, linewidths=1.8)
        if c > 1:
            axes[1].scatter(pop[k_idx, 0], pop[k_idx, 1], s=320, facecolors="none",
                            edgecolors=C_ORANGE, linewidths=1.8)
    axes[1].set_title("(b) 有放回抽样\n同一对象可能被再次抽中（双圈）")

    centers = [(2.5, 7.5), (7.5, 2.5), (7.5, 7.5)]
    cols = [C_BLUE, C_ORANGE, C_GREEN]
    lab = ["层 1", "层 2", "层 3"]
    pts_all, tags = [], []
    for ci, (cx, cy) in enumerate(centers):
        pts = rng.normal((cx, cy), 0.8, (20, 2))
        pts_all.append(pts)
        axes[2].scatter(pts[:, 0], pts[:, 1], s=26, color=cols[ci], alpha=0.6)
        pick = rng.choice(20, 4, replace=False)
        axes[2].scatter(pts[pick, 0], pts[pick, 1], s=200, facecolors="none",
                        edgecolors=C_RED, linewidths=1.8)
        axes[2].text(cx, cy + 2.0, lab[ci], ha="center", fontsize=10, color=cols[ci])
    axes[2].set_title("(c) 分层抽样\n每层抽取相同个数，适合偏斜数据")
    for ax in axes:
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlim(-0.5, 11); ax.set_ylim(-0.5, 11)
    fig.tight_layout()
    save(fig, "fig3_06_sampling.png")


# ---------------------------------------------------------------- 3-7 规范化对比
def fig3_07_normalization_compare():
    v = rng.gamma(2.0, 150.0, 800)          # 类降雨量：右偏，0~1000 量级
    v_mm = (v - v.min()) / (v.max() - v.min())
    v_z = (v - v.mean()) / v.std()
    j = int(np.ceil(np.log10(v.max())))
    v_d = v / 10 ** j
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.6))
    datas = [(v, "原始数据（降雨量 P）", "取值 0~1000，量级大", C_GRAY),
             (v_mm, "最小-最大规范化", r"$v'=(v-\min)/(\max-\min)$，落入 [0, 1]", C_BLUE),
             (v_z, "Z 得分规范化", r"$v'=(v-\bar v)/\sigma_v$，均值 0、标准差 1", C_GREEN),
             (v_d, "小数定标规范化", rf"$v'=v/10^{{{j}}}$，移动小数点", C_ORANGE)]
    for ax, (d, ttl, sub, col) in zip(axes, datas):
        ax.hist(d, bins=30, color=col, alpha=0.8, edgecolor="white")
        ax.set_title(ttl + "\n" + sub, fontsize=10)
        ax.grid(alpha=0.3)
    fig.suptitle("三种常用规范化方法的效果对比（同一份右偏数据）", fontsize=12, y=1.06)
    fig.tight_layout()
    save(fig, "fig3_07_normalization_compare.png")


# ---------------------------------------------------------------- 3-8 越界问题
def fig3_08_new_data_overflow():
    fig, axes = plt.subplots(2, 1, figsize=(9.5, 5.6))

    def two_axis(ax, omin, omax, points, title, note, note_col):
        ax.axis("off")
        ax.set_xlim(-0.35, 1.45); ax.set_ylim(-0.15, 1.3)
        # 原始轴
        ax.annotate("", xy=(1.35, 1.0), xytext=(-0.05, 1.0),
                    arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.6))
        for x0, lab in [(0.0, str(omin)), (1.3, str(omax))]:
            ax.text(x0, 1.08, lab, ha="center", fontsize=10, color=C_GRAY)
        ax.text(-0.3, 0.86, "原始取值", fontsize=9.5, color=C_GRAY)
        # 变换后轴
        ax.annotate("", xy=(1.35, 0.15), xytext=(-0.05, 0.15),
                    arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.6))
        for x0, lab in [(0.0, "0"), (1.3, "1")]:
            ax.text(x0, 0.23, lab, ha="center", fontsize=10, color=C_GRAY)
        ax.text(-0.3, 0.02, "变换后", fontsize=9.5, color=C_GRAY)
        for ox, nv, col, lab in points:
            fx = (ox - omin) / (omax - omin)
            fy = nv
            ax.plot([fx], [1.0], "o", ms=7, color=C_BLUE)
            ax.plot([fy], [0.15], "o", ms=7, color=col)
            ax.annotate("", xy=(fy, 0.15), xytext=(fx, 1.0),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.4,
                                        connectionstyle="arc3,rad=0.25"))
            ax.text(fx, 1.08, str(ox), ha="center", fontsize=10, color=C_BLUE)
            ax.text(fy, 0.23, f"{nv:.2f}", ha="center", fontsize=10, color=col)
            ax.text((fx + fy) / 2, 0.6, lab, ha="center", fontsize=9.5, color=col)
        ax.set_title(title, fontsize=11)
        ax.text(0.55, -0.12, note, ha="center", fontsize=10, color=note_col)

    two_axis(axes[0], 1, 100,
             [(50, 0.495, C_GREEN, "旧数据 50"),
              (110, 1.09, C_RED, "新数据 110"),
              (0.2, -0.008, C_RED, "新数据 0.2")],
             "(a) 问题：按历史数据的 min=1、max=100 建立映射",
             "新数据超出 [min, max] 时，变换结果跑出 [0, 1] 甚至变成负数，后续计算可能报错", C_RED)
    two_axis(axes[1], 0, 150,
             [(50, 0.333, C_GREEN, "旧数据 50"),
              (110, 0.733, C_GREEN, "新数据 110"),
              (0.2, 0.001, C_GREEN, "新数据 0.2")],
             "(b) 解决：预留余地，把映射范围放宽为 min=0、max=150",
             "边界适当外扩后，新数据仍落在 [0, 1] 内；Z 得分规范化同理，均值与标准差也应放宽估计", C_GREEN)
    fig.tight_layout()
    save(fig, "fig3_08_new_data_overflow.png")


# ---------------------------------------------------------------- 3-9 离散化
def fig3_09_discretization():
    v = np.sort(rng.gamma(2.0, 150.0, 200))
    fig, axes = plt.subplots(2, 1, figsize=(10, 5.2))
    for ax, mode in zip(axes, ["width", "freq"]):
        ax.set_xlim(v.min() - 30, v.max() + 30)
        ax.set_ylim(-0.35, 1.45)
        # 数轴与数
        ax.axhline(0, color=C_GRAY, lw=1.4)
        ax.plot(v, np.zeros_like(v), "|", color=C_BLUE, ms=9)
        if mode == "width":
            edges = np.linspace(v.min(), v.max(), 6)
            ttl = "(a) 等宽法：区间宽度相等，各区间样本数不等（右端稀疏）"
        else:
            edges = np.quantile(v, np.linspace(0, 1, 6))
            ttl = "(b) 等频法：按频数划分，各区间样本数相等、宽度不等"
        for k in range(5):
            fc = ["#dceefb", "#e8f5e9", "#fff3e0", "#f3e5f5", "#ffebee"][k]
            ax.add_patch(Rectangle((edges[k], 0.12), edges[k + 1] - edges[k], 0.5,
                                   fc=fc, ec=C_GRAY, lw=1.0))
            cnt = np.sum((v >= edges[k]) & (v < edges[k + 1] + (1e-9 if k == 4 else 0)))
            ax.text((edges[k] + edges[k + 1]) / 2, 0.37, f"{cnt} 个", ha="center",
                    va="center", fontsize=9.5)
            ax.plot([(edges[k] + edges[k + 1]) / 2], [0.78], "o", color=C_RED, ms=6)
        ax.plot([(edges[k] + edges[k + 1]) / 2 for k in range(5)], [0.78] * 5,
                "none")
        ax.text((edges[2] + edges[3]) / 2, 1.0, "落入各区间的值用区间代表值（圆点）代替",
                ha="center", fontsize=9.5, color=C_RED)
        for e in edges[1:-1]:
            ax.axvline(e, ymax=0.62, color=C_GRAY, ls="--", lw=1.0)
        ax.set_title(ttl, fontsize=11)
        ax.set_xlabel("属性取值（一维数轴）")
        ax.set_yticks([])
    fig.tight_layout()
    save(fig, "fig3_09_discretization.png")


# ---------------------------------------------------------------- 3-10 对数变换
def fig3_10_log_transform():
    x = rng.uniform(1, 10, 60)
    y = 5 * x ** 3 * (1 + rng.normal(0, 0.08, 60))     # 流量随水深近似三次方
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4))
    axes[0].scatter(x, y, s=26, color=C_BLUE, alpha=0.8)
    xs = np.linspace(1, 10, 100)
    axes[0].plot(xs, 5 * xs ** 3, "--", color=C_RED, lw=1.5)
    axes[0].text(2.0, 2900, "$y \\approx 5x^{3}$（曲线关系）", fontsize=11, color=C_RED)
    axes[0].set_xlabel("水深 x（m）"); axes[0].set_ylabel("流量 Q（m³/s）")
    axes[0].set_title("(a) 原始数据：流量随水深呈高次方增长")
    lx, ly = np.log10(x), np.log10(y)
    axes[1].scatter(lx, ly, s=26, color=C_GREEN, alpha=0.8)
    k, b = np.polyfit(lx, ly, 1)
    xsl = np.linspace(lx.min(), lx.max(), 50)
    axes[1].plot(xsl, k * xsl + b, "--", color=C_RED, lw=1.5)
    axes[1].text(0.15, 2.35, f"$\\lg y = {b:.2f} + {k:.2f}\\,\\lg x$（斜率≈3）",
                 fontsize=11, color=C_RED)
    axes[1].set_xlabel("$\\lg x$（水深对数）"); axes[1].set_ylabel("$\\lg Q$（流量对数）")
    axes[1].set_title("(b) 双对数变换后：近似直线关系")
    for ax in axes:
        ax.grid(alpha=0.3)
    fig.tight_layout()
    save(fig, "fig3_10_log_transform.png")


# ---------------------------------------------------------------- 3-11 季节星期
def fig3_11_season_week():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    wd = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    cnt = np.array([8.2, 8.5, 8.3, 8.6, 8.4, 5.2, 4.9]) + rng.normal(0, 0.15, 7)
    cols = [C_BLUE] * 5 + [C_ORANGE] * 2
    axes[0].bar(wd, cnt, color=cols, alpha=0.85, edgecolor="white")
    axes[0].set_ylabel("借车量（千次）")
    axes[0].set_title("(a) 星期因素：工作日与周末的用量明显不同")
    axes[0].grid(alpha=0.3, axis="y")
    axes[0].text(3.0, 9.6, "用哑变量区分“工作日/周末”", ha="center", fontsize=9.5, color=C_GRAY)
    ss = ["春", "夏", "秋", "冬"]
    cnt2 = np.array([7.6, 8.8, 8.1, 4.2]) + rng.normal(0, 0.15, 4)
    axes[1].bar(ss, cnt2, color=[C_GREEN, C_RED, C_ORANGE, C_BLUE], alpha=0.85, edgecolor="white")
    axes[1].set_ylabel("日均借车量（千次）")
    axes[1].set_title("(b) 季节因素：冬季寒冷，骑行量显著下降")
    axes[1].grid(alpha=0.3, axis="y")
    fig.suptitle("时间数据类型的特征构造：地铁口共享单车借用量示意", fontsize=12)
    fig.tight_layout()
    save(fig, "fig3_11_season_week.png")


# ---------------------------------------------------------------- 3-12 MATLAB 基本二维
def fig3_12_matlab_basic_2d():
    fig, axes = plt.subplots(2, 3, figsize=(12.5, 6.6))
    t = np.linspace(0, 2 * np.pi, 60)
    y1, y2 = np.sin(t) * 8 + 15, np.cos(t) * 90 + 100

    ax = axes[0, 0]
    ax.plot(t, y1, "-o", color=C_BLUE, ms=4, label="温度")
    ax.plot(t, y1 - 4, "-s", color=C_ORANGE, ms=4, label="湿度")
    ax.grid(alpha=0.4)
    ax.set_title("plot + grid + legend")
    ax.set_xlabel("t/h"); ax.set_ylabel("观测值")
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    ax.plot(t, y1, color=C_BLUE, lw=2)
    ax.set_ylabel("温度（℃）", color=C_BLUE)
    ax2 = ax.twinx()
    ax2.plot(t, y2, color=C_ORANGE, lw=2)
    ax2.set_ylabel("降雨量（mm）", color=C_ORANGE)
    ax.set_title("plotyy：双坐标轴图")

    ax = axes[0, 2]
    ax.bar(t, 3 + np.abs(np.sin(t * 2)), width=0.09, color="#dceefb", edgecolor=C_BLUE, label="柱状")
    ax.plot(t, 3.6 + 0.9 * np.sin(t * 2), "o-", color=C_RED, ms=3, lw=1.4, label="曲线")
    ax.set_title("hold on：重叠图")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    ax.hist(rng.normal(20, 4, 300), bins=18, color=C_GREEN, alpha=0.8, edgecolor="white")
    ax.set_title("hist：直方图")
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    ax.pie([28, 34, 22, 16], labels=["A 类", "B 类", "C 类", "D 类"],
           autopct="%.0f%%", colors=[C_BLUE, C_ORANGE, C_GREEN, C_RED],
           textprops=dict(fontsize=8), startangle=90)
    ax.set_title("pie：饼状图")

    ax = axes[1, 2]
    ax.stairs(np.round(3 + 2 * np.abs(np.sin(t))),
              np.append(t, t[-1] + t[1] - t[0]), color=C_PURPLE, lw=1.8)
    ax.set_title("stairs：阶梯图")
    ax.grid(alpha=0.3)

    fig.suptitle("MATLAB 基本二维绘图命令效果示例", fontsize=12, y=1.0)
    fig.tight_layout()
    save(fig, "fig3_12_matlab_basic_2d.png")


# ---------------------------------------------------------------- 3-13 MATLAB 三维
def fig3_13_matlab_3d():
    fig = plt.figure(figsize=(11, 8))
    ax1 = fig.add_subplot(2, 2, 1, projection="3d")
    th = np.linspace(0, 6 * np.pi, 300)
    ax1.plot(np.cos(th), np.sin(th), th * 0.2, color=C_BLUE, lw=1.4)
    ax1.set_title("plot3：三维曲线")

    x = np.linspace(-3, 3, 40); y = np.linspace(-3, 3, 40)
    X, Y = np.meshgrid(x, y)
    Z = (1 - X / 4 + X ** 3 / 16 + Y ** 2 / 9) * np.exp(-0.25 * (X ** 2 + Y ** 2))

    ax2 = fig.add_subplot(2, 2, 2, projection="3d")
    ax2.plot_wireframe(X, Y, Z, color=C_BLUE, lw=0.6)
    ax2.set_title("mesh：曲面的网格图")

    ax3 = fig.add_subplot(2, 2, 3, projection="3d")
    s = ax3.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
    ax3.set_title("surf + colormap：着色表面图")
    fig.colorbar(s, ax=ax3, shrink=0.7)

    ax4 = fig.add_subplot(2, 2, 4)
    cs = ax4.contourf(X, Y, Z, levels=14, cmap="viridis")
    fig.colorbar(cs, ax=ax4, shrink=0.9)
    ax4.set_title("contour：等高线（填充）图")
    fig.suptitle("MATLAB 常用三维绘图命令效果示例", fontsize=12)
    fig.tight_layout()
    save(fig, "fig3_13_matlab_3d.png")


# ---------------------------------------------------------------- 3-14 相关系数矩阵
def fig3_14_corr_matrix():
    p = 8
    base = rng.normal(0, 1, (300, 4))
    cols = []
    names = ["高程", "坡度", "降雨", "径流", "气温", "湿度", "人口", "GDP"]
    group = [0, 0, 1, 1, 2, 2, 3, 3]
    for g in group:
        z = 0.8 * base[:, g] + rng.normal(0, 0.6, 300)
        cols.append(z)
    D = np.column_stack(cols)
    C = np.corrcoef(D, rowvar=False)
    fig, ax = plt.subplots(figsize=(8.2, 7))
    im = ax.imshow(C, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(p)); ax.set_yticks(range(p))
    ax.set_xticklabels(names, rotation=45, ha="right")
    ax.set_yticklabels(names)
    for i in range(p):
        for j_ in range(p):
            ax.text(j_, i, f"{C[i, j_]:.2f}", ha="center", va="center",
                    fontsize=8.5, color="black")
    cb = fig.colorbar(im, ax=ax, shrink=0.85)
    cb.set_label("相关系数")
    ax.set_title("相关系数矩阵图：一眼看出 8 个变量两两之间的相关强弱")
    fig.tight_layout()
    save(fig, "fig3_14_corr_matrix.png")


# ---------------------------------------------------------------- 3-15 置信区间填充
def fig3_15_confidence_band():
    x = np.linspace(0, 10, 40)
    y = 2.5 + 1.2 * x + rng.normal(0, 1.6, 40)
    k, b = np.polyfit(x, y, 1)
    xs = np.linspace(0, 10, 200)
    yhat = k * xs + b
    n = len(x)
    se = np.sqrt(np.sum((y - (k * x + b)) ** 2) / (n - 2))
    sx = np.sum((x - x.mean()) ** 2)
    conf = 1.96 * se * np.sqrt(1 / n + (xs - x.mean()) ** 2 / sx)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.fill_between(xs, yhat - conf, yhat + conf, color=C_BLUE, alpha=0.22,
                    label="95% 置信区间")
    ax.plot(xs, yhat, color=C_RED, lw=2, label="线性拟合")
    ax.scatter(x, y, s=26, color=C_BLUE, alpha=0.8, label="观测值")
    ax.set_xlabel("年降雨量（mm）"); ax.set_ylabel("年径流量（mm）")
    ax.set_title("线性拟合 + 置信区间填充：加一层半透明填充，图形档次立刻提升")
    ax.grid(alpha=0.3); ax.legend(fontsize=9)
    fig.tight_layout()
    save(fig, "fig3_15_confidence_band.png")


# ---------------------------------------------------------------- 3-16 案例分布
def fig3_16_case_result():
    # 模拟案例流程：S1 100 个站点；S2 与 S1 有 60 个共同站点 + 40 个新站点
    s1 = rng.choice(10000, 100, replace=False) + 1
    common = rng.choice(s1, 60, replace=False)
    pool = np.setdiff1d(np.arange(1, 10001), s1)
    s2 = np.concatenate([common, rng.choice(pool, 40, replace=False)])
    n2 = len(s2)
    T = -10 + 55 * rng.random(n2)
    P = 1000 * rng.random(n2)
    Y = 10 * T + P
    s3 = np.intersect1d(s1, s2)
    idx = np.argsort(s2)
    order = idx[np.searchsorted(s2[idx], s3)]
    d3 = np.column_stack([s3, T[order], P[order], Y[order]])

    fig = plt.figure(figsize=(12, 6.4))
    outer = gridspec.GridSpec(1, 2, width_ratios=[4, 3], wspace=0.3)
    left = gridspec.GridSpecFromSubplotSpec(2, 2, subplot_spec=outer[0], hspace=0.55, wspace=0.35)
    right = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=outer[1], hspace=0.75)

    labs = ["站点编号 S", "温度 T（℃）", "降雨 P（mm）", "虚拟变量 Y"]
    for k in range(4):
        ax = fig.add_subplot(left[k])
        ax.hist(d3[:, k], bins=12, color=C_BLUE, alpha=0.8, edgecolor="white")
        ax.set_title(f"Data3：{labs[k]}", fontsize=9.5)
        ax.grid(alpha=0.3)
        ax.tick_params(labelsize=8)

    for k, lab in enumerate(["T", "P", "Y"]):
        ax = fig.add_subplot(right[k])
        col = d3[:, k + 1]
        coln = (col - col.min()) / (col.max() - col.min())
        ax.hist(coln, bins=12, color=C_ORANGE, alpha=0.85, edgecolor="white")
        ax.set_title(f"Data5：{lab} 列规范化后（0~1）", fontsize=9.5)
        ax.grid(alpha=0.3)
        ax.tick_params(labelsize=8)

    fig.suptitle("案例结果：Data3 四列分布（左）与 Data5 最小-最大规范化后的分布（右）",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save(fig, "fig3_16_case_result.png")


if __name__ == "__main__":
    fig3_01_four_tasks()
    fig3_02_process()
    fig3_03_missing_value_fill()
    fig3_04_boxplot()
    fig3_05_correlation_redundancy()
    fig3_06_sampling()
    fig3_07_normalization_compare()
    fig3_08_new_data_overflow()
    fig3_09_discretization()
    fig3_10_log_transform()
    fig3_11_season_week()
    fig3_12_matlab_basic_2d()
    fig3_13_matlab_3d()
    fig3_14_corr_matrix()
    fig3_15_confidence_band()
    fig3_16_case_result()
    print("ALL DONE")
