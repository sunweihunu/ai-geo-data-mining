# -*- coding: utf-8 -*-
"""第05章 降维 插图生成脚本。

运行（在项目根目录）：
    uv run --no-project --with matplotlib --with numpy python tmp_fig5/gen_figures.py
输出：书稿/figs/ch05/fig5_XX_*.png（dpi=150，bbox_inches="tight"）
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

C_BLUE = "#1f77b4"
C_ORANGE = "#ff7f0e"
C_GREEN = "#2ca02c"
C_RED = "#d62728"
C_PURPLE = "#9467bd"

OUT = os.path.join("书稿", "figs", "ch05")
os.makedirs(OUT, exist_ok=True)

rng = np.random.default_rng(42)


def savefig(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved:", name)


# ---------------------------------------------------------------- 数据
# 2004 年中国 31 个省区市 8 项经济指标（转录自课件表格截图，
# 原始来源《中国统计年鉴 2005》，个别数值可能与年鉴略有出入，仅用于教学演示）
REGIONS = [
    "北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江",
    "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南",
    "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州",
    "云南", "西藏", "陕西", "甘肃", "青海", "宁夏", "新疆",
]
VAR_NAMES = ["GDP", "工业增加值", "固定资产投资", "职工平均工资",
             "城镇居民消费", "农村居民消费", "居民消费价格指数", "商品零售价格指数"]
X2004 = np.array([
    [4283.3, 1259.5, 2528.2, 29674, 12200, 4617, 100.6, 99.2],
    [2931.9, 1436.7, 1258.9, 21754, 8802, 2642, 101.3, 100.4],
    [8768.8, 2459.2, 3251.6, 12925, 5819, 1834, 103.5, 102.9],
    [3042.4, 1242.9, 1458.5, 12943, 5484, 1636, 103.7, 103.1],
    [2712.1, 776.8, 1808.9, 13324, 5897, 1691, 102.5, 102.3],
    [6872.7, 2255.7, 2980.5, 14931, 6543, 2073, 102.6, 101.8],
    [2958.2, 995.2, 1169.1, 12431, 6069, 1971, 103.7, 103.4],
    [5303.0, 1619.6, 1515.3, 13955, 5815, 1830, 102.8, 102.2],
    [7450.3, 3492.9, 3084.7, 30085, 12631, 4565, 100.9, 99.8],
    [15403.2, 6447.5, 6827.6, 18202, 7052, 2495, 103.0, 102.2],
    [11243.0, 4173.4, 5781.4, 23506, 10636, 3654, 102.1, 100.9],
    [4812.7, 1735.6, 1914.2, 13092, 5711, 1814, 103.1, 102.3],
    [6053.1, 2532.7, 1899.1, 15603, 7557, 2715, 102.2, 100.9],
    [3495.9, 1110.7, 1713.2, 11915, 5337, 1717, 102.4, 101.5],
    [15490.7, 6498.3, 7589.1, 14332, 6644, 2438, 102.2, 100.4],
    [8815.1, 3862.2, 3099.3, 12114, 5294, 1664, 103.6, 102.7],
    [6309.9, 2322.7, 2356.7, 13569, 5925, 1831, 102.9, 102.0],
    [5612.3, 1780.9, 2072.6, 13917, 6083, 1926, 102.7, 101.6],
    [16039.5, 8011.2, 7105.2, 19986, 8981, 3050, 101.6, 100.2],
    [3320.1, 1044.8, 1263.7, 13580, 5893, 1846, 102.6, 101.7],
    [790.1, 184.1, 320.4, 12652, 5802, 1743, 101.4, 100.6],
    [2665.4, 927.6, 1609.1, 14357, 5975, 1854, 101.9, 100.7],
    [6556.0, 2166.2, 2818.4, 14063, 5759, 1747, 102.5, 101.7],
    [1591.9, 576.4, 865.7, 13231, 5494, 1527, 102.2, 101.0],
    [2959.5, 881.2, 1300.3, 14590, 5924, 1571, 102.7, 101.8],
    [211.5, 27.6, 168.4, 30873, 8738, 1471, 100.7, 99.5],
    [2884.0, 1069.7, 1544.2, 13024, 5666, 1618, 102.2, 101.4],
    [1558.9, 505.1, 756.1, 13548, 5935, 1466, 101.6, 100.6],
    [465.7, 150.2, 318.1, 17229, 5759, 1425, 101.6, 100.5],
    [460.4, 147.7, 379.7, 14620, 5821, 1586, 100.7, 99.5],
    [2200.1, 745.0, 1147.5, 14484, 5774, 1683, 101.5, 100.3],
])


def zscore(X):
    return (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)


def f_stat_single(x, y):
    """单变量线性关系的 F 统计量（由相关系数换算）。"""
    r = np.corrcoef(x, y)[0, 1]
    n = len(x)
    return r ** 2 * (n - 2) / (1 - r ** 2)


def mutual_info_hist(x, y, bins=8):
    """基于二维直方图离散化的互信息估计。"""
    n = len(x)
    hx, _ = np.histogram(x, bins=bins)
    hy, _ = np.histogram(y, bins=bins)
    joint, _, _ = np.histogram2d(x, y, bins=bins)
    px = hx / n
    py = hy / n
    pxy = joint / n
    mi = 0.0
    for i in range(bins):
        for j in range(bins):
            if pxy[i, j] > 0:
                mi += pxy[i, j] * np.log(pxy[i, j] / (px[i] * py[j]))
    return mi


def varimax(Phi, gamma=1.0, q=200, tol=1e-8):
    """方差最大正交旋转。"""
    p, k = Phi.shape
    R = np.eye(k)
    d = 0.0
    for _ in range(q):
        d_old = d
        Lam = Phi @ R
        u, s, vh = np.linalg.svd(
            Phi.T @ (Lam ** 3 - (gamma / p) * Lam @ np.diag(np.diag(Lam.T @ Lam))))
        R = u @ vh
        d = s.sum()
        if d_old != 0 and d / d_old < 1 + tol:
            break
    return Phi @ R, R


# ---------------------------------------------------------------- 图 5-1
def fig5_01_f_test_vs_mi():
    """三个特征与 Y 的相关性：F 检验只能发现线性关系，互信息能发现任意关系。"""
    rng = np.random.default_rng(42)
    n = 300
    x = rng.uniform(-1, 1, (n, 3))
    y = (x[:, 0]                              # 与 x1 线性相关
         + np.cos(2 * np.pi * x[:, 1])        # 与 x2 非线性相关
         + rng.normal(0, 0.25, n))            # 与 x3 无关
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.4), sharey=True)
    labels = ["特征 $x_1$（线性相关）", "特征 $x_2$（非线性相关）", "特征 $x_3$（无关）"]
    for k, ax in enumerate(axes):
        ax.scatter(x[:, k], y, s=8, c=C_BLUE, alpha=0.65, edgecolors="none")
        f = f_stat_single(x[:, k], y)
        mi = mutual_info_hist(x[:, k], y, bins=8)
        ax.set_title(f"{labels[k]}\nF 检验 $F$={f:6.1f}   互信息 MI={mi:.3f}", fontsize=9.5)
        ax.set_xlabel(labels[k].split("（")[0])
        ax.tick_params(labelsize=8)
    axes[0].set_ylabel("$y$")
    fig.suptitle("同一因变量与三个自变量的关系：F 检验（只捕捉线性）与互信息（捕捉任意关系）", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    savefig(fig, "fig5_01_f_test_vs_mi.png")


# ---------------------------------------------------------------- 图 5-2
def fig5_02_scatter_matrix():
    """四个自变量的散点图矩阵：年径流量与年降雨量高度相关。"""
    rng = np.random.default_rng(42)
    n = 120
    rain = rng.normal(1100, 220, n)                      # 年降雨量
    runoff = 0.55 * rain + rng.normal(0, 55, n)          # 年径流量（强相关）
    temp = rng.normal(15, 3.5, n)                        # 年平均气温
    dens = rng.normal(420, 150, n)                       # 人口密度
    data = np.c_[rain, runoff, temp, dens]
    names = ["年降雨量", "年径流量", "年平均气温", "人口密度"]
    p = 4
    fig, axes = plt.subplots(p, p, figsize=(8.6, 8.6))
    for i in range(p):
        for j in range(p):
            ax = axes[i, j]
            ax.tick_params(labelsize=7)
            if i == j:
                ax.hist(data[:, i], bins=15, color=C_BLUE, alpha=0.75)
            elif i > j:
                ax.scatter(data[:, j], data[:, i], s=5, c=C_BLUE, alpha=0.6, edgecolors="none")
                if (i, j) == (1, 0):
                    ax.scatter(data[:, j], data[:, i], s=5, c=C_RED, alpha=0.6, edgecolors="none")
            else:
                r = np.corrcoef(data[:, j], data[:, i])[0, 1]
                ax.text(0.5, 0.5, f"$r$={r:5.2f}", ha="center", va="center",
                        fontsize=11, color=(C_RED if abs(r) > 0.8 else "#444444"),
                        transform=ax.transAxes)
                ax.set_xticks([])
                ax.set_yticks([])
            if i == p - 1:
                ax.set_xlabel(names[j], fontsize=9)
            if j == 0:
                ax.set_ylabel(names[i], fontsize=9)
    fig.suptitle("四个自变量的散点图矩阵（对角线为分布直方图，上三角为相关系数）\n"
                 "年降雨量与年径流量高度相关（$r$=0.90），二者取其一即可", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    savefig(fig, "fig5_02_scatter_matrix.png")


# ---------------------------------------------------------------- 图 5-3
def fig5_03_r_clustering():
    """R 型聚类：对属性（变量）做层次聚类的树状图 + 相关系数矩阵热力图。"""
    rng = np.random.default_rng(42)
    n = 60
    f1 = rng.normal(0, 1, n)          # 潜在共同因子
    f2 = rng.normal(0, 1, n)
    e = rng.normal(0, 0.35, (n, 6))
    rain = 1.0 * f1 + e[:, 0]         # 降雨/径流/湿度一族：受 f1 影响
    runoff = 0.95 * f1 + e[:, 1]
    humid = 0.9 * f1 + e[:, 2]
    temp = 1.0 * f2 + e[:, 3]         # 气温/蒸发一族：受 f2 影响
    evap = 0.9 * f2 + e[:, 4]
    dens = 0.6 * f2 + e[:, 5]         # 人口密度与 f2 弱相关
    names = ["年降雨量", "年径流量", "相对湿度", "年平均气温", "蒸发量", "人口密度"]
    data = np.c_[rain, runoff, humid, temp, evap, dens]
    R = np.corrcoef(data, rowvar=False)
    D = 1 - np.abs(R)                 # 变量间距离 = 1 - |相关系数|

    # 平均链接层次聚类（手工实现，供树状图绘制）
    nvar = 6
    clusters = {i: [i] for i in range(nvar)}
    merges = []                       # (height, members)
    heights = {}
    active = list(range(nvar))
    while len(active) > 1:
        best = None
        for a in active:
            for b in active:
                if a >= b:
                    continue
                dmean = np.mean([D[i, j] for i in clusters[a] for j in clusters[b]])
                if best is None or dmean < best[0]:
                    best = (dmean, a, b)
        _, a, b = best
        new_id = max(clusters) + 1
        clusters[new_id] = clusters.pop(a) + clusters.pop(b)
        active = [c for c in active if c not in (a, b)] + [new_id]
        merges.append((new_id, a, b))
        heights[new_id] = best[0]

    fig = plt.figure(figsize=(10.5, 4.4))
    gs = GridSpec(1, 2, width_ratios=[1.15, 1], wspace=0.25)

    # 左：树状图
    ax1 = fig.add_subplot(gs[0])
    pos = {}
    leaf_x = 0
    for i in range(nvar):
        pos[i] = leaf_x
        leaf_x += 1

    def draw_node(node):
        if node < nvar:
            return pos[node]
        _, a, b = next(m for m in merges if m[0] == node)
        xa = draw_node(a)
        xb = draw_node(b)
        h = heights[node]
        ax1.plot([xa, xa], [0, h], color="#555555", lw=1.2)
        ax1.plot([xb, xb], [0, h], color="#555555", lw=1.2)
        ax1.plot([xa, xb], [h, h], color="#555555", lw=1.2)
        pos[node] = (xa + xb) / 2
        return pos[node]

    root = max(clusters)
    draw_node(root)
    ax1.set_xticks(range(nvar))
    ax1.set_xticklabels(names, fontsize=9)
    ax1.set_ylabel("变量间距离（$1-|r|$）", fontsize=10)
    ax1.set_ylim(0, 1.0)
    ax1.set_title("R 型聚类（对属性/变量聚类）的树状图", fontsize=11)
    ax1.axhline(0.45, color=C_RED, ls="--", lw=1)
    ax1.text(0.02, 0.48, "阈值", color=C_RED, fontsize=9, transform=ax1.get_yaxis_transform())

    # 右：相关系数热力图
    ax2 = fig.add_subplot(gs[1])
    im = ax2.imshow(R, cmap="RdBu_r", vmin=-1, vmax=1)
    ax2.set_xticks(range(nvar))
    ax2.set_yticks(range(nvar))
    ax2.set_xticklabels(names, fontsize=8, rotation=38, ha="right")
    ax2.set_yticklabels(names, fontsize=8)
    for i in range(nvar):
        for j in range(nvar):
            ax2.text(j, i, f"{R[i, j]:4.2f}", ha="center", va="center", fontsize=7.5,
                     color="white" if abs(R[i, j]) > 0.6 else "#222222")
    cb = fig.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    cb.ax.tick_params(labelsize=8)
    ax2.set_title("相关系数矩阵热力图", fontsize=11)
    savefig(fig, "fig5_03_r_clustering.png")


# ---------------------------------------------------------------- 图 5-4
def fig5_04_pca_3d_plane():
    """三维点云投影到最优二维平面（PCA），两个视角。"""
    rng = np.random.default_rng(42)
    n = 260
    t = np.array([1.0, 0.15, 0.05])
    a = rng.normal(0, 2.4, n)
    b = rng.normal(0, 1.3, n)
    c = rng.normal(0, 0.35, n)     # 第三方向离散很小
    v1 = np.array([0.85, 0.50, 0.16])
    v2 = np.array([-0.50, 0.86, 0.10])
    v3 = np.cross(v1, v2)
    v3 = v3 / np.linalg.norm(v3)
    P = a[:, None] * v1 + b[:, None] * v2 + c[:, None] * v3 + 4 * t

    # PCA 平面
    Zc = P - P.mean(axis=0)
    cov = Zc.T @ Zc / (n - 1)
    w, V = np.linalg.eigh(cov)
    idx = np.argsort(w)[::-1]
    V = V[:, idx]
    w = w[idx]
    ctr = P.mean(axis=0)
    s1, s2 = 6.5, 4.5
    corner = (ctr + s1 * V[:, 0] + s2 * V[:, 1],
              ctr + s1 * V[:, 0] - s2 * V[:, 1],
              ctr - s1 * V[:, 0] - s2 * V[:, 1],
              ctr - s1 * V[:, 0] + s2 * V[:, 1])
    xx = [c[0] for c in corner]
    yy = [c[1] for c in corner]
    zz = [c[2] for c in corner]

    fig = plt.figure(figsize=(10.5, 4.4))
    for k, (elev, azim, title) in enumerate([
            (18, 35, "原始三维视角"),
            (88, 0, "旋转后正对二维平面")]):
        ax = fig.add_subplot(1, 2, k + 1, projection="3d")
        ax.scatter(P[:, 0], P[:, 1], P[:, 2], s=10, c=C_ORANGE, alpha=0.75, edgecolors="none")
        ax.plot_surface(np.array(xx).reshape(2, 2), np.array(yy).reshape(2, 2),
                        np.array(zz).reshape(2, 2), color=C_BLUE, alpha=0.16)
        for vec, col, lab in [(V[:, 0], C_GREEN, "$z_1$"),
                              (V[:, 1], C_RED, "$z_2$")]:
            ax.quiver(ctr[0], ctr[1], ctr[2], vec[0], vec[1], vec[2],
                      color=col, lw=2, arrow_length_ratio=0.12)
            ax.text(*(ctr + 1.25 * vec), lab, color=col, fontsize=12)
        ax.set_xlabel("$x_1$", fontsize=9)
        ax.set_ylabel("$x_2$", fontsize=9)
        ax.set_zlabel("$x_3$", fontsize=9)
        ax.view_init(elev=elev, azim=azim)
        ax.tick_params(labelsize=7)
        ax.set_title(f"{title}\n前两个主成分方差占比 {100 * (w[0] + w[1]) / w.sum():.1f}%", fontsize=10)
        ax.set_box_aspect((1, 1, 0.85))
    fig.suptitle("三维点云投影到方差最大的二维平面：第三方向离散程度极小，损失的信息很少", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    savefig(fig, "fig5_04_pca_3d_plane.png")


# ---------------------------------------------------------------- 图 5-5
def fig5_05_ellipse_rotation():
    """二维椭圆点云的坐标旋转：原坐标 x1-x2 与主成分坐标 y1-y2。"""
    rng = np.random.default_rng(42)
    n = 300
    theta = np.deg2rad(32)
    major = np.array([np.cos(theta), np.sin(theta)])
    minor = np.array([-np.sin(theta), np.cos(theta)])
    a = rng.normal(0, 2.2, n)
    b = rng.normal(0, 0.55, n)
    X = a[:, None] * major + b[:, None] * minor

    Y = np.c_[X @ major, X @ minor]
    v1 = np.var(Y[:, 0], ddof=1)
    v2 = np.var(Y[:, 1], ddof=1)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.5))
    ax = axes[0]
    ax.scatter(X[:, 0], X[:, 1], s=10, c=C_BLUE, alpha=0.7, edgecolors="none")
    for vec, col, lab in [(major, C_GREEN, "$y_1$（第一主成分，长轴）"),
                          (minor, C_RED, "$y_2$（第二主成分，短轴）")]:
        v = vec / np.linalg.norm(vec) * 3.6
        ax.annotate("", xy=(v[0], v[1]), xytext=(-v[0], -v[1]),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2))
        ax.text(1.16 * v[0], 1.16 * v[1], lab, color=col, fontsize=10,
                ha="left" if v[0] > 0 else "right")
    ax.axhline(0, color="#999999", lw=0.8, ls=":")
    ax.axvline(0, color="#999999", lw=0.8, ls=":")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_title("原坐标系 $x_1$–$x_2$：椭圆斜置，\n坐标轴与长短轴不平行", fontsize=10.5)
    ax.set_xlim(-7, 7)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")

    ax = axes[1]
    ax.scatter(Y[:, 0], Y[:, 1], s=10, c=C_BLUE, alpha=0.7, edgecolors="none")
    ax.axhline(0, color=C_GREEN, lw=1.6)
    ax.axvline(0, color=C_RED, lw=1.6)
    ax.set_xlabel("$y_1$")
    ax.set_ylabel("$y_2$")
    share = 100 * v1 / (v1 + v2)
    ax.set_title("正交旋转后的坐标系 $y_1$–$y_2$：\n方差集中到 $y_1$ 轴上", fontsize=10.5)
    ax.text(0.03, 0.95, f"$var(y_1)$={v1:5.2f}（占 {share:.1f}%）\n$var(y_2)$={v2:4.2f}（占 {100 - share:.1f}%）",
            transform=ax.transAxes, fontsize=10, va="top",
            bbox=dict(fc="white", ec="#bbbbbb", alpha=0.9))
    ax.set_xlim(-7, 7)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    fig.suptitle("主成分的几何解释：把坐标轴正交旋转到椭圆的长短轴方向", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    savefig(fig, "fig5_05_ellipse_rotation.png")


# ---------------------------------------------------------------- 图 5-6
def fig5_06_max_variance():
    """最大可分性：投影方差大的方向 vs 差的方向。"""
    rng = np.random.default_rng(42)
    n = 220
    theta = np.deg2rad(40)
    major = np.array([np.cos(theta), np.sin(theta)])
    minor = np.array([-np.sin(theta), np.cos(theta)])
    X = (rng.normal(0, 2.1, n)[:, None] * major
         + rng.normal(0, 0.5, n)[:, None] * minor)
    u_good = major / np.linalg.norm(major)
    u_bad = minor / np.linalg.norm(minor)
    p_good = X @ u_good
    p_bad = X @ u_bad

    fig = plt.figure(figsize=(8.6, 5.2))
    gs = GridSpec(2, 2, height_ratios=[2.1, 1], hspace=0.32, wspace=0.22)
    ax0 = fig.add_subplot(gs[0, :])
    ax0.scatter(X[:, 0], X[:, 1], s=12, c=C_BLUE, alpha=0.7, edgecolors="none")
    for u, col, lab in [(u_good, C_GREEN, "投影方差大的方向（第一主成分）"),
                        (u_bad, C_RED, "投影方差小的方向")]:
        v = 4.4 * u
        ax0.annotate("", xy=(v[0], v[1]), xytext=(-v[0], -v[1]),
                     arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2))
    ax0.annotate("投影方差大的方向（第一主成分）", xy=(4.4 * u_good[0], 4.4 * u_good[1]),
                 xytext=(3.1, 5.2), fontsize=10, color=C_GREEN,
                 arrowprops=dict(arrowstyle="->", color=C_GREEN))
    ax0.annotate("投影方差小的方向", xy=(4.4 * u_bad[0], 4.4 * u_bad[1]),
                 xytext=(3.0, -4.9), fontsize=10, color=C_RED,
                 arrowprops=dict(arrowstyle="->", color=C_RED))
    ax0.set_xlabel("$x_1$")
    ax0.set_ylabel("$x_2$")
    ax0.set_xlim(-6.5, 8.5)
    ax0.set_ylim(-5.8, 6.5)
    ax0.set_title("二维散点与两个候选投影方向", fontsize=11)

    for k, (p, col, lab) in enumerate([
            (p_good, C_GREEN, "沿方差大的方向投影：点被拉开"),
            (p_bad, C_RED, "沿方差小的方向投影：点挤在一起")]):
        ax = fig.add_subplot(gs[1, k])
        ax.hist(p, bins=24, color=col, alpha=0.8)
        ax.set_title(f"{lab}（方差 {np.var(p):4.2f}）", fontsize=10)
        ax.set_xlabel("投影取值", fontsize=9)
        ax.tick_params(labelsize=8)
    savefig(fig, "fig5_06_max_variance.png")


# ---------------------------------------------------------------- 图 5-7
def fig5_07_pca_workflow():
    """PCA 求解流程图。"""
    fig, ax = plt.subplots(figsize=(10.2, 2.9))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 2.9)
    ax.axis("off")
    steps = [
        ("① 数据标准化", "消除量纲差异\n$Z=(X-\\bar{x})/s$", C_BLUE),
        ("② 计算协方差\n（相关系数）矩阵", "$E=\\mathrm{cov}(Z)$\n$=Z^{T}Z/(n-1)$", C_BLUE),
        ("③ 特征值分解", "$E v_i=\\lambda_i v_i$\n特征值降序排列", C_PURPLE),
        ("④ 确定主成分个数 $k$", "累计方差贡献\n$\\geq 80\\%$，或\n特征值 $> 1$", C_ORANGE),
        ("⑤ 投影得到主成分", "载荷 $A=[v_1..v_k]$\n得分 $T=ZA$", C_GREEN),
    ]
    bw, bh, y0 = 1.72, 1.5, 0.75
    xs = [0.25 + i * 2.0 for i in range(5)]
    for (title, body, col), x in zip(steps, xs):
        box = FancyBboxPatch((x, y0), bw, bh, boxstyle="round,pad=0.08",
                             fc="white", ec=col, lw=1.8)
        ax.add_patch(box)
        ax.text(x + bw / 2, y0 + bh - 0.28, title, ha="center", va="center",
                fontsize=10, color=col, weight="bold")
        ax.text(x + bw / 2, y0 + bh / 2 - 0.33, body, ha="center", va="center",
                fontsize=9.5, color="#333333")
    for i in range(4):
        ax.add_patch(FancyArrowPatch((xs[i] + bw + 0.06, y0 + bh / 2),
                                     (xs[i + 1] - 0.10, y0 + bh / 2),
                                     arrowstyle="-|>", mutation_scale=16,
                                     color="#555555", lw=1.6))
    ax.text(5.1, 0.28, "第 $i$ 个特征值 = 数据在第 $i$ 个主成分上投影的方差；"
                       "特征值大小顺序 = 主成分顺序", ha="center", fontsize=10, color="#444444")
    ax.text(5.1, 2.62, "主成分分析的求解流程", ha="center", fontsize=12, weight="bold")
    savefig(fig, "fig5_07_pca_workflow.png")


# ---------------------------------------------------------------- 图 5-8
def fig5_08_fa_path_diagram():
    """因子分析路径图：公因子 -> 观测变量 + 特殊因子（课程成绩例子）。"""
    fig, ax = plt.subplots(figsize=(9.6, 5.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis("off")

    fx, fy1, fy2 = 1.55, 4.35, 1.75
    for fy, lab in [(fy1, "$F_1$：逻辑推理\n能力（公因子）"), (fy2, "$F_2$：语言驾驭\n能力（公因子）")]:
        c = Circle((fx, fy), 0.72, fc="#eef4fb", ec=C_BLUE, lw=2)
        ax.add_patch(c)
        ax.text(fx, fy, lab, ha="center", va="center", fontsize=9.5)

    obs = [("数学", 5.15), ("物理", 5.65), ("计算机", 6.15),
           ("语文", 7.15), ("英语", 7.65), ("写作", 8.15)]
    loads = {(0, 0): 0.91, (0, 1): 0.88, (0, 2): 0.85, (0, 3): 0.18, (0, 4): 0.15, (0, 5): 0.22,
             (1, 0): 0.12, (1, 1): 0.20, (1, 2): 0.17, (1, 3): 0.89, (1, 4): 0.92, (1, 5): 0.86}
    for j, (name, xj) in enumerate(obs):
        yj = 3.05
        box = FancyBboxPatch((xj - 0.42, yj - 0.30), 0.84, 0.60,
                             boxstyle="round,pad=0.04", fc="white", ec="#555555", lw=1.4)
        ax.add_patch(box)
        ax.text(xj, yj, name, ha="center", va="center", fontsize=9.5)
        for i, fy in [(0, fy1), (1, fy2)]:
            a = loads[(i, j)]
            col = C_BLUE if a > 0.5 else "#b0b0b0"
            ax.add_patch(FancyArrowPatch((fx + 0.74, fy), (xj - 0.44, yj),
                                         arrowstyle="-|>", mutation_scale=11,
                                         color=col, lw=2.2 if a > 0.5 else 0.9,
                                         alpha=0.9,
                                         connectionstyle="arc3,rad=0.06"))
            tx = 0.62 * (xj - fx) + fx
            ty = 0.62 * (yj - fy) + fy + (0.24 if i == 0 else -0.24)
            ax.text(tx, ty, f"$a_{{{j + 1}{i + 1}}}$={a:.2f}", fontsize=8,
                    color=col, ha="center")
        # 特殊因子
        ex = xj + 0.95
        c = Circle((ex, yj), 0.20, fc="#fdf1ec", ec=C_ORANGE, lw=1.5)
        ax.add_patch(c)
        ax.text(ex, yj, r"$\varepsilon$", ha="center", va="center", fontsize=10, color=C_ORANGE)
        ax.add_patch(FancyArrowPatch((ex - 0.21, yj), (xj + 0.44, yj),
                                     arrowstyle="-|>", mutation_scale=10,
                                     color=C_ORANGE, lw=1.2))

    ax.text(3.0, 5.9, "公共因子（不可观测的潜在变量）", fontsize=9.5, color=C_BLUE)
    ax.text(6.05, 2.15, "特殊因子（各变量独有）", fontsize=9.5, color=C_ORANGE)
    ax.text(5.0, 0.75, "$x_j = a_{j1}F_1 + a_{j2}F_2 + \\varepsilon_j$"
                       "（载荷 $a_{jk}$ 为变量 $x_j$ 与因子 $F_k$ 的相关系数）",
            ha="center", fontsize=11)
    ax.text(5.0, 5.9, "因子分析模型：每门课程成绩由少数公因子与一个特殊因子决定",
            ha="center", fontsize=12, weight="bold")
    savefig(fig, "fig5_08_fa_path_diagram.png")


# ---------------------------------------------------------------- 图 5-9
def fig5_09_pca_vs_fa():
    """PCA（往后推，综合）与 FA（往前推，分解）的对比示意。"""
    fig, axes = plt.subplots(2, 1, figsize=(9.4, 5.6))
    for ax in axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 3.1)
        ax.axis("off")

    ax = axes[0]
    ax.text(5, 2.92, "主成分分析（PCA）：由 $X$ 综合出 $Z$ —— “往后推”，找后果的指标",
            ha="center", fontsize=11.5, weight="bold")
    for j, (name, y) in enumerate([("$x_1$ GDP", 2.25), ("$x_2$ 工业增加值", 1.55), ("$x_3$ 固定资产投资", 0.85)]):
        b = FancyBboxPatch((6.6, y - 0.26), 2.6, 0.52, boxstyle="round,pad=0.04",
                           fc="white", ec="#555555", lw=1.3)
        ax.add_patch(b)
        ax.text(7.9, y, name, ha="center", va="center", fontsize=9.5)
        ax.add_patch(FancyArrowPatch((4.35, 1.82), (6.55, y), arrowstyle="-|>",
                                     mutation_scale=13, color=C_GREEN, lw=1.8,
                                     connectionstyle="arc3,rad=0.05"))
        ax.text(5.42, 1.82 + (y - 1.82) * 0.42 + 0.16, f"$w_{{{j + 1}}}$", fontsize=8.5, color=C_GREEN)
    b = FancyBboxPatch((2.1, 1.42), 2.25, 0.80, boxstyle="round,pad=0.05",
                       fc="#eaf6ea", ec=C_GREEN, lw=2)
    ax.add_patch(b)
    ax.text(3.22, 1.82, "$z_1 = w_1x_1+w_2x_2+w_3x_3$\n（主成分，综合指标）",
            ha="center", va="center", fontsize=9.5)
    ax.text(0.35, 1.82, "$Z = XA$\n（线性组合）", ha="center", va="center",
            fontsize=10, color=C_GREEN)

    ax = axes[1]
    ax.text(5, 2.92, "因子分析（FA）：把 $X$ 分解为潜在因子 $F$ —— “往前推”，找前因的要素",
            ha="center", fontsize=11.5, weight="bold")
    for j, (name, y) in enumerate([("$x_1$ GDP", 2.25), ("$x_2$ 工业增加值", 1.55), ("$x_3$ 固定资产投资", 0.85)]):
        b = FancyBboxPatch((6.6, y - 0.26), 2.6, 0.52, boxstyle="round,pad=0.04",
                           fc="white", ec="#555555", lw=1.3)
        ax.add_patch(b)
        ax.text(7.9, y, name, ha="center", va="center", fontsize=9.5)
        ax.add_patch(FancyArrowPatch((4.35, y), (6.55, y), arrowstyle="-|>",
                                     mutation_scale=13, color=C_BLUE, lw=1.8))
    for fy, lab in [(2.1, "$F_1$：经济规模因子"), (1.2, "$F_2$：生活消费因子")]:
        b = FancyBboxPatch((1.55, fy - 0.30), 2.75, 0.60, boxstyle="round,pad=0.05",
                           fc="#eef4fb", ec=C_BLUE, lw=2)
        ax.add_patch(b)
        ax.text(2.92, fy, lab, ha="center", va="center", fontsize=9.5)
    ax.add_patch(FancyArrowPatch((4.33, 2.1), (5.5, 1.95), arrowstyle="-|>",
                                 mutation_scale=13, color=C_BLUE, lw=1.6,
                                 connectionstyle="arc3,rad=-0.15"))
    ax.add_patch(FancyArrowPatch((4.33, 1.2), (5.5, 1.42), arrowstyle="-|>",
                                 mutation_scale=13, color=C_BLUE, lw=1.6,
                                 connectionstyle="arc3,rad=0.15"))
    c = Circle((5.62, 2.35), 0.21, fc="#fdf1ec", ec=C_ORANGE, lw=1.5)
    ax.add_patch(c)
    ax.text(5.62, 2.35, r"$\varepsilon$", ha="center", va="center", fontsize=10, color=C_ORANGE)
    ax.text(5.62, 2.72, "特殊因子", ha="center", fontsize=8.5, color=C_ORANGE)
    ax.text(0.35, 1.65, "$X = AF + \\varepsilon$\n（分解）", ha="center", va="center",
            fontsize=10, color=C_BLUE)
    savefig(fig, "fig5_09_pca_vs_fa.png")


# ---------------------------------------------------------------- 图 5-10
def fig5_10_rotation_varimax():
    """因子旋转前后载荷的两极分化效果。"""
    rng = np.random.default_rng(42)
    p = 8
    angle0 = np.deg2rad(40)
    V = np.array([[np.cos(angle0), -np.sin(angle0)],
                  [np.sin(angle0), np.cos(angle0)]])
    base = np.zeros((p, 2))
    for j in range(p):
        ph = angle0 + rng.normal(0, np.deg2rad(9)) + (0 if j < 4 else np.pi / 2)
        r = rng.uniform(0.82, 0.97)
        base[j] = [r * np.cos(ph), r * np.sin(ph)]
    Lam_unrot = base @ V.T          # 旋转前：变量点斜聚在 45° 方向附近
    Lam_rot, T = varimax(base)      # 旋转后：贴近坐标轴

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.6))
    th = np.linspace(0, 2 * np.pi, 200)
    names = ["降雨量", "径流量", "空气湿度", "云量", "气温", "蒸发量", "日照时数", "地温"]
    for ax, Lam, title in [
            (axes[0], Lam_unrot, "旋转前：载荷在两轴上都比较平均，\n因子的含义模糊"),
            (axes[1], Lam_rot, "方差最大正交旋转后：载荷向两轴两极分化，\n因子的含义清晰")]:
        ax.plot(np.cos(th), np.sin(th), color="#cccccc", lw=1)
        ax.axhline(0, color="#999999", lw=0.9)
        ax.axvline(0, color="#999999", lw=0.9)
        cols = [C_BLUE] * 4 + [C_ORANGE] * 4
        ax.scatter(Lam[:, 0], Lam[:, 1], s=46, c=cols, zorder=3)
        for j in range(p):
            ax.plot([0, Lam[j, 0]], [0, Lam[j, 1]], color=cols[j], lw=1.1, alpha=0.6)
            dx, dy = 0.06, 0.05
            if Lam[j, 0] < 0:
                dx = -0.30
            ax.text(Lam[j, 0] + dx, Lam[j, 1] + dy, names[j], fontsize=8.6)
        ax.set_xlim(-1.15, 1.15)
        ax.set_ylim(-0.35, 1.15)
        ax.set_aspect("equal")
        ax.set_xlabel("因子 $F_1$ 上的载荷", fontsize=10)
        ax.set_ylabel("因子 $F_2$ 上的载荷", fontsize=10)
        ax.set_title(title, fontsize=10.5)
    fig.suptitle("因子旋转的目的：使载荷矩阵每列元素的绝对值尽可能向 0 和 1 两极分化", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.91])
    savefig(fig, "fig5_10_rotation_varimax.png")


# ---------------------------------------------------------------- 案例公共计算
def _case_fa():
    """31 省市区 8 指标：主成分法因子分析 + varimax 旋转 + 回归法得分。"""
    Z = zscore(X2004)
    R = np.corrcoef(Z, rowvar=False)
    w, V = np.linalg.eigh(R)
    idx = np.argsort(w)[::-1]
    w = w[idx]
    V = V[:, idx]
    explained = 100 * w / w.sum()
    cum = np.cumsum(explained)
    m = 2
    A0 = V[:, :m] * np.sqrt(w[:m])          # 未旋转载荷（主成分法）
    A, T = varimax(A0)                       # 方差最大正交旋转
    # 因子方向规约：因子符号本身是任意的，约定每列主导载荷为正，便于解读
    lead_rows = np.argmax(np.abs(A), axis=0)
    signs = np.sign(A[lead_rows, np.arange(m)])
    A = A * signs
    # 回归法（Thomson）得分系数：B = R^{-1} A
    B = np.linalg.solve(R, A)
    F = Z @ B
    # 因子方差贡献（旋转后载荷列平方和）
    contrib = (A ** 2).sum(axis=0)
    contrib_rate = contrib / 8 * 100
    return dict(Z=Z, R=R, w=w, explained=explained, cum=cum, A0=A0, A=A,
                B=B, F=F, contrib=contrib, contrib_rate=contrib_rate)


# ---------------------------------------------------------------- 图 5-11
def fig5_11_case_scree():
    res = _case_fa()
    exp = res["explained"]
    cum = res["cum"]
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    xs = np.arange(1, 9)
    bars = ax.bar(xs, exp, color=C_BLUE, alpha=0.85, width=0.62)
    for x, v in zip(xs, exp):
        ax.text(x, v + 1.2, f"{v:.1f}%", ha="center", fontsize=8.6)
    ax.plot(xs, cum, color=C_ORANGE, marker="o", lw=1.8, ms=5, label="累计方差贡献率")
    for x, v in zip(xs, cum):
        ax.text(x + 0.08, v - 4.6, f"{v:.1f}", fontsize=8.2, color=C_ORANGE)
    ax.axhline(80, color=C_RED, ls="--", lw=1.2)
    ax.text(7.9, 81.5, "80% 标准", color=C_RED, fontsize=9, ha="right")
    ax.axhline(1 * 100 / 8, color="#999999", ls=":", lw=1)
    ax.text(1.06, 100 / 8 + 1.6, "特征值=1（贡献率 12.5%）", color="#777777", fontsize=8.2)
    ax.set_xticks(xs)
    ax.set_xticklabels([f"PC{i}" for i in xs])
    ax.set_ylim(0, 108)
    ax.set_ylabel("方差贡献率（%）")
    ax.set_xlabel("主成分（按方差降序）")
    ax.legend(fontsize=9, loc="center right")
    ax.set_title("31 省市区 8 项经济指标主成分的 pareto 图：\n"
                 f"前两个主成分累计贡献率 {cum[1]:.1f}%，超过 80% 标准", fontsize=11)
    savefig(fig, "fig5_11_case_scree.png")


# ---------------------------------------------------------------- 图 5-12
def fig5_12_case_loading():
    res = _case_fa()
    A = res["A"]
    th = np.linspace(0, 2 * np.pi, 300)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.7))
    for ax, M, title in [
            (axes[0], res["A0"], "旋转前的载荷"),
            (axes[1], A, "方差最大正交旋转后的载荷")]:
        ax.plot(np.cos(th), np.sin(th), color="#cccccc", lw=1)
        ax.axhline(0, color="#999999", lw=0.9)
        ax.axvline(0, color="#999999", lw=0.9)
        for j in range(8):
            ax.plot([0, M[j, 0]], [0, M[j, 1]], color=C_PURPLE, lw=1.4, alpha=0.75)
            ax.scatter(M[j, 0], M[j, 1], s=42, c=C_PURPLE, zorder=3)
            dx = 0.07 if M[j, 0] >= 0 else -0.07
            ha = "left" if M[j, 0] >= 0 else "right"
            ax.text(M[j, 0] + dx, M[j, 1] + 0.03, VAR_NAMES[j], fontsize=8.6, ha=ha)
        ax.set_xlim(-1.12, 1.12)
        ax.set_ylim(-0.62, 1.14)
        ax.set_aspect("equal")
        ax.set_xlabel(f"$F_1$ 载荷（方差贡献率 {res['contrib_rate'][0]:.1f}%）", fontsize=9.5)
        ax.set_ylabel(f"$F_2$ 载荷（方差贡献率 {res['contrib_rate'][1]:.1f}%）", fontsize=9.5)
        ax.set_title(title, fontsize=10.5)
    fig.suptitle("因子载荷图（主成分法）：旋转后 $F_1$ 集中反映生活消费类指标，"
                 "$F_2$ 集中反映生产规模类指标", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.91])
    savefig(fig, "fig5_12_case_loading.png")


# ---------------------------------------------------------------- 图 5-13
def fig5_13_case_score():
    res = _case_fa()
    F = res["F"]
    fig, ax = plt.subplots(figsize=(8.8, 6.6))
    ax.axhline(0, color="#999999", lw=0.8)
    ax.axvline(0, color="#999999", lw=0.8)
    ax.scatter(F[:, 0], F[:, 1], s=30, c=C_BLUE, alpha=0.8, edgecolors="none")
    offsets = {"北京": (6, 6), "天津": (6, 2), "上海": (6, 4), "江苏": (6, 4),
               "浙江": (6, 4), "西藏": (6, -12), "广东": (6, 2), "山东": (6, -3),
               "宁夏": (-14, -13), "青海": (5, -12), "海南": (-20, 4),
               "重庆": (-6, -13), "黑龙江": (-6, 10), "吉林": (5, -2)}
    for i, name in enumerate(REGIONS):
        dx, dy = offsets.get(name, (5, 3))
        ax.text(F[i, 0] + dx * 0.018, F[i, 1] + dy * 0.018, name, fontsize=7.8,
                ha="left" if dx > 0 else "right")
    ax.set_xlabel(f"$F_1$ 因子得分（生活消费，贡献率 {res['contrib_rate'][0]:.1f}%）", fontsize=10.5)
    ax.set_ylabel(f"$F_2$ 因子得分（生产规模，贡献率 {res['contrib_rate'][1]:.1f}%）", fontsize=10.5)
    ax.set_title("31 省市区在前两个因子上的得分（主成分法 + 方差最大旋转）\n"
                 "京津沪 $F_1$ 得分高，粤鲁苏浙 $F_2$ 得分高", fontsize=11)
    savefig(fig, "fig5_13_case_score.png")


# ---------------------------------------------------------------- 图 5-14
def fig5_14_case_composite():
    res = _case_fa()
    F = res["F"]
    rate = res["contrib_rate"]
    comp = (F @ rate) / rate.sum()
    order = np.argsort(comp)
    fig, ax = plt.subplots(figsize=(8.0, 7.6))
    colors = [C_BLUE if v >= 0 else C_ORANGE for v in comp[order]]
    ax.barh(np.arange(31), comp[order], color=colors, alpha=0.88, height=0.66)
    ax.set_yticks(np.arange(31))
    ax.set_yticklabels([REGIONS[i] for i in order], fontsize=9)
    for i, v in enumerate(comp[order]):
        ax.text(v + (0.04 if v >= 0 else -0.04), i, f"{v:5.2f}", va="center",
                ha="left" if v >= 0 else "right", fontsize=7.8)
    ax.axvline(0, color="#555555", lw=0.9)
    ax.set_xlabel("综合因子得分", fontsize=10.5)
    r1, r2 = rate[0] / rate.sum(), rate[1] / rate.sum()
    ax.set_title(f"综合因子得分排序：$S$ = {r1:.2f}$F_1$ + {r2:.2f}$F_2$\n"
                 "（权重为旋转后各因子的方差贡献率占比）", fontsize=11)
    ax.set_xlim(comp.min() - 0.75, comp.max() + 0.75)
    savefig(fig, "fig5_14_case_composite.png")


# ---------------------------------------------------------------- 输出摘要
def print_case_summary():
    res = _case_fa()
    print("== 案例计算摘要（主成分法 + varimax） ==")
    print("特征值:", np.round(res["w"], 3))
    print("方差贡献率%:", np.round(res["explained"], 2))
    print("累计贡献率%:", np.round(res["cum"], 2))
    print("旋转后载荷矩阵:")
    for j in range(8):
        print(f"  {VAR_NAMES[j]:12s} F1={res['A'][j, 0]:6.3f}  F2={res['A'][j, 1]:6.3f}"
              f"   共性方差={res['A'][j, 0] ** 2 + res['A'][j, 1] ** 2:5.3f}")
    print("旋转后因子方差贡献:", np.round(res["contrib"], 3),
          " 贡献率%:", np.round(res["contrib_rate"], 2))
    comp = (res["F"] @ res["contrib_rate"]) / res["contrib_rate"].sum()
    idx = np.argsort(comp)[::-1]
    print("综合得分前8:", [(REGIONS[i], round(comp[i], 2)) for i in idx[:8]])
    print("综合得分后5:", [(REGIONS[i], round(comp[i], 2)) for i in idx[-5:]])


if __name__ == "__main__":
    fig5_01_f_test_vs_mi()
    fig5_02_scatter_matrix()
    fig5_03_r_clustering()
    fig5_04_pca_3d_plane()
    fig5_05_ellipse_rotation()
    fig5_06_max_variance()
    fig5_07_pca_workflow()
    fig5_08_fa_path_diagram()
    fig5_09_pca_vs_fa()
    fig5_10_rotation_varimax()
    fig5_11_case_scree()
    fig5_12_case_loading()
    fig5_13_case_score()
    fig5_14_case_composite()
    print_case_summary()
