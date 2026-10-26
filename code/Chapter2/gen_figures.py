# -*- coding: utf-8 -*-
"""第02章 编程环境与语言 插图生成脚本（全示意类图，无随机数据）"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle

OUT = r"C:\20260905\项目 人工智能与地理数据挖掘\书稿\figs\ch02"

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
C_LBLUE = "#aec7e8"
C_LORANGE = "#ffbb78"
C_LGREEN = "#98df8a"
C_LPURPLE = "#c5b0d5"


def save(fig, name):
    fig.savefig(f"{OUT}\\{name}", bbox_inches="tight")
    plt.close(fig)
    print("saved:", name)


def box(ax, x, y, w, h, text, fc="#eaf2fb", ec=C_BLUE, fs=11, lw=1.4, tc="black", rounded=True, weight="normal", ls="-"):
    if rounded:
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12",
                           fc=fc, ec=ec, lw=lw, linestyle=ls)
    else:
        p = Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, linestyle=ls)
    ax.add_patch(p)
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs, color=tc, weight=weight, linespacing=1.5)
    return p


def arrow(ax, x1, y1, x2, y2, color=C_GRAY, lw=1.6, style="-|>", ms=14, ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=ms, color=color, lw=lw, linestyle=ls))


# ---------------------------------------------------------------- 2-1 Linux 发展时间线
def fig2_01_linux_timeline():
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    ax.set_xlim(1972, 2012)
    ax.set_ylim(-4.1, 3.8)
    ax.axhline(0, color="black", lw=2, zorder=1)

    # 事件：(年份, 上/下, 标题, 说明, 颜色)；同侧相邻事件用远/近两层错开
    events = [
        (1975, 1, "Emacs 编辑器", "Stallman 开发", C_PURPLE),
        (1984, -1, "MINIX", "Tanenbaum 为教学开发的类 UNIX 系统", C_ORANGE),
        (1985, 1, "GNU 计划 / FSF", "Stallman 创建，目标：自由的完整操作系统", C_PURPLE),
        (1989, -1, "GPL 协议", "通用公共许可，Linux 内核依此发布", C_PURPLE),
        (1991, 1, "Linux 内核 0.02", "本科生 Torvalds 公开内核源代码", C_BLUE),
        (1993, -1, "Linux 1.0", "正式发行，转向 GPL 版权协议", C_BLUE),
        (1994, 1, "Slackware", "第一个商业发行版问世", C_GREEN),
        (1999, -1, "简体中文发行版", "Linux 中文发行版问世", C_GREEN),
        (2004, 1, "Ubuntu", "首个版本发布，后成最流行发行版之一", C_GREEN),
    ]
    tier_count = {1: 0, -1: 0}
    for year, side, title, desc, color in events:
        k = tier_count[side]
        tier_count[side] += 1
        tier = (1.05 if k % 2 == 0 else 2.15) * side
        ax.plot([year, year], [0, tier * 0.85], color=color, lw=1.4)
        ax.plot([year], [0], marker="o", ms=7, color=color, zorder=3)
        va = "bottom" if side > 0 else "top"
        ax.text(year, tier, f"{year} 年\n{title}", ha="center", va=va, fontsize=10.5,
                color=color, weight="bold")
        ax.text(year, tier + 0.72 * side, desc, ha="center", va=va, fontsize=9, color="#404040")
    # 图例说明（放在左下角，避开上方标注）
    ax.text(1972.2, -3.5, "GNU 阵营（紫色）提供编辑器、编译器与协议；", fontsize=10,
            color=C_PURPLE, ha="left")
    ax.text(1972.2, -3.85, "MINIX（橙色）提供教学原型；Linux（蓝色）在 MINIX 上起步", fontsize=10,
            color=C_GRAY, ha="left")
    ax.annotate("", xy=(2011.5, 0), xytext=(2006, 0),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=2))
    ax.axis("off")
    save(fig, "fig2_01_linux_timeline.png")


# ---------------------------------------------------------------- 2-2 Linux 分层体系结构
def fig2_02_linux_layers():
    fig, ax = plt.subplots(figsize=(10, 6.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    layers = [
        (8.2, "用户应用程序", "整个系统的最顶层：浏览器、办公软件、MATLAB / Python 等", C_LBLUE, C_BLUE),
        (6.0, "操作系统服务", "为应用程序提供内核调用接口：Shell、图形桌面、系统工具", C_LGREEN, C_GREEN),
        (3.8, "Linux 内核（Kernel）", "常驻内存部分：进程、内存、设备与网络的管理", C_LORANGE, C_ORANGE),
        (1.6, "硬件系统", "CPU、内存、硬盘、网卡等全部物理设备", "#f2d5d5", C_RED),
    ]
    for y, name, desc, fc, ec in layers:
        box(ax, 1.2, y, 6.6, 1.5, "", fc=fc, ec=ec, lw=1.8)
        ax.text(4.5, y + 0.98, name, ha="center", va="center", fontsize=13, weight="bold")
        ax.text(4.5, y + 0.42, desc, ha="center", va="center", fontsize=9.5, color="#303030")
    for y1, y2 in [(8.2, 7.5), (6.0, 5.3), (3.8, 3.1)]:
        arrow(ax, 4.5, y1, 4.5, y2, color=C_GRAY, style="<|-|>")
    ax.text(8.25, 8.95, "系统调用 / 服务请求", fontsize=9.5, color="#303030")
    ax.text(8.25, 8.6, "（自上而下）", fontsize=9, color="#606060")
    ax.text(8.25, 2.3, "硬件中断 / 数据返回", fontsize=9.5, color="#303030")
    ax.text(8.25, 1.95, "（自下而上）", fontsize=9, color="#606060")
    arrow(ax, 8.2, 8.75, 8.2, 2.45, color=C_GRAY, style="<|-|>", lw=1.2)
    ax.set_title("Linux 分层设计的体系结构", fontsize=14, pad=12)
    save(fig, "fig2_02_linux_layers.png")


# ---------------------------------------------------------------- 2-3 Linux 目录树
def fig2_03_dir_tree():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.4)
    ax.axis("off")

    box(ax, 5.0, 6.3, 2.0, 0.8, "根目录  /", fc="#dbe9f6", ec=C_BLUE, fs=12, weight="bold")
    # 左右两列二级目录
    left = [
        ("bin", "基本命令的可执行文件"),
        ("boot", "系统启动所需的文件"),
        ("dev", "设备文件（一切皆文件）"),
        ("etc", "系统配置文件"),
        ("home", "普通用户的主目录"),
        ("lib", "系统库文件"),
        ("media / mnt", "外接设备、临时挂载点"),
    ]
    right = [
        ("opt", "第三方应用软件"),
        ("proc", "进程与内核信息（虚拟）"),
        ("root", "root 用户的主目录"),
        ("sbin", "系统管理类命令"),
        ("tmp", "临时文件"),
        ("usr", "应用程序与资源"),
        ("var", "日志等经常变化的数据"),
    ]
    xl, xr = 0.3, 6.3
    y_top, dy = 5.35, 0.78
    for i, (name, desc) in enumerate(left):
        y = y_top - i * dy
        box(ax, xl, y, 1.6, 0.62, "/" + name, fc="#f5f5f5", ec=C_GRAY, fs=10.5)
        ax.text(xl + 1.75, y + 0.31, desc, fontsize=9.5, va="center", color="#303030")
        ax.plot([6.0, 6.0], [6.3, y + 0.31], color="#b8b8b8", lw=1)
        ax.plot([6.0, xl + 1.6], [y + 0.31, y + 0.31], color="#b8b8b8", lw=1)
    for i, (name, desc) in enumerate(right):
        y = y_top - i * dy
        box(ax, xr, y, 1.8, 0.62, "/" + name, fc="#f5f5f5", ec=C_GRAY, fs=10.5)
        ax.text(xr + 1.95, y + 0.31, desc, fontsize=9.5, va="center", color="#303030")
        ax.plot([6.0, 6.0], [6.3, y + 0.31], color="#b8b8b8", lw=1)
        ax.plot([6.0, xr + 1.8], [y + 0.31, y + 0.31], color="#b8b8b8", lw=1)
    # home 展开示例
    ax.plot([xl + 0.8, xl + 0.8], [y_top - 4 * dy, 0.85], color="#b8b8b8", lw=1)
    box(ax, 0.3, 0.25, 1.6, 0.6, "sw", fc="#eaf6ea", ec=C_GREEN, fs=10.5)
    ax.text(2.0, 0.55, "/home/sw：用户 sw 的地盘（家目录）", fontsize=9.5, va="center", color="#303030")
    ax.plot([xl + 0.8, 1.9], [0.55, 0.55], color="#b8b8b8", lw=1)
    ax.set_title("Linux 的目录结构：一棵倒挂的树，根在顶端", fontsize=14, pad=10)
    save(fig, "fig2_03_dir_tree.png")


# ---------------------------------------------------------------- 2-4 ls -l 文件属性与权限
def fig2_04_ls_attributes():
    fig, ax = plt.subplots(figsize=(12.5, 7))
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 7.2)
    ax.axis("off")

    # 命令行示例
    ax.text(0.3, 6.6, "$ ls -l", fontsize=13, family="monospace", color="black")
    fields = [
        ("drwxr-xr-x", "文件类型\n+ 九个权限位"),
        ("2", "硬链接\n个数"),
        ("nscc-gz_sw", "所有者\n(用户)"),
        ("nscc-gz", "所属\n用户组"),
        ("4096", "大小\n(字节)"),
        ("Apr 15 11:23", "最后修改\n时间"),
        ("sun_paper", "文件或\n目录名"),
    ]
    widths = [1.85, 0.45, 1.55, 1.15, 0.75, 1.75, 1.45]
    x = 0.3
    y_cmd = 5.75
    colors = [C_BLUE, C_GRAY, C_ORANGE, C_ORANGE, C_GREEN, C_GREEN, C_PURPLE]
    xs = []
    for (txt, _), w, c in zip(fields, widths, colors):
        ax.text(x, y_cmd, txt, fontsize=12.5, family="monospace", color=c, weight="bold")
        xs.append((x, w))
        x += w + 0.18
    # 字段标注箭头
    for i, ((x0, w), (txt, _)) in enumerate(zip(xs, fields)):
        xc = x0 + w / 2
        ax.annotate(txt, xy=(xc, y_cmd - 0.12), xytext=(xc, y_cmd - 1.05),
                    fontsize=9.5, ha="center", va="top", color="#303030",
                    arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.1))
    ax.text(0.3, 3.55, "九个权限位 = 三组 × (读 r / 写 w / 执行 x)：", fontsize=11.5, weight="bold")
    # 权限位展开
    perm = list("drwxr-xr-x")
    pcolors = [C_RED] + [C_BLUE] * 3 + [C_ORANGE] * 3 + [C_GREEN] * 3
    labels = ["类型\nd=目录\n-=普通\nl=链接", "所有者\nr w x", "所属组\nr - x", "其他用户\nr - x"]
    x0 = 0.6
    for i, ch in enumerate(perm):
        w = 0.9
        box(ax, x0 + i * w, 1.5, w - 0.08, 0.85, "", rounded=False,
            fc="white", ec=pcolors[i], lw=1.6)
        ax.text(x0 + i * w + (w - 0.08) / 2, 1.925, ch, ha="center", va="center",
                fontsize=14, family="monospace", weight="bold", color=pcolors[i])
    for xc, lab, c in [(x0 + 0.45 + 3.0, labels[1], C_BLUE),
                       (x0 + 0.45 + 3.0 * 2 + 0.9, labels[2], C_ORANGE),
                       (x0 + 0.45 + 3.0 * 3 + 1.8, labels[3], C_GREEN)]:
        pass
    ax.text(x0 + 1.35, 0.95, labels[0], ha="center", va="top", fontsize=9.5, color=C_RED)
    ax.text(x0 + 1.35 + 2.7, 0.95, labels[1], ha="center", va="top", fontsize=9.5, color=C_BLUE)
    ax.text(x0 + 1.35 + 5.4, 0.95, labels[2], ha="center", va="top", fontsize=9.5, color=C_ORANGE)
    ax.text(x0 + 1.35 + 8.1, 0.95, labels[3], ha="center", va="top", fontsize=9.5, color=C_GREEN)
    # 分组括线
    for a, b, c in [(1, 3, C_BLUE), (4, 6, C_ORANGE), (7, 9, C_GREEN)]:
        xa = x0 + (a - 1) * 0.9 + 0.41
        xb = x0 + b * 0.9 - 0.5
        ax.plot([xa, xb], [2.55, 2.55], color=c, lw=2)
    ax.text(11.0, 1.93, "r = 读\nw = 写\nx = 执行\n- = 无", fontsize=9.5, va="center", color="#303030")
    ax.set_title("ls -l：一条命令读出文件的全部“户口信息”", fontsize=14, pad=10)
    save(fig, "fig2_04_ls_attributes.png")


# ---------------------------------------------------------------- 2-5 Kernel / Shell / Utility
def fig2_05_shell_structure():
    fig, ax = plt.subplots(figsize=(10.5, 6.6))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6.6)
    ax.axis("off")

    # 用户
    ax.add_patch(Circle((1.3, 5.5), 0.42, fc=C_LBLUE, ec=C_BLUE, lw=1.6))
    ax.text(1.3, 5.5, "用户", ha="center", va="center", fontsize=10.5)
    box(ax, 0.3, 4.1, 2.0, 0.85, "终端\nTerminal", fc="#f5f5f5", ec=C_GRAY, fs=11)
    arrow(ax, 1.3, 5.05, 1.3, 5.0, style="<|-|>")
    # Shell
    box(ax, 3.4, 4.1, 3.1, 2.25, "", fc="#e8f0e8", ec=C_GREEN, lw=1.8)
    ax.text(4.95, 5.85, "Shell（命令解释器）", ha="center", fontsize=12, weight="bold", color=C_GREEN)
    ax.text(4.95, 5.3, "用户与内核交互的接口", ha="center", fontsize=9.5, color="#303030")
    ax.text(4.95, 4.75, "bash  csh  tcsh\nksh  zsh ...", ha="center", va="center",
            fontsize=10.5, family="monospace")
    arrow(ax, 2.35, 4.52, 3.35, 4.52, style="<|-|>", color=C_GRAY)
    # Kernel
    box(ax, 3.4, 2.0, 3.1, 1.4, "", fc="#fdf0e3", ec=C_ORANGE, lw=1.8)
    ax.text(4.95, 2.98, "内核 Kernel", ha="center", fontsize=12, weight="bold", color=C_ORANGE)
    ax.text(4.95, 2.4, "管理系统资源：多任务、内存、\n网络协议与服务", ha="center", fontsize=9, color="#303030")
    arrow(ax, 4.95, 4.05, 4.95, 3.45, style="<|-|>", color=C_GRAY)
    # 硬件
    box(ax, 3.4, 0.35, 3.1, 1.05, "硬件系统（CPU / 内存 / 磁盘 / 网卡）",
        fc="#f7e6e6", ec=C_RED, fs=10.5)
    arrow(ax, 4.95, 1.95, 4.95, 1.45, style="<|-|>", color=C_GRAY)
    # Utility
    box(ax, 7.6, 2.0, 2.6, 4.35, "", fc="#f0ebf7", ec=C_PURPLE, lw=1.8)
    ax.text(8.9, 5.95, "Utility 应用程序", ha="center", fontsize=12, weight="bold", color=C_PURPLE)
    ax.text(8.9, 5.35, "各种管理工具与应用：\n\nMATLAB\nPython\ngcc / vim ...\n\n（经 Shell 启动运行）",
            ha="center", va="center", fontsize=9.5, color="#303030")
    arrow(ax, 6.55, 5.2, 7.55, 5.2, style="<|-|>", color=C_GRAY)
    ax.text(7.05, 5.45, "启动", fontsize=9, ha="center", color="#606060")
    ax.set_title("Shell 在 Linux 中的位置：用户与内核之间的“翻译官”", fontsize=14, pad=10)
    save(fig, "fig2_05_shell_structure.png")


# ---------------------------------------------------------------- 2-6 使用 Linux 的几种方式
def fig2_06_ways_to_use():
    fig, axes = plt.subplots(2, 3, figsize=(13, 7.6))
    titles = ["① 远程登录（不安装）", "② 远程桌面（不安装）", "③ 安装真实系统",
              "④ 虚拟机安装", "⑤ WSL 子系统", "⑥ AI 代理（Agent）"]
    notes = ["本地终端经 ssh 协议连接服务器\n适用：超算中心、课题组工作站",
             "RDP 协议或 TeamViewer、向日葵等\n适用：临时使用服务器的图形界面",
             "单独硬盘分区 + 多系统引导启动\n适用：有经验的高级学习者",
             "Windows 中装 VMware 等虚拟机软件\n适用：初学者安全的完整体验",
             "Win10+ 应用商店直接安装子系统\n适用：初学者，与 Windows 无缝配合",
             "Agent 自动维护 ssh 连接与环境\n适用：了解 AI 能力边界的使用者"]
    for ax, t, n in zip(axes.flat, titles, notes):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis("off")
        ax.text(5, 5.6, t, ha="center", fontsize=12, weight="bold")
        ax.text(5, 0.6, n, ha="center", va="center", fontsize=9, color="#303030", linespacing=1.6)
    # ① ssh
    a = axes[0, 0]
    box(a, 0.6, 2.6, 3.0, 1.4, "本地电脑\n终端 ssh 客户端", fc="#eaf2fb", ec=C_BLUE, fs=9.5)
    box(a, 6.4, 2.6, 3.0, 1.4, "远程 Linux\n服务器", fc="#e8f0e8", ec=C_GREEN, fs=9.5)
    arrow(a, 3.7, 3.3, 6.3, 3.3, color=C_GRAY)
    a.text(5.0, 3.65, "网络 / ssh 协议", ha="center", fontsize=8.5, color="#606060")
    # ② 远程桌面
    a = axes[0, 1]
    box(a, 0.6, 2.6, 3.0, 1.4, "本地电脑\n远程桌面客户端", fc="#eaf2fb", ec=C_BLUE, fs=9.5)
    box(a, 6.4, 2.6, 3.0, 1.4, "远程服务器\n整个图形桌面", fc="#e8f0e8", ec=C_GREEN, fs=9.5)
    arrow(a, 3.7, 3.3, 6.3, 3.3, color=C_GRAY)
    a.text(5.0, 3.65, "RDP 等协议", ha="center", fontsize=8.5, color="#606060")
    # ③ 真实系统
    a = axes[0, 2]
    box(a, 1.0, 2.4, 8.0, 1.8, "", fc="#f5f5f5", ec=C_GRAY, rounded=False)
    box(a, 1.3, 2.7, 3.4, 1.2, "Windows 分区", fc="#eaf2fb", ec=C_BLUE, fs=9.5, rounded=False)
    box(a, 5.3, 2.7, 3.4, 1.2, "Linux 分区", fc="#e8f0e8", ec=C_GREEN, fs=9.5, rounded=False)
    a.text(5.0, 4.5, "一块硬盘，开机时选择启动哪个系统", ha="center", fontsize=8.5, color="#606060")
    # ④ 虚拟机
    a = axes[1, 0]
    box(a, 0.8, 2.2, 8.4, 2.2, "Windows 宿主系统", fc="#eaf2fb", ec=C_BLUE, fs=9.5)
    box(a, 2.2, 2.5, 5.6, 1.4, "虚拟机软件（VMware）\n里面装一套完整 Linux", fc="#e8f0e8", ec=C_GREEN, fs=9)
    # ⑤ WSL
    a = axes[1, 1]
    box(a, 0.8, 2.2, 8.4, 2.2, "Windows 10 及以上", fc="#eaf2fb", ec=C_BLUE, fs=9.5)
    box(a, 2.2, 2.5, 5.6, 1.4, "应用商店安装 WSL\nUbuntu 子系统", fc="#e8f0e8", ec=C_GREEN, fs=9)
    # ⑥ Agent
    a = axes[1, 2]
    box(a, 0.6, 2.6, 3.0, 1.4, "本地电脑\n+ AI 代理 Agent", fc="#f0ebf7", ec=C_PURPLE, fs=9.5)
    box(a, 6.4, 2.6, 3.0, 1.4, "远程 Linux\n服务器", fc="#e8f0e8", ec=C_GREEN, fs=9.5)
    arrow(a, 3.7, 3.3, 6.3, 3.3, color=C_PURPLE, ls="--")
    a.text(5.0, 3.65, "ssh 由 Agent 维护", ha="center", fontsize=8.5, color=C_PURPLE)
    fig.suptitle("使用 Linux 的六种方式：从“完全不安装”到“交给 AI”", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    save(fig, "fig2_06_ways_to_use.png")


# ---------------------------------------------------------------- 2-7 Git 模型
def fig2_07_git_model():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.6), width_ratios=[1.05, 1])

    # 左：本地三区 + 远程
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 8)
    ax1.axis("off")
    box(ax1, 0.3, 5.6, 2.7, 1.5, "工作区\n编辑代码", fc="#eaf2fb", ec=C_BLUE, fs=10.5)
    box(ax1, 3.6, 5.6, 2.7, 1.5, "暂存区\n(index)", fc="#fdf0e3", ec=C_ORANGE, fs=10.5)
    box(ax1, 6.9, 5.6, 2.7, 1.5, "本地仓库\n(版本库)", fc="#e8f0e8", ec=C_GREEN, fs=10.5)
    arrow(ax1, 3.05, 6.35, 3.55, 6.35, color=C_GRAY)
    ax1.text(3.3, 6.75, "add", fontsize=9, ha="center", color="#303030")
    arrow(ax1, 6.35, 6.35, 6.85, 6.35, color=C_GRAY)
    ax1.text(6.6, 6.75, "commit", fontsize=9, ha="center", color="#303030")
    box(ax1, 3.6, 2.2, 5.9, 1.5, "远程仓库（GitHub / Gitee / GitLab）\n网络上的仓库，团队协作的中转站",
        fc="#f0ebf7", ec=C_PURPLE, fs=10)
    arrow(ax1, 8.2, 5.55, 7.2, 3.75, color=C_GRAY)
    ax1.text(8.85, 4.7, "push\n推送", fontsize=9.5, ha="center", color="#303030")
    arrow(ax1, 5.6, 3.75, 4.2, 5.55, color=C_GRAY)
    ax1.text(4.3, 4.7, "pull / fetch\n拉取", fontsize=9.5, ha="center", color="#303030")
    ax1.text(5.0, 7.75, "本地三区 + 远程仓库", fontsize=12.5, weight="bold", ha="center")
    ax1.text(5.0, 0.9, "add 与 commit 只在本地完成，断网也能提交版本；\npush 之后别人才看得到你的修改",
             fontsize=9.5, ha="center", color="#303030")

    # 右：分支管理
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 8)
    ax2.axis("off")
    # master 主线
    y0 = 2.2
    xs = np.linspace(0.7, 9.3, 5)
    ax2.plot([0.5, 9.7], [y0, y0], color=C_BLUE, lw=2.2, zorder=1)
    for x in xs:
        ax2.add_patch(Circle((x, y0), 0.14, fc=C_BLUE, ec=C_BLUE, zorder=3))
    ax2.text(0.7, 1.55, "master（主分支）", fontsize=10, color=C_BLUE, weight="bold")
    # dev 分支
    yd = 4.2
    ax2.plot([xs[1], xs[2]], [y0, yd], color=C_GREEN, lw=2, zorder=1)
    ax2.plot([xs[2], xs[4]], [yd, yd], color=C_GREEN, lw=2.2, zorder=1)
    ax2.plot([xs[4], 9.5], [yd, y0], color=C_GREEN, lw=2, zorder=1)
    for x in xs[2:]:
        ax2.add_patch(Circle((x, yd), 0.14, fc=C_GREEN, ec=C_GREEN, zorder=3))
    ax2.text(xs[2] + 0.15, yd + 0.35, "dev（开发分支）", fontsize=10, color=C_GREEN, weight="bold")
    # feature 分支
    yf = 6.2
    ax2.plot([xs[2], xs[2] + 0.9], [yd, yf], color=C_ORANGE, lw=2, zorder=1)
    ax2.plot([xs[2] + 0.9, xs[3] + 0.4], [yf, yf], color=C_ORANGE, lw=2.2, zorder=1)
    ax2.plot([xs[3] + 0.4, xs[3] + 0.8], [yf, yd], color=C_ORANGE, lw=2, zorder=1)
    for x in [xs[2] + 0.9, xs[3] - 0.2, xs[3] + 0.4]:
        ax2.add_patch(Circle((x, yf), 0.14, fc=C_ORANGE, ec=C_ORANGE, zorder=3))
    ax2.text(xs[2] + 0.7, yf + 0.4, "feature-xxx（功能分支）", fontsize=10, color=C_ORANGE, weight="bold")
    ax2.annotate("切出", xy=(xs[1] + 0.35, y0 + 0.75), fontsize=9, color="#606060")
    ax2.annotate("合并", xy=(9.15, y0 + 0.8), fontsize=9, color="#606060")
    ax2.text(5.0, 7.5, "分支：互不干扰的平行开发线", fontsize=12.5, weight="bold", ha="center")
    ax2.text(5.0, 0.9, "master 发布稳定版本，dev 开发新功能；\n每个功能各开一条分支，做完再合并回去",
             fontsize=9.5, ha="center", color="#303030")
    fig.suptitle("Git：先把修改“存档”在本地，再与远程仓库同步", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    save(fig, "fig2_07_git_model.png")


# ---------------------------------------------------------------- 2-8 VS Code 界面
def fig2_08_vscode_ui():
    fig, ax = plt.subplots(figsize=(12.5, 7.8))
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 7.8)
    ax.axis("off")

    # 外框窗口
    box(ax, 0.5, 0.5, 7.6, 6.0, "", fc="white", ec="#555555", rounded=False, lw=1.6)
    # 标题栏
    ax.add_patch(Rectangle((0.5, 6.15), 7.6, 0.35, fc="#3c3c3c", ec="#555555"))
    ax.text(0.7, 6.32, "VS Code — chapter2 (文件夹)", fontsize=9, color="white", va="center")
    # 活动栏
    ax.add_patch(Rectangle((0.5, 0.9), 0.55, 5.25, fc="#2d2d30", ec="#555555"))
    icons = ["文件", "搜索", "Git", "调试", "插件"]
    for i, s in enumerate(icons):
        ax.text(0.775, 5.7 - i * 0.62, s, fontsize=7.5, color="white", ha="center", va="center",
                rotation=0)
    ax.add_patch(Rectangle((0.5, 5.47), 0.08, 0.68, fc=C_ORANGE))  # 选中标识
    # 侧边栏
    ax.add_patch(Rectangle((1.05, 0.9), 1.9, 5.25, fc="#252526", ec="#555555"))
    ax.text(1.18, 5.9, "资源管理器", fontsize=8.5, color="white", weight="bold")
    tree = ["▼ CHAPTER2", "  > figs", "  > data", "  ▾ code", "      demo.py", "      utils.py",
            "  ▾ docs", "      README.md", "      notes.md"]
    for i, t in enumerate(tree):
        ax.text(1.2, 5.55 - i * 0.38, t, fontsize=8, color="#d4d4d4", family="monospace")
    # 编辑器
    ax.add_patch(Rectangle((2.95, 2.7), 5.15, 3.45, fc="#1e1e1e", ec="#555555"))
    ax.text(3.15, 5.85, "demo.py", fontsize=9, color="white")
    code = ["import numpy as np",
            "x = np.arange(0, 8, 0.2)",
            "y1 = np.sin(x)",
            "y2 = np.cos(x)",
            "plt.plot(x, y1, 'rx-')",
            "plt.plot(x, y2, 'bo-')",
            "plt.show()"]
    for i, c in enumerate(code):
        color = "#9cdcfe" if i else "#c586c0"
        ax.text(3.2, 5.45 - i * 0.4, c, fontsize=8.5, color=color, family="monospace")
    # 面板
    ax.add_patch(Rectangle((2.95, 1.0), 5.15, 1.6, fc="#181818", ec="#555555"))
    ax.text(3.15, 2.35, "问题  输出  调试控制台  终端", fontsize=8, color="#d4d4d4")
    ax.text(3.2, 2.0, "PS C:\\chapter2> python demo.py", fontsize=8.5, color="#cccccc", family="monospace")
    ax.text(3.2, 1.6, "[figure saved]", fontsize=8.5, color="#4ec94e", family="monospace")
    # 状态栏
    ax.add_patch(Rectangle((0.5, 0.9), 7.6, 0.28, fc=C_BLUE, ec="none"))
    ax.text(0.7, 1.04, "main*   搜索", fontsize=7.5, color="white", va="center")
    ax.text(7.95, 1.04, "UTF-8  Python 3.10  12, 8", fontsize=7.5, color="white",
            va="center", ha="right")

    # 标注（全部放在窗口外侧）
    ax.annotate("活动栏 Activity Bar\n一级功能菜单", xy=(0.78, 6.05), xytext=(0.4, 7.25),
                fontsize=10.5, ha="left", va="center", color="#202020",
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.2))
    ax.annotate("侧边栏 Side Bar\n二级功能内容", xy=(2.0, 6.05), xytext=(2.7, 7.5),
                fontsize=10.5, ha="left", va="center", color="#202020",
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.2))
    ax.annotate("编辑器 Editor\n编写代码的主战场", xy=(5.6, 5.1), xytext=(8.7, 5.3),
                fontsize=10.5, ha="left", va="center", color="#202020",
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.2))
    ax.annotate("面板 Panels\n终端 / 报错 / 输出 / 调试信息", xy=(5.6, 1.9), xytext=(8.7, 3.2),
                fontsize=10.5, ha="left", va="center", color="#202020",
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.2))
    ax.annotate("状态栏 Status Bar\n当前文件与编程环境的\n动态信息", xy=(4.5, 1.06), xytext=(8.7, 1.3),
                fontsize=10.5, ha="left", va="center", color="#202020",
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.2))
    ax.set_title("VS Code 界面五要素", fontsize=14, pad=10)
    save(fig, "fig2_08_vscode_ui.png")


# ---------------------------------------------------------------- 2-9 VS Code 定位
def fig2_09_vscode_navigate():
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 5.2))
    titles = ["第一层：文件夹 → 文件", "第二层：文件内的大纲", "第三层：光标处的面包屑"]
    for ax, t in zip(axes, titles):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis("off")
        ax.text(5, 5.55, t, ha="center", fontsize=12, weight="bold")
    # 1 资源管理器
    a = axes[0]
    box(a, 1.2, 1.0, 7.6, 3.9, "", fc="#f7f7f7", ec=C_GRAY)
    a.text(1.6, 4.45, "活动栏 > 资源管理器（侧边栏）", fontsize=10, color="#303030", weight="bold")
    items = [("▼ CHAPTER2", 0), ("    > data", 1), ("    ▾ report", 1), ("        ▾ ch02.md", 2),
             ("        > fig2_01.png", 2), ("    > demo.py", 1)]
    for i, (txt, lv) in enumerate(items):
        y = 3.95 - i * 0.5
        color = C_BLUE if txt.endswith("ch02.md") else "#404040"
        a.text(1.7 + lv * 0.35, y, txt, fontsize=9.5, family="monospace", color=color)
    a.text(5, 0.55, "从成百上千的文件里找到目标", ha="center", fontsize=9, color="#606060")
    # 2 大纲
    a = axes[1]
    box(a, 1.2, 1.0, 7.6, 3.9, "", fc="#f7f7f7", ec=C_GRAY)
    a.text(1.6, 4.45, "侧边栏 > 大纲（Outline）", fontsize=10, color="#303030", weight="bold")
    outline = [("# 第2章 编程环境", 0), ("## 2.1 Linux", 1), ("### 2.1.7 文件系统", 2),
               ("### 2.1.8 权限", 2), ("## 2.2 Shell", 1)]
    for i, (txt, lv) in enumerate(outline):
        color = C_ORANGE if "文件系统" in txt else "#404040"
        a.text(1.7 + lv * 0.5, 3.95 - i * 0.55, txt, fontsize=9.5, color=color)
    a.text(5, 0.55, "看清一个长文件内部的标题结构", ha="center", fontsize=9, color="#606060")
    # 3 面包屑
    a = axes[2]
    box(a, 1.2, 1.0, 7.6, 3.9, "", fc="#f7f7f7", ec=C_GRAY)
    a.text(1.6, 4.45, "编辑器顶端 > 定位条（面包屑）", fontsize=10, color="#303030", weight="bold")
    a.text(1.8, 3.5, "CHAPTER2 › report › ch02.md ›\n2.1 Linux › 2.1.7 文件系统",
           fontsize=9.5, va="top", color=C_GREEN)
    box(a, 2.2, 1.8, 5.6, 1.1, "光标当前停在哪个标题之下\n（还可以并排编辑 / 打开微缩图定位）",
        fc="#eaf2fb", ec=C_BLUE, fs=9.5)
    a.text(5, 0.55, "把光标位置精确到文件内部的段落", ha="center", fontsize=9, color="#606060")
    for a in axes:
        pass
    arrow(axes[0], 9.7, 3.0, 10.0, 3.0, color=C_GRAY)  # 视觉分隔
    fig.suptitle("VS Code 怎么“定位”：先找文件，再看结构，最后落到光标", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    save(fig, "fig2_09_vscode_navigate.png")


# ---------------------------------------------------------------- 2-10 隔离环境概念
def fig2_10_venv_concept():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.8))

    # 左：隔离
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 8)
    ax1.axis("off")
    box(ax1, 0.3, 0.8, 9.4, 6.6, "", fc="#fafafa", ec=C_GRAY, lw=1.5)
    ax1.text(5.0, 6.95, "同一台电脑（隔离后）", fontsize=12, weight="bold", ha="center")
    envs = [
        (0.8, 3.6, "环境 py27a\npython 2.7\n+ tf 1.2\n（项目 A）", C_BLUE, "#eaf2fb"),
        (3.85, 3.6, "环境 py27b\npython 2.7\n+ tf 1.6\n（项目 B）", C_GREEN, "#e8f0e8"),
        (0.8, 1.1, "环境 py37\npython 3.7\n+ numpy / scipy\n（论文复现）", C_ORANGE, "#fdf0e3"),
        (3.85, 1.1, "base 环境\npython 3.10\n日常通用", C_PURPLE, "#f0ebf7"),
    ]
    for x, y, t, ec, fc in envs:
        box(ax1, x, y, 2.6, 2.3, t, fc=fc, ec=ec, fs=9.5)
    ax1.plot([6.9, 6.9], [1.0, 7.1], color="#c8c8c8", lw=1, ls="--")
    ax1.text(8.3, 4.0, "环境之间\n互相隔离\n各自安装\n互不干扰", ha="center", va="center",
             fontsize=11, color="#404040")
    for x in (2.1, 5.15):
        for y in (4.7, 2.2):
            ax1.add_patch(Circle((x, y), 0.07, fc=C_GRAY))

    # 右：不隔离
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 8)
    ax2.axis("off")
    box(ax2, 0.3, 0.8, 9.4, 6.6, "", fc="#fafafa", ec=C_GRAY, lw=1.5)
    ax2.text(5.0, 6.95, "同一台电脑（不隔离）", fontsize=12, weight="bold", ha="center")
    box(ax2, 1.6, 3.0, 6.8, 2.6, "全局唯一的 Python 2.7", fc="#f7e6e6", ec=C_RED, fs=11)
    ax2.text(5.0, 5.75, "tf 1.2   ←→   tf 1.6", fontsize=13, ha="center",
             family="monospace", color=C_RED, weight="bold")
    ax2.text(5.0, 4.15, "跑项目 A 就卸载 tf1.6 装 tf1.2\n跑项目 B 再卸载 tf1.2 装 tf1.6\n连带依赖模块来回装卸……",
             fontsize=10, ha="center", va="center", color="#303030", linespacing=1.8)
    ax2.text(5.0, 1.5, "切换一次 = 卸装一大串包，极易出错", fontsize=10.5, ha="center", color=C_RED)
    ax2.text(5.0, 0.35, "多人共用服务器时更糟：人人都得动全局环境", fontsize=9.5,
             ha="center", color="#606060")
    fig.suptitle("隔离环境：给每个项目一间自己的“机房”", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    save(fig, "fig2_10_venv_concept.png")


# ---------------------------------------------------------------- 2-11 Anaconda 组成
def fig2_11_anaconda():
    fig, ax = plt.subplots(figsize=(11.5, 6.8))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 6.8)
    ax.axis("off")

    # Anaconda 大盒
    box(ax, 0.4, 3.0, 10.7, 3.4, "", fc="#f4f8fc", ec=C_BLUE, lw=2)
    ax.text(5.75, 6.05, "Anaconda：用于科学计算的 Python 发行版", fontsize=13,
            weight="bold", ha="center", color=C_BLUE)
    parts = [
        (0.8, 3.35, 2.4, 2.2, "conda\n包管理 +\n环境管理\n（核心引擎）", C_GREEN, "#e8f0e8"),
        (3.45, 3.35, 2.4, 2.2, "Anaconda\nNavigator\n图形界面\n（点一点）", C_ORANGE, "#fdf0e3"),
        (6.1, 3.35, 2.4, 2.2, "科学计算包\nNumPy\nMatplotlib\npandas ...", C_PURPLE, "#f0ebf7"),
        (8.75, 3.35, 2.0, 2.2, "关联软件\nJupyter\nSpyder\nVS Code ...", C_RED, "#f7e6e6"),
    ]
    for x, y, w, h, t, ec, fc in parts:
        box(ax, x, y, w, h, t, fc=fc, ec=ec, fs=9.5)
    # Miniconda
    box(ax, 0.4, 0.7, 4.6, 1.7, "Miniconda（精简版）\n= conda + Python + 少量必备包", fc="#f5f5f5",
        ec=C_GRAY, fs=10)
    # 两种使用方式
    box(ax, 5.5, 0.7, 5.6, 1.7, "两种使用方式：Navigator 图形界面 / Anaconda Prompt 命令行\n（命令行的背后就是 conda 命令）",
        fc="#f5f5f5", ec=C_GRAY, fs=9.5)
    arrow(ax, 2.7, 2.45, 2.7, 3.3, color=C_GRAY)
    arrow(ax, 8.3, 2.45, 8.3, 3.3, color=C_GRAY)
    ax.set_title("conda、Anaconda 与 Miniconda 的关系", fontsize=14, pad=12)
    save(fig, "fig2_11_anaconda.png")


# ---------------------------------------------------------------- 2-12 MATLAB 与 Python 双时间线
def fig2_12_history():
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    ax.set_xlim(1975, 2024)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # MATLAB 线（上）
    ax.annotate("", xy=(2023.5, 6.2), xytext=(1975.5, 6.2),
                arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=2.4))
    ax.text(1975.5, 7.5, "MATLAB（蓝）", fontsize=12.5, weight="bold", color=C_BLUE)
    m_ev = [
        (1978, "20 世纪 70 年代末：Moler（新墨西哥大学）\n用 FORTRAN 编写最早的 MATLAB，减轻学生负担", 1, "right"),
        (1981, "1981：IBM 推出 PC，\nLittle 与 Bangert 用 C 重写\n（M 文件、工具箱、画图）", -1, "center"),
        (1984, "1984：Little、Moler、Bangert\n创立 MathWorks 公司", 1, "left"),
        (2003, "2003 起：每年两个版本\n（a 版 3 月，b 版 9 月，如 2022a/2022b）", -1, "center"),
    ]
    for year, txt, side, halign in m_ev:
        ax.plot([year], [6.2], marker="o", ms=7, color=C_BLUE)
        ax.plot([year, year], [6.2, 6.2 + 0.42 * side], color=C_BLUE, lw=1.2)
        va = "bottom" if side > 0 else "top"
        ax.text(year, 6.2 + 0.55 * side, txt, fontsize=9, ha=halign, va=va, color="#303030")
    # Python 线（下）
    ax.annotate("", xy=(2023.5, 1.8), xytext=(1975.5, 1.8),
                arrowprops=dict(arrowstyle="-|>", color=C_GREEN, lw=2.4))
    ax.text(1975.5, 0.7, "Python（绿）", fontsize=12.5, weight="bold", color=C_GREEN)
    p_ev = [
        (1989, "1989：荷兰人 Guido van Rossum\n开发 Python", 1, "center"),
        (2000, "2000.10：Python 2 发布（稳定版 2.7）\n2001：Python 软件基金会（PSF）成立", -1, "center"),
        (2008, "2008.12：Python 3 发布，\n与 Python 2 不完全兼容", 1, "center"),
        (2020, "2020.11：Guido 加入微软\n（VS Code 的 Python 体验继续增强）", -1, "center"),
    ]
    for year, txt, side, halign in p_ev:
        ax.plot([year], [1.8], marker="o", ms=7, color=C_GREEN)
        ax.plot([year, year], [1.8, 1.8 + 0.42 * side], color=C_GREEN, lw=1.2)
        va = "bottom" if side > 0 else "top"
        ax.text(year, 1.8 + 0.55 * side, txt, fontsize=9, ha=halign, va=va, color="#303030")
    ax.set_title("MATLAB 与 Python 的发展历史：一横一纵两条时间线", fontsize=14, pad=10)
    save(fig, "fig2_12_history.png")


# ---------------------------------------------------------------- 2-13 经典对照实验 x + y
def fig2_14_x_plus_y():
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 6.4))

    def term(ax, title, tc, lines, note):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8.6)
        ax.axis("off")
        box(ax, 0.4, 6.9, 9.2, 1.3, title, fc=tc, ec=tc, fs=12, tc="white", weight="bold")
        box(ax, 0.4, 2.5, 9.2, 4.2, "", fc="#1e1e1e", ec="#555555", rounded=False)
        for i, (ln, c) in enumerate(lines):
            ax.text(0.8, 6.1 - i * 0.62, ln, fontsize=11, family="monospace", color=c)
        ax.text(5.0, 1.8, note, ha="center", va="top", fontsize=10.5, color="#303030")

    m_lines = [
        (">> x = [1, 2, 3];", "#cccccc"),
        (">> y = [4, 5, 6];", "#cccccc"),
        (">> z = x + y", "#cccccc"),
        ("z =", "#d4d4d4"),
        ("     5     7     9", "#4ec94e"),
    ]
    term(axes[0], "MATLAB：一切皆矩阵", C_BLUE, m_lines,
         "数组逐元素相加，结果仍是同形状数组\n（线性代数的直觉在这里成立）")
    p_lines = [
        (">>> x = [1, 2, 3]", "#cccccc"),
        (">>> y = [4, 5, 6]", "#cccccc"),
        (">>> z = x + y", "#cccccc"),
        (">>> z", "#cccccc"),
        ("[1, 2, 3, 4, 5, 6]", "#f2b8b8"),
    ]
    term(axes[1], "Python：一切皆对象", C_GREEN, p_lines,
         "列表是通用对象，"+"+"+"是“拼接”而非数值加法\n逐元素相加需借助 NumPy 数组")

    # 底部色块对比
    for ax, cells, colors, lab in [
        (axes[0], [5, 7, 9], [C_BLUE] * 3, ""),
        (axes[1], [1, 2, 3, 4, 5, 6], [C_GREEN] * 3 + [C_ORANGE] * 3, ""),
    ]:
        x0 = 5.0 - len(cells) * 0.75 / 2 * 1.0
        for j, v in enumerate(cells):
            box(ax, x0 + j * 0.78, 0.25, 0.68, 0.7, str(v), rounded=False,
                fc="white", ec=colors[j], fs=10)
    axes[1].text(5.0, 1.15, "前 3 格来自 x，后 3 格来自 y：直接“接龙”", ha="center",
                 fontsize=9, color="#606060")
    axes[0].text(5.0, 1.15, "对应位置相加：1+4，2+5，3+6", ha="center",
                 fontsize=9, color="#606060")
    fig.suptitle("同一句 z = x + y，两种语言两种结果", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    save(fig, "fig2_14_x_plus_y.png")


# ---------------------------------------------------------------- 2-14 索引与切片
def fig2_13_index_slice():
    fig, ax = plt.subplots(figsize=(12.5, 6.8))
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 6.8)
    ax.axis("off")

    values = list(range(1, 11))
    n = len(values)
    x0, w = 1.0, 1.0

    ax.text(0.35, 5.9, "同一个序列，值 1~10：", fontsize=11.5, weight="bold")
    for j, v in enumerate(values):
        box(ax, x0 + j * w, 5.0, w - 0.08, 0.8, str(v), rounded=False, fc="#f5f5f5",
            ec="#909090", fs=11)
    # MATLAB 行
    ax.text(0.35, 4.35, "MATLAB 下标（从 1 开始）", fontsize=10.5, color=C_BLUE, weight="bold")
    for j in range(n):
        ax.text(x0 + j * w + (w - 0.08) / 2, 4.0, str(j + 1), ha="center", va="center",
                fontsize=10.5, color=C_BLUE)
    ax.text(x0 + n * w + 0.25, 4.0, "a(1:10) 取全部；\na(2:5) = [2 3 4 5]\n（前闭后闭）",
            fontsize=9.5, va="center", color="#303030")
    # 高亮 MATLAB 2:5 → 下标2..5 即值2..5
    for j in [1, 2, 3, 4]:
        box(ax, x0 + j * w, 5.0, w - 0.08, 0.8, "", rounded=False, fc="none",
            ec=C_BLUE, lw=2.4)
    # Python 行
    ax.text(0.35, 3.15, "Python 下标（从 0 开始，末元素也可用负数下标）", fontsize=10.5,
            color=C_GREEN, weight="bold")
    for j in range(n):
        ax.text(x0 + j * w + (w - 0.08) / 2, 2.8, str(j), ha="center", va="center",
                fontsize=10.5, color=C_GREEN)
        ax.text(x0 + j * w + (w - 0.08) / 2, 2.35, str(j - n), ha="center", va="center",
                fontsize=9, color=C_GREEN, alpha=0.65)
    ax.text(x0 + n * w + 0.25, 2.6, "a[0:10] 取全部；\na[1:5] = [2 3 4 5]\n（前闭后开）",
            fontsize=9.5, va="center", color="#303030")
    # 高亮 Python 1:5 → 下标1..4 即值2..5
    for j in [1, 2, 3, 4]:
        box(ax, x0 + j * w, 5.0, w - 0.08, 0.8, "", rounded=False, fc="none",
            ec=C_GREEN, lw=2.4, ls="--")
    # 说明
    box(ax, 1.0, 0.35, 10.5, 1.35,
        "结论：MATLAB 的 a(2:5) 与 Python 的 a[1:5] 取到的是同一批元素。\n"
        "起点差 1 是“从 1 数”与“从 0 数”的区别；终点规则不同是“含头含尾”与“含头不含尾”的区别。",
        fc="#fdf6e8", ec=C_ORANGE, fs=10.5)
    ax.set_title("索引与切片：起点与终点的两套约定", fontsize=14, pad=10)
    save(fig, "fig2_13_index_slice.png")


if __name__ == "__main__":
    todo = [
        fig2_01_linux_timeline,
        fig2_02_linux_layers,
        fig2_03_dir_tree,
        fig2_04_ls_attributes,
        fig2_05_shell_structure,
        fig2_06_ways_to_use,
        fig2_07_git_model,
        fig2_08_vscode_ui,
        fig2_09_vscode_navigate,
        fig2_10_venv_concept,
        fig2_11_anaconda,
        fig2_12_history,
        fig2_14_x_plus_y,
        fig2_13_index_slice,
    ]
    for f in todo:
        f()
    print("all done")
