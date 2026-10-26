# -*- coding: utf-8 -*-
"""第10章 支持向量机 插图生成脚本
运行：uv run --no-project --with matplotlib --with numpy python gen_figures.py
输出：书稿/figs/ch10/fig10_*.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "书稿", "figs", "ch10")
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


# ---------------------------------------------------------------- SVM 训练器
def _kernel_matrix(X, kernel, gamma=1.0, degree=3, coef0=1.0):
    if kernel == "linear":
        return X @ X.T
    if kernel == "rbf":
        sq = np.sum(X ** 2, axis=1)
        d2 = sq[:, None] + sq[None, :] - 2.0 * (X @ X.T)
        np.maximum(d2, 0, out=d2)
        return np.exp(-gamma * d2)
    if kernel == "poly":
        return (gamma * (X @ X.T) + coef0) ** degree
    raise ValueError(kernel)


def smo_train(X, y, C, kernel="linear", tol=1e-3, max_passes=30, **kw):
    """简化 SMO 求解软间隔 SVM 对偶问题，返回 (alpha, b)。"""
    m = len(y)
    K = _kernel_matrix(X, kernel, **kw)
    alpha = np.zeros(m)
    b = 0.0
    passes = 0
    while passes < max_passes:
        num_changed = 0
        for i in range(m):
            Ei = (alpha * y) @ K[:, i] + b - y[i]
            if (y[i] * Ei < -tol and alpha[i] < C) or (y[i] * Ei > tol and alpha[i] > 0):
                j = (i + 1 + int(rng.integers(m - 1))) % m
                Ej = (alpha * y) @ K[:, j] + b - y[j]
                ai_old, aj_old = alpha[i], alpha[j]
                if y[i] != y[j]:
                    L, H = max(0.0, aj_old - ai_old), min(C, C + aj_old - ai_old)
                else:
                    L, H = max(0.0, ai_old + aj_old - C), min(C, ai_old + aj_old)
                if H - L < 1e-12:
                    continue
                eta = 2.0 * K[i, j] - K[i, i] - K[j, j]
                if eta >= -1e-12:
                    continue
                alpha[j] = aj_old - y[j] * (Ei - Ej) / eta
                alpha[j] = min(H, max(L, alpha[j]))
                if abs(alpha[j] - aj_old) < 1e-5:
                    continue
                alpha[i] = ai_old + y[i] * y[j] * (aj_old - alpha[j])
                b1 = (b - Ei - y[i] * (alpha[i] - ai_old) * K[i, i]
                      - y[j] * (alpha[j] - aj_old) * K[i, j])
                b2 = (b - Ej - y[i] * (alpha[i] - ai_old) * K[i, j]
                      - y[j] * (alpha[j] - aj_old) * K[j, j])
                if 0 < alpha[i] < C:
                    b = b1
                elif 0 < alpha[j] < C:
                    b = b2
                else:
                    b = 0.5 * (b1 + b2)
                num_changed += 1
        passes = passes + 1 if num_changed == 0 else 0
    return alpha, b


def svm_decision(Xs, ys, alpha, b, XX, YY, kernel="linear", **kw):
    """在网格 (XX,YY) 上计算决策函数值。"""
    G = np.stack([XX.ravel(), YY.ravel()], axis=1)
    K = _kernel_matrix_pair(Xs, G, kernel, **kw)
    f = K.T @ (alpha * ys) + b
    return f.reshape(XX.shape)


def _kernel_matrix_pair(A, B, kernel, gamma=1.0, degree=3, coef0=1.0):
    if kernel == "linear":
        return A @ B.T
    if kernel == "rbf":
        sa = np.sum(A ** 2, axis=1)[:, None]
        sb = np.sum(B ** 2, axis=1)[None, :]
        d2 = sa + sb - 2.0 * (A @ B.T)
        np.maximum(d2, 0, out=d2)
        return np.exp(-gamma * d2)
    if kernel == "poly":
        return (gamma * (A @ B.T) + coef0) ** degree
    raise ValueError(kernel)


def plot_svm(ax, X, y, alpha, b, kernel="linear", lw_boundary=1.8, **kw):
    """在已有散点的 ax 上补画决策边界(0)与间隔边界(+/-1)。"""
    x1min, x1max = ax.get_xlim()
    x2min, x2max = ax.get_ylim()
    g1 = np.linspace(x1min, x1max, 220)
    g2 = np.linspace(x2min, x2max, 220)
    XX, YY = np.meshgrid(g1, g2)
    F = svm_decision(X, y, alpha, b, XX, YY, kernel, **kw)
    ax.contour(XX, YY, F, levels=[-1.0, 0.0, 1.0],
               colors=[C_GRAY, C_RED, C_GRAY],
               linestyles=["--", "-", "--"], linewidths=[0.9, lw_boundary, 0.9])


# ---------------------------------------------------------------- 图 10-01
def fig01_margin_idea():
    """两条候选分割线对比：考虑误差与新样本后大间隔更稳。"""
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    n = 22
    a = rng.standard_normal((n, 2)) * 0.55 + np.array([0.0, 0.0])
    bb = rng.standard_normal((n, 2)) * 0.55 + np.array([2.6, 2.0])
    ax.scatter(a[:, 0], a[:, 1], marker="o", s=42, c=C_BLUE,
               edgecolors="white", linewidths=0.6, label="负类样本", zorder=3)
    ax.scatter(bb[:, 0], bb[:, 1], marker="s", s=40, c=C_ORANGE,
               edgecolors="white", linewidths=0.6, label="正类样本", zorder=3)
    x = np.linspace(-2.6, 5.0, 50)
    # 贴近负类的“差”分割线 A：从点 (0.9,-1.2) 附近擦过
    a1 = np.array([-2.6, 1.05 + (-2.6) * 0.15])
    a2 = np.array([5.0, 1.05 + 5.0 * 0.15])
    ax.plot(x, 1.05 + 0.15 * x, color=C_GREEN, lw=1.8, zorder=2)
    ax.annotate("分割线 A（间隔小）", xy=(3.4, 1.56), xytext=(1.4, 2.9),
                fontsize=10, color=C_GREEN,
                arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1.0))
    # 大间隔分割线 B：两类中线方向
    ax.plot(x, 0.62 + 0.86 * x, color=C_PURPLE, lw=1.8, zorder=2)
    ax.annotate("分割线 B（间隔大）", xy=(-1.7, -0.85), xytext=(-2.5, -1.9),
                fontsize=10, color=C_PURPLE,
                arrowprops=dict(arrowstyle="->", color=C_PURPLE, lw=1.0))
    # 新样本：落在 A 的负侧（错分）但 B 的正侧
    new = np.array([2.1, 1.95])
    ax.scatter([new[0]], [new[1]], marker="*", s=230, c=C_RED,
               edgecolors="white", linewidths=0.6, zorder=5)
    ax.annotate("新来的正类样本", xy=new, xytext=(2.5, 3.3), fontsize=10,
                color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.0))
    # 扰动箭头：受测量误差影响的样本漂移
    p0 = a[3] if a[3][0] < 0.8 else a[5]
    ax.annotate("", xy=(p0[0] + 0.55, p0[1] + 0.55), xytext=(p0[0], p0[1]),
                arrowprops=dict(arrowstyle="->", color=C_GRAY, lw=1.2))
    ax.text(p0[0] + 0.62, p0[1] + 0.5, "测量误差\n使样本漂移", fontsize=9,
            color=C_GRAY, ha="left", va="center")
    ax.set_xlim(-2.6, 5.2)
    ax.set_ylim(-2.2, 3.8)
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    save(fig, "fig10_01_margin_idea.png")


# ---------------------------------------------------------------- 图 10-02
def fig02_margin_geometry():
    """最大间隔超平面几何：w^T x + b = 0、±1 边界、间隔 2/||w||、支持向量。"""
    fig, ax = plt.subplots(figsize=(6.6, 5.2))
    wvec = np.array([1.2, 1.0])
    # 负类（w·x <= -1）
    xa = np.array([[-2.5, -1.5], [-1.8, -0.9], [-0.9, -2.0], [0.2, -2.6],
                   [-3.0, 0.2], [-1.5, -1.2], [0.6, -1.72], [-1.0, 0.2]])
    # 正类（w·x >= +1）
    xb = np.array([[2.2, 1.0], [1.4, 0.8], [2.6, 0.2], [0.8, 1.6],
                   [1.9, 1.8], [2.9, 1.4], [0.4, 0.52]])
    sv = [6, 7, 13]  # xa[6], xa[7], xb[6] 落在间隔边界上
    xs = np.linspace(-3.4, 3.2, 40)
    ax.plot(xs, -1.2 * xs, color=C_RED, lw=2.0, zorder=2)
    ax.plot(xs, -1.2 * xs + 1.0, color=C_GRAY, lw=1.1, ls="--", zorder=2)
    ax.plot(xs, -1.2 * xs - 1.0, color=C_GRAY, lw=1.1, ls="--", zorder=2)
    ax.scatter(xa[:, 0], xa[:, 1], marker="o", s=42, c=C_BLUE,
               edgecolors="white", linewidths=0.6, label="负类（$y_i=-1$）", zorder=3)
    ax.scatter(xb[:, 0], xb[:, 1], marker="s", s=40, c=C_ORANGE,
               edgecolors="white", linewidths=0.6, label="正类（$y_i=+1$）", zorder=3)
    X = np.vstack([xa, xb])
    ax.scatter(X[sv, 0], X[sv, 1], s=200, facecolors="none",
               edgecolors=C_RED, linewidths=1.6, zorder=4)
    # 间隔 gamma 双箭头（x=0 处：边界 y=±1）
    ax.annotate("", xy=(0.0, 1.0), xytext=(0.0, -1.0),
                arrowprops=dict(arrowstyle="<->", color=C_RED, lw=1.6))
    ax.text(0.14, 0.0, r"间隔 $\gamma=\dfrac{2}{\left\| \omega \right\|}$",
            fontsize=12.5, color=C_RED, va="center")
    # 支持向量到决策边界的垂距 r
    p = np.array([0.6, -1.72])          # 负类支持向量
    foot = p + wvec * 0.64              # 垂足
    ax.annotate("", xy=foot, xytext=p,
                arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1.4, ls="-"))
    ax.text(0.72, -1.18, r"$r=\dfrac{\left| \omega^{T}x+b \right|}{\left\| \omega \right\|}=\dfrac{1}{\left\| \omega \right\|}$",
            fontsize=10.5, color=C_GREEN)
    ax.text(-3.25, 2.85, r"决策边界：$\omega^{T}x+b=0$", fontsize=11, color=C_RED)
    ax.text(-3.25, 2.52, r"间隔边界：$\omega^{T}x+b=\pm 1$", fontsize=11, color=C_GRAY)
    ax.annotate("支持向量", xy=(0.4, 0.52), xytext=(-3.3, -2.5),
                fontsize=10, color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.0))
    ax.set_xlim(-3.4, 3.3)
    ax.set_ylim(-3.0, 3.1)
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    save(fig, "fig10_02_margin_geometry.png")


# ---------------------------------------------------------------- 图 10-03
def fig03_normalization():
    """标准化的重要性：量纲悬殊时未标准化边界失真。"""
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.2))
    n = 40
    x1 = rng.standard_normal(n) * 18 + 60          # 高程: 数百米量级
    x2 = rng.standard_normal(n) * 0.06 + 0.55      # 坡度: 零点几量级
    lab = (x1 / 25.0 + x2 * 8.0 + rng.standard_normal(n) * 0.4 > 6.8).astype(float)
    lab[lab == 0] = -1
    X = np.stack([x1, x2], axis=1)
    for ax, Xd, title in [(axes[0], X, "未标准化：边界被大量纲特征“压扁”"),
                          (axes[1], (X - X.mean(0)) / X.std(0), "标准化后：边界正常")]:
        alpha, b = smo_train(Xd, lab, C=50, kernel="linear")
        ax.scatter(Xd[lab == -1, 0], Xd[lab == -1, 1], marker="o", s=30, c=C_BLUE,
                   edgecolors="white", linewidths=0.5, label="负类", zorder=3)
        ax.scatter(Xd[lab == 1, 0], Xd[lab == 1, 1], marker="s", s=28, c=C_ORANGE,
                   edgecolors="white", linewidths=0.5, label="正类", zorder=3)
        ax.set_xlim(Xd[:, 0].min() - 0.3 * np.ptp(Xd[:, 0]), Xd[:, 0].max() + 0.3 * np.ptp(Xd[:, 0]))
        ax.set_ylim(Xd[:, 1].min() - 0.4 * np.ptp(Xd[:, 1]), Xd[:, 1].max() + 0.4 * np.ptp(Xd[:, 1]))
        plot_svm(ax, Xd, lab, alpha, b, kernel="linear")
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("特征 1（标准化前量级为 $10^2$）" if ax is axes[0] else "特征 1（标准化后）")
        ax.set_ylabel("特征 2（量级为 $10^{-1}$）" if ax is axes[0] else "特征 2（标准化后）")
    axes[0].legend(loc="lower right", frameon=False, fontsize=9)
    save(fig, "fig10_03_normalization.png")


# ---------------------------------------------------------------- 图 10-04
def fig04_hyperplane_dims():
    """1/2/3 维空间中的超平面：点、线、面（维数 = 空间维数 - 1）。"""
    fig = plt.figure(figsize=(9.6, 3.4))
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.scatter(rng.standard_normal(6) * 0.3 - 1.6, np.zeros(6), s=40, c=C_BLUE, zorder=3)
    ax1.scatter(rng.standard_normal(6) * 0.3 + 1.6, np.zeros(6), s=40, c=C_ORANGE, zorder=3)
    ax1.axvline(0, color=C_RED, lw=2)
    ax1.set_yticks([])
    ax1.set_xlim(-2.6, 2.6)
    ax1.set_ylim(-0.6, 0.9)
    ax1.set_title("一维：超平面是一个点", fontsize=11)
    ax1.set_xlabel("$x_1$")
    ax2 = fig.add_subplot(1, 3, 2)
    n = 14
    a = rng.standard_normal((n, 2)) * 0.42 + np.array([-1.1, -0.9])
    bb = rng.standard_normal((n, 2)) * 0.42 + np.array([1.1, 0.9])
    ax2.scatter(a[:, 0], a[:, 1], s=30, c=C_BLUE, zorder=3)
    ax2.scatter(bb[:, 0], bb[:, 1], s=30, c=C_ORANGE, zorder=3)
    xs = np.linspace(-2.4, 2.4, 10)
    ax2.plot(xs, -0.8 * xs + 0.02, color=C_RED, lw=2)
    ax2.set_xlim(-2.6, 2.6)
    ax2.set_ylim(-2.2, 2.2)
    ax2.set_title("二维：超平面是一条直线", fontsize=11)
    ax2.set_xlabel("$x_1$")
    ax2.set_ylabel("$x_2$")
    ax3 = fig.add_subplot(1, 3, 3, projection="3d")
    m = 26
    aa = rng.standard_normal((m, 3)) * 0.34 + np.array([-1.0, -1.0, -1.0])
    cc = rng.standard_normal((m, 3)) * 0.34 + np.array([1.0, 1.0, 1.0])
    ax3.scatter(aa[:, 0], aa[:, 1], aa[:, 2], s=22, c=C_BLUE)
    ax3.scatter(cc[:, 0], cc[:, 1], cc[:, 2], s=22, c=C_ORANGE)
    g1, g2 = np.meshgrid(np.linspace(-2.0, 2.0, 8), np.linspace(-2.0, 2.0, 8))
    ax3.plot_surface(g1, g2, -g1 - g2 + 0.05, color=C_RED, alpha=0.42,
                     edgecolor=C_RED, lw=0.4)
    ax3.set_title("三维：超平面是一个平面", fontsize=11)
    ax3.set_xlabel("$x_1$")
    ax3.set_ylabel("$x_2$")
    ax3.set_zlabel("$x_3$")
    ax3.view_init(elev=16, azim=-58)
    save(fig, "fig10_04_hyperplane_dims.png")


# ---------------------------------------------------------------- 图 10-05
def fig05_kernel_mapping():
    """高维映射：二维线性不可分 → 映射 z=x1^2+x2^2 后线性可分。"""
    fig = plt.figure(figsize=(9.8, 4.4))
    ax1 = fig.add_subplot(1, 2, 1)
    n1, n2 = 45, 60
    th1 = rng.uniform(0, 2 * np.pi, n1)
    r1 = rng.uniform(0.05, 0.55, n1)
    th2 = rng.uniform(0, 2 * np.pi, n2)
    r2 = rng.uniform(1.25, 1.85, n2)
    xi = np.stack([r1 * np.cos(th1), r1 * np.sin(th1)], axis=1)
    xo = np.stack([r2 * np.cos(th2), r2 * np.sin(th2)], axis=1)
    ax1.scatter(xi[:, 0], xi[:, 1], s=26, c=C_BLUE, label="正类（内圈）", zorder=3)
    ax1.scatter(xo[:, 0], xo[:, 1], s=26, c=C_ORANGE, label="负类（外圈）", zorder=3)
    ax1.set_xlim(-2.4, 2.4)
    ax1.set_ylim(-2.2, 2.2)
    ax1.set_title("原始二维空间：线性不可分", fontsize=11)
    ax1.set_xlabel("$x_1$")
    ax1.set_ylabel("$x_2$")
    ax1.legend(loc="upper right", frameon=False, fontsize=9)
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    zi = np.sum(xi ** 2, axis=1)
    zo = np.sum(xo ** 2, axis=1)
    ax2.scatter(xi[:, 0], xi[:, 1], zi, s=22, c=C_BLUE)
    ax2.scatter(xo[:, 0], xo[:, 1], zo, s=22, c=C_ORANGE)
    g1, g2 = np.meshgrid(np.linspace(-2.0, 2.0, 10), np.linspace(-2.0, 2.0, 10))
    ax2.plot_surface(g1, g2, np.full_like(g1, 0.95), color=C_RED, alpha=0.35,
                     edgecolor=C_RED, lw=0.4)
    ax2.set_title(r"映射 $z=x_1^{2}+x_2^{2}$ 后：一个平面即可分开", fontsize=11)
    ax2.set_xlabel("$x_1$")
    ax2.set_ylabel("$x_2$")
    ax2.set_zlabel(r"$z=\phi(x)$")
    ax2.view_init(elev=15, azim=-60)
    save(fig, "fig10_05_kernel_mapping.png")


# ---------------------------------------------------------------- 图 10-06
def _moon(n, r, w, off, sign):
    t = rng.uniform(0, np.pi, n)
    x = r * np.cos(t) + off[0]
    y = sign * r * np.sin(t) + off[1] + sign * w * 0.0
    return np.stack([x, y], axis=1) + rng.standard_normal((n, 2)) * 0.12


def fig06_kernels_classification():
    """不同核函数的分类决策边界。"""
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.6))
    top = _moon(45, 1.0, 0.0, np.array([0.0, 0.35]), 1)
    bot = _moon(45, 1.0, 0.0, np.array([1.0, -0.35]), -1)
    X = np.vstack([top, bot])
    y = np.hstack([np.ones(45), -np.ones(45)])
    mu, sd = X.mean(0), X.std(0)
    Xs = (X - mu) / sd
    cfgs = [("linear", "线性核", dict()),
            ("poly", "多项式核（$d=3$）", dict(degree=3, gamma=1.0, coef0=1.0)),
            ("rbf", "高斯核（RBF）", dict(gamma=1.6))]
    for ax, (ker, name, kw) in zip(axes, cfgs):
        alpha, b = smo_train(Xs, y, C=20, kernel=ker, **kw)
        ax.scatter(Xs[y == -1, 0], Xs[y == -1, 1], marker="o", s=24, c=C_BLUE,
                   edgecolors="white", linewidths=0.4, zorder=3)
        ax.scatter(Xs[y == 1, 0], Xs[y == 1, 1], marker="s", s=22, c=C_ORANGE,
                   edgecolors="white", linewidths=0.4, zorder=3)
        ax.set_xlim(-2.1, 2.1)
        ax.set_ylim(-1.9, 1.9)
        plot_svm(ax, Xs, y, alpha, b, kernel=ker, **kw)
        sv = alpha > 1e-3
        ax.scatter(Xs[sv, 0], Xs[sv, 1], s=110, facecolors="none",
                   edgecolors=C_RED, linewidths=1.1, zorder=4)
        acc = np.mean(np.sign((alpha * y) @ _kernel_matrix_pair(Xs, Xs, ker, **kw) + b) == y)
        ax.set_title(f"{name}（训练正确率 {acc:.0%}）", fontsize=11)
        ax.set_xlabel("$x_1$（标准化）")
    axes[0].set_ylabel("$x_2$（标准化）")
    save(fig, "fig10_06_kernels_classification.png")


# ---------------------------------------------------------------- 图 10-07
def _krr(X, y, lam, kernel, **kw):
    K = _kernel_matrix(X, kernel, **kw)
    a = np.linalg.solve(K + lam * np.eye(len(y)), y)
    return a


def fig07_svr_kernels():
    """不同核函数下的回归曲线（以核回归示意，SVR 形状类似）。"""
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.5))
    n = 46
    X = np.sort(rng.uniform(-3, 3, n))
    y = np.sin(0.9 * X) + 0.12 * rng.standard_normal(n)
    Xc = X[:, None]
    cfgs = [("linear", "线性核：只能给直线", dict()),
            ("poly", "多项式核（$d=3$）", dict(degree=3, gamma=0.5, coef0=1.0)),
            ("rbf", "高斯核（RBF）", dict(gamma=0.35))]
    xs = np.linspace(-3.3, 3.3, 240)[:, None]
    for ax, (ker, name, kw) in zip(axes, cfgs):
        a = _krr(Xc, y, lam=0.01, kernel=ker, **kw)
        f = _kernel_matrix_pair(Xc, xs, ker, **kw).T @ a
        ax.scatter(X, y, s=20, c=C_BLUE, edgecolors="white", linewidths=0.4,
                   zorder=3, label="样本")
        ax.plot(xs, f, color=C_RED, lw=2, zorder=4, label="回归曲线")
        ax.plot(xs, np.sin(0.9 * xs), color=C_GREEN, lw=1.1, ls=":", zorder=2,
                label="真实趋势")
        ax.set_ylim(-1.9, 1.9)
        ax.set_title(name, fontsize=11)
        ax.set_xlabel("$x$")
    axes[0].set_ylabel("$y$")
    axes[0].legend(loc="upper left", frameon=False, fontsize=9)
    save(fig, "fig10_07_svr_kernels.png")


MAIN = [fig01_margin_idea, fig02_margin_geometry, fig03_normalization,
        fig04_hyperplane_dims, fig05_kernel_mapping, fig06_kernels_classification,
        fig07_svr_kernels]


# ---------------------------------------------------------------- 图 10-08
def fig08_history():
    """SVM 发展史时间轴。"""
    fig, ax = plt.subplots(figsize=(9.6, 4.0))
    ax.axhline(0, color=C_GRAY, lw=2, zorder=1)
    events = [
        (1963, "Vapnik 与 Lerner 发表\n广义肖像算法研究", 1, C_BLUE),
        (1964, "Vapnik 与 Chervonenkis\n建立硬边距线性 SVM", -1, C_BLUE),
        (1975, "20 世纪 70—80 年代：\n最大边距理论、松弛变量规划、\nVC 维，统计学习理论成形", 1, C_GREEN),
        (1992, "Boser、Guyon 与 Vapnik\n用核方法得到非线性 SVM", -1, C_ORANGE),
        (1995, "Cortes 与 Vapnik 提出\n软边距非线性 SVM，\n用于手写字符识别", 1, C_RED),
    ]
    for yr, txt, side, col in events:
        ax.scatter([yr], [0], s=130, c=col, zorder=4, edgecolors="white", linewidths=1.2)
        ax.annotate(str(yr), xy=(yr, 0), xytext=(yr, -0.14 * side if side < 0 else 0.07),
                    ha="center", fontsize=12, fontweight="bold", color=col)
        ax.annotate(txt, xy=(yr, 0), xytext=(yr, 0.42 * side),
                    ha="center", fontsize=9.5, color="black",
                    arrowprops=dict(arrowstyle="-", color=col, lw=1.0))
    ax.set_xlim(1958, 2001)
    ax.set_ylim(-1.05, 1.05)
    ax.set_yticks([])
    ax.set_xticks([1960, 1970, 1980, 1990, 2000])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_title("SVM 发展史：从广义肖像算法到软边距非线性 SVM", fontsize=12)
    save(fig, "fig10_08_history.png")


# ---------------------------------------------------------------- 图 10-09
def fig09_convex_qp():
    """间隔最大化与凸二次目标：gamma=2/||w|| 关系 + 1/2||w||^2 抛物面。"""
    fig = plt.figure(figsize=(9.6, 3.9))
    ax1 = fig.add_subplot(1, 2, 1)
    wn = np.linspace(0.35, 4.0, 200)
    ax1.plot(wn, 2.0 / wn, color=C_BLUE, lw=2.2)
    ax1.scatter([1.0], [2.0], s=70, c=C_RED, zorder=4)
    ax1.annotate(r"$\left\| \omega \right\|=1,\ \gamma=2$", xy=(1.0, 2.0),
                 xytext=(1.7, 3.2), fontsize=11,
                 arrowprops=dict(arrowstyle="->", color=C_GRAY))
    ax1.set_xlabel(r"法向量模 $\left\| \omega \right\|$")
    ax1.set_ylabel(r"间隔 $\gamma=2/\left\| \omega \right\|$")
    ax1.set_title(r"$\left\| \omega \right\|$ 越小，间隔越大", fontsize=11)
    ax1.set_ylim(0, 5.6)
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    g1, g2 = np.meshgrid(np.linspace(-2.2, 2.2, 40), np.linspace(-2.2, 2.2, 40))
    Z = 0.5 * (g1 ** 2 + g2 ** 2)
    ax2.plot_surface(g1, g2, Z, cmap="viridis", alpha=0.85,
                     rstride=1, cstride=1, linewidth=0)
    ax2.set_xlabel(r"$\omega_1$")
    ax2.set_ylabel(r"$\omega_2$")
    ax2.set_zlabel(r"$\frac{1}{2}\left\| \omega \right\|^{2}$")
    ax2.set_title("凸二次目标：碗状曲面，最小值唯一", fontsize=11)
    ax2.view_init(elev=22, azim=-58)
    save(fig, "fig10_09_convex_qp.png")


# ---------------------------------------------------------------- 图 10-10
def fig10_soft_margin():
    """软间隔：松弛变量 xi 允许少数样本违反间隔约束。"""
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.2))
    n = 26
    a = rng.standard_normal((n, 2)) * 0.62 + np.array([-1.4, -0.9])
    bb = rng.standard_normal((n, 2)) * 0.62 + np.array([1.4, 0.9])
    # 人为加入交叉点
    a = np.vstack([a, [[0.9, 0.75], [0.35, 1.15]]])
    bb = np.vstack([bb, [[-0.7, -1.2]]])
    X = np.vstack([a, bb])
    y = np.hstack([-np.ones(len(a)), np.ones(len(bb))])
    mu, sd = X.mean(0), X.std(0)
    Xs = (X - mu) / sd
    ys = y
    for ax, C, title in [(axes[0], 1e5, "硬间隔（C 极大）：强行可分，边界被个别点带偏"),
                         (axes[1], 1.0, "软间隔（C 适中）：容忍少数点越界，边界更稳")]:
        alpha, b = smo_train(Xs, ys, C=C, kernel="linear")
        ax.scatter(Xs[ys == -1, 0], Xs[ys == -1, 1], marker="o", s=32, c=C_BLUE,
                   edgecolors="white", linewidths=0.5, label="负类", zorder=3)
        ax.scatter(Xs[ys == 1, 0], Xs[ys == 1, 1], marker="s", s=30, c=C_ORANGE,
                   edgecolors="white", linewidths=0.5, label="正类", zorder=3)
        ax.set_xlim(-3.0, 3.0)
        ax.set_ylim(-2.8, 2.8)
        plot_svm(ax, Xs, ys, alpha, b, kernel="linear")
        sv = alpha > 1e-4
        ax.scatter(Xs[sv, 0], Xs[sv, 1], s=150, facecolors="none",
                   edgecolors=C_RED, linewidths=1.3, zorder=4)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("$x_1$（标准化）")
    axes[0].set_ylabel("$x_2$（标准化）")
    axes[0].legend(loc="lower right", frameon=False, fontsize=9)
    # 右图标出 xi
    ax = axes[1]
    xline = 0.15
    wv = (alpha * ys) @ Xs
    yu = (1.0 - wv[0] * xline - b) / wv[1]
    y0 = (-wv[0] * xline - b) / wv[1]
    yd = (-1.0 - wv[0] * xline - b) / wv[1]
    ax.annotate("", xy=(xline, yu), xytext=(xline, y0),
                arrowprops=dict(arrowstyle="-", color=C_RED, lw=1.4, ls=":"))
    ax.text(xline + 0.08, 0.5 * (yu + y0), r"$\xi_{i}$", fontsize=12, color=C_RED)
    ax.text(xline + 0.08, 0.5 * (y0 + yd), r"$\xi_{k}$", fontsize=12, color=C_RED)
    ax.annotate("越界点：以 $\\xi$ 计松弛量，\n由超参数 $C$ 控制惩罚",
                xy=(-1.05, -0.75), xytext=(-2.95, 1.5), fontsize=10, color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.0))
    save(fig, "fig10_11_soft_margin.png")


# ---------------------------------------------------------------- 图 10-11
def fig11_kernel_functions():
    """常用核函数曲线（固定 x'，观察 K 随 x 的变化）。"""
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    x = np.linspace(-3, 3, 400)
    x0 = 0.5
    ax.plot(x, x * x0, color=C_BLUE, lw=2, label=r"线性核：$K=x_i^{T}x_j$")
    ax.plot(x, (x * x0 + 1.0) ** 3, color=C_ORANGE, lw=2,
            label=r"多项式核：$K=(x_i^{T}x_j+1)^{3}$")
    ax.plot(x, np.exp(-(x - x0) ** 2), color=C_RED, lw=2,
            label=r"高斯核：$K=\exp(-\left\| x_i-x_j \right\|^{2})$")
    ax.plot(x, np.exp(-np.abs(x - x0)), color=C_GREEN, lw=2, ls="--",
            label=r"拉普拉斯核：$K=\exp(-\left\| x_i-x_j \right\|)$")
    ax.plot(x, np.tanh(x * x0), color=C_PURPLE, lw=2, ls="-.",
            label=r"Sigmoid 核：$K=\tanh(x_i^{T}x_j)$")
    ax.axvline(x0, color=C_GRAY, lw=0.8, ls=":")
    ax.text(x0 + 0.05, -1.72, r"固定 $x_j=0.5$", fontsize=9, color=C_GRAY)
    ax.set_xlabel("$x_i$")
    ax.set_ylabel("$K(x_i,\\ x_j)$")
    ax.set_ylim(-2.0, 4.6)
    ax.set_title("常用核函数的形状（一维示意）", fontsize=12)
    ax.legend(loc="upper left", frameon=False, fontsize=9.5)
    save(fig, "fig10_10_kernel_functions.png")


