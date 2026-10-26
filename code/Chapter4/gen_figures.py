# -*- coding: utf-8 -*-
"""第4章 聚类分析 插图生成脚本
运行：uv run --no-project --with matplotlib --with numpy python gen_figures.py
输出：书稿/figs/ch04/fig4_*.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Arc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "书稿", "figs", "ch04")
os.makedirs(OUT, exist_ok=True)

C_BLUE = "#1f77b4"
C_ORANGE = "#ff7f0e"
C_GREEN = "#2ca02c"
C_RED = "#d62728"
C_PURPLE = "#9467bd"
C_GRAY = "#7f7f7f"

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["savefig.dpi"] = 150

rng = np.random.default_rng(42)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight")
    plt.close(fig)
    print("saved", name)


# --------------------------------------------------------------- 基础算法实现
def kmeans_fit(X, k, init=None, iters=100):
    """简单 k 均值：返回 (标签, 中心, 迭代过程列表[(centers, labels), ...])"""
    if init is None:
        init = X[rng.choice(len(X), k, replace=False)]
    centers = np.array(init, dtype=float)
    hist = []
    for _ in range(iters):
        d = np.linalg.norm(X[:, None, :] - centers[None, :, :], axis=2)
        labels = d.argmin(axis=1)
        hist.append((centers.copy(), labels.copy()))
        new_centers = np.array([
            X[labels == j].mean(axis=0) if np.any(labels == j) else centers[j]
            for j in range(k)])
        if np.allclose(new_centers, centers):
            centers = new_centers
            break
        centers = new_centers
    d = np.linalg.norm(X[:, None, :] - centers[None, :, :], axis=2)
    labels = d.argmin(axis=1)
    hist.append((centers.copy(), labels.copy()))
    return labels, centers, hist


def sse_of(X, labels, centers):
    return sum(np.sum((X[labels == j] - centers[j]) ** 2) for j in range(len(centers)))


def agglomerative(D, method):
    """Lance-Williams 通用的凝聚层次聚类。
    D: n×n 距离矩阵；返回合并记录 [(ida, idb, height), ...]（id 用并查集代表元编号）"""
    n0 = len(D)
    D0 = np.asarray(D)
    D = np.full((2 * n0 - 1, 2 * n0 - 1), np.inf)
    D[:n0, :n0] = D0
    alive = list(range(n0))
    size = {i: 1 for i in range(n0)}
    merges = []
    members = {i: [i] for i in range(n0)}
    for _ in range(n0 - 1):
        m = len(alive)
        best = (np.inf, -1, -1)
        for a in range(m):
            for b in range(a + 1, m):
                v = D[alive[a], alive[b]]
                if v < best[0]:
                    best = (v, a, b)
        _, a, b = best
        ia, ib = alive[a], alive[b]
        merges.append((ia, ib, D[ia, ib]))
        # 新簇编号
        new_id = max(members) + 1
        na, nb, nk = size[ia], size[ib], size[ia] + size[ib]
        for j in alive:
            if j in (ia, ib):
                continue
            nj = size[j]
            if method == "single":
                v = 0.5 * D[ia, j] + 0.5 * D[ib, j] - 0.5 * abs(D[ia, j] - D[ib, j])
            elif method == "complete":
                v = 0.5 * D[ia, j] + 0.5 * D[ib, j] + 0.5 * abs(D[ia, j] - D[ib, j])
            elif method == "average":
                v = na / nk * D[ia, j] + nb / nk * D[ib, j]
            elif method == "centroid":
                v = (na / nk * D[ia, j] + nb / nk * D[ib, j]
                     - na * nb / nk ** 2 * D[ia, ib])
            elif method == "ward":
                v = ((na + nj) / (nk + nj) * D[ia, j] + (nb + nj) / (nk + nj) * D[ib, j]
                     - nj / (nk + nj) * D[ia, ib])
            else:
                raise ValueError(method)
            D[new_id, j] = D[j, new_id] = max(v, 0.0)
        D[new_id, new_id] = 0.0
        size[new_id] = nk
        members[new_id] = members.pop(ia) + members.pop(ib)
        alive = [j for j in alive if j not in (ia, ib)] + [new_id]
    return merges


def cut_k(merges, n, k):
    """把层次聚类合并记录切成 k 类，返回长度 n 的标签（噪声无）。"""
    parent = list(range(2 * n - 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for step, (ia, ib, _) in enumerate(merges):
        if step >= n - k:
            break
        parent[find(ia)] = n + step
        parent[find(ib)] = n + step
    roots = {}
    labels = np.zeros(n, dtype=int)
    for i in range(n):
        r = find(i)
        if r not in roots:
            roots[r] = len(roots)
        labels[i] = roots[r]
    return labels


def tree_layout(merges, n):
    """由合并记录得到树叶次序与各内部节点坐标，供手绘谱系图。"""
    left = {}
    right = {}
    height = {}
    for step, (ia, ib, h) in enumerate(merges):
        nid = n + step
        left[nid] = ia
        right[nid] = ib
        height[nid] = h
    height = {**{i: 0.0 for i in range(n)}, **height}
    order = []

    def inorder(v):
        if v < n:
            order.append(v)
            return [v]
        ls = inorder(left[v])
        rs = inorder(right[v])
        return ls + rs

    root = n + len(merges) - 1
    inorder(root)
    xpos = {leaf: i for i, leaf in enumerate(order)}
    node_x = dict(xpos)

    def setx(v):
        if v < n:
            return node_x[v]
        x1 = setx(left[v])
        x2 = setx(right[v])
        node_x[v] = (x1 + x2) / 2.0
        return node_x[v]

    setx(root)
    return node_x, height, left, right, root


def draw_dendrogram(merges, n, labels, ax, cut=None, colors=None, leaf_font=11):
    """手绘谱系图：labels 为每个叶子的文字，colors 为叶子上色（可 None）。"""
    node_x, height, left, right, root = tree_layout(merges, n)
    ymax = max(height.values()) * 1.06
    ax.set_ylim(-ymax * 0.16, ymax * 1.02)
    for v in range(n, n + len(merges)):
        x0, h = node_x[v], height[v]
        for child in (left[v], right[v]):
            xc, hc = node_x[child], height[child]
            ax.plot([x0, x0, xc, xc], [h, hc, hc, h], color="0.35", lw=1.1, zorder=2)
    if cut is not None:
        ax.axhline(cut, color=C_RED, ls="--", lw=1.2, zorder=3)
    for leaf in range(n):
        c = colors[leaf] if colors is not None else "0.2"
        ax.text(node_x[leaf], -ymax * 0.06, str(labels[leaf]), ha="center", va="top",
                fontsize=leaf_font, color=c, rotation=0)
    ax.set_xticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)


def dbscan_fit(X, eps, minpts):
    """简单 DBSCAN：返回 (标签, 是否核心点)；标签 -1 为噪声。"""
    n = len(X)
    d = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
    neighbors = [np.where(d[i] <= eps)[0] for i in range(n)]
    core = np.array([len(nb) >= minpts for nb in neighbors])
    labels = np.full(n, -1, dtype=int)
    cid = 0
    for i in range(n):
        if labels[i] != -1 or not core[i]:
            continue
        queue = [i]
        labels[i] = cid
        while queue:
            j = queue.pop()
            if not core[j]:
                continue
            for nb in neighbors[j]:
                if labels[nb] == -1:
                    labels[nb] = cid
                    if core[nb]:
                        queue.append(nb)
        cid += 1
    return labels, core


def silhouette_values(X, labels):
    n = len(X)
    D = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
    s = np.zeros(n)
    for i in range(n):
        same = labels == labels[i]
        a = D[i, same].sum() / (same.sum() - 1) if same.sum() > 1 else 0.0
        bs = []
        for c in np.unique(labels):
            if c == labels[i]:
                continue
            other = labels == c
            bs.append(D[i, other].mean())
        b = min(bs) if bs else 0.0
        s[i] = 0.0 if max(a, b) == 0 else (b - a) / max(a, b)
    return s


# --------------------------------------------------------------- 图 4-1
def fig_ambiguous_clusters():
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9))
    a = rng.normal([0, 0], 0.9, (60, 2))
    b = rng.normal([4.2, 1.2], 0.9, (60, 2))
    c = rng.normal([2.0, 4.0], 0.9, (60, 2))
    X = np.vstack([a, b, c])
    labels, centers, _ = kmeans_fit(X, 3)
    ax = axes[0]
    ax.scatter(X[:, 0], X[:, 1], s=18, color=C_BLUE, alpha=0.75)
    ax.set_title("原始数据：能聚成几类？", fontsize=12)
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax = axes[1]
    cols = [C_BLUE, C_ORANGE, C_GREEN]
    for j in range(3):
        ax.scatter(X[labels == j, 0], X[labels == j, 1], s=18, color=cols[j], alpha=0.8)
    ax.scatter(centers[:, 0], centers[:, 1], marker="*", s=220, color=C_RED,
               edgecolor="white", zorder=5, label="类中心")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    ax.set_title("按 $k$=3 做 K-均值聚类的结果", fontsize=12)
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    for ax in axes:
        ax.set_aspect("equal")
    fig.tight_layout()
    save(fig, "fig4_01_ambiguous_clusters.png")


# --------------------------------------------------------------- 图 4-2
def fig_hierarchical_demo():
    pts = np.array([[1.0, 2.0], [1.2, 2.1], [2.0, 1.0], [2.2, 1.2],
                    [3.0, 2.4], [3.2, 2.3], [2.7, 3.4], [4.2, 3.2]])
    n = len(pts)
    D = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
    merges = agglomerative(D, "single")
    labels3 = cut_k(merges, n, 3)
    cols = [C_BLUE, C_ORANGE, C_GREEN]
    leaf_colors = [cols[labels3[i]] for i in range(n)]

    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.0),
                             gridspec_kw={"width_ratios": [1.0, 1.15]})
    ax = axes[0]
    ax.scatter(pts[:, 0], pts[:, 1], s=60, color=[leaf_colors[i] for i in range(n)],
               edgecolor="white", zorder=4)
    for i, (x, y) in enumerate(pts):
        ax.text(x + 0.07, y + 0.07, str(i + 1), fontsize=11)
    # 画出最先合并的 3 条最近邻连线（虚线示意逐层合并）
    for i, j in [(0, 1), (2, 3), (4, 5)]:
        ax.plot([pts[i, 0], pts[j, 0]], [pts[i, 1], pts[j, 1]], ls="--",
                color="0.5", lw=1, zorder=2)
    ax.plot([1.1, 2.1], [2.05, 1.1], ls=":", color=C_RED, lw=1.2, zorder=3)
    ax.plot([2.9, 2.75], [2.5, 3.3], ls=":", color=C_RED, lw=1.2, zorder=3)
    ax.set_title("8 个样本点（颜色为最终 3 类）", fontsize=12)
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.set_aspect("equal")
    ax.set_xlim(0.6, 4.7); ax.set_ylim(0.6, 3.9)

    ax = axes[1]
    draw_dendrogram(merges, n, [str(i + 1) for i in range(n)], ax,
                    cut=0.72, colors=leaf_colors)
    ax.set_title("层次聚类的谱系图（最短距离法）", fontsize=12)
    ax.set_ylabel("合并高度（类间距离）")
    ax.annotate("合并法：自下而上逐层合并", xy=(0.98, 0.06), xycoords="axes fraction",
                ha="right", fontsize=10, color=C_BLUE)
    ax.annotate("分解法：自上而下逐层拆分", xy=(0.98, 0.94), xycoords="axes fraction",
                ha="right", fontsize=10, color=C_ORANGE)
    ax.annotate("在此处画线\n→ 分成 3 类", xy=(2.6, 0.72), xytext=(4.6, 1.6),
                fontsize=10, color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED))
    fig.tight_layout()
    save(fig, "fig4_02_hierarchical_demo.png")


# --------------------------------------------------------------- 图 4-3
def fig_gmm_soft():
    a = rng.multivariate_normal([-1.2, -1.0], [[0.55, 0.42], [0.42, 0.55]], 120)
    b = rng.multivariate_normal([1.3, 1.1], [[0.6, 0.4], [0.4, 0.65]], 120)
    X = np.vstack([a, b])
    # EM 拟合 2 分量高斯混合
    mu = np.array([[-1.0, -0.8], [1.0, 0.9]])
    cov = np.array([np.eye(2), np.eye(2)]) * 0.4
    w = np.array([0.5, 0.5])
    for _ in range(120):
        dens = np.stack([w[j] * _gauss(X, mu[j], cov[j]) for j in range(2)], axis=1)
        R = dens / dens.sum(axis=1, keepdims=True)
        nk = R.sum(axis=0)
        w = nk / len(X)
        mu = np.stack([(R[:, j:j + 1] * X).sum(axis=0) / nk[j] for j in range(2)])
        for j in range(2):
            dx = X - mu[j]
            cov[j] = (R[:, j:j + 1] * dx).T @ dx / nk[j] + 1e-4 * np.eye(2)

    fig, axes = plt.subplots(1, 3, figsize=(10.6, 3.6))
    ax = axes[0]
    ax.scatter(X[:, 0], X[:, 1], s=12, color=C_BLUE, alpha=0.55)
    gx, gy = np.meshgrid(np.linspace(-4, 4, 160), np.linspace(-4, 4, 160))
    G = np.stack([gx.ravel(), gy.ravel()], axis=1)
    Z = sum(w[j] * _gauss(G, mu[j], cov[j]) for j in range(2)).reshape(gx.shape)
    ax.contour(gx, gy, Z, levels=6, colors=C_PURPLE, linewidths=1.0)
    ax.set_title("高斯混合概率密度等值线", fontsize=12)

    ax = axes[1]
    hard = R.argmax(axis=1)
    ax.scatter(X[hard == 0, 0], X[hard == 0, 1], s=12, color=C_BLUE, alpha=0.8)
    ax.scatter(X[hard == 1, 0], X[hard == 1, 1], s=12, color=C_ORANGE, alpha=0.8)
    ax.set_title("硬聚类：每点只属一类", fontsize=12)

    ax = axes[2]
    sc = ax.scatter(X[:, 0], X[:, 1], s=14, c=R[:, 0], cmap="coolwarm",
                    vmin=0, vmax=1, alpha=0.9)
    cb = fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.03)
    cb.set_label("属于左侧类的概率", fontsize=9)
    ax.set_title("软聚类：颜色表示隶属概率", fontsize=12)
    for ax in axes:
        ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
        ax.set_aspect("equal")
    fig.tight_layout()
    save(fig, "fig4_03_gmm_soft.png")


def _gauss(X, mu, cov):
    inv = np.linalg.inv(cov)
    det = np.linalg.det(cov)
    dx = X - mu
    q = np.einsum("ni,ij,nj->n", dx, inv, dx)
    return np.exp(-0.5 * q) / (2 * np.pi * np.sqrt(det))


# --------------------------------------------------------------- 图 4-4
def _datasets():
    # 两同心圆（近等距采样+抖动，避免外环随机稀疏断裂）
    def _ring(npts, radius, noise):
        t = np.linspace(0, 2 * np.pi, npts, endpoint=False) \
            + rng.uniform(-np.pi / npts, np.pi / npts, npts)
        p = np.stack([np.cos(t), np.sin(t)], axis=1) * radius
        return p + rng.normal(0, noise, (npts, 2))
    circles = np.vstack([_ring(130, 0.4, 0.035), _ring(130, 1.2, 0.04)])
    # 两半月
    t = rng.uniform(0, np.pi, 130)
    m1 = np.stack([np.cos(t), np.sin(t)], axis=1) + rng.normal(0, 0.07, (130, 2))
    m2 = np.stack([1 - np.cos(t), 0.5 - np.sin(t)], axis=1) + rng.normal(0, 0.07, (130, 2))
    moons = np.vstack([m1, m2])
    # 三团
    blobs = np.vstack([
        rng.normal([-1.2, -0.9], 0.22, (87, 2)),
        rng.normal([1.2, -0.9], 0.22, (87, 2)),
        rng.normal([0.0, 1.1], 0.24, (86, 2))])
    # 三条形
    def _stripe(ys, m):
        return np.hstack([rng.uniform(-1.4, 1.4, (m, 1)),
                          rng.normal(ys, 0.055, (m, 1))])
    stripes = np.vstack([_stripe(-1.0, 87), _stripe(0.0, 87), _stripe(1.0, 86)])
    return [("两同心圆", circles, 2), ("两半月", moons, 2),
            ("三团点", blobs, 3), ("三条形", stripes, 3)]


def fig_methods_comparison():
    cols = [C_BLUE, C_ORANGE, C_GREEN]
    rows = _datasets()
    fig, axes = plt.subplots(4, 3, figsize=(10.0, 11.4))
    params = {"两同心圆": (0.26, 5), "两半月": (0.22, 5), "三团点": (0.32, 5),
              "三条形": (0.24, 5)}
    for r, (name, X, k) in enumerate(rows):
        # K 均值
        labels, centers, _ = kmeans_fit(X, k)
        ax = axes[r, 0]
        for j in range(k):
            ax.scatter(X[labels == j, 0], X[labels == j, 1], s=9, color=cols[j], alpha=0.8)
        ax.scatter(centers[:, 0], centers[:, 1], marker="*", s=150, color=C_RED,
                   edgecolor="white", zorder=5)
        # 层次聚类（完全连接，切 k 类）
        D = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
        merges = agglomerative(D, "complete")
        hl = cut_k(merges, len(X), k)
        ax = axes[r, 1]
        for j in range(k):
            ax.scatter(X[hl == j, 0], X[hl == j, 1], s=9, color=cols[j], alpha=0.8)
        # DBSCAN
        eps, mp = params[name]
        dl, _ = dbscan_fit(X, eps, mp)
        ax = axes[r, 2]
        for j in sorted(set(dl) - {-1}):
            ax.scatter(X[dl == j, 0], X[dl == j, 1], s=9,
                       color=cols[j % 3], alpha=0.8)
        if np.any(dl == -1):
            ax.scatter(X[dl == -1, 0], X[dl == -1, 1], s=16, marker="x",
                       color="0.4", linewidths=1.0)
        for c in range(3):
            axes[r, c].set_title(
                ["K-均值（k=%d）" % k, "层次聚类（完全连接，切 k 类）",
                 "DBSCAN（eps=%.2f, MinPts=%d）" % (eps, mp)][c] if r == 0 else "",
                fontsize=11)
            axes[r, c].set_xticks([]); axes[r, c].set_yticks([])
            axes[r, c].set_ylabel(name if c == 0 else "", fontsize=12)
            axes[r, c].set_aspect("equal")
    fig.tight_layout()
    save(fig, "fig4_04_methods_comparison.png")


# --------------------------------------------------------------- 图 4-5
def fig_linkage_strategies():
    t = rng.uniform(0, np.pi, 110)
    m1 = np.stack([np.cos(t), np.sin(t)], axis=1) + rng.normal(0, 0.06, (110, 2))
    m2 = np.stack([1 - np.cos(t), 0.5 - np.sin(t)], axis=1) + rng.normal(0, 0.06, (110, 2))
    X = np.vstack([m1, m2])
    D = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
    methods = [("single", "最短距离法（single）"),
               ("complete", "最长距离法（complete）"),
               ("average", "组间平均法（average）"),
               ("ward", "离差平方和法（ward）")]
    cols = [C_BLUE, C_ORANGE]
    fig, axes = plt.subplots(2, 2, figsize=(8.6, 8.0))
    for ax, (m, title) in zip(axes.ravel(), methods):
        merges = agglomerative(D, m)
        labels = cut_k(merges, len(X), 2)
        for j in range(2):
            ax.scatter(X[labels == j, 0], X[labels == j, 1], s=10, color=cols[j], alpha=0.8)
        ax.set_title(title, fontsize=12)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_aspect("equal")
    fig.suptitle("同一数据集、同一层次聚类方法，不同合并策略的结果", fontsize=13, y=0.995)
    fig.tight_layout()
    save(fig, "fig4_05_linkage_strategies.png")


# --------------------------------------------------------------- 图 4-6
def fig_variable_angle():
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    v1 = np.array([3.4, 1.0])
    v2 = np.array([2.5, 2.4])
    ax.arrow(0, 0, v1[0], v1[1], width=0.025, head_width=0.14, length_includes_head=True,
             color=C_BLUE, zorder=4)
    ax.arrow(0, 0, v2[0], v2[1], width=0.025, head_width=0.14, length_includes_head=True,
             color=C_ORANGE, zorder=4)
    ax.text(3.52, 0.92, "变量 $x_1$\n（$n$ 个样本取值\n构成的向量）", fontsize=10, color=C_BLUE)
    ax.text(2.28, 2.62, "变量 $x_2$", fontsize=10, color=C_ORANGE)
    ang = Arc((0, 0), 2.2, 2.2, angle=0,
              theta1=np.degrees(np.arctan2(v2[1], v2[0])),
              theta2=np.degrees(np.arctan2(v1[1], v1[0])), color=C_RED, lw=1.6)
    ax.add_patch(ang)
    ax.text(1.18, 0.98, r"$\theta$", fontsize=13, color=C_RED)
    ax.text(1.35, -0.55,
            r"$\cos\theta=\dfrac{\sum_{i=1}^{n} x_{i1}\,x_{i2}}"
            r"{\sqrt{\sum_{i=1}^{n} x_{i1}^{2}}\sqrt{\sum_{i=1}^{n} x_{i2}^{2}}}$",
            fontsize=12)
    ax.text(1.35, -1.15, r"$\theta$ 越小（$\cos\theta$ 越接近 1），两变量越相似",
            fontsize=10, color="0.25")
    ax.set_xlim(-0.3, 5.2); ax.set_ylim(-1.5, 3.1)
    ax.axhline(0, color="0.8", lw=0.8); ax.axvline(0, color="0.8", lw=0.8)
    ax.set_title("用夹角余弦度量两个变量的相似性", fontsize=12)
    ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout()
    save(fig, "fig4_06_variable_angle.png")


# --------------------------------------------------------------- 图 4-7
def fig_point_distances():
    fig, axes = plt.subplots(2, 2, figsize=(8.4, 7.6))
    th = np.linspace(0, 2 * np.pi, 200)
    diag1 = np.cos(th) - np.sin(th)
    diag2 = np.cos(th) + np.sin(th)
    balls = [
        (axes[0, 0], r"欧氏距离：$\sqrt{\sum_{k}|x_{1k}-x_{2k}|^{2}}$ 的等距线（圆）",
         [(np.cos(th), np.sin(th), C_BLUE)]),
        (axes[0, 1], r"街区距离：$\sum_{k}|x_{1k}-x_{2k}|$ 的等距线（菱形）",
         [(diag1, diag2, C_ORANGE), (-diag1, diag2, C_ORANGE)]),
        (axes[1, 0], r"切比雪夫距离：$\max_{k}|x_{1k}-x_{2k}|$ 的等距线（方形）",
         [(diag1, diag2, C_ORANGE), (-diag1, diag2, C_ORANGE),
          (diag1, -diag2, C_ORANGE), (-diag1, -diag2, C_ORANGE)])]
    for ax, t, curves in balls:
        for cx, cy, c in curves:
            ax.plot(cx, cy, color=c, lw=1.8)
        ax.set_title(t, fontsize=11)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_aspect("equal")
        ax.set_xlim(-1.75, 1.75); ax.set_ylim(-1.75, 1.75)
    ax = axes[1, 1]
    P = rng.multivariate_normal([0, 0], [[1.0, 0.82], [0.82, 1.0]], 300)
    ax.scatter(P[:, 0], P[:, 1], s=10, color=C_BLUE, alpha=0.5)
    rot = np.array([[np.cos(0.7), -np.sin(0.7)], [np.sin(0.7), np.cos(0.7)]])
    for r in (0.6, 1.2, 1.8):
        e = np.stack([r * 1.62 * np.cos(th), r * 0.62 * np.sin(th)], axis=1) @ rot
        ax.plot(e[:, 0], e[:, 1], color=C_RED, lw=1.4)
    ax.set_title(r"马氏距离：$D=\sqrt{(x-y)^{T}\Sigma^{-1}(x-y)}$"
                 "\n的等距线（椭圆）", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    fig.suptitle("不同点间距离度量的等距线（到原点距离相等的位置）", fontsize=13, y=0.995)
    fig.tight_layout()
    save(fig, "fig4_07_point_distances.png")


# --------------------------------------------------------------- 图 4-8
def fig_class_distances():
    g1 = rng.normal([1.4, 2.6], 0.28, (7, 2))
    g2 = rng.normal([4.2, 1.6], 0.3, (7, 2))
    c1, c2 = g1.mean(axis=0), g2.mean(axis=0)
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    for a, b in [(g1, g2)]:
        for p in a:
            for q in b:
                ax.plot([p[0], q[0]], [p[1], q[1]], color="0.82", lw=0.6, zorder=1)
    ax.scatter(g1[:, 0], g1[:, 1], s=42, color=C_BLUE, zorder=3, label="类 $G_1$")
    ax.scatter(g2[:, 0], g2[:, 1], s=42, color=C_ORANGE, zorder=3, label="类 $G_2$")
    # 最短与最长点对
    D = np.linalg.norm(g1[:, None, :] - g2[None, :, :], axis=2)
    i, j = np.unravel_index(D.argmin(), D.shape)
    ax.plot([g1[i, 0], g2[j, 0]], [g1[i, 1], g2[j, 1]], color=C_GREEN, lw=2.2, zorder=4)
    ax.text((g1[i, 0] + g2[j, 0]) / 2 + 0.06, (g1[i, 1] + g2[j, 1]) / 2 + 0.10,
            "最短距离", fontsize=10, color=C_GREEN)
    i, j = np.unravel_index(D.argmax(), D.shape)
    ax.plot([g1[i, 0], g2[j, 0]], [g1[i, 1], g2[j, 1]], color=C_RED, lw=2.2, zorder=4)
    ax.text((g1[i, 0] + g2[j, 0]) / 2 + 0.06, (g1[i, 1] + g2[j, 1]) / 2 - 0.16,
            "最长距离", fontsize=10, color=C_RED)
    # 中心连线
    ax.scatter(*c1, marker="*", s=300, color=C_PURPLE, edgecolor="white", zorder=5)
    ax.scatter(*c2, marker="*", s=300, color=C_PURPLE, edgecolor="white", zorder=5)
    ax.plot([c1[0], c2[0]], [c1[1], c2[1]], color=C_PURPLE, lw=2.0, ls="--", zorder=4)
    ax.text((c1[0] + c2[0]) / 2, (c1[1] + c2[1]) / 2 + 0.14, "中心（重心）距离",
            fontsize=10, color=C_PURPLE, ha="center")
    ax.text(2.35, 0.62, "灰色细线：两类之间所有点对的距离\n（其平均即组间平均距离）",
            fontsize=10, color="0.35")
    ax.set_title("类别之间距离的几种定义", fontsize=12)
    ax.legend(loc="upper right", fontsize=10, frameon=False)
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.set_aspect("equal")
    ax.set_xlim(0.2, 5.4); ax.set_ylim(0.2, 3.6)
    fig.tight_layout()
    save(fig, "fig4_08_class_distances.png")


# --------------------------------------------------------------- 图 4-9
def fig_kmeans_steps():
    a = rng.normal([1.0, 1.2], 0.45, (26, 2))
    b = rng.normal([4.0, 3.4], 0.5, (26, 2))
    X = np.vstack([a, b])
    init = np.array([[1.8, 3.0], [3.2, 1.1]])
    labels, centers, hist = kmeans_fit(X, 2, init=init, iters=12)
    fig, axes = plt.subplots(1, 4, figsize=(12.4, 3.3))
    cols = [C_BLUE, C_ORANGE]
    titles = ["第 0 步：假设 $k$=2，选定初始中心",
              "第 1 步：按距离最近原则分配各点",
              "第 2 步：重算各类均值作新中心",
              "迭代至收敛：中心和划分不再变化"]
    for step in range(4):
        ax = axes[step]
        if step == 0:
            ax.scatter(X[:, 0], X[:, 1], s=14, color="0.6", alpha=0.8)
            ax.scatter(init[:, 0], init[:, 1], marker="*", s=260, color=C_RED,
                       edgecolor="white", zorder=5)
        else:
            idx = step - 1 if step < 3 else len(hist) - 1
            c, lb = (centers, labels) if step == 3 else hist[idx]
            for j in range(2):
                ax.scatter(X[lb == j, 0], X[lb == j, 1], s=14, color=cols[j], alpha=0.85)
            if step == 2 and idx > 0:
                prev = hist[idx - 1][0]
                for j in range(2):
                    ax.annotate("", xy=(c[j, 0], c[j, 1]), xytext=(prev[j, 0], prev[j, 1]),
                                arrowprops=dict(arrowstyle="->", color=C_PURPLE, lw=1.6))
            ax.scatter(c[:, 0], c[:, 1], marker="*", s=260, color=C_RED,
                       edgecolor="white", zorder=5)
        ax.set_title(titles[step], fontsize=11)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_aspect("equal")
        ax.set_xlim(0, 5.2); ax.set_ylim(0, 4.6)
    fig.tight_layout()
    save(fig, "fig4_09_kmeans_steps.png")


# --------------------------------------------------------------- 图 4-10
def fig_kmeans_1d():
    data = [2, 4, 10, 12, 3, 20, 30, 11, 25]
    steps = [  # 与教材表 4-11 完全一致的 (m1, m2, K1, K2)
        (2.0, 4.0, [2, 3], [4, 10, 12, 20, 30, 11, 25]),
        (2.5, 16.0, [2, 3, 4], [10, 12, 20, 30, 11, 25]),
        (3.0, 18.0, [2, 3, 4, 10], [12, 20, 30, 11, 25]),
        (4.75, 19.6, [2, 3, 4, 10, 11, 12], [20, 30, 25]),
        (7.0, 25.0, [2, 3, 4, 10, 11, 12], [20, 30, 25])]
    fig, axes = plt.subplots(5, 1, figsize=(7.6, 7.2), sharex=True)
    for r, (m1, m2, k1, k2) in enumerate(steps):
        ax = axes[r]
        for v in data:
            c = C_BLUE if v in k1 else C_ORANGE
            ax.plot([v], [0], "o", ms=9, color=c)
        for m, c, lb in [(m1, C_BLUE, "$m_1$"), (m2, C_ORANGE, "$m_2$")]:
            ax.axvline(m, color=c, ls="--", lw=1.3)
            ax.text(m, 0.62, "%s=%.2f" % (lb, m), ha="center", fontsize=10, color=c)
        ax.set_ylim(-0.55, 1.0)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_title("第 %d 次迭代：$K_1$=%s，$K_2$=%s" % (
            r + 1, sorted(k1), sorted(k2)), fontsize=10.5, pad=1.5)
        if r == 4:
            ax.text(16, -0.5, "中心不再变化，聚类收敛", fontsize=10, color=C_GREEN,
                    ha="center")
    axes[-1].set_xticks(range(0, 33, 4))
    axes[-1].set_xlabel("一维数据取值")
    fig.tight_layout()
    save(fig, "fig4_10_kmeans_1d.png")


# --------------------------------------------------------------- 图 4-11
def fig_dbscan_points():
    fig, ax = plt.subplots(figsize=(7.4, 5.4))
    r = 1.0
    pts = {
        "A": (2.0, 2.0), "p1": (1.55, 1.72), "p2": (2.28, 1.42), "p3": (2.52, 2.38),
        "B": (2.68, 2.08),
        "D": (5.2, 1.5), "q1": (4.62, 1.05), "q2": (5.38, 0.86), "q3": (5.05, 2.16),
        "C": (5.94, 1.24), "N": (0.6, 4.3)}
    core_circ = ["A", "D"]
    for name, (x, y) in pts.items():
        if name in core_circ:
            circ = Circle((x, y), r, fill=False, color=C_RED, ls="--", lw=1.5)
        else:
            circ = Circle((x, y), r, fill=False, color="0.55", ls=":", lw=1.1)
        ax.add_patch(circ)
    for name, (x, y) in pts.items():
        if name in ("A", "D"):
            ax.plot(x, y, "o", ms=11, color=C_RED)
            ax.text(x, y + 0.16, name, ha="center", fontsize=12, color=C_RED)
        elif name in ("B", "C", "N"):
            ax.plot(x, y, "s", ms=9, color=C_GREEN if name != "N" else C_GRAY)
            ax.text(x + 0.1, y + 0.14, name, fontsize=12,
                    color=C_GREEN if name != "N" else C_GRAY)
        else:
            ax.plot(x, y, "o", ms=7, color=C_BLUE)
    ax.annotate("核心点 A\n（邻域内对象数 $\\geq$ MinPts）", xy=pts["A"],
                xytext=(0.35, 2.85), fontsize=10, color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED))
    ax.annotate("边界点 B\n（不是核心点，但落在\n核心点 A 的邻域内）", xy=pts["B"],
                xytext=(2.4, 3.45), fontsize=10, color=C_GREEN,
                arrowprops=dict(arrowstyle="->", color=C_GREEN))
    ax.annotate("噪音点 N\n（既非核心点也非边界点）", xy=pts["N"],
                xytext=(1.15, 4.9), fontsize=10, color=C_GRAY,
                arrowprops=dict(arrowstyle="->", color=C_GRAY))
    ax.annotate("", xy=(3.0, 2.0), xytext=(2.0, 2.0),
                arrowprops=dict(arrowstyle="-", color=C_RED, lw=1.0))
    ax.text(2.86, 2.14, "Eps", fontsize=10, color=C_RED)
    ax.set_title("DBSCAN 的 $Eps$ 邻域与三种点（示意 MinPts=5）", fontsize=12)
    ax.set_xlim(-0.4, 7.6); ax.set_ylim(-0.2, 5.6)
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.set_aspect("equal")
    fig.tight_layout()
    save(fig, "fig4_11_dbscan_points.png")


# --------------------------------------------------------------- 图 4-12
def fig_dbscan_reachability():
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    r = 1.0
    pts = {"P": (1.0, 2.0), "p1": (0.55, 2.62), "M": (1.82, 2.18), "p2": (2.58, 1.78),
           "Q": (2.62, 2.62), "O": (5.3, 1.9), "o1": (4.85, 1.42), "S": (6.02, 1.48),
           "R": (5.72, 2.62)}
    for name, (x, y) in pts.items():
        style = dict(color=C_RED, ls="--", lw=1.4) if name in ("P", "M", "O") \
            else dict(color="0.6", ls=":", lw=1.0)
        ax.add_patch(Circle((x, y), r, fill=False, **style))
    for name, (x, y) in pts.items():
        if name in ("P", "M", "O"):
            ax.plot(x, y, "o", ms=11, color=C_RED)
        else:
            ax.plot(x, y, "o", ms=8, color=C_BLUE)
        ax.text(x + 0.09, y + 0.13, name, fontsize=12)
    ax.text(0.1, 3.6, "MinPts=3：P、M、O 各自邻域内\n都至少含 3 个对象，均为核心点",
            fontsize=10, color=C_RED)
    ax.annotate("M 从 P 直接密度可达；\nQ 从 M 直接密度可达", xy=pts["Q"],
                xytext=(2.15, 3.75), fontsize=10,
                arrowprops=dict(arrowstyle="->", color="0.3"))
    ax.annotate("于是 Q 从 P 密度可达\n（传递；但 P 从 Q 不可达，\n密度可达不对称）",
                xy=(1.35, 2.62), xytext=(0.05, 4.65), fontsize=10,
                arrowprops=dict(arrowstyle="->", color="0.3"))
    ax.annotate("S、R 都从 O 密度可达\n→ S 与 R 密度相连（对称）", xy=pts["R"],
                xytext=(4.6, 3.9), fontsize=10,
                arrowprops=dict(arrowstyle="->", color="0.3"))
    ax.set_title("密度可达与密度相达示意（$Eps$=1.0）", fontsize=12)
    ax.set_xlim(-0.5, 7.6); ax.set_ylim(0.2, 5.6)
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.set_aspect("equal")
    fig.tight_layout()
    save(fig, "fig4_12_dbscan_reachability.png")


# --------------------------------------------------------------- 图 4-13
def fig_kdistance():
    a = rng.normal([0, 0], 0.35, (70, 2))
    b = rng.normal([2.4, 1.6], 0.4, (70, 2))
    c = rng.normal([2.2, -1.4], 0.38, (70, 2))
    noise = np.array([[-1.6, 2.6], [4.3, 3.1], [-1.8, -2.2], [4.6, -2.8], [1.2, 3.4]])
    X = np.vstack([a, b, c, noise])
    k = 5  # 第 5 近邻（含自身计 6）
    D = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
    kd = np.sort(D, axis=1)[:, k]
    kd_sorted = np.sort(kd)
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.8),
                             gridspec_kw={"width_ratios": [1, 1.15]})
    ax = axes[0]
    ax.scatter(X[:210, 0], X[:210, 1], s=12, color=C_BLUE, alpha=0.75)
    ax.scatter(noise[:, 0], noise[:, 1], s=34, marker="x", color=C_RED, linewidths=1.6)
    ax.set_title("含少量噪音点的数据集", fontsize=12)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    ax = axes[1]
    ax.plot(np.arange(1, len(X) + 1), kd_sorted, color=C_BLUE, lw=1.8)
    elbow_x = 205
    ax.axvline(elbow_x, color="0.6", ls=":")
    ax.axhline(kd_sorted[elbow_x - 1], color=C_RED, ls="--", lw=1.2)
    ax.annotate("拐点：噪音点的第 %d 近邻\n距离陡增 → 取此处距离\n作为 Eps 的初值" % k,
                xy=(elbow_x, kd_sorted[elbow_x - 1]), xytext=(120, 0.62),
                fontsize=10, color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED))
    ax.set_xlabel("样本点（按第 %d 近邻距离升序排列）" % k, fontsize=11)
    ax.set_ylabel("第 %d 近邻距离" % k, fontsize=11)
    ax.set_title("$k$ 距离图（k-distance plot）", fontsize=12)
    fig.tight_layout()
    save(fig, "fig4_13_kdistance.png")


# --------------------------------------------------------------- 图 4-14
def fig_silhouette():
    a = rng.normal([0, 0], 0.32, (30, 2))
    b = rng.normal([2.2, 1.5], 0.34, (30, 2))
    c = rng.normal([2.0, -1.6], 0.34, (30, 2))
    X = np.vstack([a, b, c])
    labels, centers, _ = kmeans_fit(X, 3, init=np.array([[0, 0], [2.2, 1.5], [2.0, -1.6]]))
    s = silhouette_values(X, labels)
    fig = plt.figure(figsize=(10.4, 4.0))
    ax1 = fig.add_subplot(1, 2, 1)
    cols = [C_BLUE, C_ORANGE, C_GREEN]
    # 目标点 i
    i = 5
    ax1.scatter(X[labels == 0, 0], X[labels == 0, 1], s=18, color=C_BLUE, alpha=0.8)
    ax1.scatter(X[labels == 1, 0], X[labels == 1, 1], s=18, color=C_ORANGE, alpha=0.8)
    ax1.scatter(X[labels == 2, 0], X[labels == 2, 1], s=18, color=C_GREEN, alpha=0.8)
    ax1.plot(X[i, 0], X[i, 1], "o", ms=13, mfc="none", mec=C_RED, mew=2)
    ax1.text(X[i, 0] + 0.1, X[i, 1] + 0.1, "$i$", fontsize=13, color=C_RED)
    same = np.where((labels == labels[i]) & (np.arange(len(X)) != i))[0]
    for j in same:
        ax1.plot([X[i, 0], X[j, 0]], [X[i, 1], X[j, 1]], color=C_BLUE, lw=0.7, alpha=0.6)
    nearest = np.unique(labels)[np.unique(labels) != labels[i]][0]
    for j in np.where(labels == nearest)[0]:
        ax1.plot([X[i, 0], X[j, 0]], [X[i, 1], X[j, 1]], color=C_ORANGE, lw=0.7,
                 alpha=0.5, ls="--")
    ax1.text(-0.1, -1.35, "实线：到同类各点的距离 → 平均为 $a(i)$\n"
             "虚线：到最近的其他类各点的距离 → 平均为 $b(i)$", fontsize=10, color="0.25")
    ax1.set_title("单点轮廓值的 $a(i)$ 与 $b(i)$", fontsize=12)
    ax1.set_xticks([]); ax1.set_yticks([])
    ax1.set_aspect("equal")

    ax2 = fig.add_subplot(1, 2, 2)
    order = np.argsort(-s)
    y = np.arange(len(X))
    ax2.barh(y, s[order], color=[cols[labels[j]] for j in order], height=0.75)
    ax2.axvline(s.mean(), color=C_RED, ls="--", lw=1.3)
    ax2.text(s.mean() + 0.02, 2, "平均轮廓值 = %.2f" % s.mean(), fontsize=10,
             color=C_RED, rotation=90, va="bottom")
    ax2.axvline(0, color="0.3", lw=0.8)
    ax2.set_ylim(-1, len(X))
    ax2.set_yticks([])
    ax2.set_xlabel("轮廓值 $S(i)$，越接近 1 越合理", fontsize=11)
    ax2.set_title("轮廓图（按类着色）", fontsize=12)
    fig.tight_layout()
    save(fig, "fig4_14_silhouette.png")


# --------------------------------------------------------------- 图 4-15
def fig_sse_elbow():
    a = rng.normal([0, 0], 0.4, (60, 2))
    b = rng.normal([2.6, 1.8], 0.42, (60, 2))
    c = rng.normal([2.4, -1.8], 0.42, (60, 2))
    X = np.vstack([a, b, c])
    ks = range(1, 9)
    sse = []
    for k in ks:
        if k == 1:
            sse.append(((X - X.mean(axis=0)) ** 2).sum())
        else:
            lb, ct, _ = kmeans_fit(X, k)
            sse.append(sse_of(X, lb, ct))
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    ax.plot(list(ks), sse, "o-", color=C_BLUE, lw=1.8, ms=6)
    ax.scatter([3], [sse[2]], s=170, facecolor="none", edgecolor=C_RED, lw=2.2, zorder=5)
    ax.annotate("“肘部”：K=3 之后 SSE 下降\n明显变缓 → 取 K=3",
                xy=(3, sse[2]), xytext=(4.0, sse[1] * 0.75), fontsize=11, color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED))
    ax.set_xlabel("类别数 $K$", fontsize=12)
    ax.set_ylabel("簇内误差平方和 SSE", fontsize=12)
    ax.set_title("SSE 随 K 的变化与“肘部法”", fontsize=12)
    ax.set_xticks(list(ks))
    fig.tight_layout()
    save(fig, "fig4_15_sse_elbow.png")


# --------------------------------------------------------------- 图 4-16
FUKUOKA_CITIES = ["福冈", "合肥", "武汉", "长沙", "桂林", "温州", "成都"]
# 指标：年平均气温(℃)、年降水量(mm)、年日照时数(h)、极端最低气温(℃)、1月平均气温(℃)
FUKUOKA_DATA = np.array([
    [16.2, 1492, 2000, -8.2, 6.2],   # 福冈（据课件）
    [15.7, 970, 2209, -20.6, 1.9],   # 合肥（据课件）
    [16.9, 1250, 1950, -18.1, 3.9],  # 武汉（示例值）
    [17.2, 1400, 1650, -11.5, 4.8],  # 长沙（示例值）
    [18.9, 1900, 1550, -4.9, 8.0],   # 桂林（示例值）
    [17.9, 1720, 1750, -4.5, 7.7],   # 温州（示例值）
    [16.3, 976, 1239, -4.6, 5.6]])   # 成都（据课件）


def _seuclidean_dists(X):
    sd = X.std(axis=0, ddof=1)
    Z = X / sd
    return np.linalg.norm(Z[:, None, :] - Z[None, :, :], axis=2)


def fig_case_fukuoka():
    X = FUKUOKA_DATA
    n = len(X)
    D = _seuclidean_dists(X)
    merges = agglomerative(D, "average")
    order_d = D[0, 1:]
    names = FUKUOKA_CITIES
    order = np.argsort(order_d)          # 与福冈距离升序：长沙最近
    vals = np.sqrt(order_d)[order]

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.1),
                             gridspec_kw={"width_ratios": [1.3, 1]})
    ax = axes[0]
    cutlab = cut_k(merges, n, 4)
    cmap = [C_BLUE, C_ORANGE, C_GREEN, C_PURPLE]
    leafcolor = [cmap[cutlab[i]] for i in range(n)]
    draw_dendrogram(merges, n, names, ax, cut=1.8, colors=leafcolor, leaf_font=10.5)
    ax.set_ylabel("组间平均法 + 标准欧氏距离\n合并高度（标准化距离）", fontsize=10)
    ax.set_title("引种案例的层次聚类谱系图", fontsize=12)

    ax = axes[1]
    ypos = np.arange(len(order))
    cols = [cmap[cutlab[i + 1]] for i in order]
    ax.barh(ypos, vals, color=cols, height=0.6)
    ax.set_yticks(ypos)
    ax.set_yticklabels([names[i + 1] for i in order], fontsize=11)
    ax.invert_yaxis()                    # 最近的城市排在最上方
    ax.axvline(vals[0], color=C_RED, ls="--", lw=1.2)
    ax.text(vals[0] + 0.04, 0.06, "最近：%s（%.2f）" % (names[order[0] + 1], vals[0]),
            fontsize=10, color=C_RED, va="center")
    ax.set_xlabel("与福冈的标准欧氏距离", fontsize=11)
    ax.set_title("各候选城市与福冈的距离", fontsize=12)
    ax.set_xlim(0, vals[-1] * 1.3)
    fig.tight_layout()
    save(fig, "fig4_16_case_fukuoka.png")
    print("fukuoka nearest:", [names[i + 1] for i in order][:3],
          "dists:", np.round(vals[:3], 3))


# --------------------------------------------------------------- 图 4-17
IRIS_STATS = [  # (萼片长, 萼片宽, 花瓣长, 花瓣宽) 各品种均值与标准差
    ([5.01, 3.42, 1.46, 0.246], [0.352, 0.379, 0.174, 0.105]),   # setosa
    ([5.94, 2.77, 4.26, 1.326], [0.516, 0.314, 0.470, 0.198]),   # versicolor
    ([6.59, 2.97, 5.55, 2.026], [0.636, 0.322, 0.552, 0.275])]    # virginica


def fig_case_iris():
    np.random.seed(7)
    Xs, ys = [], []
    for c, (mu, sd) in enumerate(IRIS_STATS):
        Xs.append(np.random.normal(mu, sd, (50, 4)))
        ys += [c] * 50
    X = np.vstack(Xs)
    y = np.array(ys)
    # 用花瓣长（第3列）、花瓣宽（第4列）作图；聚类用全部 4 个属性
    labels, centers, _ = kmeans_fit(X, 3, init=np.array(IRIS_STATS)[:, 0, :])
    # 类号与品种对齐（以中心最匹配者计）
    perm = {}
    for c in range(3):
        j = np.argmin(np.linalg.norm(centers - np.array(IRIS_STATS)[c, 0], axis=1))
        perm[j] = c
    mapped = np.array([perm[l] for l in labels])
    acc = (mapped == y).mean()
    cols = [C_BLUE, C_ORANGE, C_GREEN]
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.1))
    for c in range(3):
        axes[0].scatter(X[mapped == c, 2], X[mapped == c, 3], s=15, color=cols[c],
                        alpha=0.8)
    axes[0].scatter(centers[:, 2], centers[:, 3], marker="*", s=240, color=C_RED,
                    edgecolor="white", zorder=5, label="类中心")
    axes[0].legend(loc="upper left", fontsize=9, frameon=False)
    axes[0].set_title("K-均值聚类结果（k=3，与真实品种一致率 %.0f%%）" % (acc * 100),
                      fontsize=11.5)
    for c in range(3):
        axes[1].scatter(X[y == c, 2], X[y == c, 3], s=15, color=cols[c], alpha=0.8)
    axes[1].set_title("真实品种（山鸢尾 / 变色鸢尾 / 维吉尼亚鸢尾）", fontsize=11.5)
    for ax in axes:
        ax.set_xlabel("花瓣长度 (cm)", fontsize=11)
        ax.set_ylabel("花瓣宽度 (cm)", fontsize=11)
    fig.tight_layout()
    save(fig, "fig4_17_case_iris.png")
    print("iris agreement: %.3f" % acc)


if __name__ == "__main__":
    fig_ambiguous_clusters()
    fig_hierarchical_demo()
    fig_gmm_soft()
    fig_methods_comparison()
    fig_linkage_strategies()
    fig_variable_angle()
    fig_point_distances()
    fig_class_distances()
    fig_kmeans_steps()
    fig_kmeans_1d()
    fig_dbscan_points()
    fig_dbscan_reachability()
    fig_kdistance()
    fig_silhouette()
    fig_sse_elbow()
    fig_case_fukuoka()
    fig_case_iris()
    print("ALL DONE")
