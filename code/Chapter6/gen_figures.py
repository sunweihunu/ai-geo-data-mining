# -*- coding: utf-8 -*-
"""第六章 线性模型 插图生成脚本"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# ---------- 全局风格 ----------
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3

OUT = r"C:\20260905\项目 人工智能与地理数据挖掘\书稿\figs\ch06"
rng = np.random.default_rng(42)

C_BLUE = "#1f77b4"
C_ORANGE = "#ff7f0e"
C_GREEN = "#2ca02c"
C_RED = "#d62728"
C_PURPLE = "#9467bd"
C_GRAY = "#7f7f7f"


def ols(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    b = ((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum()
    a = y.mean() - b * x.mean()
    return a, b


# ----------------------------------------------------------------
# fig6_01 一元线性回归示意
# ----------------------------------------------------------------
def fig6_01():
    x = np.linspace(0, 10, 40)
    y = 2.0 + 0.8 * x + rng.normal(0, 0.9, x.size)
    a, b = ols(x, y)
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.scatter(x, y, s=28, color=C_BLUE, alpha=0.85, label="观测点 $(x_i,\\ y_i)$", zorder=3)
    xs = np.linspace(-0.3, 10.3, 100)
    ax.plot(xs, a + b * xs, color=C_RED, lw=2, label="回归直线 $\\hat{y}=a+bx$", zorder=2)
    ax.set_xlabel("自变量 x（预报因子）")
    ax.set_ylabel("因变量 y（预报量）")
    ax.set_title("一元线性回归：用直线逼近散点")
    ax.legend(loc="upper left")
    fig.savefig(f"{OUT}/fig6_01_simple_regression.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig6_02 残差示意
# ----------------------------------------------------------------
def fig6_02():
    x = np.linspace(1, 10, 14)
    y = 1.5 + 0.9 * x + rng.normal(0, 0.75, x.size)
    a, b = ols(x, y)
    yhat = a + b * x
    resid = y - yhat

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    ax = axes[0]
    ax.scatter(x, y, s=30, color=C_BLUE, zorder=3, label="观测值 $y_i$")
    xs = np.linspace(0.5, 10.5, 50)
    ax.plot(xs, a + b * xs, color=C_RED, lw=2, label="回归直线 $\\hat{y}=a+bx$")
    # 残差竖线段
    for xi, yi, yh in zip(x, y, yhat):
        ax.plot([xi, xi], [yi, yh], color=C_GREEN, lw=1.4, ls="--", zorder=2)
    ax.annotate("残差 $e_i=y_i-\\hat{y}_i$",
                xy=(x[6], yhat[6] + (y[6] - yhat[6]) / 2),
                xytext=(x[6] - 3.4, yhat[6] + 2.0),
                arrowprops=dict(arrowstyle="->", color=C_GREEN),
                color=C_GREEN, fontsize=10)
    ax.set_xlabel("自变量 x")
    ax.set_ylabel("因变量 y")
    ax.set_title("残差：沿 y 方向度量")
    ax.legend(loc="upper left")

    ax = axes[1]
    ax.scatter(yhat, resid, s=30, color=C_PURPLE, zorder=3)
    ax.axhline(0, color=C_RED, lw=1.5)
    ax.set_xlabel("拟合值 $\\hat{y}$")
    ax.set_ylabel("残差 $e=y-\\hat{y}$")
    ax.set_title("残差图")
    fig.savefig(f"{OUT}/fig6_02_residuals.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig6_03 多元线性回归：三维平面拟合
# ----------------------------------------------------------------
def fig6_03():
    n = 90
    x1 = rng.uniform(0, 10, n)
    x2 = rng.uniform(0, 10, n)
    y = 2.0 + 1.2 * x1 - 0.9 * x2 + rng.normal(0, 1.2, n)
    # OLS 多元
    X = np.column_stack([np.ones(n), x1, x2])
    w = np.linalg.lstsq(X, y, rcond=None)[0]

    fig = plt.figure(figsize=(7.2, 5.2))
    ax = fig.add_subplot(projection="3d")
    ax.scatter(x1, x2, y, s=18, color=C_BLUE, alpha=0.75, label="观测点")
    gx, gy = np.meshgrid(np.linspace(0, 10, 20), np.linspace(0, 10, 20))
    gz = w[0] + w[1] * gx + w[2] * gy
    ax.plot_surface(gx, gy, gz, alpha=0.35, color=C_ORANGE, edgecolor="none")
    ax.set_xlabel("自变量 $x_1$")
    ax.set_ylabel("自变量 $x_2$")
    ax.set_zlabel("因变量 y", labelpad=-6)
    ax.set_title("多元线性回归：用平面（超平面）逼近三维散点")
    ax.view_init(elev=22, azim=-58)
    ax.legend(loc="upper left")
    fig.savefig(f"{OUT}/fig6_03_plane_fit_3d.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig6_04 拟合优度 R² 对比
# ----------------------------------------------------------------
def fig6_04():
    x = np.linspace(0, 10, 45)
    b0 = 3.0
    slope = 0.7
    noise_levels = [0.0, 0.6, 1.6, 4.0]
    titles = ["最好情形：点全落在直线上", "拟合较好", "拟合一般", "几乎无线性关系"]
    fig, axes = plt.subplots(1, 4, figsize=(13.5, 3.4), sharey=True)
    for ax, s, t in zip(axes, noise_levels, titles):
        y = b0 + slope * x + rng.normal(0, s, x.size)
        a, b = ols(x, y)
        yhat = a + b * x
        ss_res = ((y - yhat) ** 2).sum()
        ss_tot = ((y - y.mean()) ** 2).sum()
        r2 = 1 - ss_res / ss_tot
        ax.scatter(x, y, s=16, color=C_BLUE)
        ax.plot(x, yhat, color=C_RED, lw=1.8)
        ax.set_title(f"{t}\n$R^2$={r2:.2f}", fontsize=10)
        ax.set_xlabel("x")
    axes[0].set_ylabel("y")
    fig.suptitle("可决系数 $R^2$：数据点与回归直线逼近程度的度量", y=1.06)
    fig.savefig(f"{OUT}/fig6_04_goodness_of_fit.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig6_05 时间序列自相关
# ----------------------------------------------------------------
def fig6_05():
    n = 300
    # AR(1) 模拟逐日降雨量/水位类序列
    z = rng.normal(0, 1, n)
    y = np.zeros(n)
    for t in range(1, n):
        y[t] = 0.85 * y[t - 1] + z[t]

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4))
    ax = axes[0]
    ax.plot(np.arange(n), y, color=C_BLUE, lw=0.9)
    ax.set_xlabel("时间 t")
    ax.set_ylabel("y(t)")
    ax.set_title("随时间变化的序列（如水位、降雨）")

    ax = axes[1]
    lag1 = y[1:]
    y0 = y[:-1]
    r = np.corrcoef(y0, lag1)[0, 1]
    ax.scatter(y0, lag1, s=10, color=C_ORANGE, alpha=0.7)
    a, b = ols(y0, lag1)
    xs = np.linspace(y0.min(), y0.max(), 50)
    ax.plot(xs, a + b * xs, color=C_RED, lw=1.8)
    ax.set_xlabel("y(t-1)")
    ax.set_ylabel("y(t)")
    ax.set_title(f"滞后一期散点图：自相关 r={r:.2f}")
    fig.savefig(f"{OUT}/fig6_05_autocorrelation_lag.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig6_06 先聚类后回归
# ----------------------------------------------------------------
def fig6_06():
    n = 30
    g1x = rng.uniform(0, 4, n);  g1y = 0.8 * g1x + 1.0 + rng.normal(0, 0.35, n)
    g2x = rng.uniform(3, 7, n);  g2y = 0.5 * g2x + 3.0 + rng.normal(0, 0.35, n)
    g3x = rng.uniform(6, 10, n); g3y = 0.2 * g3x + 6.2 + rng.normal(0, 0.35, n)
    X = np.concatenate([g1x, g2x, g3x])
    Y = np.concatenate([g1y, g2y, g3y])

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), sharex=True, sharey=True)
    ax = axes[0]
    ax.scatter(X, Y, s=18, color=C_GRAY, alpha=0.85)
    a, b = ols(X, Y)
    xs = np.linspace(-0.2, 10.2, 50)
    ax.plot(xs, a + b * xs, color=C_RED, lw=2)
    ax.set_title("全部数据统一建模：整体呈非线性，一条直线难以逼近")
    ax.set_xlabel("x"); ax.set_ylabel("y")

    ax = axes[1]
    for gx, gy, c, name in [(g1x, g1y, C_BLUE, "类1"), (g2x, g2y, C_ORANGE, "类2"), (g3x, g3y, C_GREEN, "类3")]:
        ax.scatter(gx, gy, s=18, color=c, alpha=0.85, label=name)
        a, b = ols(gx, gy)
        xs = np.linspace(gx.min() - 0.3, gx.max() + 0.3, 20)
        ax.plot(xs, a + b * xs, color=c, lw=2)
    ax.set_title("先聚类后回归：每一类内部建立线性模型")
    ax.set_xlabel("x")
    ax.legend(loc="upper left")
    fig.savefig(f"{OUT}/fig6_06_cluster_then_regression.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig6_07 单位阶跃函数 vs 对数几率函数
# ----------------------------------------------------------------
def fig6_07():
    z = np.linspace(-6, 6, 400)
    sig = 1 / (1 + np.exp(-z))
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(z, sig, color=C_BLUE, lw=2.4, label="对数几率（logistic/Sigmoid）函数 $y=\\dfrac{1}{1+e^{-z}}$")
    # 阶跃
    ax.plot([-6, 0], [0, 0], color=C_RED, lw=2.2)
    ax.plot([0, 6], [1, 1], color=C_RED, lw=2.2, label="单位阶跃函数（不连续）")
    ax.plot(0, 0.5, "o", color=C_RED, ms=6)
    ax.annotate("z=0 处 y=0.5", xy=(0, 0.5), xytext=(1.2, 0.42),
                arrowprops=dict(arrowstyle="->", color=C_GRAY), color="#333")
    ax.axhline(0.5, color=C_GRAY, lw=0.8, ls=":")
    ax.axvline(0, color=C_GRAY, lw=0.8, ls=":")
    ax.set_xlabel(r"$z = w^{T}x + b$")
    ax.set_ylabel("y")
    ax.set_ylim(-0.08, 1.12)
    ax.set_title("单位阶跃函数及其替代函数")
    ax.legend(loc="center left", fontsize=9)
    fig.savefig(f"{OUT}/fig6_07_step_vs_sigmoid.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig6_08 广义线性视角：logit 变换
# ----------------------------------------------------------------
def fig6_08():
    z = np.linspace(-6, 6, 400)
    p = 1 / (1 + np.exp(-z))
    logit = np.log(p / (1 - p))
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4))
    ax = axes[0]
    ax.plot(z, p, color=C_BLUE, lw=2.2)
    ax.axhline(0.5, color=C_GRAY, lw=0.8, ls=":")
    ax.axvline(0, color=C_GRAY, lw=0.8, ls=":")
    ax.set_xlabel(r"$z = w^{T}x + b$")
    ax.set_ylabel("p")
    ax.set_title(r"概率输出：$p = 1/(1+e^{-z})$，取值 (0,1)")
    ax = axes[1]
    ax.plot(z, logit, color=C_GREEN, lw=2.2)
    ax.set_xlabel(r"$z = w^{T}x + b$")
    ax.set_ylabel(r"$\ln[p/(1-p)]$")
    ax.set_title(r"对数几率变换后：$\ln[p/(1-p)] = w^{T}x + b$ 为线性")
    fig.suptitle("logistic 回归的广义线性视角", y=1.02)
    fig.savefig(f"{OUT}/fig6_08_logit_linearity.png")
    plt.close(fig)


# ----------------------------------------------------------------
# Fisher LDA 工具
# ----------------------------------------------------------------
def fisher_lda(X1, X2):
    m1, m2 = X1.mean(0), X2.mean(0)
    S1 = np.cov(X1.T)
    S2 = np.cov(X2.T)
    Sw = S1 + S2
    w = np.linalg.solve(Sw, (m2 - m1))
    return w / np.linalg.norm(w), m1, m2


# ----------------------------------------------------------------
# fig6_09 Fisher 判别投影思想
# ----------------------------------------------------------------
def fig6_09():
    n = 60
    X1 = rng.multivariate_normal([2.2, 2.6], [[1.1, 0.55], [0.55, 0.8]], n)
    X2 = rng.multivariate_normal([5.2, 4.4], [[1.2, 0.5], [0.5, 0.9]], n)
    w, m1, m2 = fisher_lda(X1, X2)

    # 投影坐标轴（过两均值中点、方向 w）
    c = (m1 + m2) / 2
    L = 4.6
    p0 = c - L * w
    p1 = c + L * w

    # 投影方向坐标 u = x·w（一维判别值）
    u1 = X1 @ w
    u2 = X2 @ w

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"width_ratios": [1.35, 1]})
    ax = axes[0]
    ax.scatter(X1[:, 0], X1[:, 1], s=16, color=C_BLUE, alpha=0.8, label="类1（如不易患病）")
    ax.scatter(X2[:, 0], X2[:, 1], s=16, color=C_ORANGE, alpha=0.8, label="类2（如易患病）")
    ax.plot(*zip(p0, p1), color=C_RED, lw=2, ls="--", label="判别投影方向 w")
    ax.plot(*m1, "x", color=C_BLUE, ms=11, mew=2.5)
    ax.plot(*m2, "x", color=C_ORANGE, ms=11, mew=2.5)
    ax.plot(*c, "*", color=C_RED, ms=13, label="两类均值中点（阈值 c）")
    # 若干投影线
    for xi in X1[::6]:
        u = xi @ w
        proj = u * w
        ax.plot([xi[0], proj[0]], [xi[1], proj[1]], color=C_BLUE, lw=0.7, alpha=0.5)
    for xi in X2[::6]:
        u = xi @ w
        proj = u * w
        ax.plot([xi[0], proj[0]], [xi[1], proj[1]], color=C_ORANGE, lw=0.7, alpha=0.5)
    ax.set_xlabel("$x_1$（如运动频率）")
    ax.set_ylabel("$x_2$（如吸烟频率）")
    ax.set_title("原始空间：寻找使类间分离最大的投影方向")
    ax.legend(loc="upper left", fontsize=8.5)

    ax = axes[1]
    ax.scatter(u1, np.zeros_like(u1) + 0.05, s=16, color=C_BLUE, alpha=0.8, clip_on=False)
    ax.scatter(u2, np.zeros_like(u2) - 0.05, s=16, color=C_ORANGE, alpha=0.8, clip_on=False)
    uc = c @ w
    ax.axvline(uc, color=C_RED, lw=1.8, ls="--")
    ax.text(uc, 0.14, "阈值 c", color=C_RED, ha="center")
    ax.set_ylim(-0.15, 0.2)
    ax.set_yticks([])
    ax.set_xlabel(r"投影值 $u = w^{T}x$")
    ax.set_title("投影后：两类几乎不重叠")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    fig.savefig(f"{OUT}/fig6_09_lda_projection.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig6_10 LDA 与 PCA 投影方向对比
# ----------------------------------------------------------------
def fig6_10():
    n = 80
    # 类沿斜向拉长，PCA 方向（方差最大）与 LDA 方向（分类最好）明显不同
    X1 = rng.multivariate_normal([3.0, 3.2], [[2.6, 1.4], [1.4, 1.0]], n)
    X2 = rng.multivariate_normal([6.2, 2.0], [[2.6, 1.4], [1.4, 1.0]], n)
    Xall = np.vstack([X1, X2])
    C = np.cov(Xall.T)
    evals, evecs = np.linalg.eigh(C)
    wpca = evecs[:, np.argmax(evals)]
    wlda, m1, m2 = fisher_lda(X1, X2)

    c = (X1.mean(0) + X2.mean(0)) / 2
    fig, ax = plt.subplots(figsize=(6.8, 5))
    ax.scatter(X1[:, 0], X1[:, 1], s=16, color=C_BLUE, alpha=0.8, label="类1")
    ax.scatter(X2[:, 0], X2[:, 1], s=16, color=C_ORANGE, alpha=0.8, label="类2")

    for w, col, name in [(wpca, C_GREEN, "PCA 方向（投影方差最大）"),
                         (wlda, C_RED, "LDA 方向（组间/组内方差比最大）")]:
        p0 = c - 3.2 * w
        p1 = c + 3.2 * w
        ax.annotate("", xy=p1, xytext=p0,
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.4))
    # 投影分离对比（右上角内嵌）
    up1_pca, up2_pca = X1 @ wpca, X2 @ wpca
    up1_lda, up2_lda = X1 @ wlda, X2 @ wlda
    axin = ax.inset_axes([0.60, 0.06, 0.37, 0.34])
    axin.hist(up1_pca, bins=18, color=C_BLUE, alpha=0.6)
    axin.hist(up2_pca, bins=18, color=C_ORANGE, alpha=0.6)
    axin.set_title("投影到 PCA 方向：重叠较多", fontsize=8, color=C_GREEN)
    axin.set_xticks([]); axin.set_yticks([])
    axin2 = ax.inset_axes([0.60, 0.46, 0.37, 0.34])
    axin2.hist(up1_lda, bins=18, color=C_BLUE, alpha=0.6)
    axin2.hist(up2_lda, bins=18, color=C_ORANGE, alpha=0.6)
    axin2.set_title("投影到 LDA 方向：基本分开", fontsize=8, color=C_RED)
    axin2.set_xticks([]); axin2.set_yticks([])

    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.set_title("LDA 与 PCA：两类数据上不同的“最优”投影方向")
    ax.legend(loc="upper left", fontsize=9)
    fig.savefig(f"{OUT}/fig6_10_lda_vs_pca.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig6_11 正则化示意（Ridge 与 Lasso 约束区域）
# ----------------------------------------------------------------
def fig6_11():
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.4))
    w1 = np.linspace(-1.7, 1.7, 400)
    w2 = np.linspace(-1.7, 1.7, 400)
    W1, W2 = np.meshgrid(w1, w2)

    # RSS 等值线（斜椭圆，模拟最小二乘解偏离原点）
    a, b = 0.55, 0.62
    th = np.deg2rad(35)
    U = (W1 - 0.8) * np.cos(th) + (W2 - 0.6) * np.sin(th)
    V = -(W1 - 0.8) * np.sin(th) + (W2 - 0.6) * np.cos(th)
    Z = (U / a) ** 2 + (V / b) ** 2

    t = 1.0
    # Lasso: |w1|+|w2| <= t 菱形
    diamond = plt.Polygon([(-t, 0), (0, -t), (t, 0), (0, t)], closed=True,
                          fill=False, color=C_RED, lw=2)
    # Ridge: w1^2+w2^2 <= t 圆
    circ = plt.Circle((0, 0), t, fill=False, color=C_RED, lw=2)

    for ax, shape, title, inter in [
        (axes[0], diamond, "Lasso：一阶范数约束（菱形）", (0.0, 1.0)),
        (axes[1], circ, "Ridge：二阶范数约束（圆）", None),
    ]:
        cs = ax.contour(W1, W2, Z, levels=[1, 3, 8, 20], colors=C_BLUE, linewidths=1.3)
        ax.clabel(cs, fontsize=8, fmt="%.0f")
        ax.add_artist(shape)
        ax.plot(0.8, 0.6, "k*", ms=12, label="最小二乘解 $\\hat{w}$")
        if title.startswith("Lasso"):
            ax.plot(0, 1, "o", color=C_GREEN, ms=9, zorder=5)
            ax.annotate("交点易落在角上\n（某些权重为 0，特征选择）", xy=(0, 1), xytext=(-1.6, 1.35),
                        fontsize=8.5, color=C_GREEN, arrowprops=dict(arrowstyle="->", color=C_GREEN))
        else:
            ax.plot(0.707, 0.707, "o", color=C_GREEN, ms=9, zorder=5)
            ax.annotate("交点在圆上\n（权重被压缩但不为 0）", xy=(0.707, 0.707), xytext=(-1.6, 1.35),
                        fontsize=8.5, color=C_GREEN, arrowprops=dict(arrowstyle="->", color=C_GREEN))
        ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.3, 1.9)
        ax.set_xlabel("权重 $w_1$"); ax.set_ylabel("权重 $w_2$")
        ax.set_title(title, fontsize=10)
        ax.legend(loc="lower left", fontsize=8.5)
    fig.suptitle("正则化：在残差平方和（蓝线）上加权约束（红线），约束区域内求交点", y=1.03)
    fig.savefig(f"{OUT}/fig6_11_regularization.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig6_12 二分类混淆矩阵示例
# ----------------------------------------------------------------
def fig6_12():
    cm = np.array([[35, 5], [10, 50]])
    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    im = ax.imshow(cm, cmap="Blues", vmin=0, vmax=60)
    labels = [["TP = 35\n(真阳性)", "FN = 5\n(假阴性)"],
              ["FP = 10\n(假阳性)", "TN = 50\n(真阴性)"]]
    for i in range(2):
        for j in range(2):
            ax.text(j, i - 0.12, str(cm[i, j]), ha="center", va="center",
                    fontsize=16, fontweight="bold",
                    color="white" if cm[i, j] > 30 else "#1a1a1a")
            ax.text(j, i + 0.22, labels[i][j], ha="center", va="center",
                    fontsize=8.5, color="white" if cm[i, j] > 30 else "#333")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["预测为正例", "预测为负例"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["真实为正例\n(40 个)", "真实为负例\n(60 个)"], rotation=90, va="center")
    ax.set_title("二分类混淆矩阵（n = 100）：正确率 = (35+50)/100 = 85%")
    ax.grid(False)
    fig.savefig(f"{OUT}/fig6_12_confusion_matrix.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig6_13 案例：UNDP 国家发展水平判别（模拟数据）
# ----------------------------------------------------------------
def fig6_13():
    n1, n2 = 8, 6
    # 模拟指标：出生时预期寿命、成人识字率（高/中水平两组）
    X1_tr = rng.multivariate_normal([79, 97], [[4.0, 1.2], [1.2, 3.0]], n1)   # 高水平
    X2_tr = rng.multivariate_normal([68, 84], [[5.0, 4.0], [4.0, 12.0]], n2)  # 中水平
    # 待判国家
    S1 = np.array([[72, 88], [75, 93], [81, 95], [66, 82]])
    S2 = np.array([[77, 90], [70, 87]])

    w, m1, m2 = fisher_lda(X1_tr, X2_tr)
    c = (m1 + m2) / 2

    def cls(P):
        return (P @ w >= c @ w).astype(int)

    fig, ax = plt.subplots(figsize=(6.8, 5))
    ax.scatter(X1_tr[:, 0], X1_tr[:, 1], s=55, color=C_BLUE, marker="s", label="训练：高水平国家")
    ax.scatter(X2_tr[:, 0], X2_tr[:, 1], s=55, color=C_ORANGE, marker="^", label="训练：中水平国家")
    pred = cls(S1)
    for (x, y), p in zip(S1, pred):
        ax.scatter(x, y, s=110, facecolor="none",
                   edgecolor=C_BLUE if p == 1 else C_ORANGE, lw=1.8, marker="o", zorder=4)
    ax.scatter([], [], s=110, facecolor="none", edgecolor=C_GRAY, lw=1.8, marker="o",
               label="待判国家（圈色=判别结果）")

    # 判别边界线：wᵀx = wᵀc
    xs = np.linspace(60, 86, 50)
    if abs(w[1]) > 1e-9:
        ys = (c @ w - w[0] * xs) / w[1]
        ax.plot(xs, ys, color=C_RED, ls="--", lw=1.8, label="Fisher 判别边界")
    ax.plot(*m1, "x", color=C_BLUE, ms=11, mew=2.5)
    ax.plot(*m2, "x", color=C_ORANGE, ms=11, mew=2.5)
    ax.set_xlabel("出生时预期寿命（岁）")
    ax.set_ylabel("成人识字率（%）")
    ax.set_title("案例（示意）：用判别分析划分国家发展水平")
    ax.set_xlim(60, 86); ax.set_ylim(74, 104)
    ax.legend(loc="lower right", fontsize=8.5)
    fig.savefig(f"{OUT}/fig6_13_case_lda_countries.png")
    plt.close(fig)


# ----------------------------------------------------------------
# fig6_14 指数模型线性化：取对数后成为直线
# ----------------------------------------------------------------
def fig6_14():
    x = np.linspace(0.5, 6, 30)
    a, b = 1.6, 0.42
    y = a * np.exp(b * x) * (1 + rng.normal(0, 0.05, x.size))
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    ax = axes[0]
    ax.scatter(x, y, s=26, color=C_BLUE, zorder=3)
    xs = np.linspace(0.3, 6.2, 100)
    ax.plot(xs, a * np.exp(b * xs), color=C_RED, lw=2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(r"指数模型：$y = a\,e^{bx}$（曲线拟合）")
    ax = axes[1]
    lny = np.log(y)
    a2, b2 = ols(x, lny)
    ax.scatter(x, lny, s=26, color=C_GREEN, zorder=3)
    ax.plot(xs, a2 + b2 * xs, color=C_RED, lw=2)
    ax.set_xlabel("x")
    ax.set_ylabel(r"$y' = \ln y$")
    ax.set_title(r"取对数后：$\ln y = \ln a + bx$（直线拟合）")
    fig.suptitle("指数模型取对数转化为线性模型", y=1.02)
    fig.savefig(f"{OUT}/fig6_14_exponential_to_loglinear.png")
    plt.close(fig)


if __name__ == "__main__":
    for fn in [fig6_01, fig6_02, fig6_03, fig6_04, fig6_05, fig6_06, fig6_07,
               fig6_08, fig6_09, fig6_10, fig6_11, fig6_12, fig6_13, fig6_14]:
        fn()
        print("done", fn.__name__)
