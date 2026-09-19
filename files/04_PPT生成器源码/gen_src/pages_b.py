# -*- coding: utf-8 -*-
"""第二章 项目创新：P12-P23"""
from core import *
from skeletons import nav, page_title_bar, panel, kpi, chip, feature_row

# ---------------- P12 项目总览 ----------------
def p12_overview():
    els = bg_base() + nav("项目总览", 2)
    els += page_title_bar("算法歧视众包观测平台", "一句话定位：让每一位网购者都成为算法监督的“移动观测站”", y=54)
    # 左：定位与三类用户
    els.append(panel(40, 112, 430, 118, fill="#123C8F99", border_c=GOLD, eid="p12pos"))
    els.append(T(58, 122, 400, 98,
                 "<p><strong>我们做什么：</strong>一款公益诉讼用途的浏览器插件 + 云端统计分析平台。</p>"
                 "<p>用户授权后一键采集电商商品页的<b>公开价格信息</b>，云端以统计检验识别群体价格歧视，一键导出<b>可呈证的证据包</b>。</p>",
                 eid="p12pos_b", fontSize=12, color="#FFFFFF", lineHeight=1.55))
    roles = [("志愿者", "授权后一键/自动采集，匿名贡献观测数据", "fas:hand-holding-heart", CYAN),
             ("研究者", "查询歧视分析结果，复现统计检验过程", "fas:microscope", GOLD),
             ("公益律师 / 消协", "下载标准化证据包，支撑公益诉讼", "fas:gavel", "#7EE2A8")]
    yy = 244
    for i, (t, d, ic, c) in enumerate(roles):
        els.append(panel(40, yy, 430, 76, eid=f"p12r{i}"))
        els.append(S(54, yy + 14, 44, 44, shape="roundRect", adjustments=[24000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1, "color": c}, eid=f"p12ri{i}"))
        els.append(ICON(65, yy + 25, 22, 22, ic, c, eid=f"p12ric{i}"))
        els.append(T(112, yy + 12, 340, 22, f"<p><strong>{t}</strong></p>", eid=f"p12rt{i}",
                     fontSize=14.5, color="#FFFFFF", wrap=False))
        els.append(T(112, yy + 36, 340, 32, f"<p>{d}</p>", eid=f"p12rd{i}",
                     fontSize=11, color=SUB, lineHeight=1.35))
        yy += 88
    # 右：全链路图
    els.append(panel(486, 112, 434, 390, eid="p12flow"))
    els.append(T(504, 122, 400, 24, "<p><strong>取证全链路（端云协同）</strong></p>",
                 eid="p12ft", fontSize=16, color="#FFFFFF", wrap=False))
    steps = [
        ("① 页面观测", "插件在商品详情页提取商品 / 价格 / 优惠 / 发货地", "fas:eye"),
        ("② 白名单脱敏", "sanitize() 逐字段显式拷贝，敏感信息不出浏览器", "fas:mask"),
        ("③ 云端汇聚", "FastAPI 接收上报，清洗入库 PostgreSQL", "fas:cloud-arrow-up"),
        ("④ 统计检验", "MWU 检验 + OLS 回归 + 假折扣识别 + 平台级复现", "fas:chart-line"),
        ("⑤ 证据导出", "zip 证据包：观测数据 + SHA-256 校验清单", "fas:file-shield"),
    ]
    yy = 156
    for i, (t, d, ic) in enumerate(steps):
        els.append(S(510, yy, 60, 52, shape="roundRect", adjustments=[20000],
                     fill=solid("#0A2A63"), border={"style": "solid", "width": 1, "color": "#3B82F6"}, eid=f"p12si{i}"))
        els.append(ICON(528, yy + 8, 24, 24, ic, CYAN, eid=f"p12sic{i}"))
        els.append(T(510, yy + 34, 60, 14, f"<p>{['采集','脱敏','汇聚','检验','导出'][i]}</p>",
                     eid=f"p12sil{i}", fontSize=9, color=SUB, wrap=False, align=["center", "middle"]))
        els.append(T(586, yy + 2, 320, 20, f"<p><strong>{t}</strong></p>", eid=f"p12st{i}",
                     fontSize=13.5, color="#FFFFFF", wrap=False))
        els.append(T(586, yy + 24, 320, 28, f"<p>{d}</p>", eid=f"p12sd{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.3))
        if i < 4:
            els.append(ICON(531, yy + 50, 16, 16, "fas:angle-down", GOLD, eid=f"p12ar{i}"))
        yy += 68
    # 底部 KPI
    kpis = [("4", "大电商平台适配"), ("2", "端：插件 + 云平台"), ("158", "条真实观测数据"), ("v0.4.0", "已迭代 8 个版本")]
    for i, (n, lb) in enumerate(kpis):
        x = 40 + i * 226
        els.append(panel(x, 516 - 60, 212, 60, eid=f"p12k{i}"))
        els.append(T(x, 516 - 52, 212, 30,
                     f'<p><span style="font-size:22px;color:{GOLD}"><strong>{n}</strong></span></p>',
                     eid=f"p12kn{i}", wrap=False, align=["center", "middle"]))
        els.append(T(x, 516 - 24, 212, 16, f"<p>{lb}</p>", eid=f"p12kl{i}",
                     fontSize=10, color=SUB, wrap=False, align=["center", "middle"]))
    return els

# ---------------- P13 解决方案五步链路 ----------------
def p13_solution():
    els = bg_base() + nav("解决方案", 2)
    els += page_title_bar("五步，把一次浏览变成一份证据", "问题导向 × 目标导向：每一步都对应调研发现的一道关卡", y=54)
    steps = [
        ("S1", "页面采集", "商品页一键/自动采集\n双通道提取价格字段", "对应关卡①：数据困在页面里", "fas:puzzle-piece"),
        ("S2", "脱敏上报", "白名单字段拷贝\n敏感信息绝不上传", "对应关卡③：隐私合规红线", "fas:user-shield"),
        ("S3", "云端汇聚", "API 校验清洗入库\n多用户数据对齐", "为群体级分析奠基", "fas:database"),
        ("S4", "统计检验", "MWU + OLS + 假折扣\n平台级复现检验", "对应关卡②：单点证据没效力", "fas:chart-line"),
        ("S5", "证据打包", "zip 含校验清单\n对接公益诉讼", "对应关卡④：证据链不完整", "fas:box-archive"),
    ]
    x0, cw, g, y0 = 36, 168, 10, 128
    for i, (s, t, d, rel, ic) in enumerate(steps):
        x = x0 + i * (cw + g)
        els.append(panel(x, y0, cw, 210, eid=f"p13s{i}"))
        els.append(T(x + 12, y0 + 10, 50, 24, f"<p>{s}</p>", eid=f"p13sn{i}",
                     fontSize=18, color=GOLD, bold=True, wrap=False))
        els.append(S(x + 12, y0 + 40, 52, 52, shape="roundRect", adjustments=[24000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1, "color": "#3B82F6"}, eid=f"p13si{i}"))
        els.append(ICON(x + 25, y0 + 53, 26, 26, ic, CYAN, eid=f"p13sic{i}"))
        els.append(T(x + 12, y0 + 102, cw - 24, 24, f"<p><strong>{t}</strong></p>", eid=f"p13st{i}",
                     fontSize=16, color="#FFFFFF", wrap=False))
        lines = d.split("\n")
        els.append(T(x + 12, y0 + 130, cw - 24, 36, "".join(f"<p>{s2}</p>" for s2 in lines),
                     eid=f"p13sd{i}", fontSize=10.5, color=SUB, lineHeight=1.35))
        els.append(S(x + 12, y0 + 172, cw - 24, 1, fill=solid("#2D4E8F"), eid=f"p13sl{i}"))
        els.append(T(x + 12, y0 + 178, cw - 24, 28, f"<p>{rel}</p>", eid=f"p13sr{i}",
                     fontSize=9.5, color=GOLD_L, lineHeight=1.3))
        if i < 4:
            els.append(ICON(x + cw + 1, y0 + 92, 16, 16, "fas:angle-right", GOLD, eid=f"p13ar{i}"))
    # 下：与传统方式对比条
    els.append(panel(36, 372, 888, 130, fill="#0C2B66CC", border_c="#2D4E8F", eid="p13cmp"))
    els.append(T(54, 382, 300, 22, "<p><strong>为什么众包 + 统计检验是更优解</strong></p>",
                 eid="p13cmp_t", fontSize=14, color="#FFFFFF", wrap=False))
    rows = [
        ("传统个人截图", "单点、不可复现、易被促销解释推翻", "#FF8A8A"),
        ("公证处逐页公证", "权威但 ~1,000 元/页，无法规模化", "#FFB86B"),
        ("本项目众包观测", "近零边际成本、群体级样本、检验过程留痕可复现", "#7EE2A8"),
    ]
    for i, (t, d, c) in enumerate(rows):
        y = 410 + i * 30
        els.append(S(54, y + 3, 10, 10, shape="ellipse", fill=solid(c), eid=f"p13cp{i}"))
        els.append(T(74, y - 2, 180, 22, f"<p><strong>{t}</strong></p>", eid=f"p13ct{i}",
                     fontSize=11.5, color=c, wrap=False))
        els.append(T(260, y - 2, 640, 22, f"<p>{d}</p>", eid=f"p13cd{i}",
                     fontSize=11.5, color="#FFFFFF", wrap=False))
    return els

# ---------------- P14 系统架构 ----------------
def p14_arch():
    els = bg_base() + nav("系统架构", 2)
    els += page_title_bar("端云协同的技术架构", "浏览器插件（Manifest V3）+ FastAPI 云端 + 统计分析引擎", y=54)
    # 左：插件端
    els.append(panel(40, 112, 420, 320, fill="#0A2A63DD", eid="p14ext"))
    els.append(T(58, 122, 380, 22, "<p><strong>🧩 浏览器插件端（Chrome / Edge · MV3）</strong></p>",
                 eid="p14ext_t", fontSize=14, color="#FFFFFF", wrap=False))
    mods = [
        ("content script", "按平台规则提取商品/价格/店铺/发货地；未授权时注入提示条", "#38BDF8"),
        ("background worker", "截图、IP 城市、白名单脱敏、上报与本地留存（500 条滚动）", "#7EE2A8"),
        ("popup 弹窗", "识别状态、授权开关、采集按钮、上报结果反馈", "#FFC000"),
        ("options 设置页", "用途说明、端点与密钥配置、脱敏开关、历史管理", "#C4B5FD"),
        ("report 报告页", "本地数据报告，纯手写 SVG 图表（零图表库依赖）", "#F9A8D4"),
    ]
    yy = 152
    for i, (t, d, c) in enumerate(mods):
        els.append(S(58, yy, 12, 12, shape="ellipse", fill=solid(c), eid=f"p14md{i}"))
        els.append(T(80, yy - 4, 170, 20, f"<p><strong>{t}</strong></p>", eid=f"p14mt{i}",
                     fontSize=12, color=c, wrap=False))
        els.append(T(80, yy + 16, 366, 32, f"<p>{d}</p>", eid=f"p14mdc{i}",
                     fontSize=10, color=SUB, lineHeight=1.3))
        yy += 54
    # 中间：数据流
    els.append(panel(468, 240, 130, 64, fill="#FFC00018", border_c=GOLD, eid="p14mid"))
    els.append(T(468, 246, 130, 34, "<p><strong>POST /api/observations</strong></p>", eid="p14mid_t",
                 fontSize=10.5, color=GOLD_L, wrap=False, align=["center", "middle"]))
    els.append(T(468, 278, 130, 20, "<p>X-API-Key 鉴权</p>", eid="p14mid_s",
                 fontSize=9, color=SUB, wrap=False, align=["center", "middle"]))
    els.append(ICON(458, 264, 18, 18, "fas:angle-right", GOLD, eid="p14a1"))
    els.append(ICON(598, 264, 18, 18, "fas:angle-right", GOLD, eid="p14a2"))
    # 右：云端
    els.append(panel(620, 112, 300, 320, fill="#0A2A63DD", eid="p14srv"))
    els.append(T(638, 122, 260, 22, "<p><strong>☁️ 云端平台（FastAPI）</strong></p>",
                 eid="p14srv_t", fontSize=14, color="#FFFFFF", wrap=False))
    smods = [
        ("路由与鉴权层", "X-API-Key / X-User-Id 双体系，Pydantic v2 校验", "#38BDF8"),
        ("清洗入库", "cleaning 管道 → PostgreSQL（本地 SQLite 兜底）", "#7EE2A8"),
        ("统计分析引擎", "Mann-Whitney U · OLS（HC3）· 假折扣标注 · 平台级复现", "#FFC000"),
        ("证据打包", "/api/export/bundle：zip + SHA-256 清单", "#C4B5FD"),
        ("门户与看板", "landing / 用户看板 / 管理台 / 分析页 / 下载页", "#F9A8D4"),
    ]
    yy = 152
    for i, (t, d, c) in enumerate(smods):
        els.append(S(638, yy, 12, 12, shape="ellipse", fill=solid(c), eid=f"p14sd{i}"))
        els.append(T(660, yy - 4, 240, 20, f"<p><strong>{t}</strong></p>", eid=f"p14st{i}",
                     fontSize=12, color=c, wrap=False))
        els.append(T(660, yy + 16, 246, 32, f"<p>{d}</p>", eid=f"p14sdc{i}",
                     fontSize=10, color=SUB, lineHeight=1.3))
        yy += 54
    # 底：技术栈（两行）
    els.append(panel(40, 444, 880, 68, eid="p14stack"))
    els.append(T(58, 444, 96, 68, "<p><strong>技术栈</strong></p>", eid="p14stack_t",
                 fontSize=13, color="#FFFFFF", wrap=False, align=["left", "middle"]))
    stack = ["TypeScript", "Vite", "Manifest V3", "Python 3.10+", "FastAPI",
             "SQLAlchemy", "PostgreSQL", "SciPy", "Vercel", "Docker"]
    for i, s in enumerate(stack):
        w = len(s) * 8 + 20
        if i == 0 or i == 5:
            xx = 160
        els += chip(xx, 452 if i < 5 else 482, s, color=CYAN, w=w)
        xx += w + 10
    return els

# ---------------- P15 创新点一：双通道提取 ----------------
def p15_innov1():
    els = bg_base() + nav("创新点一", 2)
    els += page_title_bar("双通道多策略价格提取", "产品创新：DOM 选择器优先 + 内嵌 JSON 回退，每个字段带来源标注", y=54)
    # 左：双通道对比
    els.append(panel(40, 112, 285, 190, eid="p15dom"))
    els.append(T(56, 122, 250, 22, "<p><strong>通道 A · DOM 选择器</strong></p>", eid="p15dom_t",
                 fontSize=14, color=CYAN, wrap=False))
    els.append(T(56, 148, 256, 146,
                 "<p>· 平台规则集中在 platforms.ts，扩展新平台只改一处</p>"
                 "<p>· 淘系收紧到明确容器：highlightPrice-- / subPrice-- / 经典节点</p>"
                 "<p>· 双价归属语义：subPrice 命中才存在“原价”，到手价绝不回退售价</p>"
                 "<p>· 排除吸顶栏干扰价（ItemHeadFixed--）</p>",
                 eid="p15dom_b", fontSize=10.5, color=SUB, lineHeight=1.5))
    els.append(panel(40, 312, 285, 190, eid="p15json"))
    els.append(T(56, 322, 250, 22, "<p><strong>通道 B · 内嵌 JSON 回退</strong></p>", eid="p15json_t",
                 fontSize=14, color=GOLD, wrap=False))
    els.append(T(56, 348, 256, 146,
                 "<p>· 收集全部内联 script（上限 2MB）</p>"
                 "<p>· 按平台惯例键名优先级正则提取：priceText / promotePrice / origPrice / finalPrice…</p>"
                 "<p>· 数值合法性校验（0.01 ~ 1,000 万元），取第一个合法值</p>"
                 "<p>· 覆盖 g_config / __INIT_DATA / pageData</p>",
                 eid="p15json_b", fontSize=10.5, color=SUB, lineHeight=1.5))
    # 中：状态 A/B 适配
    els.append(panel(341, 112, 300, 390, eid="p15ab"))
    els.append(T(357, 122, 270, 22, "<p><strong>状态 A / 状态 B 双渲染态适配</strong></p>",
                 eid="p15ab_t", fontSize=14, color="#FFFFFF", wrap=False))
    ab = [
        ("问题", "2025 版淘系详情页为 React SSR：先入状态 A 简化渲染，再异步注水为状态 B 完整价格模块"),
        ("对策", "extractWithPriceWait 每 500ms 探测，最长等待约 10 秒，直到完整价格容器出现才返回"),
        ("实证", "同一页面：状态 A 误抓 48 元 → 状态 B 正确取得 1,029 元 / 到手价 528.84 元"),
        ("兜底", "大小关系校验：到手价 > 原价时自动交换；无价格记录跳过上报，提示刷新"),
    ]
    yy = 152
    for i, (t, d) in enumerate(ab):
        els.append(S(357, yy + 2, 52, 20, shape="roundRect", adjustments=[50000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1, "color": "#3B82F6"}, eid=f"p15abt{i}"))
        els.append(T(357, yy + 2, 52, 20, f"<p>{t}</p>", eid=f"p15abtt{i}",
                     fontSize=10.5, color=CYAN, bold=True, wrap=False, align=["center", "middle"]))
        els.append(T(419, yy - 2, 210, 66, f"<p>{d}</p>", eid=f"p15abd{i}",
                     fontSize=10, color=SUB, lineHeight=1.4))
        yy += 88
    # 右：实测矩阵
    els.append(panel(657, 112, 263, 390, eid="p15test"))
    els.append(T(673, 122, 230, 22, "<p><strong>模拟页回归实测（jsdom）</strong></p>",
                 eid="p15test_t", fontSize=14, color="#FFFFFF", wrap=False))
    els.append({"elementId": "p15table", "elementType": "table", "bounds": [669, 152, 240, 240],
                "columnWidths": [0.42, 0.30, 0.28],
                "rowHeights": [0.16, 0.21, 0.21, 0.21, 0.21],
                "rows": [
                    [{"text": "模拟页", "bold": True, "color": "#FFC000", "fontSize": 10},
                     {"text": "原价", "bold": True, "color": "#FFC000", "fontSize": 10},
                     {"text": "到手价", "bold": True, "color": "#FFC000", "fontSize": 10}],
                    [{"text": "天猫 A（双价）", "fontSize": 9.5}, {"text": "3799 ✓", "fontSize": 9.5}, {"text": "3188.55 ✓", "fontSize": 9.5}],
                    [{"text": "天猫 B（双价）", "fontSize": 9.5}, {"text": "18.7 ✓", "fontSize": 9.5}, {"text": "15.74 ✓", "fontSize": 9.5}],
                    [{"text": "淘宝 C（单价）", "fontSize": 9.5}, {"text": "3850 ✓", "fontSize": 9.5}, {"text": "null ✓", "fontSize": 9.5}],
                    [{"text": "天猫 D（状态A）", "fontSize": 9.5}, {"text": "1029 ✓", "fontSize": 9.5}, {"text": "null ✓", "fontSize": 9.5}],
                ],
                "style": {"cellStyle": {"color": "#FFFFFF", "fontSize": 10, "border": None,
                                        "align": ["center", "middle"], "fill": {"type": "solid", "color": "#0A2A6380"}}}})
    els.append(T(673, 400, 240, 90,
                 '<p><span style="font-size:30px;color:#FFC000"><strong>29</strong></span><span style="font-size:12px;color:#C7D7F2"> 项提取断言全部通过</span></p>'
                 '<p style="margin-top:6px"><span style="font-size:10.5px;color:#C7D7F2">每页 7 组断言：平台/商品ID、原价、到手价、发货地原文+归一化、店铺名、店铺ID、来源标注</span></p>',
                 eid="p15test_b", fontSize=11, color="#FFFFFF", lineHeight=1.4))
    return els

# ---------------- P16 创新点二：隐私设计 ----------------
def p16_innov2():
    els = bg_base() + nav("创新点二", 2)
    els += page_title_bar("授权优先 · 白名单脱敏", "服务创新：把隐私合规做成产品的第一性原理，而不是事后补丁", y=54)
    # 左：授权流程
    els.append(panel(40, 112, 430, 158, eid="p16auth"))
    els.append(T(58, 122, 400, 22, "<p><strong>授权优先的三重校验</strong></p>", eid="p16auth_t",
                 fontSize=15, color="#FFFFFF", wrap=False))
    flow = [("页面提示条", "同意并采集 / 仅本次 / 忽略"), ("弹窗授权", "consent=true 才可采集"), ("双重校验", "content 与 background 同时把关")]
    xx = 58
    for i, (t, d) in enumerate(flow):
        els.append(S(xx, 154, 128, 66, shape="roundRect", adjustments=[16000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1, "color": "#3B82F6"}, eid=f"p16f{i}"))
        els.append(T(xx + 6, 160, 116, 22, f"<p><strong>{t}</strong></p>", eid=f"p16ft{i}",
                     fontSize=12, color="#FFFFFF", wrap=False, align=["center", "middle"]))
        els.append(T(xx + 6, 182, 116, 34, f"<p>{d}</p>", eid=f"p16fd{i}",
                     fontSize=9, color=SUB, lineHeight=1.25, align=["center", "top"]))
        if i < 2:
            els.append(ICON(xx + 132, 178, 14, 14, "fas:angle-right", GOLD, eid=f"p16fa{i}"))
        xx += 146
    els.append(T(58, 232, 400, 30, "<p>未授权（consent=false）时自动采集硬禁用， Shadow DOM 提示条不读取任何页面数据。</p>",
                 eid="p16auth_b", fontSize=10.5, color=SUB, lineHeight=1.35))
    # 左下：隐私红线清单
    els.append(panel(40, 284, 430, 218, fill="#0A2A63DD", eid="p16red"))
    els.append(T(58, 294, 400, 22, "<p><strong>六条隐私红线（写入代码与文档）</strong></p>",
                 eid="p16red_t", fontSize=15, color="#FFFFFF", wrap=False))
    reds = [
        "最小化采集：仅商品页公开信息 + 脱敏环境概况",
        "cookie 红线：只判断键名是否存在，值从不读取",
        "昵称与推断依据（userMarker / evidence）绝不上传",
        "白名单脱敏：sanitize() 逐字段显式拷贝，未列出字段不进入记录",
        "本地留存上限 500 条滚动删除，可一键清空",
        "构建产物不压缩混淆（minify: false），行为可审计",
    ]
    for i, r in enumerate(reds):
        y = 322 + i * 28
        els.append(ICON(58, y, 16, 16, "fas:lock", "#7EE2A8", eid=f"p16r{i}"))
        els.append(T(84, y - 2, 372, 24, f"<p>{r}</p>", eid=f"p16rt{i}",
                     fontSize=10.5, color="#FFFFFF", wrap=False, align=["left", "middle"]))
    # 右：脱敏前后对照
    els.append(panel(486, 112, 434, 240, eid="p16cmp"))
    els.append(T(504, 122, 400, 22, "<p><strong>脱敏前后对照（店铺名 / 昵称）</strong></p>",
                 eid="p16cmp_t", fontSize=15, color="#FFFFFF", wrap=False))
    els.append({"elementId": "p16table", "elementType": "table", "bounds": [500, 152, 406, 186],
                "columnWidths": [0.24, 0.38, 0.38],
                "rowHeights": [0.2, 0.27, 0.27, 0.26],
                "rows": [
                    [{"text": "字段", "bold": True, "color": "#FFC000", "fontSize": 11},
                     {"text": "页面原始值", "bold": True, "color": "#FFC000", "fontSize": 11},
                     {"text": "入库 / 上报值", "bold": True, "color": "#FFC000", "fontSize": 11}],
                    [{"text": "店铺名", "fontSize": 10.5}, {"text": "明智电脑科技", "fontSize": 10.5},
                     {"text": "明＊＊＊＊（可选打码）", "fontSize": 10.5, "color": "#7EE2A8"}],
                    [{"text": "用户昵称", "fontSize": 10.5}, {"text": "张**（页面角标）", "fontSize": 10.5},
                     {"text": "不上传", "fontSize": 10.5, "color": "#7EE2A8"}],
                    [{"text": "登录态 cookie", "fontSize": 10.5}, {"text": "unb / _nk_ / pin", "fontSize": 10.5},
                     {"text": "只传“是否存在”", "fontSize": 10.5, "color": "#7EE2A8"}],
                ],
                "style": {"cellStyle": {"color": "#FFFFFF", "fontSize": 10.5, "border": None,
                                        "align": ["center", "middle"], "fill": {"type": "solid", "color": "#0A2A6380"}}}})
    # 右下：合规对齐
    els.append(panel(486, 366, 434, 136, fill="#123C8F99", border_c="#3B82F6", eid="p16law"))
    els.append(T(504, 376, 400, 22, "<p><strong>与法规要求逐条对齐</strong></p>", eid="p16law_t",
                 fontSize=14, color="#FFFFFF", wrap=False))
    els.append(T(504, 402, 402, 92,
                 "<p>· 《个人信息保护法》最小必要原则 → 白名单逐字段拷贝</p>"
                 "<p>· 告知—同意规则 → 采集前明示用途，授权状态可随时撤回</p>"
                 "<p>· 匿名化要求 → crypto.randomUUID() 匿名身份，不含注册信息</p>"
                 "<p>· 公益诉讼取证合规 → 仅采集本人页面公开展示信息</p>",
                 eid="p16law_b", fontSize=11, color=SUB, lineHeight=1.6))
    return els

# ---------------- P17 创新点三：统计检验引擎 ----------------
def p17_innov3():
    els = bg_base() + nav("创新点三", 2)
    els += page_title_bar("统计检验引擎：让“感觉被宰”变成“检验显著”", "技术创新：四级判定规则，结论可复现、过程全留痕", y=54)
    rules = [
        ("R1", "Mann-Whitney U 检验", "比较两名匿名用户（价差最大用户对）到手价分布，p < 0.05 记为显著；小样本自动降级为描述性输出。", "MWU_SIGNIFICANT", "fas:vial"),
        ("R2", "价差门槛", "两用户中位数价差超过 5%（相对低价侧）才进入疑似集，过滤随机波动。", "PRICE_DIFF_OVER_5PCT", "fas:percent"),
        ("R3", "OLS 回归控制", "控制城市 / 时段 / 设备价格分等因素后，“是否高价侧”仍显著（HC3 稳健标准误），排除混杂解释。", "REGRESSION_SIGNIFICANT", "fas:chart-line"),
        ("R4", "假折扣识别 + 平台级复现", "原价群体差异且折扣深度 > 10% 记为假折扣型歧视；同一价差模式需在 ≥2 个商品上复现，才判定系统性歧视。", "FAKE_DISCOUNT_PATTERN", "fas:copy"),
    ]
    x0, y0, cw, ch, g = 40, 116, 428, 128, 24
    for i, (r, t, d, code, ic) in enumerate(rules):
        x, y = x0 + (i % 2) * (cw + g), y0 + (i // 2) * (ch + g)
        els.append(panel(x, y, cw, ch, eid=f"p17r{i}"))
        els.append(T(x + 14, y + 10, 44, 26, f"<p>{r}</p>", eid=f"p17rn{i}",
                     fontSize=18, color=GOLD, bold=True, wrap=False))
        els.append(ICON(x + cw - 44, y + 12, 26, 26, ic, CYAN, eid=f"p17ic{i}"))
        els.append(T(x + 62, y + 12, cw - 120, 24, f"<p><strong>{t}</strong></p>", eid=f"p17t{i}",
                     fontSize=14.5, color="#FFFFFF", wrap=False))
        els.append(T(x + 14, y + 42, cw - 28, 56, f"<p>{d}</p>", eid=f"p17d{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.45))
        els.append(S(x + 14, y + 102, cw - 28, 18, shape="roundRect", adjustments=[50000],
                     fill=solid("#0A1F4A"), eid=f"p17cd{i}"))
        els.append(T(x + 22, y + 102, cw - 44, 18, f"<p>{code}</p>", eid=f"p17cdt{i}",
                     fontSize=9.5, color="#7EE2A8", fontFamily="Consolas", wrap=False, align=["left", "middle"]))
    # 底：输出样例
    els.append(panel(40, 404, 880, 98, fill="#0C2B66CC", border_c="#2D4E8F", eid="p17out"))
    els.append(T(58, 414, 300, 22, "<p><strong>引擎输出示例（判定理由中文释义）</strong></p>",
                 eid="p17out_t", fontSize=13.5, color="#FFFFFF", wrap=False))
    els.append(T(58, 440, 850, 56,
                 '<p><span style="color:#7EE2A8">✔ MWU_SIGNIFICANT</span>　两用户价格分布差异超出随机波动（p&lt;0.05）　　'
                 '<span style="color:#7EE2A8">✔ PRICE_DIFF_OVER_5PCT</span>　中位数价差 8.6%　　'
                 '<span style="color:#FFB86B">⚠ LOW_CONFIDENCE</span>　样本不足时降级为低置信疑似</p>'
                 '<p><span style="color:#C7D7F2">平台级复现检验：同一价差模式在 ≥2 个商品上复现 → 才更像系统性差别待遇，而非单品促销巧合</span></p>',
                 eid="p17out_b", fontSize=11, color="#FFFFFF", lineHeight=1.6))
    return els

# ---------------- P18 创新点四：证据打包 ----------------
def p18_innov4():
    els = bg_base() + nav("创新点四", 2)
    els += page_title_bar("一键证据包：从数据到呈证", "模式创新：标准化证据格式，让个案得以升级为公益诉讼", y=54)
    # 左：证据包结构
    els.append(panel(40, 112, 420, 300, eid="p18zip"))
    els.append(T(58, 122, 380, 22, "<p><strong>📦 /api/export/bundle 证据包结构</strong></p>",
                 eid="p18zip_t", fontSize=15, color="#FFFFFF", wrap=False))
    tree = [
        ("evidence_bundle.zip", 0, GOLD),
        ("├─ observations.json（观测记录全集）", 1, "#FFFFFF"),
        ("│   · 平台 / 商品 / 价格 / 优惠 / 发货地", 2, SUB),
        ("│   · 采集时间 / 匿名用户 / 城市 / 设备概况", 2, SUB),
        ("│   · 字段来源标注（DOM / JSON 通道）", 2, SUB),
        ("├─ manifest.json（清单与校验）", 1, "#FFFFFF"),
        ("│   · 每条记录的 SHA-256 摘要", 2, SUB),
        ("│   · 生成时间 / 版本 / 记录数", 2, SUB),
        ("└─ analysis_report.json（检验过程留痕）", 1, "#FFFFFF"),
    ]
    for i, (t, lv, c) in enumerate(tree):
        y = 152 + i * 28
        els.append(T(58 + lv * 18, y, 390 - lv * 18, 24, f"<p>{t}</p>", eid=f"p18tr{i}",
                     fontSize=11, color=c, fontFamily="Consolas", wrap=False, align=["left", "middle"]))
    els.append(T(58, 386, 380, 20, "<p>任何一方都可重算 SHA-256 验证数据未被篡改</p>",
                 eid="p18zip_n", fontSize=10.5, color="#7EE2A8", wrap=False))
    # 右：对接流程
    els.append(panel(476, 112, 444, 300, eid="p18flow"))
    els.append(T(494, 122, 400, 22, "<p><strong>与公益诉讼的对接流程</strong></p>",
                 eid="p18flow_t", fontSize=15, color="#FFFFFF", wrap=False))
    flow = [
        ("线索发现", "平台级复现检验命中疑似歧视商品", "fas:magnifying-glass"),
        ("证据固定", "导出证据包，时间戳 + 校验值固化", "fas:fingerprint"),
        ("专业评估", "律师 / 检察官复核检验过程与法律要件", "fas:user-tie"),
        ("公益诉讼", "作为起诉与调解的量化证据支撑", "fas:gavel"),
    ]
    yy = 152
    for i, (t, d, ic) in enumerate(flow):
        els.append(S(500, yy, 40, 40, shape="ellipse", fill=solid("#123C8F"),
                     border={"style": "solid", "width": 1.5, "color": GOLD if i == 3 else "#3B82F6"}, eid=f"p18fi{i}"))
        els.append(ICON(510, yy + 10, 20, 20, ic, GOLD if i == 3 else CYAN, eid=f"p18fic{i}"))
        els.append(T(556, yy - 2, 340, 20, f"<p><strong>{i+1}. {t}</strong></p>", eid=f"p18ft{i}",
                     fontSize=13, color="#FFFFFF", wrap=False))
        els.append(T(556, yy + 20, 340, 20, f"<p>{d}</p>", eid=f"p18fd{i}",
                     fontSize=10.5, color=SUB, wrap=False))
        if i < 3:
            els.append(ICON(511, yy + 40, 16, 16, "fas:angle-down", "#3B82F6", eid=f"p18ar{i}"))
        yy += 62
    # 底：为什么是“模式创新”
    els.append(panel(40, 428, 880, 74, fill="#FFC00018", border_c=GOLD, eid="p18why"))
    els.append(T(58, 436, 844, 58,
                 '<p><strong>模式创新点：</strong>首次把“众包采集 + 统计检验 + 标准化证据包”组合为面向公益诉讼的完整取证范式——</p>'
                 '<p>个人数据贡献从“吐槽”升级为“证据”，公益诉讼从“找个案碰运气”升级为“按图索骥选线索”。</p>',
                 eid="p18why_b", fontSize=11.5, color="#FFFFFF", lineHeight=1.5, align=["left", "middle"]))
    return els

# ---------------- P19 产品演示①：插件端 ----------------
def p19_demo1():
    els = bg_base() + nav("产品演示 · 插件端", 2)
    els += page_title_bar("插件端：30 秒完成一次规范取证", "Edge / Chrome 双浏览器支持 · 真实运行界面（非效果图）", y=54)
    # 左：popup 截图
    els.append(IMG(60, 108, 240, 400, "media/popup.png", fit={"mode": "contain"},
                   cropShape={"shapeName": "roundRect", "adjustments": [4000]},
                   border={"style": "solid", "width": 1.5, "color": "#3B82F6"},
                   shadow={"blur": 16, "color": "#00000066", "offset": [0, 6]}, eid="p19pop"))
    els.append(T(60, 508, 240, 16, "<p>▲ 插件弹窗（真实截图）</p>", eid="p19pop_c",
                 fontSize=9.5, color=DIM, wrap=False, align=["center", "middle"]))
    # 中：功能点
    feats = [
        ("智能识别", "进入商品详情页自动识别平台与商品 ID，提示条轻量不打扰", "fas:wand-magic-sparkles"),
        ("一键采集", "提取商品 / 价格 / 优惠 / 发货地，10 分钟内同商品去重", "fas:hand-pointer"),
        ("自动采集", "授权后商品页自动触发，SPA 路由兼容，失败静默", "fas:robot"),
        ("失败重试", "上报失败本地暂存，错误翻译成可执行提示，手动重试不丢数", "fas:rotate"),
        ("可观测性", "后端返回 observationId 与清洗提示，弹窗即时反馈", "fas:eye"),
    ]
    yy = 116
    for i, (t, d, ic) in enumerate(feats):
        els += feature_row(330, yy, 330, ic, t, d, h=72)
        yy += 78
    # 右：options 截图
    els.append(IMG(684, 108, 240, 214, "media/options.png", fit={"mode": "cover"},
                   crop={"top": 0, "bottom": 0.55},
                   cropShape={"shapeName": "roundRect", "adjustments": [4000]},
                   border={"style": "solid", "width": 1.5, "color": "#3B82F6"}, eid="p19opt"))
    els.append(T(684, 328, 240, 16, "<p>▲ 设置页：端点 / 脱敏 / 历史管理</p>", eid="p19opt_c",
                 fontSize=9.5, color=DIM, wrap=False, align=["center", "middle"]))
    els.append(panel(684, 352, 240, 156, fill="#123C8F99", border_c="#3B82F6", eid="p19tip"))
    els.append(T(700, 362, 210, 20, "<p><strong>用户旅程</strong></p>", eid="p19tip_t",
                 fontSize=13, color="#FFFFFF", wrap=False))
    els.append(T(700, 386, 210, 116,
                 "<p>① 安装插件（解压加载）</p><p>② 阅读用途并同意授权</p><p>③ 测试连接显示绿色</p><p>④ 浏览商品页自动采集</p><p>⑤ 数据报告页看个人贡献</p>",
                 eid="p19tip_b", fontSize=11, color=SUB, lineHeight=1.65))
    return els

# ---------------- P20 产品演示②：数据报告 ----------------
def p20_demo2():
    els = bg_base() + nav("产品演示 · 数据报告", 2)
    els += page_title_bar("本地数据报告：每个人都是数据的主人", "零图表库依赖 · 纯手写 SVG · 数据只存在用户浏览器里", y=54)
    els.append(IMG(40, 108, 470, 396, "media/report.png", fit={"mode": "cover"},
                   crop={"top": 0, "bottom": 0.28},
                   cropShape={"shapeName": "roundRect", "adjustments": [3000]},
                   border={"style": "solid", "width": 1.5, "color": "#3B82F6"},
                   shadow={"blur": 16, "color": "#00000066", "offset": [0, 6]}, eid="p20rep"))
    feats = [
        ("四张统计卡", "总采集数 / 上报成功数 / 覆盖平台数 / 覆盖城市数"),
        ("平台均价对比", "各平台到手价均值横向条形图，平台间差异一眼可见"),
        ("城市均价 Top12", "按 IP 城市聚合，揭示地域维度价格差异"),
        ("优惠金额分布", "原价 − 到手价直方图，假折扣无处遁形"),
        ("明细细表", "时间 / 平台 / 商品 / 到手价 / 城市 / 上报状态全留痕"),
    ]
    yy = 116
    for i, (t, d) in enumerate(feats):
        els.append(panel(534, yy, 386, 66, eid=f"p20f{i}"))
        els.append(S(548, yy + 14, 8, 38, fill=solid(GOLD), eid=f"p20fb{i}"))
        els.append(T(566, yy + 8, 340, 22, f"<p><strong>{t}</strong></p>", eid=f"p20ft{i}",
                     fontSize=13.5, color="#FFFFFF", wrap=False))
        els.append(T(566, yy + 32, 340, 28, f"<p>{d}</p>", eid=f"p20fd{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.3))
        yy += 76
    return els

# ---------------- P21 产品演示③：云端 ----------------
def p21_demo3():
    els = bg_base() + nav("产品演示 · 云端平台", 2)
    els += page_title_bar("云端平台：从观测数据到歧视判定", "门户 / 用户看板 / 管理控制台 / 统计分析 四位一体（真实截图）", y=54)
    shots = [
        ("media/console.png", "管理控制台 · 总览", "158 条观测 · 采集→入库→检验→判定 流水线实时状态", 40, 300),
        ("media/analysis.png", "统计分析页", "单商品 MWU + 回归判定 · 平台级复现检验批量输出", 340, 300),
        ("media/me.png", "用户看板", "免密一键登录 · 个人贡献统计与近 7 天趋势", 640, 280),
    ]
    for i, (src, t, d, x, w) in enumerate(shots):
        els.append(IMG(x, 112, w, 240, src, fit={"mode": "cover"}, crop={"top": 0, "bottom": 0.45},
                       cropShape={"shapeName": "roundRect", "adjustments": [3000]},
                       border={"style": "solid", "width": 1.5, "color": "#3B82F6"}, eid=f"p21s{i}"))
        els.append(T(x, 358, w, 20, f"<p><strong>{t}</strong></p>", eid=f"p21t{i}",
                     fontSize=13, color="#FFFFFF", wrap=False, align=["center", "middle"]))
        els.append(T(x + 6, 380, w - 12, 34, f"<p>{d}</p>", eid=f"p21d{i}",
                     fontSize=10, color=SUB, lineHeight=1.35, align=["center", "top"]))
    # 底：云端能力条
    caps = [("双登录体系", "用户免密 UUID + 管理员密钥 SHA-256 哈希校验"),
            ("数据看板", "总观测 / 可分析商品 / 覆盖平台 / 7 天趋势"),
            ("批量分析", "一键平台级批量检验，疑似商品自动标注"),
            ("证据导出", "zip 证据包 + SHA-256 校验清单")]
    for i, (t, d) in enumerate(caps):
        x = 40 + i * 226
        els.append(panel(x, 428, 212, 74, eid=f"p21c{i}"))
        els.append(T(x + 12, 436, 188, 20, f"<p><strong>{t}</strong></p>", eid=f"p21ct{i}",
                     fontSize=12.5, color=GOLD_L, wrap=False))
        els.append(T(x + 12, 458, 188, 38, f"<p>{d}</p>", eid=f"p21cd{i}",
                     fontSize=9.5, color=SUB, lineHeight=1.35))
    return els

# ---------------- P22 技术验证与版本演进 ----------------
def p22_verify():
    els = bg_base() + nav("技术验证", 2)
    els += page_title_bar("用工程师的方式证明可靠", "48 项自动化断言 + 8 个版本迭代 + 真实页面探针端到端验证", y=54)
    # 左：测试体系
    els.append(panel(40, 112, 430, 240, eid="p22test"))
    els.append(T(58, 122, 400, 22, "<p><strong>三层自动化测试体系</strong></p>", eid="p22test_t",
                 fontSize=15, color="#FFFFFF", wrap=False))
    tests = [
        ("19 项", "字段映射单元测试", "backendMapping：插件记录 → 后端扁平 schema，价格统一换算为整数分", CYAN),
        ("29 项", "页面提取回归测试", "jsdom 加载 4 个真实结构模拟页，逐字段断言（价格容差 0.001）", GOLD),
        ("端到端", "真实页面探针", "自包含 JS 探针经 CDP 在真实商品页验证「提取→映射→上报」链路", "#7EE2A8"),
    ]
    yy = 152
    for i, (n, t, d, c) in enumerate(tests):
        els.append(T(58, yy, 76, 30, f"<p><strong>{n}</strong></p>", eid=f"p22tn{i}",
                     fontSize=19, color=c, wrap=False, align=["left", "middle"]))
        els.append(T(142, yy + 2, 310, 20, f"<p><strong>{t}</strong></p>", eid=f"p22tt{i}",
                     fontSize=13, color="#FFFFFF", wrap=False))
        els.append(T(142, yy + 24, 312, 32, f"<p>{d}</p>", eid=f"p22td{i}",
                     fontSize=10, color=SUB, lineHeight=1.3))
        yy += 66
    # 左下：构建核验
    els.append(panel(40, 366, 430, 136, fill="#0A2A63DD", eid="p22build"))
    els.append(T(58, 376, 400, 22, "<p><strong>构建即核验（npm run verify）</strong></p>", eid="p22build_t",
                 fontSize=14, color="#FFFFFF", wrap=False))
    els.append(T(58, 402, 396, 92,
                 "<p>· TypeScript strict 全量类型检查纳入 build</p>"
                 "<p>· dist 产物完整性与 content script IIFE 形态自动核验</p>"
                 "<p>· 两段式构建：主构建 ESM + content 独立 IIFE（MV3 硬性要求）</p>"
                 "<p>· 产物不压缩混淆，任何第三方可直接审查实际行为</p>",
                 eid="p22build_b", fontSize=10.5, color=SUB, lineHeight=1.6))
    # 右：版本演进时间线
    els.append(panel(486, 112, 434, 390, eid="p22ver"))
    els.append(T(504, 122, 400, 22, "<p><strong>版本演进：从能用到可信</strong></p>", eid="p22ver_t",
                 fontSize=15, color="#FFFFFF", wrap=False))
    vers = [
        ("v0.2.0", "自动采集", "商品页自动触发 + 10 分钟去重"),
        ("v0.2.1", "失败重试", "失败暂存 + 手动重试 + 错误翻译"),
        ("v0.3.0", "增强抓取", "多策略提取框架：DOM + JSON 双通道"),
        ("v0.3.2", "真实页面适配", "2025 版详情页实测诊断修复"),
        ("v0.3.4/5", "价格抓取收紧", "状态A/B 双渲染态 + 等待逻辑修正"),
        ("v0.3.6", "回归全绿", "29 项提取断言 + 19 项映射单测"),
        ("v0.4.0", "公网版", "双登录体系 + 门户/看板/分析页 + Vercel 部署"),
    ]
    yy = 154
    for i, (v, t, d) in enumerate(vers):
        c = GOLD if i == 6 else CYAN
        els.append(S(510, yy + 4, 10, 10, shape="ellipse", fill=solid(c), eid=f"p22vn{i}"))
        if i < 6:
            els.append(S(514, yy + 16, 2, 30, fill=solid("#2D4E8F"), eid=f"p22vl{i}"))
        els.append(T(530, yy - 2, 64, 20, f"<p><strong>{v}</strong></p>", eid=f"p22vv{i}",
                     fontSize=11.5, color=c, wrap=False))
        els.append(T(600, yy - 2, 130, 20, f"<p><strong>{t}</strong></p>", eid=f"p22vt{i}",
                     fontSize=11.5, color="#FFFFFF", wrap=False))
        els.append(T(600, yy + 18, 300, 18, f"<p>{d}</p>", eid=f"p22vd{i}",
                     fontSize=9.5, color=SUB, wrap=False))
        yy += 48
    return els

# ---------------- P23 创新成果与知识产权 ----------------
def p23_ip():
    els = bg_base() + nav("创新成果", 2)
    els += page_title_bar("创新成果与知识产权布局", "论文 · 专利 · 软著 · 开源 · 应用证明 —— 成果在持续累积", y=54)
    # 左：成果清单
    items = [
        ("软件著作权", "《算法歧视众包观测平台 V1.0》已提交受理（受理号占位，×× 团队）", "fas:file-circle-check", "已受理"),
        ("发明专利", "一种面向公益诉讼的电商价格歧视众包取证方法（申请中，×× 团队）", "fas:file-signature", "申请中"),
        ("学术论文", "《基于众包观测的电商价格歧视统计检验方法》撰写中，拟投 ×× 期刊", "fas:file-lines", "撰写中"),
        ("开源社区", "GitHub / Gitee 双平台开源（MIT），插件与后端分版本发布", "fab:github", "已开源"),
        ("应用证明", "×× 区消费者协会试用意向函（洽谈中）；×× 律师事务所合作备忘录", "fas:handshake", "洽谈中"),
    ]
    yy = 112
    for i, (t, d, ic, st) in enumerate(items):
        els.append(panel(40, yy, 560, 66, eid=f"p23i{i}"))
        els.append(S(54, yy + 13, 40, 40, shape="roundRect", adjustments=[24000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1, "color": "#3B82F6"}, eid=f"p23ii{i}"))
        els.append(ICON(64, yy + 23, 20, 20, ic, GOLD if st in ("已受理", "已开源") else CYAN, eid=f"p23iic{i}"))
        els.append(T(108, yy + 8, 380, 20, f"<p><strong>{t}</strong></p>", eid=f"p23it{i}",
                     fontSize=13.5, color="#FFFFFF", wrap=False))
        els.append(T(108, yy + 30, 400, 30, f"<p>{d}</p>", eid=f"p23id{i}",
                     fontSize=10, color=SUB, lineHeight=1.3))
        stc = {"已受理": "#7EE2A8", "已开源": "#7EE2A8", "申请中": GOLD, "撰写中": CYAN, "洽谈中": "#C4B5FD"}[st]
        els.append(S(516, yy + 20, 70, 24, shape="roundRect", adjustments=[50000],
                     fill=solid(stc + "22"), border={"style": "solid", "width": 1, "color": stc}, eid=f"p23st{i}"))
        els.append(T(516, yy + 20, 70, 24, f"<p>{st}</p>", eid=f"p23stt{i}",
                     fontSize=10.5, color=stc, bold=True, wrap=False, align=["center", "middle"]))
        yy += 78
    # 右：证书图墙（模板素材，示意）
    els.append(IMG(624, 116, 140, 186, "media/patent1.jpg", fit={"mode": "cover"},
                   cropShape={"shapeName": "roundRect", "adjustments": [4000]},
                   border={"style": "solid", "width": 1, "color": "#3B82F6"},
                   shadow={"blur": 12, "color": "#00000055", "offset": [0, 4]}, eid="p23c1"))
    els.append(IMG(776, 116, 140, 186, "media/patent2.png", fit={"mode": "cover"},
                   cropShape={"shapeName": "roundRect", "adjustments": [4000]},
                   border={"style": "solid", "width": 1, "color": "#3B82F6"},
                   shadow={"blur": 12, "color": "#00000055", "offset": [0, 4]}, eid="p23c2"))
    els.append(IMG(624, 314, 140, 186, "media/honor1.png", fit={"mode": "cover"},
                   cropShape={"shapeName": "roundRect", "adjustments": [4000]},
                   border={"style": "solid", "width": 1, "color": "#3B82F6"},
                   shadow={"blur": 12, "color": "#00000055", "offset": [0, 4]}, eid="p23c3"))
    els.append(IMG(776, 314, 140, 186, "media/certs.png", fit={"mode": "cover"},
                   cropShape={"shapeName": "roundRect", "adjustments": [4000]},
                   border={"style": "solid", "width": 1, "color": "#3B82F6"},
                   shadow={"blur": 12, "color": "#00000055", "offset": [0, 4]}, eid="p23c4"))
    els.append(T(624, 502, 292, 16, "<p>▲ 知识产权与荣誉材料（示意位，替换为实际证书）</p>",
                 eid="p23cnote", fontSize=9, color=DIM, wrap=False, align=["center", "middle"]))
    return els
