# -*- coding: utf-8 -*-
"""页面骨架：封面 / 目录 / 章节页 / 尾页"""
from core import *

# ---------------- 封面 ----------------
def cover_page():
    els = bg_base()
    # 芯片主视觉（右侧）
    els.append(IMG(430, 60, 530, 420, "media/bg_chip.png", fit={"mode": "cover"},
                   opacity=0.9, eid="cv_chip"))
    # 顶部大赛横幅
    els += [
        S(40, 26, 396, 34, shape="roundRect", adjustments=[50000],
          fill=solid("#123C8FCC"), border={"style": "solid", "width": 1, "color": "#3B82F6"}, eid="cv_bn"),
        ICON(56, 33, 20, 20, "fas:trophy", GOLD, eid="cv_bn_i"),
        T(84, 26, 344, 34, "<p>中国国际大学生创新大赛（2026）</p>", eid="cv_bn_t",
          fontSize=16, color="#FFFFFF", bold=True, wrap=False, align=["left", "middle"]),
    ]
    # 右上校名占位
    els += [
        IMG(838, 22, 40, 40, "media/logo.png", fit={"mode": "contain"}, eid="cv_logo"),
        T(700, 26, 130, 32, "<p>××大学</p>", eid="cv_uni",
          fontSize=16, color="#FFFFFF", bold=True, wrap=False, align=["right", "middle"]),
        T(700, 52, 178, 14, "<p>（替换为学校名称）</p>", eid="cv_uni2",
          fontSize=9, color=DIM, wrap=False, align=["right", "middle"]),
    ]
    # 大标题：算 法 歧 视（歧 金色聚焦）
    F = "飞波正点体"
    els += [
        T(40, 128, 178, 167, "<p>算</p>", eid="cv_c1", fontSize=138, fontFamily=F,
          gradient=white_grad_text(), shadow=TXT_SHADOW, wrap=False),
        T(172, 108, 178, 190, "<p>法</p>", eid="cv_c2", fontSize=166, fontFamily=F,
          gradient=white_grad_text(), shadow=TXT_SHADOW, wrap=False),
        T(330, 84, 200, 230, "<p>歧</p>", eid="cv_c3", fontSize=206, fontFamily=F, bold=True,
          gradient=gold_grad_text(), shadow={"blur": 6, "color": "#0000008F", "offset": [3, 3]}, wrap=False),
        T(512, 108, 178, 190, "<p>视</p>", eid="cv_c4", fontSize=166, fontFamily=F,
          gradient=white_grad_text(), shadow=TXT_SHADOW, wrap=False),
    ]
    # 副标题
    els += [
        T(40, 308, 640, 42, "<p>众包观测平台 —— 公益诉讼视角的电商价格歧视取证工具</p>",
          eid="cv_sub", fontSize=24, color="#FFFFFF", bold=True, wrap=False, align=["left", "middle"]),
        T(40, 352, 560, 16, "<p>ALGORITHMIC DISCRIMINATION · CROWDSOURCED OBSERVATORY FOR PUBLIC-INTEREST LITIGATION</p>",
          eid="cv_en", fontSize=8.5, color=DIM, letterSpacing=2.4, wrap=False),
    ]
    # 政策标签条（评审要求：第一页体现国家政策）
    els += [
        S(40, 384, 632, 34, shape="roundRect", adjustments=[50000],
          fill=solid("#FFC00018"), border={"style": "solid", "width": 1.2, "color": GOLD}, eid="cv_pl"),
        ICON(54, 391, 20, 20, "fas:landmark", GOLD, eid="cv_pl_i"),
        T(82, 384, 584, 34,
          "<p>落实《互联网信息服务算法推荐管理规定》 · 响应“十五五”数字经济治理部署 · 守护消费公平</p>",
          eid="cv_pl_t", fontSize=13.5, color=GOLD_L, bold=True, wrap=False, align=["left", "middle"]),
    ]
    # 参赛信息
    els += [
        T(40, 440, 420, 22, "<p>赛　　道：高教主赛道 · 创意组</p>", eid="cv_i1",
          fontSize=15, color="#FFFFFF", bold=True, wrap=False),
        T(40, 468, 420, 22, "<p>项目类型：公益诉讼 · 数字治理 · 平台经济</p>", eid="cv_i2",
          fontSize=15, color="#FFFFFF", bold=True, wrap=False),
        T(40, 496, 420, 22, "<p>负 责 人：×××（替换姓名）</p>", eid="cv_i3",
          fontSize=15, color="#FFFFFF", bold=True, wrap=False),
    ]
    return els

# ---------------- 目录 ----------------
TOC = [
    ("壹", "项目缘起", "政策背景 · 社会痛点 · 深入调研", "04"),
    ("贰", "项目创新", "解决方案 · 四大创新 · 产品演示", "11"),
    ("叁", "个人成长", "立德树人 · 知识转化 · 育人成效", "24"),
    ("肆", "产业价值", "产业认知 · 商业模式 · 社会影响", "31"),
    ("伍", "团队协作", "团队结构 · 成员分工 · 专家资源", "39"),
    ("陆", "未来规划", "路线图 · 风险应对 · 材料承诺", "44"),
]

