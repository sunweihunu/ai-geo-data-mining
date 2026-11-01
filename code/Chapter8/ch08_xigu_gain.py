# -*- coding: utf-8 -*-
"""第8章 西瓜数据集2.0 信息增益复算（验证表8-3中各属性信息增益数值）

数据：周志华《机器学习》"西瓜数据集2.0"（17 个样例，6 个离散属性，好瓜 8/9）。
运行：uv run --no-project python ch08_xigu_gain.py
预期输出：
  Ent(D) = 0.998
  色泽 0.109  根蒂 0.143  敲声 0.141  纹理 0.381  脐部 0.289  触感 0.006
  最优划分属性：纹理
"""
import numpy as np

# 编号, 色泽, 根蒂, 敲声, 纹理, 脐部, 触感, 好瓜(1=是,0=否)
DATA = [
    (1,  "青绿", "蜷缩", "浊响", "清晰", "凹陷", "硬滑", 1),
    (2,  "乌黑", "蜷缩", "沉闷", "清晰", "凹陷", "硬滑", 1),
    (3,  "乌黑", "蜷缩", "浊响", "清晰", "凹陷", "硬滑", 1),
    (4,  "青绿", "蜷缩", "沉闷", "清晰", "凹陷", "硬滑", 1),
    (5,  "浅白", "蜷缩", "浊响", "清晰", "凹陷", "硬滑", 1),
    (6,  "青绿", "稍蜷", "浊响", "清晰", "稍凹", "软粘", 1),
    (7,  "乌黑", "稍蜷", "浊响", "稍糊", "稍凹", "软粘", 1),
    (8,  "乌黑", "稍蜷", "浊响", "清晰", "稍凹", "硬滑", 1),
    (9,  "乌黑", "稍蜷", "沉闷", "稍糊", "稍凹", "硬滑", 0),
    (10, "青绿", "硬挺", "清脆", "清晰", "平坦", "软粘", 0),
    (11, "浅白", "硬挺", "清脆", "模糊", "平坦", "硬滑", 0),
    (12, "浅白", "蜷缩", "浊响", "模糊", "平坦", "软粘", 0),
    (13, "青绿", "稍蜷", "浊响", "稍糊", "凹陷", "硬滑", 0),
    (14, "浅白", "稍蜷", "沉闷", "稍糊", "凹陷", "硬滑", 0),
    (15, "乌黑", "稍蜷", "浊响", "清晰", "稍凹", "软粘", 0),
    (16, "浅白", "蜷缩", "浊响", "模糊", "平坦", "硬滑", 0),
    (17, "青绿", "蜷缩", "沉闷", "稍糊", "稍凹", "硬滑", 0),
]
ATTRS = ["色泽", "根蒂", "敲声", "纹理", "脐部", "触感"]


def entropy(pos, neg):
    n = pos + neg
    if n == 0:
        return 0.0
    ent = 0.0
    for k in (pos, neg):
        p = k / n
        if p > 0:
            ent -= p * np.log2(p)
    return ent


def main():
    y = np.array([row[-1] for row in DATA])
    ent_d = entropy((y == 1).sum(), (y == 0).sum())
    print("Ent(D) = %.3f（8 正例 / 9 反例）" % ent_d)
    gains = {}
    for ai, attr in enumerate(ATTRS):
        values = sorted(set(row[1 + ai] for row in DATA))
        weighted = 0.0
        parts = []
        for v in values:
            sub = [row for row in DATA if row[1 + ai] == v]
            pos = sum(r[-1] for r in sub)
            neg = len(sub) - pos
            weighted += len(sub) / len(DATA) * entropy(pos, neg)
            parts.append("%s:%d(正%d/反%d)Ent=%.3f" % (v, len(sub), pos, neg,
                                                       entropy(pos, neg)))
        gains[attr] = ent_d - weighted
        print("%s: Gain = %.3f   [%s]" % (attr, gains[attr], "  ".join(parts)))
    best = max(gains, key=gains.get)
    print("最优划分属性：%s（信息增益 %.3f 最大）" % (best, gains[best]))

    # 增益率的分母 IV(a)（固定值）与增益率，供对照
    print("\n增益率对照（Gain_ratio = Gain / IV）：")
    for ai, attr in enumerate(ATTRS):
        values = sorted(set(row[1 + ai] for row in DATA))
        iv = 0.0
        for v in values:
            n_v = sum(1 for row in DATA if row[1 + ai] == v)
            p = n_v / len(DATA)
            iv -= p * np.log2(p)
        print("%s: IV(a) = %.3f, Gain_ratio = %.3f" % (attr, iv,
                                                       gains[attr] / iv))


if __name__ == "__main__":
    main()
