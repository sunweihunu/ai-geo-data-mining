# -*- coding: utf-8 -*-
"""demo02_compare.py —— 第02章 MATLAB/Python 对照演示（Python 侧）
对应书稿 2.8.10 两个经典对照实验与 2.8.11 画图对照
运行：uv run --no-project --with numpy --with matplotlib python demo02_compare.py
"""
import numpy as np
import matplotlib.pyplot as plt

# 1) 实验一：一切皆对象 —— 列表相加是拼接，逐元素相加需 NumPy
x = [1, 2, 3]
y = [4, 5, 6]
z = x + y
print("列表相加(拼接):", z)                       # [1, 2, 3, 4, 5, 6]
print("NumPy 逐元素相加:", np.array(x) + np.array(y))  # [5 7 9]

# 2) 索引与切片：从 0 起、前闭后开，末元素可用 -1
a = list(range(1, 11))
print("a[0:10]:", a[0:10])     # 全部
print("a[1:5]:", a[1:5])       # [2, 3, 4, 5]（MATLAB 等价写法是 a(2:5)）
print("末元素:", a[-1])        # 10

# 3) range 五例（range 返回序列对象，用 list() 展开）
print(list(range(5)))             # [0, 1, 2, 3, 4]
print(list(range(1, 5)))          # [1, 2, 3, 4]
print(list(range(1, 11, 2)))      # [1, 3, 5, 7, 9]
r = range(2, 2468, 2)
print(r[0], r[1], r[2], r[len(r) - 1])   # 2 4 6 2466
print(list(range(100, 80, -2)))   # [100, 98, ..., 82]

# 4) 实验二对照要点：块由缩进决定（有无缩进结果不同）
for i in range(5):
    print(i)
print("end")       # 顶格 → 循环外，只打印一次；若缩进则每轮都打印

# 5) sin/cos 曲线图（与 MATLAB 版逐行对应）
x = np.arange(0.0, 8.0, 0.2)
y1, y2 = np.sin(x), np.cos(x)
plt.figure(3)
plt.plot(x, y1, "rx-")
plt.plot(x, y2, "bo-")
plt.title("Function", fontsize=20)
plt.legend(["sin", "cos"], fontsize=15)
plt.text(1.6, 0.5, "y > 0", fontsize=18)
plt.grid()
plt.xlabel("x", fontsize=18)
plt.ylabel("y", fontsize=18)
plt.xlim(0, 6.3)
plt.ylim(-1.2, 1.2)
plt.show()
