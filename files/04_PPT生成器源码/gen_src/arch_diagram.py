# -*- coding: utf-8 -*-
"""价衡卫士整体系统架构图（计划书用，法学科普风格）"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(14, 10), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

C = {
    "bg": "#F7F9FC",
    "l1": ("#E8F1FB", "#2B6CB0"),  # 数据感知层 蓝
    "l2": ("#E6F6F0", "#2F855A"),  # 数据服务层 绿
    "l3": ("#FFF4E5", "#C05621"),  # 智能分析层 橙
    "l4": ("#F3E8FF", "#6B46C1"),  # 法律应用层 紫
    "title": "#1A202C",
    "text": "#2D3748",
}

fig.patch.set_facecolor(C["bg"])
ax.set_facecolor(C["bg"])

ax.text(50, 97.5, "价衡卫士 · 整体系统架构", ha="center", va="center",
        fontsize=22, fontweight="bold", color=C["title"])
ax.text(50, 94.3, "采集 → 存证 → 推断 → 评估 → 固证：大数据价格歧视全链条监测",
        ha="center", va="center", fontsize=11.5, color="#718096")

layers = [
    ("l1", 75, 17, "① 数据感知层（浏览器插件 · 用户侧）"),
    ("l2", 54.5, 14.5, "② 数据服务层（后端平台）"),
    ("l3", 33, 16, "③ 智能分析层（价格歧视推断引擎）"),
    ("l4", 11.5, 15, "④ 法律应用层（规划中）"),
]

for key, y, h, label in layers:
    bgc, edge = C[key]
    box = FancyBboxPatch((2, y), 96, h, boxstyle="round,pad=0.6,rounding_size=1.6",
                         linewidth=1.4, edgecolor=edge, facecolor=bgc, alpha=0.55)
    ax.add_patch(box)
    ax.text(4, y + h - 2.4, label, fontsize=12.5, fontweight="bold",
            color=edge, va="center")

def card(x, y, w, h, key, title, lines):
    bgc, edge = C[key]
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                         linewidth=1.3, edgecolor=edge, facecolor="white", alpha=0.96)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h - 2.2, title, ha="center", va="center",
            fontsize=10.5, fontweight="bold", color=edge)
    ax.text(x + 1.6, y + h - 4.1, "\n".join(lines), ha="left", va="top",
            fontsize=8.8, color=C["text"], linespacing=1.5)

# ---- ① 数据感知层（4 卡，w=19.5，间隙 5）----
card(4, 75.4, 19.5, 12.6, "l1", "授权与提示", [
    "· 页面顶部弹出授权提示条",
    "· 用户自愿选择是否采集",
    "· 不同意则绝不采集",
])
card(28.5, 75.4, 19.5, 12.6, "l1", "页面数据提取", [
    "· 读取商品页公开信息：",
    "  价格、优惠、店铺、发货地",
    "· 双通道提取，保证抓得准",
    "· 仅判断登录状态，不读账号",
])
card(53, 75.4, 19.5, 12.6, "l1", "本地脱敏", [
    "· 白名单逐字段脱敏",
    "· 昵称打码、敏感字段剔除",
    "· 数据离开电脑前已匿名化",
])
card(77.5, 75.4, 19.5, 12.6, "l1", "暂存与重试", [
    "· 上报失败自动存本地",
    "· 联网后手动一键重试",
    "· 浏览器内留存可查可删",
])

# ---- ② 数据服务层（3 卡，w=27.5，间隙 5.25）----
card(4, 55, 27.5, 10.6, "l2", "接收与清洗（FastAPI）", [
    "· 接口密钥鉴权，拒绝伪造上报",
    "· 字段校验、异常数据清洗",
    "· 每条数据入库留痕、来源可溯",
])
card(36.75, 55, 27.5, 10.6, "l2", "数据库（PostgreSQL）", [
    "· 结构化存储全部观测记录",
    "· 支持按商品/平台/用户查询",
    "· 正式部署用专业数据库",
])
card(69.5, 55, 27.5, 10.6, "l2", "证据打包导出", [
    "· 观测数据 + 清单打包成 zip",
    "· SHA-256 哈希校验防篡改",
    "· 为公证与诉讼准备原始材料",
])

# ---- ③ 智能分析层 ----
card(4, 33.4, 27.5, 12.6, "l3", "同商品分组对比", [
    "· 锁定同一商品的不同匿名用户",
    "· 自动挑出价差最大的一对",
    "· 算清两组用户各看了多少次、",
    "  各自价格中位数差多少",
])
card(36.75, 33.4, 27.5, 12.6, "l3", "显著性检验", [
    "· Mann-Whitney U 检验：",
    "  两组价差是否纯属偶然",
    "· OLS 回归控制城市、时段、",
    "  促销等干扰因素后再判断",
])
card(69.5, 33.4, 27.5, 12.6, "l3", "判定与标注", [
    "· 价差 >5% 且检验显著",
    "  → 疑似歧视",
    "· 多商品复现 → 平台级疑似",
    "· 原价群体差异 + 深折扣",
    "  → “假折扣型杀熟”",
])

# ---- ④ 法律应用层 ----
card(4, 12, 27.5, 11, "l4", "法律规则知识库", [
    "· 《个保法》24条、《电商法》",
    "  18条等拆解为结构化规则表",
    "· “构成要件—证据—法律后果”对应",
])
card(36.75, 12, 27.5, 11, "l4", "自动法律评估", [
    "· 疑似样本与规则表自动比对",
    "· 报告含涉嫌条款、证据强度、",
    "  维权建议，人工复核后出具",
])
card(69.5, 12, 27.5, 11, "l4", "电子证据固化", [
    "· 截图+数据+哈希打包存证",
    "· 对接可信时间戳与区块链",
    "· 让证据符合法庭采信标准",
])

# ---- 层间箭头（走卡片间隙）----
def arrow(x, y1, y2, label):
    a = FancyArrowPatch((x, y1), (x, y2), arrowstyle="-|>",
                        mutation_scale=22, linewidth=2.2, color="#4A5568",
                        zorder=5)
    ax.add_patch(a)
    ax.text(x, (y1 + y2) / 2, label, fontsize=8.5, color="white",
            va="center", ha="center", zorder=6,
            bbox=dict(boxstyle="round,pad=0.32", fc="#4A5568", ec="none"))

arrow(50.5, 75, 70, "加密上报")
arrow(34.1, 54.4, 50.3, "调用分析")
arrow(66.9, 54.4, 50.3, "打包存证")
arrow(34.1, 32.9, 28.6, "疑似样本推送")

ax.text(50, 5.2, "图例：①②③④ 为数据流向四层架构；第④层法律应用层为二期规划能力",
        ha="center", fontsize=9.5, color="#718096")

out = Path(r"C:\Users\郭家锴\Documents\Kimi\Workspaces\算法歧视证据搜集插件\架构图_价衡卫士.png")
fig.savefig(out, bbox_inches="tight", facecolor=C["bg"])
print("saved:", out)