# ---------------------------------------------------------------- 图 10-12
def fig12_svr_epsilon():
    """SVR 的 epsilon 间隔带与 epsilon-不敏感损失。"""
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.2))
    # 左：epsilon 带示意
    ax = axes[0]
    n = 40
    X = np.sort(rng.uniform(-2.6, 2.6, n))
    yf = 0.55 * np.sin(1.1 * X)
    yobs = yf + 0.22 * rng.standard_normal(n)
    a = _krr(X[:, None], yf, lam=0.01, kernel="rbf", gamma=1.2)
    xs = np.linspace(-3.0, 3.0, 240)[:, None]
    f = _kernel_matrix_pair(X[:, None], xs, "rbf", gamma=1.2).T @ a
    eps = 0.25
    ax.fill_between(xs.ravel(), f - eps, f + eps, color=C_BLUE, alpha=0.16,
                    label=r"$2\varepsilon$ 间隔带（带内损失为 0）")
    ax.plot(xs, f, color=C_RED, lw=2, label="回归曲线 $f(x)$")
    inside = np.abs(yobs - np.interp(X, xs.ravel(), f)) <= eps
    ax.scatter(X[inside], yobs[inside], s=26, c=C_BLUE, zorder=4)
    out_idx = np.where(~inside)[0]
    ax.scatter(X[out_idx], yobs[out_idx], s=30, c=C_ORANGE, zorder=4)
    for i in out_idx[:4]:
        fi = np.interp(X[i], xs.ravel(), f)
        ax.annotate("", xy=(X[i], fi + (eps if yobs[i] > fi else -eps)),
                    xytext=(X[i], yobs[i]),
                    arrowprops=dict(arrowstyle="->", color=C_ORANGE, lw=1.2))
        ax.text(X[i] + 0.06, 0.5 * (yobs[i] + fi), r"$\xi$", fontsize=11, color=C_ORANGE)
    ax.scatter([], [], s=26, c=C_BLUE, label="带内样本（不计损失）")
    ax.scatter([], [], s=30, c=C_ORANGE, label="带外样本（按 $\\xi$、$\\xi^{*}$ 计损失）")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title(r"支持向量回归的 $\varepsilon$ 间隔带", fontsize=11)
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    # 右：损失函数对比
    ax = axes[1]
    e = np.linspace(-2.2, 2.2, 400)
    ax.plot(e, e ** 2, color=C_BLUE, lw=2, label="最小二乘损失 $e^{2}$")
    epsl = 0.5
    ax.plot(e, np.maximum(0.0, np.abs(e) - epsl), color=C_RED, lw=2,
            label=r"$\varepsilon$-不敏感损失 $\max(0,\ |e|-\varepsilon)$")
    ax.axvspan(-epsl, epsl, color=C_RED, alpha=0.10)
    ax.text(0, 2.6, r"$|e|\leq\varepsilon$：损失为 0", ha="center", fontsize=10, color=C_RED)
    ax.set_xlabel("误差 $e=y-f(x)$")
    ax.set_ylabel("损失")
    ax.set_ylim(-0.25, 4.9)
    ax.set_title(r"$\varepsilon$-不敏感损失 vs 最小二乘损失（$\varepsilon=0.5$）", fontsize=11)
    ax.legend(loc="upper center", frameon=False, fontsize=9.5)
    save(fig, "fig10_13_svr_epsilon.png")


