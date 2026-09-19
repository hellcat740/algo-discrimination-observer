# -*- coding: utf-8 -*-
"""国创赛路演 PPT 生成器 —— 核心骨架（背景/导航/章节页/卡片）"""
import json
from pathlib import Path
import yaml

ROOT = Path(r"C:/Users/郭家锴/Documents/Kimi/Workspaces/算法歧视证据搜集插件")
DECK = ROOT / "deck"
NAV_JSON = ROOT / "shots_work" / "nav_elements.json"

W, H = 960, 540

# ---------------- 元素构造助手 ----------------
_eid = 0
def _id(prefix):
    global _eid
    _eid += 1
    return f"{prefix}{_eid}"

def T(x, y, w, h, text, eid=None, **kw):
    """文本元素"""
    content = {"text": text}
    for k in ["color", "fontSize", "fontFamily", "bold", "italic", "lineHeight",
              "lineHeightPx", "letterSpacing", "align", "wrap", "style",
              "gradient", "shadow", "backgroundColor", "marginTop"]:
        if k in kw and kw[k] is not None:
            content[k] = kw[k]
    el = {"elementId": eid or _id("t"), "elementType": "text",
          "bounds": [x, y, w, h], "content": content}
    return el

def S(x, y, w, h, shape="rect", eid=None, **kw):
    el = {"elementId": eid or _id("s"), "elementType": "shape",
          "bounds": [x, y, w, h], "shapeName": shape}
    for k in ["fill", "border", "shadow", "adjustments", "rotation", "flip",
              "viewBox", "path", "opacity", "arrow"]:
        if k in kw and kw[k] is not None:
            el[k] = kw[k]
    return el

def IMG(x, y, w, h, src, eid=None, **kw):
    el = {"elementId": eid or _id("img"), "elementType": "image",
          "bounds": [x, y, w, h], "src": src}
    for k in ["fit", "crop", "cropShape", "border", "shadow", "rotation", "opacity", "flip"]:
        if k in kw and kw[k] is not None:
            el[k] = kw[k]
    return el

def ICON(x, y, w, h, name, color="#FFFFFF", eid=None, **kw):
    el = {"elementId": eid or _id("ic"), "elementType": "icon",
          "bounds": [x, y, w, h], "iconName": name,
          "fill": {"type": "solid", "color": color}}
    for k in ["border", "shadow", "rotation", "opacity"]:
        if k in kw and kw[k] is not None:
            el[k] = kw[k]
    return el

def LN(x, y, w, h, pts, vb, eid=None, **kw):
    el = {"elementId": eid or _id("ln"), "elementType": "line",
          "bounds": [x, y, w, h], "viewBox": vb, "points": pts}
    for k in ["curve", "arrow", "border", "shadow", "rotation", "flip", "opacity"]:
        if k in kw and kw[k] is not None:
            el[k] = kw[k]
    return el

def solid(c):
    return {"type": "solid", "color": c}

def grad(angle, *stops):
    return {"type": "gradient", "gradientType": "linear", "angle": angle,
            "stops": [{"position": p, "color": c} for p, c in stops]}

# ---------------- 主题 ----------------
GOLD = "#FFC000"
GOLD_L = "#FFF177"
CYAN = "#38BDF8"
SUB = "#C7D7F2"
DIM = "#8FAADC"
PANEL = "#0C2B66"
INK = "#10275C"

def gold_grad_text():
    return grad(45, (0.12, "#FFF8B9"), (0.41, "#FFF8B9"), (0.71, "#FCC55E"))

def white_grad_text():
    return grad(45, (0.27, "#FFFFFF"), (0.51, "#C3D2EC"))

def gold_grad_title():
    return grad(90, (0.33, "#FFF8B9"), (0.51, "#FFF177"), (0.74, "#FCC55E"))

def num_grad():
    return grad(45, (0.11, "#FBE5D6"), (0.49, "#FEDC6B"), (0.91, "#B25E25"))

TXT_SHADOW = {"blur": 3, "color": "#0000006E", "offset": [2.1213, 2.1213]}

# ---------------- 背景 ----------------
def bg_base():
    """内容页背景：渐变 + 左纹理 + 右上城市图 + 底部网格"""
    return [
        S(0, 0, W, H, fill=grad(90, (0, "#042258"), (1, "#002456")),
          border={"style": "solid", "width": 1, "color": "#0A111D"}, eid="bg_rect"),
        IMG(0.2, -0.7, 453.1, 540, "media/bg_left.png", fit={"mode": "fill"}, eid="bg_left"),
        IMG(343.9, -65.8, 661.8, 440, "media/bg_hwy2.png", fit={"mode": "fill"}, eid="bg_hwy"),
        IMG(0, 46.5, 959.2, 493.5, "media/bg_grid.png", fit={"mode": "fill"}, eid="bg_grid"),
    ]

# ---------------- 顶部导航 ----------------
TABS = ["项目缘起", "项目创新", "个人成长", "产业价值", "团队协作", "未来规划"]
TAB_CENTERS = [96.95, 193.35, 289.75, 663.25, 759.65, 856.05]

