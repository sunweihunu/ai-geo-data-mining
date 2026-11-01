# -*- coding: utf-8 -*-
"""第八章 决策树 插图生成脚本"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ---------- 全局风格 ----------
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3

OUT = r"C:\20260905\项目 人工智能与地理数据挖掘\书稿\figs\ch08"
rng = np.random.default_rng(42)

C_BLUE = "#1f77b4"
C_ORANGE = "#ff7f0e"
C_GREEN = "#2ca02c"
C_RED = "#d62728"
C_PURPLE = "#9467bd"
C_GRAY = "#7f7f7f"

# 树节点配色
FC_TEST = "#dbeafa"      # 测试节点（内部节点）底色
FC_GOOD = "#d9f2d9"      # 好瓜叶
FC_BAD = "#fde2cf"       # 坏瓜叶
FC_VAL = "#e9e4f5"       # 回归叶（数值）
EC_GRAY = "#999999"


# ----------------------------------------------------------------
# 通用树绘制辅助
# ----------------------------------------------------------------
def tbox(ax, x, y, s, kind="test", fs=10, ls="solid", lw=1.3, text_color="#222222"):
    """在 (x, y) 画一个圆角矩形节点框"""
    if kind == "test":
        fc, ec = FC_TEST, C_BLUE
    elif kind == "good":
        fc, ec = FC_GOOD, C_GREEN
    elif kind == "bad":
        fc, ec = FC_BAD, C_ORANGE
    elif kind == "val":
        fc, ec = FC_VAL, C_PURPLE
    elif kind == "gray":
        fc, ec = "#f2f2f2", C_GRAY
    else:
        fc, ec = "white", C_BLUE
    ax.text(x, y, s, ha="center", va="center", fontsize=fs, color=text_color,
            bbox=dict(boxstyle="round,pad=0.35", fc=fc, ec=ec, lw=lw, linestyle=ls),
            zorder=4)


def edge(ax, p, c, label=None, lx=None, ly=None, color="#555555", fs=9,
         style="-", lw=1.2, label_color=None):
    """从父节点中心 p 连到子节点中心 c，可选边上标签"""
    ax.plot([p[0], c[0]], [p[1], c[1]], color=color, lw=lw, zorder=2,
            linestyle=style)
    if label is not None:
        mx = (p[0] + c[0]) / 2 if lx is None else lx
        my = (p[1] + c[1]) / 2 if ly is None else ly
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs,
                color=label_color or color, zorder=5,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9))


# ----------------------------------------------------------------
# 自实现的 CART：回归树与分类树（用于多张图与鸢尾花案例）
# ----------------------------------------------------------------
def _best_split_reg(X, y, min_leaf):
    """回归树最优二分：最小化加权平方误差"""
    n, p = X.shape
    sse_all = ((y - y.mean()) ** 2).sum()
    best = (None, None, sse_all)          # (特征 j, 阈值 t, 总SSE)
    for j in range(p):
        idx = np.argsort(X[:, j], kind="stable")
        xs, ys = X[idx, j], y[idx]
        cy = np.cumsum(ys)                 # 前缀和
        cy2 = np.cumsum(ys ** 2)
        tot, tot2 = cy[-1], cy2[-1]
        for i in range(min_leaf - 1, n - min_leaf):
            if xs[i] == xs[i + 1]:
                continue
            nl = i + 1
            nr = n - nl
            sl, s2l = cy[i], cy2[i]
            sr, s2r = tot - sl, tot2 - s2l
            sse = (s2l - sl * sl / nl) + (s2r - sr * sr / nr)
            if sse < best[2]:
                t = (xs[i] + xs[i + 1]) / 2
                best = (j, t, sse)
    return best


def build_reg(X, y, min_leaf=1, max_depth=None, depth=1):
    """构建回归树，返回嵌套 dict"""
    node = {"value": float(y.mean()), "n": len(y), "depth": depth}
    if len(np.unique(y)) <= 1 or len(y) < 2 * min_leaf:
        node["split"] = None
        return node
    if max_depth is not None and depth >= max_depth:
        node["split"] = None
        return node
    j, t, sse = _best_split_reg(X, y, min_leaf)
    if j is None:
        node["split"] = None
        return node
    m = X[:, j] <= t
    if m.all() or (~m).all():
        node["split"] = None
        return node
    node["split"] = (j, t)
    node["left"] = build_reg(X[m], y[m], min_leaf, max_depth, depth + 1)
    node["right"] = build_reg(X[~m], y[~m], min_leaf, max_depth, depth + 1)
    return node


def predict_reg(node, X):
    out = np.empty(len(X))
    for i in range(len(X)):
        nd = node
        while nd["split"] is not None:
            j, t = nd["split"]
            nd = nd["left"] if X[i, j] <= t else nd["right"]
        out[i] = nd["value"]
    return out


def _gini(cnt):
    p = cnt / max(cnt.sum(), 1)
    return 1.0 - (p ** 2).sum()


def _best_split_cls(X, y, n_class, min_leaf=1):
    """分类树最优二分：最小化加权基尼指数"""
    n, p = X.shape
    g_all = _gini(np.bincount(y, minlength=n_class))
    best = (None, None, g_all * n)
    for j in range(p):
        idx = np.argsort(X[:, j], kind="stable")
        xs, ys = X[idx, j], y[idx]
        # 按排序列逐个移动样本，增量维护左右类别计数
        cl = np.zeros(n_class)
        cr = np.bincount(ys, minlength=n_class)
        for i in range(n - 1):
            cl[ys[i]] += 1
            cr[ys[i]] -= 1
            if xs[i] == xs[i + 1]:
                continue
            nl, nr = i + 1, n - i - 1
            if nl < min_leaf or nr < min_leaf:
                continue
            g = nl * _gini(cl) + nr * _gini(cr)
            if g < best[2]:
                best = (j, (xs[i] + xs[i + 1]) / 2, g)
    return best


def build_cls(X, y, n_class, min_leaf=1, max_depth=None, depth=1, min_parent=1):
    """min_parent 模拟 MATLAB fitctree 的 'MinParentSize'（默认 10）：
    样本数少于该值的结点不再划分，直接作为叶结点"""
    cnt = np.bincount(y, minlength=n_class)
    node = {"n": len(y), "cnt": cnt, "depth": depth}
    if _gini(cnt) <= 0 or len(y) < 2 * min_leaf or len(y) < min_parent:
        node["split"] = None
        return node
    if max_depth is not None and depth >= max_depth:
        node["split"] = None
        return node
    j, t, _ = _best_split_cls(X, y, n_class, min_leaf)
    if j is None:
        node["split"] = None
        return node
    m = X[:, j] <= t
    if m.all() or (~m).all():
        node["split"] = None
        return node
    node["split"] = (j, t)
    node["left"] = build_cls(X[m], y[m], n_class, min_leaf, max_depth, depth + 1,
                             min_parent)
    node["right"] = build_cls(X[~m], y[~m], n_class, min_leaf, max_depth, depth + 1,
                              min_parent)
    return node


def predict_cls(node, X):
    out = np.empty(len(X), dtype=int)
    for i in range(len(X)):
        nd = node
        while nd["split"] is not None:
            j, t = nd["split"]
            nd = nd["left"] if X[i, j] <= t else nd["right"]
        out[i] = int(np.argmax(nd["cnt"]))
    return out


def tree_depth(node):
    if node["split"] is None:
        return node["depth"]
    return max(tree_depth(node["left"]), tree_depth(node["right"]))


def count_leaves(node):
    if node["split"] is None:
        return 1
    return count_leaves(node["left"]) + count_leaves(node["right"])


# ----------------------------------------------------------------
# fig8_01 分类决策树：挑西瓜
# ----------------------------------------------------------------
def fig8_01():
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    ax.axis("off")
    ax.set_xlim(0, 14)
    ax.set_ylim(0.4, 8.2)

    # L1 根
    r = (7, 7.4)
    # L2
    genti = (3.5, 5.4); cg = (10.0, 5.4); bad1 = (13.0, 5.4)
    # L3
    good1 = (0.8, 3.4); seze = (3.5, 3.4); bad2 = (6.2, 3.4)
    bad3 = (8.7, 3.4); good2 = (11.4, 3.4)
    # L4
    good3 = (1.6, 1.4); bad4 = (3.5, 1.4); bad5 = (5.4, 1.4)

    edge(ax, r, genti, "清晰", lx=4.6, ly=6.7)
    edge(ax, r, cg, "稍糊", lx=8.9, ly=6.7)
    edge(ax, r, bad1, "模糊", lx=10.6, ly=6.2)
    edge(ax, genti, good1, "蜷缩", lx=1.6, ly=4.7)
    edge(ax, genti, seze, "稍蜷", lx=3.5, ly=4.5)
    edge(ax, genti, bad2, "硬挺", lx=5.4, ly=4.7)
    edge(ax, cg, bad3, "硬滑", lx=9.0, ly=4.7)
    edge(ax, cg, good2, "软粘", lx=10.9, ly=4.7)
    edge(ax, seze, good3, "青绿", lx=2.3, ly=2.6)
    edge(ax, seze, bad4, "乌黑", lx=3.5, ly=2.4)
    edge(ax, seze, bad5, "浅白", lx=4.7, ly=2.6)

    tbox(ax, *r, "纹理 = ?", fs=11)
    tbox(ax, *genti, "根蒂 = ?")
    tbox(ax, *cg, "触感 = ?")
    tbox(ax, *seze, "色泽 = ?")
    tbox(ax, *good1, "好瓜", kind="good")
    tbox(ax, *good2, "好瓜", kind="good")
    tbox(ax, *good3, "好瓜", kind="good")
    tbox(ax, *bad1, "坏瓜", kind="bad")
    tbox(ax, *bad2, "坏瓜", kind="bad")
    tbox(ax, *bad3, "坏瓜", kind="bad")
    tbox(ax, *bad4, "坏瓜", kind="bad")
    tbox(ax, *bad5, "坏瓜", kind="bad")

    ax.annotate("根节点", xy=(r[0] + 0.85, r[1]), xytext=(12.6, 7.6), fontsize=9,
                color=C_BLUE, ha="center",
                arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1))
    ax.annotate("内部节点", xy=(genti[0] - 0.8, genti[1]), xytext=(1.2, 6.6),
                fontsize=9, color=C_BLUE, ha="center",
                arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1))
    ax.annotate("叶节点", xy=(bad1[0] - 0.6, bad1[1]), xytext=(12.8, 4.4),
                fontsize=9, color=C_ORANGE, ha="center",
                arrowprops=dict(arrowstyle="->", color=C_ORANGE, lw=1))
    ax.set_title("决策树分类：挑西瓜（“好瓜 / 坏瓜”二分类）", fontsize=12)
    fig.savefig(os.path.join(OUT, "fig8_01_decision_tree_watermelon.png"))
    plt.close(fig)


# ----------------------------------------------------------------
# fig8_02 回归树结构示意
# ----------------------------------------------------------------
def fig8_02():
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0.4, 6.0)

    r = (4.0, 5.2)
    n1 = (1.8, 3.6); n2 = (6.4, 3.6)
    l1 = (0.8, 1.8); l2 = (2.9, 1.8); l3 = (5.4, 1.8); l4 = (7.6, 1.8)

    edge(ax, r, n1, r"$x_{1}\leq 3085.9$", lx=1.9, ly=4.7)
    edge(ax, r, n2, r"$x_{1}> 3085.9$", lx=6.4, ly=4.7)
    edge(ax, n1, l1, r"$x_{2}\leq 90.0$", lx=0.9, ly=2.9)
    edge(ax, n1, l2, r"$x_{2}> 90.0$", lx=2.7, ly=2.9)
    edge(ax, n2, l3, r"$x_{3}\leq 3.5$", lx=5.6, ly=2.9)
    edge(ax, n2, l4, r"$x_{3}> 3.5$", lx=7.4, ly=2.9)

    tbox(ax, *r, r"$x_{1}\leq 3085.9\ ?$", fs=11)
    tbox(ax, *n1, r"$x_{2}\leq 90.0\ ?$")
    tbox(ax, *n2, r"$x_{3}\leq 3.5\ ?$")
    tbox(ax, *l1, "30.2\n(n=12)", kind="val")
    tbox(ax, *l2, "27.5\n(n=9)", kind="val")
    tbox(ax, *l3, "21.6\n(n=15)", kind="val")
    tbox(ax, *l4, "18.3\n(n=8)", kind="val")

    ax.text(5.0, 0.62, "叶节点输出实数：落在该叶的训练样本 Y 的平均值（n 为样本数）",
            ha="center", fontsize=9.5, color=C_PURPLE)
    ax.set_title("决策树回归：回归树的结构（连续自变量按临界值二分）", fontsize=12)
    fig.savefig(os.path.join(OUT, "fig8_02_regression_tree_structure.png"))
    plt.close(fig)


# ----------------------------------------------------------------
# fig8_03 树深度对回归拟合的影响
# ----------------------------------------------------------------
def fig8_03():
    n = 70
    x = np.sort(rng.uniform(0, 10, n))
    y = 2.5 * np.sin(x * 0.9) + 0.6 * x + rng.normal(0, 0.75, n)
    X = x.reshape(-1, 1)
    t2 = build_reg(X, y, min_leaf=3, max_depth=2)
    t5 = build_reg(X, y, min_leaf=3, max_depth=5)

    xs = np.linspace(0, 10, 600).reshape(-1, 1)
    p2 = predict_reg(t2, xs)
    p5 = predict_reg(t5, xs)

    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.scatter(x, y, s=26, color=C_BLUE, alpha=0.75, label="观测点", zorder=3)
    ax.plot(xs, p2, color=C_BLUE, lw=2.2, label="深度为 2 的回归树预测", zorder=2)
    ax.plot(xs, p5, color=C_GREEN, lw=2.2, label="深度为 5 的回归树预测", zorder=2)
    ax.set_xlabel("自变量 x")
    ax.set_ylabel("因变量 y")
    ax.set_title("树的深度对回归树拟合效果的影响")
    ax.legend(loc="lower right", fontsize=9)
    fig.savefig(os.path.join(OUT, "fig8_03_depth_effect.png"))
    plt.close(fig)


# ----------------------------------------------------------------
# fig8_04 叶子大小与交叉验证误差
# ----------------------------------------------------------------
def fig8_04():
    n = 300
    x = rng.uniform(0, 10, n)
    y = 2.2 * np.sin(x * 0.85) + 0.5 * x + rng.normal(0, 1.0, n)
    X = x.reshape(-1, 1)

    sizes = np.arange(2, 101, 2)
    folds = np.arange(n)
    rng.shuffle(folds)
    k = 5
    cv_err = np.zeros(len(sizes))
    tr_err = np.zeros(len(sizes))
    for si, ml in enumerate(sizes):
        errs = []
        for f in range(k):
            va = folds[f::k]
            tr = np.setdiff1d(folds, va)
            tree = build_reg(X[tr], y[tr], min_leaf=int(ml), max_depth=30)
            pv = predict_reg(tree, X[va])
            errs.append(((pv - y[va]) ** 2).mean())
        cv_err[si] = np.mean(errs)
        treef = build_reg(X, y, min_leaf=int(ml), max_depth=30)
        pt = predict_reg(treef, X)
        tr_err[si] = ((pt - y) ** 2).mean()

    bi = int(np.argmin(cv_err))
    fig, ax = plt.subplots(figsize=(7.4, 4.5))
    ax.plot(sizes, cv_err, color=C_BLUE, lw=2, label="交叉验证误差")
    ax.plot(sizes, tr_err, color=C_ORANGE, lw=1.6, ls="--", label="训练误差")
    ax.scatter([sizes[bi]], [cv_err[bi]], s=60, color=C_RED, zorder=4)
    ax.annotate(f"最佳叶子大小 ≈ {sizes[bi]}\n（验证误差最小）",
                xy=(sizes[bi], cv_err[bi]), xytext=(sizes[bi] + 14, cv_err[bi] + 0.55),
                fontsize=9.5, color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.1))
    ax.set_xlabel("最小叶子大小（叶节点最少样本数）")
    ax.set_ylabel("均方误差")
    ax.set_title("叶子大小与模型性能（交叉验证误差）")
    ax.legend(fontsize=9)
    fig.savefig(os.path.join(OUT, "fig8_04_leaf_size_cv.png"))
    plt.close(fig)
    print(f"[fig8_04] 最佳叶子大小 = {sizes[bi]}, CV误差 = {cv_err[bi]:.3f}")


# ----------------------------------------------------------------
# fig8_05 剪枝的概念：未剪枝与剪枝后
# ----------------------------------------------------------------
def _pruning_tree(ax, x0, pruned):
    """画一棵带虚线分支的示意树；x0 为水平偏移"""
    def P(dx, dy):
        return (x0 + dx, dy)
    dash = "dashed" if pruned else "dashed"
    # 保留的主干（蓝色实线）
    r = P(3.0, 6.2); b = P(1.6, 4.4); c = P(4.4, 4.4)
    b1 = P(0.7, 2.6); b2 = P(2.4, 2.6); c1 = P(3.8, 2.6); c2 = P(5.1, 2.6)
    # 将被剪去的细枝（灰色虚线）
    b2a = P(1.7, 0.9); b2b = P(3.1, 0.9)
    c2a = P(4.4, 0.9); c2b = P(5.8, 0.9)
    estyle = dict(color="#666666", lw=1.1)
    for par, ch, lab in [
        (r, b, "是"), (r, c, "否"),
        (b, b1, "是"), (b, b2, "否"),
        (c, c1, "是"), (c, c2, "否"),
    ]:
        edge(ax, par, ch, lab, fs=8)
    tbox(ax, *r, "测试 1", fs=9)
    tbox(ax, *b, "测试 2", fs=9)
    tbox(ax, *c, "测试 3", fs=9)
    if not pruned:
        tbox(ax, *b1, "叶 A", kind="val", fs=9)
        tbox(ax, *b2, "测试 4", fs=9)
        tbox(ax, *c1, "叶 B", kind="val", fs=9)
        tbox(ax, *c2, "测试 5", fs=9)
        edge(ax, b2, b2a, "是", fs=8, **estyle)
        edge(ax, b2, b2b, "否", fs=8, **estyle)
        edge(ax, c2, c2a, "是", fs=8, **estyle)
        edge(ax, c2, c2b, "否", fs=8, **estyle)
        tbox(ax, *b2a, "叶 E", kind="gray", fs=9, ls="dashed")
        tbox(ax, *b2b, "叶 F", kind="gray", fs=9, ls="dashed")
        tbox(ax, *c2a, "叶 G", kind="gray", fs=9, ls="dashed")
        tbox(ax, *c2b, "叶 H", kind="gray", fs=9, ls="dashed")
        ax.text(x0 + 3.0, 7.15, "未剪枝的树", ha="center", fontsize=11, color="#333")
        ax.text(x0 + 3.0, 0.28, "虚线节点：过于细碎、疑似记住训练集噪声",
                ha="center", fontsize=9, color=C_GRAY)
    else:
        tbox(ax, *b1, "叶 A", kind="val", fs=9)
        tbox(ax, *b2, "叶 B", kind="val", fs=9)
        tbox(ax, *c1, "叶 C", kind="val", fs=9)
        tbox(ax, *c2, "叶 D", kind="val", fs=9)
        ax.text(x0 + 3.0, 7.15, "剪枝后的树", ha="center", fontsize=11, color="#333")
        ax.text(x0 + 3.0, 1.15, "原“测试 4”“测试 5”两棵子树\n被替换为叶节点 B、D",
                ha="center", fontsize=9, color=C_RED)


def fig8_05():
    fig, ax = plt.subplots(figsize=(11.5, 4.8))
    ax.axis("off")
    ax.set_xlim(0, 13)
    ax.set_ylim(0.1, 7.8)
    _pruning_tree(ax, 0.2, pruned=False)
    _pruning_tree(ax, 6.6, pruned=True)
    ax.annotate("", xy=(6.35, 3.8), xytext=(5.75, 3.8),
                arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=2))
    ax.set_title("决策树的裁剪（剪枝）：去掉过细的分支，保留合理的规模", fontsize=12)
    fig.savefig(os.path.join(OUT, "fig8_05_pruning_concept.png"))
    plt.close(fig)


# ----------------------------------------------------------------
# fig8_06 决策树的结构与层次
# ----------------------------------------------------------------
def fig8_06():
    fig, ax = plt.subplots(figsize=(9.8, 5.6))
    ax.axis("off")
    ax.set_xlim(0, 14)
    ax.set_ylim(0.2, 8.4)

    r = (7.0, 7.2)
    g = (3.4, 5.2); g2 = (11.2, 5.2)         # 根蒂 / 敲声
    good0 = (13.1, 3.4); bad0 = (9.4, 3.4)   # 乌黑→好瓜 / 浅白→坏瓜
    g1 = (1.2, 3.4); k = (4.9, 3.4)          # 蜷缩→好瓜 / 敲声?
    good1 = (6.0, 1.6); bad1 = (3.8, 1.6)

    edge(ax, r, g, "青绿", lx=4.4, ly=6.5)
    edge(ax, r, g2, "乌黑", lx=9.6, ly=6.5)
    edge(ax, r, good0, "浅白", lx=10.8, ly=5.6)
    edge(ax, g, g1, "蜷缩", lx=1.8, ly=4.5)
    edge(ax, g, k, "稍蜷", lx=4.4, ly=4.3)
    edge(ax, g2, bad0, "浊响", lx=10.4, ly=4.5)
    edge(ax, k, good1, "浊响", lx=5.7, ly=2.7)
    edge(ax, k, bad1, "沉闷", lx=4.2, ly=2.7)

    tbox(ax, *r, "色泽 = ?", fs=11)
    tbox(ax, *g, "根蒂 = ?")
    tbox(ax, *g2, "敲声 = ?")
    tbox(ax, *k, "敲声 = ?")
    tbox(ax, *g1, "好瓜", kind="good")
    tbox(ax, *good1, "好瓜", kind="good")
    tbox(ax, *good0, "好瓜", kind="good")
    tbox(ax, *bad0, "坏瓜", kind="bad")
    tbox(ax, *bad1, "坏瓜", kind="bad")

    # 层次标注（左侧）
    for lv, (yy, name) in enumerate([(7.2, "层次 1"), (5.2, "层次 2"),
                                     (3.4, "层次 3"), (1.6, "层次 4")], start=1):
        ax.plot([0.15, 1.7], [yy, yy], ls=":", color=C_GRAY, lw=0.9)
        ax.text(0.1, yy, name, ha="right", va="center", fontsize=9, color=C_GRAY)
    ax.text(0.1, 8.05, "树的深度 = 4（最长路径的层次数）", ha="left",
            fontsize=9.5, color=C_GRAY)
    # 节点类型标注（右侧）
    ax.annotate("根节点：唯一，判断起点", xy=(7.9, 7.2), xytext=(11.4, 8.0),
                fontsize=9, color=C_BLUE,
                arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1))
    ax.annotate("内部节点（非叶节点）：\n各挂一个测试属性", xy=(11.9, 5.2), xytext=(12.9, 6.3),
                fontsize=9, color=C_BLUE, ha="center",
                arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1))
    ax.annotate("叶节点：判断终止，\n给出结论", xy=(6.7, 1.6), xytext=(8.6, 0.7),
                fontsize=9, color=C_GREEN, ha="center",
                arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1))
    ax.annotate("有向边（分支）：\n只能自上而下", xy=(5.2, 6.25), xytext=(7.6, 6.7),
                fontsize=9, color="#666666",
                arrowprops=dict(arrowstyle="->", color="#666666", lw=1))
    ax.set_title("决策树的结构：节点、有向边与层次", fontsize=12)
    fig.savefig(os.path.join(OUT, "fig8_06_tree_structure.png"))
    plt.close(fig)


# ----------------------------------------------------------------
# fig8_07 信息熵曲线
# ----------------------------------------------------------------
def fig8_07():
    p = np.linspace(0.001, 0.999, 500)
    ent = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ax.plot(p, ent, color=C_BLUE, lw=2.2)
    ax.scatter([0.5], [1.0], s=55, color=C_RED, zorder=4)
    ax.annotate("p = 0.5 时最大，Ent = 1", xy=(0.5, 1.0), xytext=(0.56, 0.9),
                fontsize=9.5, color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1))
    pk = 8 / 17
    ek = -pk * np.log2(pk) - (1 - pk) * np.log2(1 - pk)
    ax.scatter([pk], [ek], s=50, color=C_GREEN, zorder=4)
    ax.annotate(f"西瓜根节点：正例占 8/17\nEnt = {ek:.3f}", xy=(pk, ek),
                xytext=(0.13, 0.72), fontsize=9.5, color=C_GREEN,
                arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1))
    ax.set_xlabel("p（正例所占比例）")
    ax.set_ylabel("信息熵 Ent(D)")
    ax.set_title("二分类问题的信息熵：越接近 0.5 越“不纯”")
    fig.savefig(os.path.join(OUT, "fig8_07_entropy_curve.png"))
    plt.close(fig)


# ----------------------------------------------------------------
# fig8_08 信息增益计算示意（按色泽划分）
# ----------------------------------------------------------------
def fig8_08():
    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    ax.axis("off")
    ax.set_xlim(0, 14)
    ax.set_ylim(0.2, 8.0)

    r = (7, 6.6)
    c1 = (2.4, 3.9); c2 = (7.0, 3.9); c3 = (11.6, 3.9)

    edge(ax, r, c1, "色泽 = 青绿\n（权重 6/17）", lx=3.6, ly=5.55)
    edge(ax, r, c2, "色泽 = 乌黑\n（权重 6/17）", lx=7.0, ly=5.35)
    edge(ax, r, c3, "色泽 = 浅白\n（权重 5/17）", lx=10.4, ly=5.55)

    tbox(ax, *r, "根节点 D：17 个样例\n正例 8 个，反例 9 个\nEnt(D) = 0.998", fs=10.5)
    tbox(ax, *c1, "D$^{1}$：6 个样例\n正 3 / 反 3\nEnt(D$^{1}$) = 1.000", fs=10)
    tbox(ax, *c2, "D$^{2}$：6 个样例\n正 4 / 反 2\nEnt(D$^{2}$) = 0.918", fs=10)
    tbox(ax, *c3, "D$^{3}$：5 个样例\n正 1 / 反 4\nEnt(D$^{3}$) = 0.722", fs=10)

    ax.text(7.0, 1.9,
            "Gain(D, 色泽) = 0.998 − (6/17×1.000 + 6/17×0.918 + 5/17×0.722)\n"
            "               = 0.109",
            ha="center", va="center", fontsize=11, color=C_RED)
    ax.text(7.0, 0.62, "同理可算出其余属性的信息增益，取最大者作为根节点的划分属性",
            ha="center", fontsize=9.5, color=C_GRAY)
    ax.set_title("信息增益的计算：西瓜数据集按“色泽”划分", fontsize=12)
    fig.savefig(os.path.join(OUT, "fig8_08_gain_color_demo.png"))
    plt.close(fig)


# ----------------------------------------------------------------
# fig8_09 基尼指数与信息熵
# ----------------------------------------------------------------
def fig8_09():
    p = np.linspace(0.001, 0.999, 500)
    ent = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
    gini = 2 * p * (1 - p)
    fig, ax = plt.subplots(figsize=(6.8, 4.5))
    ax.plot(p, ent, color=C_BLUE, lw=2.2, label="信息熵 Ent(p)")
    ax.plot(p, gini, color=C_RED, lw=2.2, label="基尼指数 Gini(p)")
    ax.plot(p, ent / 2, color=C_GREEN, lw=1.6, ls="--", label="Ent(p)/2")
    ax.scatter([0.5, 0.5], [1.0, 0.5], s=45, color=[C_BLUE, C_RED], zorder=4)
    ax.annotate("Gini(0.5) = 0.5", xy=(0.5, 0.5), xytext=(0.58, 0.34),
                fontsize=9.5, color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1))
    ax.annotate("Ent(0.5) = 1", xy=(0.5, 1.0), xytext=(0.2, 0.95),
                fontsize=9.5, color=C_BLUE,
                arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1))
    ax.set_xlabel("p（某一类所占比例）")
    ax.set_ylabel("纯度度量值")
    ax.set_title("基尼指数与信息熵：形态一致，均可度量不纯度")
    ax.legend(fontsize=9, loc="upper center")
    fig.savefig(os.path.join(OUT, "fig8_09_gini_curve.png"))
    plt.close(fig)


# ----------------------------------------------------------------
# fig8_10 预剪枝：决策树桩
# ----------------------------------------------------------------
def fig8_10():
    fig, ax = plt.subplots(figsize=(9.6, 5.2))
    ax.axis("off")
    ax.set_xlim(0, 15)
    ax.set_ylim(0.2, 7.6)

    r = (3.6, 6.2)
    l2 = (1.2, 3.8); l3 = (3.6, 3.8); l4 = (6.0, 3.8)
    edge(ax, r, l2, "凹陷", lx=1.7, ly=5.2)
    edge(ax, r, l3, "稍凹", lx=3.6, ly=5.0)
    edge(ax, r, l4, "平坦", lx=5.5, ly=5.2)
    tbox(ax, *r, "脐部 = ?\n（结点 1）", fs=11)
    tbox(ax, *l2, "好瓜\n（结点 2）", kind="good")
    tbox(ax, *l3, "好瓜\n（结点 3）", kind="good")
    tbox(ax, *l4, "坏瓜\n（结点 4）", kind="bad")

    # 被禁止的划分（灰色虚线示意）
    ax.plot([1.2, 1.2], [3.1, 2.2], ls="dashed", color=C_GRAY, lw=1.1)
    tbox(ax, 1.2, 1.8, "试按“色泽”再划分：\n验证集精度 57.1%↓ → 禁止", kind="gray",
         fs=8.6, ls="dashed")
    ax.plot([3.6, 3.6], [3.1, 2.2], ls="dashed", color=C_GRAY, lw=1.1)
    tbox(ax, 3.6, 1.8, "试按“根蒂”再划分：\n验证集精度 71.4%＝ → 禁止", kind="gray",
         fs=8.6, ls="dashed")

    ax.text(9.3, 5.9, "预剪枝判断（基于验证集）", fontsize=11, color="#333")
    ax.text(9.3, 5.05,
            "结点 1 划分前（单叶“好瓜”）：精度 3/7 = 42.9%\n"
            "按“脐部”划分后：精度 5/7 = 71.4% ↑\n"
            "→ 决策：划分",
            fontsize=9.8, va="top", color="#333")
    ax.text(9.3, 3.35,
            "对结点 2、3、4 继续判断：\n"
            "色泽划分使精度下降、根蒂划分持平\n"
            "→ 均禁止划分，结点 4 本身已是叶",
            fontsize=9.8, va="top", color="#333")
    ax.text(9.3, 1.75,
            "最终仅剩一层划分，\n称为“决策树桩”(decision stump)",
            fontsize=9.8, va="top", color=C_RED)
    ax.set_title("预剪枝：边生成边判断，得到仅一层的“决策树桩”", fontsize=12)
    fig.savefig(os.path.join(OUT, "fig8_10_prepruning_stump.png"))
    plt.close(fig)


# ----------------------------------------------------------------
# fig8_11 后剪枝：未剪枝树 → 剪枝后的最终树
# ----------------------------------------------------------------
def fig8_11():
    fig, ax = plt.subplots(figsize=(12.6, 7.0))
    ax.axis("off")
    ax.set_xlim(0, 18)
    ax.set_ylim(0.2, 10.2)

    n1 = (8.0, 8.8)
    n2 = (3.2, 6.8); n3 = (12.4, 6.8); n4 = (16.6, 6.8)
    n5 = (11.0, 4.8)
    n6 = (13.8, 2.9)

    edge(ax, n1, n2, "凹陷", lx=4.6, ly=8.0)
    edge(ax, n1, n3, "稍凹", lx=10.6, ly=8.0)
    edge(ax, n1, n4, "平坦", lx=14.0, ly=8.0)

    # 结点 2 子树（将被剪掉 → 虚线）
    for pt, lab in [((1.0, 4.8), "青绿"), ((3.2, 4.8), "乌黑"), ((5.4, 4.8), "浅白")]:
        edge(ax, n2, pt, lab, lx=(n2[0] + pt[0]) / 2, ly=5.9, style="dashed",
             color=C_GRAY)
    tbox(ax, *n2, "色泽 = ?\n（结点 2）", ls="dashed")
    tbox(ax, 1.0, 4.8, "好瓜", kind="gray", ls="dashed")
    tbox(ax, 3.2, 4.8, "好瓜", kind="gray", ls="dashed")
    tbox(ax, 5.4, 4.8, "坏瓜", kind="gray", ls="dashed")

    # 结点 3 子树（保留）
    k1 = (8.6, 4.8); k5 = (11.0, 4.8); k2 = (14.0, 4.8)
    edge(ax, n3, k1, "蜷缩", lx=10.0, ly=5.9)
    edge(ax, n3, k5, "稍蜷", lx=11.8, ly=5.9)
    edge(ax, n3, k2, "硬挺*", lx=13.6, ly=5.9)
    tbox(ax, *n3, "根蒂 = ?\n（结点 3）")
    tbox(ax, *k1, "坏瓜", kind="bad")
    tbox(ax, *k5, "色泽 = ?\n（结点 5）")
    tbox(ax, *k2, "好瓜*", kind="good")

    # 结点 5 子树
    g1 = (9.6, 2.9); g2 = (11.6, 2.9); g3 = (12.8, 2.9)
    edge(ax, k5, g1, "青绿", lx=10.1, ly=3.95)
    edge(ax, k5, n6, "乌黑", lx=11.5, ly=3.8)
    edge(ax, k5, g3, "浅白*", lx=12.2, ly=3.95)
    tbox(ax, *g1, "好瓜", kind="good")
    tbox(ax, *g3, "好瓜*", kind="good")

    # 结点 6 子树（将被剪掉 → 虚线）
    for pt, lab in [((12.9, 1.1), "稍糊"), ((13.9, 1.1), "清晰"), ((14.9, 1.1), "模糊*")]:
        edge(ax, n6, pt, lab, lx=(n6[0] + pt[0]) / 2 + 0.3, ly=2.0, style="dashed",
             color=C_GRAY, fs=8)
    tbox(ax, *n6, "纹理 = ?\n（结点 6）", fs=9.5, ls="dashed")
    tbox(ax, 12.9, 1.1, "好瓜", kind="gray", fs=9, ls="dashed")
    tbox(ax, 13.9, 1.1, "坏瓜", kind="gray", fs=9, ls="dashed")
    tbox(ax, 14.9, 1.1, "好瓜", kind="gray", fs=9, ls="dashed")

    tbox(ax, *n4, "坏瓜\n（结点 4）", kind="bad")
    tbox(ax, *n1, "脐部 = ?\n（结点 1）", fs=11)

    # 剪枝标注
    ax.annotate("剪：结点 6（训练样本 {7,15}）\n替换为叶“好瓜”→ 精度 42.9%→57.1%",
                xy=(13.9, 2.9), xytext=(16.3, 2.4), fontsize=9, color=C_RED,
                ha="center", arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.2))
    ax.annotate("剪：结点 2 替换为叶“好瓜”\n→ 精度 57.1%→71.4%",
                xy=(3.2, 6.8), xytext=(3.2, 8.9), fontsize=9, color=C_RED,
                ha="center", arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.2))
    ax.text(9.0, 0.55,
            "* 训练集中无样本的分支按多数类标记；结点 5、3、1 替换为叶后精度不升，予以保留",
            fontsize=8.8, color=C_GRAY, ha="center")
    ax.set_title("后剪枝：先生成完整树，再自底向上考察（虚线子树被剪去）", fontsize=12)
    fig.savefig(os.path.join(OUT, "fig8_11_postpruning_tree.png"))
    plt.close(fig)


# ----------------------------------------------------------------
# fig8_12 单变量与多变量决策树
# ----------------------------------------------------------------
def fig8_12():
    n = 90
    X1 = rng.normal(0, 1.1, (n, 2)) + np.array([-1.2, -1.2])
    X2 = rng.normal(0, 1.1, (n, 2)) + np.array([1.4, 1.4])
    X = np.vstack([X1, X2])
    y = np.array([0] * n + [1] * n)

    tree = build_cls(X, y, 2, min_leaf=5, max_depth=4)
    xx, yy = np.meshgrid(np.linspace(-5, 5, 400), np.linspace(-5, 5, 400))
    grid = np.c_[xx.ravel(), yy.ravel()]
    zz = predict_cls(tree, grid).reshape(xx.shape)

    # 简单线性分类器（LDA 方向）作为“多变量”斜线
    m1, m2 = X1.mean(0), X2.mean(0)
    S = (np.cov(X1.T) + np.cov(X2.T)) / 2
    w = np.linalg.solve(S, m2 - m1)
    xm = (m1 + m2) / 2

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6), sharex=True, sharey=True)
    for axi in axes:
        axi.scatter(X1[:, 0], X1[:, 1], s=16, color=C_BLUE, alpha=0.8, label="类别 +")
        axi.scatter(X2[:, 0], X2[:, 1], s=16, color=C_RED, alpha=0.8, marker="^",
                    label="类别 −")
    axes[0].contourf(xx, yy, zz, levels=[-0.5, 0.5, 1.5],
                     colors=[C_BLUE, C_RED], alpha=0.14)
    axes[0].contour(xx, yy, zz, levels=[0.5], colors=C_BLUE, linewidths=2)
    axes[0].set_title("单变量决策树：边界与轴平行（阶梯状）")
    # 斜线
    xg = np.linspace(-5, 5, 10)
    yg = (xm[1] - (w[0] / w[1]) * (xg - xm[0]))
    axes[1].plot(xg, yg, color=C_PURPLE, lw=2.2)
    axes[1].set_title("多变量决策树：斜线边界 $w_{1}x_{1}+w_{2}x_{2}=t$")
    for axi in axes:
        axi.set_xlabel("$x_{1}$")
        axi.set_xlim(-5, 5); axi.set_ylim(-5, 5)
    axes[0].set_ylabel("$x_{2}$")
    axes[0].legend(fontsize=8, loc="upper left")
    fig.suptitle("单变量与多变量决策树的分类边界对比", fontsize=12)
    fig.savefig(os.path.join(OUT, "fig8_12_univariate_vs_multivariate.png"))
    plt.close(fig)


# ----------------------------------------------------------------
# fig8_13 / fig8_14 鸢尾花案例（CART 分类树）
# ----------------------------------------------------------------
IRIS_SUMMARY = {}


def _load_iris():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iris.csv")
    rows = []
    with open(path, encoding="utf-8") as f:
        header = f.readline()
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 5:
                rows.append([float(v) for v in parts[:4]] + [parts[4]])
    data = np.array([r[:4] for r in rows], float)
    names = sorted(set(r[4] for r in rows))
    lab = np.array([names.index(r[4]) for r in rows])
    feat_names = ["萼片长", "萼片宽", "花瓣长", "花瓣宽"]
    return data, lab, names, feat_names


def fig8_13():
    X, y, names, feat = _load_iris()
    tree = build_cls(X, y, 3, min_leaf=1, min_parent=10)
    pred = predict_cls(tree, X)
    err = (pred != y).sum()
    IRIS_SUMMARY["err"] = int(err)
    IRIS_SUMMARY["leaves"] = count_leaves(tree)
    IRIS_SUMMARY["depth"] = tree_depth(tree)
    IRIS_SUMMARY["root"] = tree["split"]
    IRIS_SUMMARY["l2"] = tree["left"]["split"], tree["right"]["split"]

    fig, ax = plt.subplots(figsize=(10.2, 5.4))
    ax.axis("off")
    ax.set_xlim(0, 16)
    ax.set_ylim(0.2, 8.0)

    def rule(nd):
        j, t = nd["split"]
        return "%s $\\leq$ %.2f ?" % (feat[j], t)

    def cnt_str(nd):
        c = nd["cnt"]
        return "/".join(str(int(v)) for v in c)

    r = (8, 6.9)
    nl = tree["left"]; nr = tree["right"]
    l_pos = (3.2, 4.6); rr_pos = (12.2, 4.6)
    edge(ax, r, l_pos, "是", lx=5.0, ly=6.0)
    edge(ax, r, rr_pos, "否", lx=10.4, ly=6.0)
    tbox(ax, *r, rule(tree), fs=11)

    if nl["split"] is None:
        tbox(ax, *l_pos, "setosa\n(%s)" % cnt_str(nl), kind="good")
    else:
        tbox(ax, *l_pos, rule(nl))
    if nr["split"] is None:
        tbox(ax, *rr_pos, "叶", kind="val")
    else:
        tbox(ax, *rr_pos, rule(nr))
        nrl, nrr = nr["left"], nr["right"]
        a = (9.6, 2.3); b = (14.4, 2.3)
        edge(ax, rr_pos, a, "是", lx=10.6, ly=3.6)
        edge(ax, rr_pos, b, "否", lx=13.6, ly=3.6)
        for nd, pos in [(nrl, a), (nrr, b)]:
            if nd["split"] is None:
                name = names[int(np.argmax(nd["cnt"]))]
                tbox(ax, *pos, "%s\n(%s)" % (name, cnt_str(nd)),
                     kind="good" if int(np.argmax(nd["cnt"])) == 0 else "val")
            else:
                tbox(ax, *pos, rule(nd) + "\n……继续划分", fs=9)

    ax.text(8.0, 0.9,
            "在 150 个训练样本上生长的 CART 分类树（按 MATLAB 默认参数，仅画出上部，深层结点略）\n"
            "框内数字为落到该节点的三类样本数（setosa/versicolor/virginica）",
            ha="center", fontsize=9.3, color=C_GRAY)
    ax.set_title("鸢尾花数据的决策树分类（view 命令看到的树结构，示意）", fontsize=12)
    fig.savefig(os.path.join(OUT, "fig8_13_iris_tree.png"))
    plt.close(fig)
    print("[fig8_13] 鸢尾花树：叶数=%d 深度=%d 训练错分=%d 根划分=%s"
          % (IRIS_SUMMARY["leaves"], IRIS_SUMMARY["depth"], IRIS_SUMMARY["err"],
             str(IRIS_SUMMARY["root"])))


def fig8_14():
    X, y, names, feat = _load_iris()
    tree = build_cls(X, y, 3, min_leaf=1, min_parent=10)
    pred = predict_cls(tree, X)
    colors = [C_GREEN, C_ORANGE, C_PURPLE]
    idx = np.arange(1, len(y) + 1)

    fig, ax = plt.subplots(figsize=(9.8, 4.1))
    for c in range(3):
        m = y == c
        ok = m & (pred == y)
        bad = m & (pred != y)
        ax.scatter(idx[ok], y[ok] + 1, s=16, color=colors[c], label=names[c],
                   zorder=3)
        if bad.any():
            ax.scatter(idx[bad], y[bad] + 1, s=110, marker="x", color=C_RED,
                       linewidths=2.2, label="错分样本" if c == 1 else None,
                       zorder=6)
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(names)
    ax.set_xlabel("样本编号（1–50：setosa；51–100：versicolor；101–150：virginica）")
    ax.set_ylim(0.4, 3.6)
    err = int((pred != y).sum())
    ax.set_title("训练集回代：实际类别与预测类别对比（错分 %d 个，回代误差率 %.3f）"
                 % (err, err / len(y)))
    ax.legend(fontsize=8.5, loc="upper center", bbox_to_anchor=(0.5, -0.32),
              ncol=4, frameon=False)
    fig.savefig(os.path.join(OUT, "fig8_14_iris_predict.png"))
    plt.close(fig)
    print("[fig8_14] 错分样本编号: %s" %
          str(idx[pred != y].tolist()))


# ----------------------------------------------------------------
if __name__ == "__main__":
    funcs = [fig8_01, fig8_02, fig8_03, fig8_04, fig8_05, fig8_06, fig8_07,
             fig8_08, fig8_09, fig8_10, fig8_11, fig8_12, fig8_13, fig8_14]
    for f in funcs:
        f()
        print("done:", f.__name__)
    print("ALL FIGURES DONE ->", OUT)