# ---------------------------------------------------------------- 图 10-13
def fig13_effect_of_C():
    """超参数 C：结构风险与经验风险的平衡。"""
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.6))
    n = 30
    a = rng.standard_normal((n, 2)) * 0.75 + np.array([-1.2, -1.0])
    bb = rng.standard_normal((n, 2)) * 0.75 + np.array([1.2, 1.0])
    a = np.vstack([a, [[0.6, 0.9]]])
    X = np.vstack([a, bb])
    y = np.hstack([-np.ones(len(a)), np.ones(len(bb))])
    mu, sd = X.mean(0), X.std(0)
    Xs = (X - mu) / sd
    for ax, C, note in [(axes[0], 0.05, "C 过小：欠拟合（间隔过宽）"),
                        (axes[1], 1.0, "C 适中：边界与间隔较均衡"),
                        (axes[2], 500.0, "C 过大：趋向硬间隔（易过拟合）")]:
        alpha, b = smo_train(Xs, y, C=C, kernel="rbf", gamma=1.3)
        ax.scatter(Xs[y == -1, 0], Xs[y == -1, 1], marker="o", s=26, c=C_BLUE,
                   edgecolors="white", linewidths=0.4, zorder=3)
        ax.scatter(Xs[y == 1, 0], Xs[y == 1, 1], marker="s", s=24, c=C_ORANGE,
                   edgecolors="white", linewidths=0.4, zorder=3)
        ax.set_xlim(-2.6, 2.6)
        ax.set_ylim(-2.3, 2.3)
        plot_svm(ax, Xs, y, alpha, b, kernel="rbf", gamma=1.3)
        sv = alpha > 1e-4
        ax.scatter(Xs[sv, 0], Xs[sv, 1], s=105, facecolors="none",
                   edgecolors=C_RED, linewidths=1.1, zorder=4)
        ax.set_title(f"C = {C:g}\n{note}", fontsize=10.5)
        ax.set_xlabel("$x_1$（标准化）")
    axes[0].set_ylabel("$x_2$（标准化）")
    save(fig, "fig10_12_effect_of_C.png")