def nav(page_title, active=0):
    """模板导航栏：6 个章节 tab + 中央页标题。active=1..6，0 表示无高亮"""
    nav_els = json.load(open(NAV_JSON, encoding="utf-8"))
    out = []
    skip_ids = {"文本框 128", "文本框 129", "文本框 130", "文本框 131", "文本框 132",
                "文本框 133", "文本框 124-text", "文本框 124-shape"}
    for el in nav_els:
        if el["elementId"] in ("矩形 7", "Picture 47", "Picture 111", "Picture 3"):
            continue  # 背景由 bg_base 提供
        if el["elementId"] in skip_ids:
            continue
        out.append(el)
    # 中央标题底板与文字（加宽以容纳长标题）
    tw = max(150, len(page_title) * 20 + 40)
    tx = (W - tw) / 2
    out.append(S(tx, 5.8, tw, 36.4, shadow={"blur": 10, "color": "#223962", "offset": [0, 4]}, eid="nav_ts"))
    out.append(T(tx, 5.8, tw, 36.4, f"<p>{page_title}</p>", eid="nav_tt",
                 fontSize=20, color="#FFFFFF", bold=True, wrap=False,
                 align=["center", "middle"], shadow=TXT_SHADOW))
    # 6 个 tab 文本
    for i, name in enumerate(TABS):
        cx = TAB_CENTERS[i]
        is_act = (active == i + 1)
        out.append(T(cx - 40, 22.7, 80, 19.5, f"<p>{name}</p>", eid=f"nav_tab{i+1}",
                     fontSize=13, color=GOLD if is_act else "#FFFFFF",
                     bold=is_act, wrap=False, align=["center", "middle"]))
    # 高亮当前 tab 的底块
    if 1 <= active <= 6:
        cx = TAB_CENTERS[active - 1]
        out.append(S(cx - 45, 21.5, 90, 20, shape="roundRect", adjustments=[50000],
                     fill=solid("#FFC00022"), border={"style": "solid", "width": 1, "color": GOLD},
                     eid="nav_act"))
    return out

# ---------------- 通用组件 ----------------
def page_title_bar(text, sub=None, y=56):
    """页内大标题（导航下方）：左侧金色竖条 + 标题"""
    els = [
        S(40, y + 4, 6, 26, fill=solid(GOLD), eid="ptb_bar"),
        T(56, y, 700, 34, f"<p>{text}</p>", eid="ptb_t",
          fontSize=24, color="#FFFFFF", bold=True, wrap=False, align=["left", "middle"]),
    ]
    if sub:
        els.append(T(56, y + 32, 860, 20, f"<p>{sub}</p>", eid="ptb_s",
                     fontSize=12, color=SUB, wrap=False, align=["left", "middle"]))
    return els

def panel(x, y, w, h, fill="#0C2B66CC", border_c="#2D4E8F", r=12000, eid=None):
    return S(x, y, w, h, shape="roundRect", adjustments=[r],
             fill=solid(fill), border={"style": "solid", "width": 1, "color": border_c},
             eid=eid or _id("pn"))

def kpi(x, y, w, h, num, unit, label, sub=None, num_color=GOLD):
    """大数字卡片"""
    els = [panel(x, y, w, h, eid=_id("kpi"))]
    els.append(T(x + 14, y + 12, w - 28, 40,
                 f'<p><span style="font-size:34px;color:{num_color}"><strong>{num}</strong></span>'
                 f'<span style="font-size:14px;color:{SUB}"> {unit}</span></p>',
                 fontSize=34, wrap=False, align=["left", "middle"]))
    els.append(T(x + 14, y + h - 30, w - 28, 20, f"<p>{label}</p>",
                 fontSize=13, color="#FFFFFF", bold=True, wrap=False, align=["left", "middle"]))
    if sub:
        els.append(T(x + 14, y + h - 48, w - 28, 16, f"<p>{sub}</p>",
                     fontSize=10, color=DIM, wrap=False, align=["left", "middle"]))
    return els

def chip(x, y, text, color=GOLD, w=None, icon=None):
    """小标签"""
    w = w or (len(text) * 14 + 24)
    return [
        S(x, y, w, 24, shape="roundRect", adjustments=[50000],
          fill=solid(color + "22"), border={"style": "solid", "width": 1, "color": color}),
        T(x, y, w, 24, f"<p>{text}</p>", fontSize=12, color=color, bold=True,
          wrap=False, align=["center", "middle"]),
    ]

def feature_row(x, y, w, icon, title, desc, num=None, h=64):
    """图标 + 标题 + 描述 横条"""
    els = []
    els.append(S(x, y, h - 16, h - 16, shape="roundRect", adjustments=[24000],
                 fill=solid("#123C8F"), border={"style": "solid", "width": 1, "color": "#3B82F6"}))
    els.append(ICON(x + (h - 16) / 2 - 11, y + (h - 16) / 2 - 11, 22, 22, icon, CYAN))
    tx = x + h
    els.append(T(tx, y, w - h, 22, f"<p><strong>{title}</strong></p>",
                 fontSize=15, color="#FFFFFF", wrap=False, align=["left", "middle"]))
    els.append(T(tx, y + 24, w - h, h - 28, f"<p>{desc}</p>",
                 fontSize=11.5, color=SUB, lineHeight=1.4, align=["left", "top"]))
    if num:
        els.append(T(x + w - 44, y - 4, 44, 30, f"<p>{num}</p>",
                     fontSize=22, color=GOLD, bold=True, wrap=False, align=["right", "middle"]))
    return els

def glow_deco(x, y, w, h):
    """蓝色发光底座装饰"""
    return IMG(x, y, w, h, "media/glow.png", fit={"mode": "fill"}, opacity=0.8)
