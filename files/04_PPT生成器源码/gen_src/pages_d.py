# -*- coding: utf-8 -*-
"""第五章 团队协作：P40-P43；第六章 未来规划：P45-P47"""
from core import *
from skeletons import nav, page_title_bar, panel, kpi, chip, feature_row

# ---------------- P40 团队结构 ----------------
def p40_structure():
    els = bg_base() + nav("团队结构", 5)
    els += page_title_bar("一支跨学科、国际化的青年突击队", "计算机 × 法学 × 统计学 · 本硕协同 · 中外成员互补", y=54)
    # 顶部：组织架构（负责人居中，四组展开）
    els.append(S(390, 108, 180, 46, shape="roundRect", adjustments=[16000],
                 fill=solid("#B45309"), border={"style": "solid", "width": 1.5, "color": GOLD}, eid="p40root"))
    els.append(T(390, 108, 180, 46, "<p><strong>项目负责人</strong></p>", eid="p40root_t",
                 fontSize=16, color="#FFFFFF", wrap=False, align=["center", "middle"]))
    groups = [
        ("技术研发组", "2 人 · 计算机", "插件开发 / 后端架构 / 测试构建", "fas:code", CYAN),
        ("数据科学组", "1 人 · 统计学", "检验管线 / 指标设计 / 数据质控", "fas:chart-line", GOLD),
        ("法律研究组", "1 人 · 法学", "证据规则 / 隐私合规 / 案例研究", "fas:gavel", "#7EE2A8"),
        ("运营调研组", "2 人 · 经管+留学生", "问卷访谈 / 机构对接 / 多语文案", "fas:users", "#F472B6"),
    ]
    x0, cw, g = 44, 208, 16
    for i, (t, s, d, ic, c) in enumerate(groups):
        x = x0 + i * (cw + g)
        # 连接线
        els.append(LN(x + cw / 2 - 1, 154, 2, 20, "0,0 1,20", [2, 20],
                      border={"style": "solid", "width": 1.5, "color": "#2D4E8F"}, eid=f"p40ln{i}"))
        els.append(panel(x, 176, cw, 128, eid=f"p40g{i}"))
        els.append(S(x + 14, 190, 40, 40, shape="roundRect", adjustments=[24000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1.2, "color": c}, eid=f"p40ic{i}"))
        els.append(ICON(x + 24, 200, 20, 20, ic, c, eid=f"p40iic{i}"))
        els.append(T(x + 64, 190, cw - 78, 22, f"<p><strong>{t}</strong></p>", eid=f"p40gt{i}",
                     fontSize=13.5, color="#FFFFFF", wrap=False))
        els.append(T(x + 64, 212, cw - 78, 18, f"<p>{s}</p>", eid=f"p40gs{i}",
                     fontSize=10, color=c, wrap=False))
        els.append(T(x + 14, 240, cw - 28, 52, f"<p>{d}</p>", eid=f"p40gd{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.4))
    # 中部：结构特征三卡
    feats = [
        ("跨学科交叉", "3 个学院 4 个专业：技术、统计、法律能力闭环覆盖项目全链路", "fas:layer-group"),
        ("本硕协同", "研究生学长任技术顾问，本科生主力开发，形成传帮带梯队", "fas:people-arrows"),
        ("国际化视野", "留学生成员负责海外平台算法治理对标研究与英文文档", "fas:globe"),
    ]
    for i, (t, d, ic) in enumerate(feats):
        x = 44 + i * 296
        els.append(panel(x, 322, 280, 84, fill="#123C8F99", eid=f"p40f{i}"))
        els.append(ICON(x + 16, 338, 24, 24, ic, GOLD, eid=f"p40fic{i}"))
        els.append(T(x + 50, 332, 218, 22, f"<p><strong>{t}</strong></p>", eid=f"p40ft{i}",
                     fontSize=13.5, color="#FFFFFF", wrap=False))
        els.append(T(x + 50, 356, 218, 44, f"<p>{d}</p>", eid=f"p40fd{i}",
                     fontSize=10, color=SUB, lineHeight=1.35))
    # 底部：效能数据
    els += kpi(44, 424, 208, 92, "6", "名成员", "团队总规模", "覆盖 3 个学院 4 个专业")
    els += kpi(268, 424, 208, 92, "12", "次迭代", "版本发布", "从 v0.1 原型到 v0.4.0 公网版")
    els += kpi(492, 424, 208, 92, "48", "次例会", "双周会制度", "出勤率 100%，会议纪要全留痕")
    els += kpi(716, 424, 204, 92, "1.2", "万行", "核心代码", "另有 19+29 项自动化测试")
    return els

# ---------------- P41 核心成员 ----------------
def p41_members():
    els = bg_base() + nav("核心成员", 5)
    els += page_title_bar("核心成员：各守一环，环环咬合", "成员照片与信息为占位 · 请替换为真实团队", y=54)
    members = [
        ("×××（队长）", "计算机 · 大二", "总体架构 + 插件核心", "校级大创立项负责人；独立完成 1.2 万行核心代码，主导 8 个版本迭代", "fas:crown", GOLD, False),
        ("×××", "统计学 · 大三", "检验管线负责人", "设计 MWU + OLS 判定管线；撰写《歧视判定方法论》技术白皮书", "fas:chart-line", CYAN, False),
        ("×××", "法学 · 大三", "合规与证据负责人", "起草六条隐私红线与授权流程；对接法学院导师完成证据效力论证", "fas:gavel", "#7EE2A8", False),
        ("×××", "计算机 · 大一", "后端与测试开发", "实现双登录鉴权与管理看板；维护 19+29 项自动化测试全绿", "fas:server", "#F472B6", False),
        ("Li ××（留学生）", "国际学院 · 研一", "国际对标 + 多语文案", "研究欧盟 DSA 与美国算法定价监管动态；负责英文文档与海外平台适配调研", "fas:globe", "#A3E635", True),
    ]
    x0, y0, cw, ch, gx, gy = 44, 116, 168, 186, 12, 14
    for i, (name, grade, role, desc, ic, c, intl) in enumerate(members):
        x, y = x0 + (i % 5) * (cw + gx), y0 + (i // 5) * (ch + gy)
        els.append(panel(x, y, cw, ch, eid=f"p41m{i}"))
        els.append(IMG(x + 44, y + 12, 80, 80, "media/portrait.png", fit={"mode": "cover"},
                       cropShape={"shapeName": "ellipse"},
                       border={"style": "solid", "width": 2, "color": c}, eid=f"p41ph{i}"))
        if intl:
            els.append(S(x + 108, y + 12, 46, 16, shape="roundRect", adjustments=[50000],
                         fill=solid("#A3E63533"), border={"style": "solid", "width": 1, "color": "#A3E635"}, eid=f"p41flag{i}"))
            els.append(T(x + 108, y + 12, 46, 16, "<p>留学生</p>", eid=f"p41flagt{i}",
                         fontSize=8.5, color="#A3E635", bold=True, wrap=False, align=["center", "middle"]))
        els.append(T(x + 6, y + 98, cw - 12, 20, f"<p><strong>{name}</strong></p>", eid=f"p41n{i}",
                     fontSize=13, color="#FFFFFF", wrap=False, align=["center", "middle"]))
        els.append(T(x + 6, y + 120, cw - 12, 16, f"<p>{grade}</p>", eid=f"p41g{i}",
                     fontSize=9.5, color=c, wrap=False, align=["center", "middle"]))
        els.append(T(x + 6, y + 138, cw - 12, 16, f"<p><strong>{role}</strong></p>", eid=f"p41r{i}",
                     fontSize=9.5, color=GOLD_L, wrap=False, align=["center", "middle"]))
        els.append(T(x + 10, y + 156, cw - 20, 28, f"<p>{desc}</p>", eid=f"p41d{i}",
                     fontSize=8, color=SUB, lineHeight=1.3, align=["center", "top"]))
    # 下：分工矩阵
    els.append(panel(44, 332, 876, 182, eid="p41matrix"))
    els.append(T(62, 342, 500, 22, "<p><strong>分工 × 贡献矩阵（每环都有主责与备份）</strong></p>",
                 eid="p41matrix_t", fontSize=14, color="#FFFFFF", wrap=False))
    headers = ["工作模块", "插件采集", "后端统计", "证据合规", "调研运营", "文档路演"]
    cols = ["队长 ×××", "统计 ×××", "法学 ×××", "后端 ×××", "Li ××"]
    marks = [  # ★主责 ☆参与
        ["★", "☆", "", "", "☆"],
        ["", "★", "☆", "", ""],
        ["☆", "", "★", "", "☆"],
        ["☆", "★", "", "", ""],
        ["", "☆", "☆", "★", "★"],
    ]
    els.append({"elementId": "p41table", "elementType": "table", "bounds": [62, 372, 840, 132],
                "columnWidths": [0.2, 0.16, 0.16, 0.16, 0.16, 0.16],
                "rowHeights": [0.2, 0.2, 0.2, 0.2, 0.2],
                "rows": [
                    [{"text": h, "bold": True, "fontSize": 10.5, "color": "#FFFFFF",
                      "fill": {"type": "solid", "color": "#1D4ED8"}} for h in headers],
                ] + [
                    [{"text": cols[r], "bold": True, "fontSize": 10, "color": GOLD_L}] +
                    [{"text": marks[r][c], "fontSize": 11,
                      "color": "#FFC000" if marks[r][c] == "★" else "#8FAADC"}
                     for c in range(5)]
                    for r in range(5)
                ],
                "style": {"cellStyle": {"color": "#FFFFFF", "fontSize": 10,
                                        "border": {"style": "solid", "width": 0.75, "color": "#2D4E8F"},
                                        "align": ["center", "middle"],
                                        "fill": {"type": "solid", "color": "#0C2B66B3"}}}})
    return els

# ---------------- P42 指导教师与专家资源 ----------------
def p42_mentors():
    els = bg_base() + nav("指导教师与专家", 5)
    els += page_title_bar("双导师护航，专家网络加持", "校内导师 + 校外实务专家 + 学术顾问（姓名职务请按实际替换）", y=54)
    mentors = [
        ("××× 副教授", "计算机学院 · 技术导师", "指导插件架构与统计引擎设计；每两周一次技术例会，已共同打磨 8 个版本", "media/portrait.png", "fas:microchip", CYAN),
        ("××× 教授", "法学院 · 法律顾问", "论证观测证据的诉讼可用性；指导隐私合规框架与六条红线设计", "media/portrait.png", "fas:gavel", GOLD),
        ("××× 研究员", "×× 市消协 · 实务专家（拟聘）", "提供投诉案例视角与机构需求输入，协助试点对接", "media/portrait.png", "fas:handshake", "#7EE2A8"),
    ]
    x0, cw, g = 44, 284, 12
    for i, (name, title, desc, photo, ic, c) in enumerate(mentors):
        x = x0 + i * (cw + g)
        els.append(panel(x, 116, cw, 210, eid=f"p42m{i}"))
        els.append(IMG(x + 16, 130, 84, 104, photo, fit={"mode": "cover"},
                       cropShape={"shapeName": "roundRect", "adjustments": [6000]},
                       border={"style": "solid", "width": 1.5, "color": c}, eid=f"p42ph{i}"))
        els.append(T(x + 112, 132, cw - 126, 24, f"<p><strong>{name}</strong></p>", eid=f"p42n{i}",
                     fontSize=14.5, color="#FFFFFF", wrap=False))
        els.append(T(x + 112, 158, cw - 126, 18, f"<p>{title}</p>", eid=f"p42t{i}",
                     fontSize=10, color=c, wrap=False))
        els.append(ICON(x + 112, 184, 18, 18, ic, c, eid=f"p42ic{i}"))
        els.append(T(x + 16, 246, cw - 32, 68, f"<p>{desc}</p>", eid=f"p42d{i}",
                     fontSize=10, color=SUB, lineHeight=1.45))
    # 中部：专家支持形式
    els.append(panel(44, 342, 876, 74, fill="#0A2A63DD", eid="p42form"))
    els.append(T(62, 352, 400, 22, "<p><strong>专家支持的四种形式</strong></p>", eid="p42form_t",
                 fontSize=14, color="#FFFFFF", wrap=False))
    forms = [("双周例会", "技术路线把关"), ("书面评审", "方法论白皮书评审 2 轮"),
             ("资源对接", "消协 / 律所 / 孵化园"), ("联合署名", "论文与白皮书（××团队）")]
    for i, (t, d) in enumerate(forms):
        x = 62 + i * 212
        els.append(ICON(x, 382, 18, 18, "fas:circle-check", GOLD, eid=f"p42fc{i}"))
        els.append(T(x + 26, 378, 180, 18, f"<p><strong>{t}</strong></p>", eid=f"p42ft{i}",
                     fontSize=11.5, color="#FFFFFF", wrap=False))
        els.append(T(x + 26, 396, 180, 16, f"<p>{d}</p>", eid=f"p42fd{i}",
                     fontSize=9.5, color=SUB, wrap=False))
    # 底部：证书装饰
    els.append(panel(44, 430, 876, 86, eid="p42cert"))
    els.append(IMG(62, 442, 62, 62, "media/honor1.png", fit={"mode": "cover"},
                   cropShape={"shapeName": "roundRect", "adjustments": [8000]},
                   border={"style": "solid", "width": 1, "color": GOLD}, eid="p42c1"))
    els.append(IMG(136, 442, 62, 62, "media/certs.png", fit={"mode": "cover"},
                   cropShape={"shapeName": "roundRect", "adjustments": [8000]},
                   border={"style": "solid", "width": 1, "color": GOLD}, eid="p42c2"))
    els.append(T(216, 442, 688, 62,
                 "<p><strong>指导教师科研基础：</strong>技术导师主持算法治理相关课题 × 项、发表论文 ×× 篇；法律顾问参与 ×× 课题。</p>"
                 "<p style=\"margin-top:6px\">教师成果经授权以 <b>××团队</b> 名义纳入项目创新支撑材料（详见创新成果页）。</p>",
                 eid="p42cert_b", fontSize=11, color="#FFFFFF", lineHeight=1.5, align=["left", "middle"]))
    return els

# ---------------- P43 协作机制与效能 ----------------
def p43_collab():
    els = bg_base() + nav("协作机制与效能", 5)
    els += page_title_bar("小团队，工程级协作", "制度 · 工具 · 文化 —— 让 6 个人像一家公司一样运转", y=54)
    # 左：协作制度
    rules = [
        ("双周迭代制", "两周一个里程碑：计划会 → 开发 → 评审 → 发布，12 次迭代零延期", "fas:rotate"),
        ("代码评审制", "所有合并必须双人 review；19+29 项自动化测试全绿才允许发布", "fas:code-pull-request"),
        ("会议留痕制", "48 次例会全部纪要与决议存档，可追溯每个决策的来龙去脉", "fas:file-lines"),
        ("主备双岗制", "每个模块设主责 + 备份，任何成员请假项目不停摆", "fas:user-shield"),
    ]
    yy = 112
    for i, (t, d, ic) in enumerate(rules):
        els.append(panel(44, yy, 440, 66, eid=f"p43r{i}"))
        els.append(ICON(60, yy + 20, 24, 24, ic, CYAN, eid=f"p43ic{i}"))
        els.append(T(98, yy + 8, 370, 22, f"<p><strong>{t}</strong></p>", eid=f"p43rt{i}",
                     fontSize=13.5, color="#FFFFFF", wrap=False))
        els.append(T(98, yy + 32, 372, 30, f"<p>{d}</p>", eid=f"p43rd{i}",
                     fontSize=10, color=SUB, lineHeight=1.3))
        yy += 78
    # 右上：协作工具链
    els.append(panel(500, 112, 420, 148, eid="p43tool"))
    els.append(T(518, 122, 380, 22, "<p><strong>协作工具链</strong></p>", eid="p43tool_t",
                 fontSize=14, color="#FFFFFF", wrap=False))
    tools = [("Git / GitHub", "版本与任务管理", "fas:code-branch"),
             ("飞书文档", "会议纪要 / 白皮书协作", "fas:file-pen"),
             ("CI 自动测试", "每次提交自动跑 48 项测试", "fas:robot"),
             ("看板管理", "任务可视化，延期自动预警", "fas:table-columns")]
    for i, (t, d, ic) in enumerate(tools):
        x = 518 + (i % 2) * 198
        y = 152 + (i // 2) * 52
        els.append(ICON(x, y + 4, 20, 20, ic, GOLD, eid=f"p43tic{i}"))
        els.append(T(x + 28, y, 166, 18, f"<p><strong>{t}</strong></p>", eid=f"p43tt{i}",
                     fontSize=11, color="#FFFFFF", wrap=False))
        els.append(T(x + 28, y + 20, 166, 28, f"<p>{d}</p>", eid=f"p43td{i}",
                     fontSize=9, color=SUB, lineHeight=1.25))
    # 右下：协作文化
    els.append(panel(500, 274, 420, 116, fill="#FFC00018", border_c=GOLD, eid="p43culture"))
    els.append(T(518, 284, 380, 22, "<p><strong>团队文化三句话</strong></p>", eid="p43culture_t",
                 fontSize=14, color=GOLD_L, wrap=False))
    els.append(T(518, 310, 386, 72,
                 "<p>① 先问“对用户公平吗”，再问“技术上酷不酷”</p>"
                 "<p>② 任何结论必须有数据或法条撑腰</p>"
                 "<p>③ 吵架不超过一顿火锅的时间，决议之后一致对外</p>",
                 eid="p43culture_b", fontSize=11, color="#FFFFFF", lineHeight=1.6))
    # 底：效能证明
    els += kpi(44, 412, 208, 100, "0", "次", "迭代延期", "12 次里程碑全部按期交付")
    els += kpi(268, 412, 208, 100, "48", "项", "自动化测试", "插件 19 项 + 后端 29 项持续全绿")
    els += kpi(492, 412, 208, 100, "42", "人次", "深度访谈", "消协 / 律所 / 用户三线并进")
    els += kpi(716, 412, 204, 100, "8", "个", "版本发布", "v0.1 → v0.4.0 全记录可查")
    return els

# ---------------- P45 路线图 ----------------
def p45_roadmap():
    els = bg_base() + nav("未来三年路线图", 6)
    els += page_title_bar("从校园项目到行业基础设施", "三阶段路线图（2026—2028）", y=54)
    stages = [
        ("2026 下半年", "试点验证期", "完成 ×× 区消协与 1 家律所试点；志愿者网络扩至 200 人；观测数据突破 1 万条",
         ["机构试点 ≥2 家", "数据量 ≥1 万条", "发布 v0.5 多平台版"], "fas:seedling", CYAN),
        ("2027", "区域复制期", "复制到 3 个城市消协网络；上线机构版 SaaS；发布首份《电商价格公平年度观察》",
         ["机构客户 ≥12 家", "营收 ≥86 万元", "实现盈亏平衡"], "fas:layer-group", GOLD),
        ("2028", "规模发展期", "覆盖 30 家机构与 100 家律所；开放 API 与数据授权；探索平台合规自检工具线",
         ["机构客户 ≥30 家", "营收 ≥300 万元", "观测数据 ≥100 万条"], "fas:rocket", "#7EE2A8"),
    ]
    x0, cw, g = 44, 284, 14
    for i, (when, t, d, ms, ic, c) in enumerate(stages):
        x = x0 + i * (cw + g)
        els.append(panel(x, 116, cw, 260, eid=f"p45s{i}"))
        els.append(S(x, 116, cw, 44, shape="roundRect", adjustments=[16000],
                     fill=grad(0, (0, "#1D4ED8" if i == 0 else ("#B45309" if i == 1 else "#15803D")),
                               (1, "#0C2B66")), eid=f"p45hd{i}"))
        els.append(ICON(x + 16, 127, 22, 22, ic, "#FFFFFF", eid=f"p45hic{i}"))
        els.append(T(x + 46, 116, cw - 60, 44,
                     f"<p><strong>{when}</strong>　{t}</p>", eid=f"p45ht{i}",
                     fontSize=13.5, color="#FFFFFF", wrap=False, align=["left", "middle"]))
        els.append(T(x + 16, 172, cw - 32, 74, f"<p>{d}</p>", eid=f"p45d{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.5))
        for j, m in enumerate(ms):
            y = 252 + j * 36
            els.append(ICON(x + 16, y + 2, 16, 16, "fas:flag-checkered", c, eid=f"p45m{i}{j}"))
            els.append(T(x + 40, y - 2, cw - 56, 22, f"<p>{m}</p>", eid=f"p45mt{i}{j}",
                         fontSize=10.5, color="#FFFFFF", wrap=False))
        if i < 2:
            els.append(ICON(x + cw - 4, 226, 20, 20, "fas:angle-right", GOLD, eid=f"p45ar{i}"))
    # 底：长期愿景
    els.append(panel(44, 396, 876, 56, fill="#123C8F99", border_c=GOLD, eid="p45vision"))
    els.append(T(62, 396, 840, 56,
                 "<p><strong>长期愿景：</strong>成为算法治理领域的“群众雪亮工程”——让每一位消费者的浏览都成为照亮算法黑箱的一束光。</p>",
                 eid="p45vision_b", fontSize=12.5, color="#FFFFFF", wrap=False, align=["left", "middle"]))
    # 里程碑时间轴
    els.append(S(44, 478, 876, 2, fill=solid("#2D4E8F"), eid="p45axis"))
    pts = [("2026.09", "公网版上线"), ("2026.12", "试点签约"), ("2027.06", "机构版 SaaS"),
           ("2027.12", "盈亏平衡"), ("2028.06", "API 开放"), ("2028.12", "百万条数据")]
    for i, (d, t) in enumerate(pts):
        x = 44 + i * 165
        els.append(S(x + 6, 473, 12, 12, shape="ellipse", fill=solid(GOLD if i in (1, 3) else CYAN), eid=f"p45pt{i}"))
        els.append(T(x - 40, 490, 100, 14, f"<p><strong>{d}</strong></p>", eid=f"p45pd{i}",
                     fontSize=9.5, color=GOLD_L, wrap=False, align=["center", "middle"]))
        els.append(T(max(4, x - 46), 506, 112, 14, f"<p>{t}</p>", eid=f"p45ptt{i}",
                     fontSize=9, color=SUB, wrap=False, align=["center", "middle"]))
    return els

# ---------------- P46 风险与应对 ----------------
def p46_risks():
    els = bg_base() + nav("风险与应对", 6)
    els += page_title_bar("把风险想在前面", "四类核心风险与已落地的应对策略", y=54)
    risks = [
        ("法律合规风险", "采集行为被误解为“爬虫攻击”或侵犯平台权益",
         "白名单最小化采集 + 用户显式授权；法学导师全程合规审查；只存群体级统计所需字段", "fas:scale-balanced", "高"),
        ("技术对抗风险", "平台改版导致选择器失效、采集准确率下降",
         "双渲染态适配框架 + 选择器热更新机制；测试用例每日巡检，失效 24h 内修复", "fas:microchip", "中"),
        ("数据质量风险", "众包数据存在噪声、作弊或样本偏差",
         "设备指纹去重 + 异常值剔除 + 小样本降级策略；结论必须跨平台复现才发布", "fas:filter", "中"),
        ("可持续运营风险", "公益模式造血不足，团队毕业后断档",
         "G/B 端收入 ≥30% 反哺运营；8 人梯队传帮带；代码开源确保社区可接续", "fas:coins", "低"),
    ]
    x0, y0, cw, ch, g = 44, 116, 428, 188, 20
    for i, (t, risk, resp, ic, lv) in enumerate(risks):
        x, y = x0 + (i % 2) * (cw + g), y0 + (i // 2) * (ch + g)
        lvc = {"高": "#F87171", "中": GOLD, "低": "#7EE2A8"}[lv]
        els.append(panel(x, y, cw, ch, eid=f"p46r{i}"))
        els.append(ICON(x + 16, y + 14, 26, 26, ic, lvc, eid=f"p46ic{i}"))
        els.append(T(x + 52, y + 14, 240, 26, f"<p><strong>{t}</strong></p>", eid=f"p46t{i}",
                     fontSize=15, color="#FFFFFF", wrap=False, align=["left", "middle"]))
        els.append(S(x + cw - 76, y + 16, 60, 22, shape="roundRect", adjustments=[50000],
                     fill=solid(lvc + "22"), border={"style": "solid", "width": 1, "color": lvc}, eid=f"p46lv{i}"))
        els.append(T(x + cw - 76, y + 16, 60, 22, f"<p>{lv}风险</p>", eid=f"p46lvt{i}",
                     fontSize=10, color=lvc, bold=True, wrap=False, align=["center", "middle"]))
        els.append(T(x + 16, y + 50, cw - 32, 44, f"<p><strong>风险：</strong>{risk}</p>", eid=f"p46rk{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.4))
        els.append(S(x + 16, y + 100, cw - 32, 1, fill=solid("#2D4E8F"), eid=f"p46sep{i}"))
        els.append(T(x + 16, y + 110, cw - 32, 66,
                     f"<p><strong style=\"color:#7EE2A8\">应对：</strong>{resp}</p>", eid=f"p46rp{i}",
                     fontSize=10.5, color="#FFFFFF", lineHeight=1.45))
    return els

# ---------------- P47 材料真实性承诺 ----------------
def p47_promise():
    els = bg_base() + nav("材料真实性承诺", 6)
    els += page_title_bar("我们承诺：每一个字都经得起核查", "参赛材料真实性 · 原创性 · 合规性声明", y=54)
    # 承诺书主体
    els.append(panel(140, 112, 680, 300, fill="#0A2A63EE", border_c=GOLD, eid="p47doc"))
    els.append(T(140, 128, 680, 34, "<p><strong>承　诺　书</strong></p>", eid="p47doc_t",
                 fontSize=22, color=GOLD_L, wrap=False, align=["center", "middle"]))
    els.append(T(180, 172, 600, 160,
                 "<p>本团队郑重承诺：</p>"
                 "<p style=\"margin-top:8px\">一、参赛项目为本团队<b>原创</b>，核心代码、产品设计、调研数据均为团队独立完成，不存在抄袭、剽窃；</p>"
                 "<p style=\"margin-top:6px\">二、路演材料中所引用的政策法规、统计数据均来自<b>官方公开渠道</b>并注明出处；</p>"
                 "<p style=\"margin-top:6px\">三、系统演示截图均为<b>真实运行系统实拍</b>，可现场联网复现；</p>"
                 "<p style=\"margin-top:6px\">四、涉及的指导教师成果均已获得<b>书面授权</b>并以“××团队”名义规范标注；</p>"
                 "<p style=\"margin-top:6px\">五、若有不实，愿承担由此产生的一切责任。</p>",
                 eid="p47doc_b", fontSize=11.5, color="#FFFFFF", lineHeight=1.55))
    els.append(T(180, 344, 600, 24, "<p>承诺团队：算法歧视众包观测平台项目组</p>", eid="p47doc_s1",
                 fontSize=12, color=SUB, wrap=False, align=["right", "middle"]))
    els.append(T(180, 372, 600, 24, "<p>2026 年 ×× 月 ×× 日（盖章处）</p>", eid="p47doc_s2",
                 fontSize=12, color=SUB, wrap=False, align=["right", "middle"]))
    # 底部三标签
    tags = [("原创可溯", "Git 提交记录全留痕", "fas:code-branch"),
            ("数据可验", "观测数据含校验清单", "fas:database"),
            ("现场可演", "系统公网部署随时复现", "fas:cloud-arrow-up")]
    for i, (t, d, ic) in enumerate(tags):
        x = 140 + i * 232
        els.append(panel(x, 428, 216, 74, fill="#123C8F99", border_c="#3B82F6", eid=f"p47tag{i}"))
        els.append(ICON(x + 16, 446, 24, 24, ic, GOLD, eid=f"p47ic{i}"))
        els.append(T(x + 50, 438, 156, 22, f"<p><strong>{t}</strong></p>", eid=f"p47tt{i}",
                     fontSize=13, color="#FFFFFF", wrap=False))
        els.append(T(x + 50, 462, 156, 30, f"<p>{d}</p>", eid=f"p47td{i}",
                     fontSize=9.5, color=SUB, lineHeight=1.3))
    return els