# ---------------------------------------------------------------- 图 10-14
def fig14_case_iris():
    """鸢尾花案例：versicolor vs virginica 的 SVC 二分类。"""
    import csv
    path = os.path.join(HERE, "data", "iris.csv")
    if not os.path.exists(path):
        path = os.path.join(HERE, "..", "脚本", "Chapter10", "data", "iris.csv")
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
    X, y = [], []
    for r in rows:
        if r["species"] in ("versicolor", "virginica"):
            X.append([float(r["petal_length"]), float(r["petal_width"])])
            y.append(1.0 if r["species"] == "virginica" else -1.0)
    X = np.array(X)
    y = np.array(y)
    mu, sd = X.mean(0), X.std(0)
    Xs = (X - mu) / sd
    alpha, b = smo_train(Xs, y, C=10.0, kernel="rbf", gamma=2.0)
    fig, ax = plt.subplots(figsize=(6.8, 5.2))
    ax.scatter(Xs[y == -1, 0], Xs[y == -1, 1], marker="o", s=34, c=C_BLUE,
               edgecolors="white", linewidths=0.5, label="versicolor（$y=-1$）", zorder=3)
    ax.scatter(Xs[y == 1, 0], Xs[y == 1, 1], marker="s", s=31, c=C_ORANGE,
               edgecolors="white", linewidths=0.5, label="virginica（$y=+1$）", zorder=3)
    ax.set_xlim(-2.8, 3.2)
    ax.set_ylim(-2.6, 3.4)
    plot_svm(ax, Xs, y, alpha, b, kernel="rbf", gamma=2.0)
    sv = alpha > 1e-3
    ax.scatter(Xs[sv, 0], Xs[sv, 1], s=160, facecolors="none",
               edgecolors=C_RED, linewidths=1.4, zorder=4,
               label=f"支持向量（{sv.sum()} 个）")
    acc = np.mean(np.sign((alpha * y) @ _kernel_matrix_pair(Xs, Xs, "rbf", gamma=2.0) + b) == y)
    ax.set_title(f"鸢尾花二分类：花瓣长度 × 花瓣宽度（训练正确率 {acc:.0%}）", fontsize=11.5)
    ax.set_xlabel("花瓣长度（标准化）")
    ax.set_ylabel("花瓣宽度（标准化）")
    ax.legend(loc="upper left", frameon=False, fontsize=9.5)
    save(fig, "fig10_14_case_iris.png")


MAIN += [fig08_history, fig09_convex_qp, fig10_soft_margin,
         fig11_kernel_functions, fig12_svr_epsilon, fig13_effect_of_C,
         fig14_case_iris]

if __name__ == "__main__":
    for fn in MAIN:
        fn()
    print("ALL DONE")