def toc_page():
    els = bg_base() + nav("目录 CONTENTS", 0)
    els += page_title_bar("目录", "CONTENTS · 全文导航", y=54)
    x0, y0, cw, ch, gx, gy = 52, 118, 268, 118, 24, 22
    for i, (num, name, desc, pg) in enumerate(TOC):
        x = x0 + (i % 3) * (cw + gx)
        y = y0 + (i // 3) * (ch + gy)
        els.append(panel(x, y, cw, ch, fill="#0C2B66E6", border_c="#2D4E8F", eid=f"toc_p{i}"))
        els.append(T(x + 18, y + 14, 60, 56, f"<p>{num}</p>", eid=f"toc_n{i}",
                     fontSize=40, fontFamily="飞波正点体", gradient=num_grad(), wrap=False))
        els.append(T(x + 74, y + 18, cw - 90, 30, f"<p><strong>{name}</strong></p>", eid=f"toc_t{i}",
                     fontSize=20, color="#FFFFFF", wrap=False, align=["left", "middle"]))
        els.append(T(x + 74, y + 50, cw - 90, 18, f"<p>{desc}</p>", eid=f"toc_d{i}",
                     fontSize=10.5, color=SUB, wrap=False, align=["left", "middle"]))
        els.append(S(x + 18, y + 82, cw - 36, 1.5, fill=solid("#2D4E8F"), eid=f"toc_l{i}"))
        els.append(T(x + 18, y + 90, cw - 36, 20,
                     f'<p><span style="color:{GOLD}">P{pg}</span><span style="color:{DIM}">　→</span></p>',
                     eid=f"toc_pg{i}", fontSize=12, wrap=False, align=["left", "middle"]))
    return els

# ---------------- 章节页 ----------------
def divider_page(num_cn, title, en, active, deco_icon="fas:compass"):
    els = bg_base() + nav(f"第{num_cn}章 · {title}", active)
    # 底部发光台
    els.append(glow_deco(240, 420, 480, 100))
    # 左侧巨大章节数字
    els.append(T(84, 66, 300, 360, f"<p>{num_cn}</p>", eid="dv_num",
                 fontSize=287, fontFamily="飞波正点体", gradient=num_grad(),
                 shadow={"blur": 20, "color": "#773F194D", "offset": [9.19, 9.19]}, wrap=False))
    # 右侧标题
    els.append(T(430, 196, 480, 76, f"<p>{title}</p>", eid="dv_t",
                 fontSize=56, fontFamily="飞波正点体", bold=True,
                 gradient=gold_grad_title(), wrap=False, align=["left", "middle"]))
    # 英文
    els.append(T(432, 280, 470, 24, f"<p>{en}</p>", eid="dv_en",
                 fontSize=13, color=SUB, letterSpacing=2, wrap=False))
    # 装饰线
    els.append(LN(432, 322, 440, 12, "0,6 200,6 220,0 240,12 260,6 440,6", [440, 12],
                  curve="sharp", border={"style": "solid", "width": 1.5, "color": DIM}, eid="dv_ln"))
    return els

# ---------------- 尾页 ----------------
def final_page():
    els = bg_base()
    els.append(IMG(280, 40, 400, 400, "media/globe.png", fit={"mode": "contain"}, opacity=0.5, eid="fn_gl"))
    els.append(glow_deco(280, 400, 400, 80))
    els += [
        T(180, 150, 600, 90, "<p>让算法在阳光下运行</p>", eid="fn_t1",
          fontSize=52, fontFamily="飞波正点体", bold=True, gradient=gold_grad_title(),
          wrap=False, align=["center", "middle"]),
        T(180, 246, 600, 30, "<p>以众包数据守护消费公平 · 以青年力量助力算法治理</p>", eid="fn_t2",
          fontSize=18, color="#FFFFFF", wrap=False, align=["center", "middle"]),
        T(180, 300, 600, 20, "<p>MAKE ALGORITHMS ACCOUNTABLE · 谢谢聆听，恳请各位专家批评指正</p>",
          eid="fn_t3", fontSize=12, color=SUB, wrap=False, align=["center", "middle"]),
    ]
    els += [
        S(330, 352, 300, 40, shape="roundRect", adjustments=[50000],
          fill=solid("#123C8FCC"), border={"style": "solid", "width": 1, "color": "#3B82F6"}, eid="fn_badge"),
        T(330, 352, 300, 40, "<p>算法歧视众包观测平台 · 项目组</p>", eid="fn_badge_t",
          fontSize=15, color=GOLD_L, bold=True, wrap=False, align=["center", "middle"]),
    ]
    return els
