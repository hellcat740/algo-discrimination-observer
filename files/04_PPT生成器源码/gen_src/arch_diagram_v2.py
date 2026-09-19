# -*- coding: utf-8 -*-
"""价衡卫士架构图 v3 · 四项技术四宫格闭环版"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

fig, ax = plt.subplots(figsize=(13, 10.5), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

BG = "#F7F9FC"
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

COLORS = {
    1: ("#E8F1FB", "#2B6CB0"),  # 采集 蓝
    2: ("#FFF4E5", "#C05621"),  # 推断 橙
    3: ("#F3E8FF", "#6B46C1"),  # 评估 紫
    4: ("#E6F6F0", "#2F855A"),  # 固证 绿
}

ax.text(50, 97, "价衡卫士 · 系统架构与四项核心技术", ha="center", va="center",
        fontsize=20, fontweight="bold", color="#1A202C")
ax.text(50, 93.8, "监测 → 推断 → 评估 → 固证：大数据价格歧视全链条技术闭环",
        ha="center", va="center", fontsize=11, color="#718096")

MODULES = {
    1: ("① 合规化数据采集与本地脱敏", "浏览器插件 · 用户侧", [
        "· 用户主动点击触发采集",
        "· 仅读取页面公开信息：价格、",
        "  优惠、店铺、发货地",
        "· 登录态只判断、不读取账号",
        "· 本地脱敏、加密后上报",
        "· 数据可用不可见",
    ]),
    2: ("② 算法歧视统计推断引擎", "后端平台 · 自动运行", [
        "· 同商品不同匿名用户自动分组",
        "· Mann-Whitney U 检验价差显著性",
        "· OLS 回归控制城市、时段、促销",
        "  等混杂变量后再判断",
        "· 价差>5%且显著 → 疑似歧视",
        "· 多商品复现 → 平台级疑似",
        "· 假折扣型杀熟特别标注",
    ]),
    3: ("③ 法律规则知识库与自动评估", "规则引擎 · 人工复核", [
        "· 《个保法》24条、《电商法》18条",
        "  等拆解为结构化规则表",
        "· 构成要件—证据—法律后果",
        "  一一对应",
        "· 疑似样本与规则表自动比对",
        "· 输出报告：涉嫌条款、证据分级、",
        "  维权路径（人工复核后出具）",
    ]),
    4: ("④ 电子证据固化", "司法存证 · 全链留痕", [
        "· 截图 + DOM快照 + 原始数据",
        "  一键打包",
        "· SHA-256 哈希防篡改",
        "· 对接可信时间戳与区块链存证",
        "· 形成完整证据链",
        "· 符合法庭采信标准",
    ]),
}

POS = {1: (3, 52), 2: (56, 52), 3: (56, 8), 4: (3, 8)}  # 左上/右上/右下/左下
W, H = 41, 36

for idx, (title, subtitle, lines) in MODULES.items():
    bgc, edge = COLORS[idx]
    x, y = POS[idx]
    box = FancyBboxPatch((x, y), W, H, boxstyle="round,pad=0.4,rounding_size=1.6",
                         linewidth=1.6, edgecolor=edge, facecolor="white", alpha=0.97)
    ax.add_patch(box)
    head = FancyBboxPatch((x + 0.7, y + H - 9), W - 1.4, 7.6,
                          boxstyle="round,pad=0.3,rounding_size=1.1",
                          linewidth=0, facecolor=edge, alpha=0.92)
    ax.add_patch(head)
    ax.text(x + W / 2, y + H - 5.2, title, ha="center", va="center",
            fontsize=12, fontweight="bold", color="white")
    ax.text(x + W / 2, y + H - 11, subtitle, ha="center", va="center",
            fontsize=9.5, color=edge, style="italic")
    ax.plot([x + 2.5, x + W - 2.5], [y + H - 12.4, y + H - 12.4],
            color=edge, linewidth=0.9, alpha=0.45)
    ax.text(x + 2.2, y + H - 14.4, "\n".join(lines), ha="left", va="top",
            fontsize=9.2, color="#2D3748", linespacing=1.62)

ARROW_C = "#4A5568"

def farrow(x1, y1, x2, y2, label=None, lx=0, ly=0):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                        mutation_scale=26, linewidth=2.6,
                        color=ARROW_C, zorder=6)
    ax.add_patch(a)
    if label:
        ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label,
                fontsize=8.6, color="white", ha="center", va="center", zorder=7,
                linespacing=1.4,
                bbox=dict(boxstyle="round,pad=0.38", fc=ARROW_C, ec="none"))

# ①→② 顶部（向右）
farrow(44.6, 70, 55.4, 70, "观测数据\n脱敏记录加密上传")
# ②→③ 右侧（向下）
farrow(76.5, 51.6, 76.5, 44.8, "疑似样本\n显著样本推送评估", lx=6.2)
# ③→④ 底部（向左）
farrow(55.4, 26, 44.6, 26, "评估结论\n涉嫌样本进入固证")
# ④→① 左侧（向上，证据反哺监测）
farrow(23.5, 44.8, 23.5, 51.6, "存证样本\n证据回流复核比对", lx=-6.2)

# 中央闭环标识
c = Circle((50, 47.8), 3.1, facecolor="#EDF2F7", edgecolor=ARROW_C,
           linewidth=1.6, zorder=8)
ax.add_patch(c)
ax.text(50, 47.8, "闭环", ha="center", va="center", fontsize=11,
        fontweight="bold", color=ARROW_C, zorder=9)

out = Path(r"C:\Users\郭家锴\Documents\Kimi\Workspaces\算法歧视证据搜集插件\架构图_价衡卫士_四项技术.png")
fig.savefig(out, bbox_inches="tight", facecolor=BG)
print("saved:", out)
