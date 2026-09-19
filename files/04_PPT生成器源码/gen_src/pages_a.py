# -*- coding: utf-8 -*-
"""第一章 项目缘起：P2 调研速览、P5-P10"""
from core import *
from skeletons import nav, page_title_bar, panel, kpi, chip, feature_row, glow_deco

# ---------------- P2 调研速览（评审要求：第二页展示调研） ----------------
def p02_research():
    els = bg_base() + nav("调研深入 · 扎根一线", 1)
    els += page_title_bar("我们把调研做到了消费者身边", "去哪里调研 · 调研谁 · 调研成果 —— 立项前历时 9 个月的田野调查", y=54)
    # 左：四个调研 KPI
    data = [
        ("1,286", "份", "有效问卷", "覆盖 21 省 38 所高校师生与社区居民", "fas:clipboard-list"),
        ("42", "人", "深度访谈", "消费者 / 公益律师 / 消协工作人员", "fas:comments"),
        ("4", "大平台", "实测取证", "淘宝 / 天猫 / 京东 / 拼多多网页版", "fas:cart-shopping"),
        ("158", "条", "真实观测数据", "双账号对照采集，留存完整取证链", "fas:database"),
    ]
    x0, y0, cw, ch, g = 40, 112, 212, 118, 14
    for i, (n, u, lb, sub, ic) in enumerate(data):
        x, y = x0 + (i % 2) * (cw + g), y0 + (i // 2) * (ch + g)
        els.append(panel(x, y, cw, ch, eid=f"p2k{i}"))
        els.append(ICON(x + 14, y + 14, 26, 26, ic, CYAN, eid=f"p2kic{i}"))
        els.append(T(x + 48, y + 10, cw - 60, 36,
                     f'<p><span style="font-size:26px;color:{GOLD}"><strong>{n}</strong></span>'
                     f'<span style="font-size:12px;color:{SUB}"> {u}</span></p>',
                     eid=f"p2kn{i}", wrap=False, align=["left", "middle"]))
        els.append(T(x + 14, y + 52, cw - 28, 20, f"<p><strong>{lb}</strong></p>",
                     eid=f"p2kl{i}", fontSize=14, color="#FFFFFF", wrap=False))
        els.append(T(x + 14, y + 74, cw - 28, 36, f"<p>{sub}</p>",
                     eid=f"p2ks{i}", fontSize=10.5, color=SUB, lineHeight=1.35))
    # 左下：调研结论
    els.append(panel(40, 372, 438, 130, fill="#123C8F99", border_c=GOLD, eid="p2c"))
    els.append(T(58, 382, 400, 22, "<p><strong>调研结论：取证难是维权死结</strong></p>",
                 eid="p2c_t", fontSize=15, color=GOLD_L, wrap=False))
    els.append(T(58, 406, 406, 88,
                 "<p>· 86.91% 受访者有被“大数据杀熟”的经历，但仅 <strong>0.43%</strong> 选择诉讼维权</p>"
                 "<p>· 79.53% 受访者认为杀熟“不容易取证”，88.01% 认为监管手段跟不上</p>"
                 "<p>· 消协与公益律师均表示：缺的不是法律依据，而是<strong>标准化、可检验的证据</strong></p>"
                 "<p>· 由此确立课题：用众包方式把“千人千价”变成可统计、可呈证的公共数据</p>",
                 eid="p2c_b", fontSize=11.5, color="#FFFFFF", lineHeight=1.55))
    # 右：调研足迹
    els.append(panel(494, 112, 426, 390, eid="p2r"))
    els.append(T(512, 122, 390, 24, "<p><strong>调研足迹（2025.09 — 2026.06）</strong></p>",
                 eid="p2r_t", fontSize=16, color="#FFFFFF", wrap=False))
    steps = [
        ("2025.09", "文献与判例调研", "梳理 40+ 篇算法歧视研究、12 起典型案例，确认“取证”为共同瓶颈", "fas:book-open"),
        ("2025.11", "问卷调研", "面向全国高校与社区发放问卷 1,500 份，回收有效问卷 1,286 份", "fas:clipboard-list"),
        ("2026.01", "深度访谈", "走访北京市 ×× 区消费者协会、×× 律师事务所，访谈 42 人", "fas:comments"),
        ("2026.03", "双账号实测", "新老账号对照浏览 4 平台 18 个品类，记录价格与优惠差异", "fas:flask"),
        ("2026.06", "数据验证", "158 条观测入库，跑通“采集—检验—证据”全链路，验证方案可行", "fas:circle-check"),
    ]
    yy = 156
    for i, (d, t, desc, ic) in enumerate(steps):
        els.append(S(516, yy + 8, 10, 10, shape="ellipse", fill=solid(GOLD if i == 4 else CYAN), eid=f"p2d{i}"))
        if i < 4:
            els.append(S(520, yy + 22, 2, 52, fill=solid("#2D4E8F"), eid=f"p2ln{i}"))
        els.append(T(538, yy - 2, 70, 20, f"<p><strong>{d}</strong></p>", eid=f"p2dt{i}",
                     fontSize=12, color=GOLD if i == 4 else CYAN, wrap=False))
        els.append(T(608, yy - 2, 290, 20, f"<p><strong>{t}</strong></p>", eid=f"p2tt{i}",
                     fontSize=13, color="#FFFFFF", wrap=False))
        els.append(T(608, yy + 20, 290, 34, f"<p>{desc}</p>", eid=f"p2ds{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.35))
        yy += 68
    return els

# ---------------- P5 政策背景 ----------------
def p05_policy():
    els = bg_base() + nav("政策背景", 1)
    els += page_title_bar("算法治理上升为国家战略", "从法律到部门规章，算法价格歧视的监管框架已经形成", y=54)
    # 左：领导人照片 + 论述
    els.append(IMG(40, 108, 300, 210, "media/xi1.png", fit={"mode": "cover"},
                   cropShape={"shapeName": "roundRect", "adjustments": [6000]},
                   border={"style": "solid", "width": 1.5, "color": GOLD}, eid="p5_xi"))
    els.append(panel(40, 330, 300, 172, fill="#123C8F99", border_c=GOLD, eid="p5_q"))
    els.append(T(56, 342, 268, 20, "<p><strong>党中央高度重视平台经济治理</strong></p>",
                 eid="p5_qt", fontSize=13.5, color=GOLD_L, wrap=False))
    els.append(T(56, 366, 268, 128,
                 "<p>习近平总书记在中央财经委员会第九次会议上强调，要<b>“推动平台经济规范健康持续发展”</b>。</p>"
                 "<p>党的二十届三中全会《决定》明确提出：<b>“促进平台经济创新发展，健全平台经济常态化监管制度。”</b></p>"
                 "<p style=\"margin-top:6px\"><span style=\"color:#8FAADC;font-size:10px\">本项目正是青年学子对“常态化监管”号召的技术回应。</span></p>",
                 eid="p5_qb", fontSize=11.5, color="#FFFFFF", lineHeight=1.5))
    # 右：三部法规卡片
    laws = [
        ("2021.11 施行", "《个人信息保护法》第 24 条", "自动化决策应当透明、公平、公正，不得对个人在交易价格等交易条件上实行不合理的差别待遇。", "fas:scale-balanced"),
        ("2022.03 施行", "《互联网信息服务算法推荐管理规定》", "四部门联合发布，剑指算法歧视、大数据杀熟，要求算法推荐服务坚持公平公正、向上向善。", "fas:landmark"),
        ("2024.09 施行", "《网络反不正当竞争暂行规定》", "市场监管总局进一步细化“大数据杀熟”行为的认定标准与处罚原则，常态化监管落地。", "fas:gavel"),
    ]
    yy = 108
    for i, (d, t, desc, ic) in enumerate(laws):
        els.append(panel(360, yy, 560, 82, eid=f"p5l{i}"))
        els.append(S(374, yy + 18, 46, 46, shape="roundRect", adjustments=[24000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1, "color": "#3B82F6"}, eid=f"p5li{i}"))
        els.append(ICON(385, yy + 29, 24, 24, ic, GOLD, eid=f"p5lic{i}"))
        els.append(T(436, yy + 10, 120, 20, f"<p>{d}</p>", eid=f"p5ld{i}",
                     fontSize=11, color=CYAN, wrap=False))
        els.append(T(436, yy + 30, 470, 22, f"<p><strong>{t}</strong></p>", eid=f"p5lt{i}",
                     fontSize=15, color="#FFFFFF", wrap=False))
        els.append(T(436, yy + 54, 470, 26, f"<p>{desc}</p>", eid=f"p5lds{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.3))
        yy += 94
    # 右下：政策窗口判断
    els.append(panel(360, 392, 560, 110, fill="#FFC00018", border_c=GOLD, eid="p5w"))
    els.append(T(378, 402, 520, 22, "<p><strong>政策窗口判断</strong></p>", eid="p5w_t",
                 fontSize=14, color=GOLD_L, wrap=False))
    els.append(T(378, 426, 524, 68,
                 "<p>法律已经“亮剑”，但监管落地仍受制于<b>取证技术</b>：价格歧视发生在毫秒级的个性化页面里，传统手段难以固定证据。</p>"
                 "<p>谁能为监管与公益诉讼提供低成本、规模化的取证工具，谁就站在算法治理产业的最前沿。</p>",
                 eid="p5w_b", fontSize=11.5, color="#FFFFFF", lineHeight=1.5))
    return els

# ---------------- P6 社会痛点·案例 ----------------
def p06_cases():
    els = bg_base() + nav("社会痛点", 1)
    els += page_title_bar("“大数据杀熟”就在身边", "三个被公开报道与验证的真实案例 · 千人千价已成消费公平的隐痛", y=54)
    cases = [
        ("手机越贵，打车越贵", "复旦大学孙金云团队“2020 打车报告”",
         "团队在北京、上海、深圳、成都、重庆 5 城花费 5 万元、打车 800 余次：苹果机主更容易被专车、优享等更贵车型接单，概率约为安卓机主的 3 倍；苹果用户平均优惠 2.07 元，非苹果用户 4.12 元。",
         "800+", "次实测打车样本", "fas:taxi"),
        ("新老用户，同品不同价", "北京市消协大数据“杀熟”体验调查（2022）",
         "对淘宝、京东、拼多多等 18 个平台完成 63 个消费体验样本，其中 27 个样本新、老用户同时购买同一商品实际成交价不一致，多为优惠额度与规则差异所致。",
         "43%", "样本存在新老不同价", "fas:cart-shopping"),
        ("路程一样，收费两样", "上海市消保委网约车暗访（2021）",
         "对在上海运营的 10 家网约车平台进行 110 次模拟乘坐，其中 57 次被多算路程、40 次被多算时间；当年全市网约车投诉 586 件，约四分之一涉及计费纠纷。",
         "57/110", "次模拟乘坐被多算路程", "fas:route"),
    ]
    x0, cw, g = 40, 285, 16
    for i, (t, src, desc, num, numlb, ic) in enumerate(cases):
        x = x0 + i * (cw + g)
        els.append(panel(x, 112, cw, 388, eid=f"p6c{i}"))
        els.append(S(x + 16, 124, 44, 44, shape="roundRect", adjustments=[24000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1, "color": "#3B82F6"}, eid=f"p6ci{i}"))
        els.append(ICON(x + 26, 134, 24, 24, ic, CYAN, eid=f"p6cic{i}"))
        els.append(T(x + 70, 126, cw - 84, 40, f"<p><strong>{t}</strong></p>", eid=f"p6ct{i}",
                     fontSize=16, color="#FFFFFF", lineHeight=1.15, align=["left", "middle"]))
        els.append(T(x + 16, 176, cw - 32, 18, f"<p>{src}</p>", eid=f"p6cs{i}",
                     fontSize=10.5, color=GOLD_L, wrap=False))
        els.append(T(x + 16, 200, cw - 32, 180, f"<p>{desc}</p>", eid=f"p6cd{i}",
                     fontSize=11.5, color=SUB, lineHeight=1.55))
        els.append(S(x + 16, 388, cw - 32, 1.5, fill=solid("#2D4E8F"), eid=f"p6cl{i}"))
        els.append(T(x + 16, 400, cw - 32, 44,
                     f'<p><span style="font-size:30px;color:{GOLD}"><strong>{num}</strong></span></p>',
                     eid=f"p6cn{i}", wrap=False, align=["center", "middle"]))
        els.append(T(x + 16, 448, cw - 32, 20, f"<p>{numlb}</p>", eid=f"p6cnl{i}",
                     fontSize=10.5, color=SUB, wrap=False, align=["center", "middle"]))
    els.append(T(40, 508, 880, 18,
                 "<p>资料来源：复旦大学“2020 打车报告”、北京市消费者协会 2022 年大数据“杀熟”调查报告、上海市消保委 2021 年网约车暗访通报（公开报道整理）</p>",
                 eid="p6src", fontSize=9.5, color=DIM, wrap=False))
    return els

# ---------------- P7 痛点量化 ----------------
def p07_data():
    els = bg_base() + nav("痛点量化", 1)
    els += page_title_bar("维权意愿与取证能力之间的巨大鸿沟", "北京市消协 2022 年调查：受侵害者众，依法维权者寡", y=54)
    # 左：条形图
    els.append(panel(40, 112, 500, 300, eid="p7ch"))
    els.append(T(58, 122, 460, 22, "<p><strong>受访者态度调查（占比 %）</strong></p>",
                 eid="p7cht", fontSize=14, color="#FFFFFF", wrap=False))
    els.append({"elementId": "p7chart", "elementType": "chart", "bounds": [56, 148, 468, 254],
                "data": {"cols": ["item", "ratio"],
                         "rows": [["认为杀熟现象普遍", 82.37], ["有过被杀熟经历", 86.91],
                                  ["认为杀熟损害权益", 89.56], ["认为不容易取证", 79.53],
                                  ["认为监管手段跟不上", 88.01], ["选择司法诉讼维权", 0.43]]},
                "series": [{"type": "bar", "encode": {"x": "ratio", "y": "item"}, "name": "占比",
                            "dataLabels": {"show": True, "fontSize": 10, "color": "#FFFFFF"},
                            "fill": {"type": "gradient", "gradientType": "linear", "angle": 0,
                                     "stops": [{"position": 0, "color": "#38BDF8"}, {"position": 1, "color": "#FFC000"}]}}],
                "xAxis": {"label": {"fontSize": 9, "color": "#C7D7F2"}, "max": 100},
                "yAxis": {"label": {"fontSize": 10, "color": "#C7D7F2"}},
                "legend": False, "barWidth": 0.55})
    # 右上 KPI：规模
    els += kpi(556, 112, 175, 128, "9.74", "亿人", "全国网络购物用户", "CNNIC 第 55 次报告（2024.12）")
    els += kpi(745, 112, 175, 128, "15.52", "万亿元", "2024 全国网上零售额", "国家统计局，同比 +7.2%")
    # 右中：鸿沟可视化
    els.append(panel(556, 254, 364, 158, fill="#123C8F99", border_c=GOLD, eid="p7gap"))
    els.append(T(572, 264, 330, 20, "<p><strong>一道触目惊心的算术题</strong></p>",
                 eid="p7gap_t", fontSize=14, color=GOLD_L, wrap=False))
    els.append(T(572, 288, 334, 116,
                 '<p>若按 86.91% 的被侵害比例估算，全国约有 <span style="color:#FFC000"><strong>8.5 亿</strong></span> 网购用户曾遭遇“杀熟”；</p>'
                 '<p>而选择司法诉讼维权的比例仅为 <span style="color:#FFC000"><strong>0.43%</strong></span>。</p>'
                 '<p style="margin-top:6px"><strong>鸿沟的根源不在法律缺失，而在证据缺失</strong>——杀熟证据藏在个性化页面里，普通消费者“看不见、存不下、证不了”。</p>',
                 eid="p7gap_b", fontSize=11.5, color="#FFFFFF", lineHeight=1.55))
    # 右下：三个“不”
    tri = [("看不见", "价格千人千面，歧视无感发生", "fas:eye-slash"),
           ("存不下", "页面随时改版，截图难以自证", "fas:camera"),
           ("证不了", "单个样本无法排除促销干扰", "fas:file-circle-xmark")]
    for i, (t, d, ic) in enumerate(tri):
        x = 40 + i * 173
        els.append(panel(x, 428, 161, 74, eid=f"p7t{i}"))
        els.append(ICON(x + 12, 440, 22, 22, ic, GOLD, eid=f"p7tic{i}"))
        els.append(T(x + 42, 436, 112, 20, f"<p><strong>{t}</strong></p>", eid=f"p7tt{i}",
                     fontSize=14, color="#FFFFFF", wrap=False))
        els.append(T(x + 12, 464, 140, 32, f"<p>{d}</p>", eid=f"p7td{i}",
                     fontSize=10, color=SUB, lineHeight=1.3))
    els.append(panel(575, 428, 345, 74, fill="#0C2B66CC", border_c="#2D4E8F", eid="p7so"))
    els.append(T(591, 436, 320, 58,
                 '<p><strong>我们的破题点：</strong>用浏览器插件把每一次浏览变成一条<b>标准化观测记录</b>，用统计检验把零散感受变成<b>可呈证结论</b>。</p>',
                 eid="p7so_b", fontSize=11.5, color="#FFFFFF", lineHeight=1.5, align=["left", "middle"]))
    return els

# ---------------- P8 调研过程 ----------------
def p08_process():
    els = bg_base() + nav("调研过程", 1)
    els += page_title_bar("九个月，四座城市，一场取证接力", "问卷调查 + 深度访谈 + 双账号实测 + 数据验证 四位一体", y=54)
    # 上：方法矩阵
    methods = [
        ("问卷调查", "面向 21 省高校与社区", "1,500 份发放 / 1,286 份有效", "覆盖学生、上班族、退休人群等 6 类消费群体", "fas:clipboard-list"),
        ("深度访谈", "消协 / 律所 / 高校", "42 人半结构化访谈", "消费者维权者 18 人、公益律师 9 人、消协干部 7 人、算法工程师 8 人", "fas:comments"),
        ("双账号实测", "4 平台 18 个品类", "新老账号对照浏览", "同一商品同屏比价，记录标价、券后价与补贴差异", "fas:flask"),
        ("数据验证", "自研插件试采集", "158 条真实观测", "验证“页面→数据→检验→证据”链路可行", "fas:circle-check"),
    ]
    x0, cw, g = 40, 212, 14
    for i, (t, a, b, c, ic) in enumerate(methods):
        x = x0 + i * (cw + g)
        els.append(panel(x, 112, cw, 168, eid=f"p8m{i}"))
        els.append(ICON(x + 14, 126, 26, 26, ic, CYAN, eid=f"p8mic{i}"))
        els.append(T(x + 48, 128, cw - 60, 24, f"<p><strong>{t}</strong></p>", eid=f"p8mt{i}",
                     fontSize=15, color="#FFFFFF", wrap=False))
        els.append(T(x + 14, 162, cw - 28, 18, f"<p>{a}</p>", eid=f"p8ma{i}",
                     fontSize=10.5, color=GOLD_L, wrap=False))
        els.append(T(x + 14, 182, cw - 28, 18, f"<p>{b}</p>", eid=f"p8mb{i}",
                     fontSize=11, color="#FFFFFF", wrap=False))
        els.append(T(x + 14, 202, cw - 28, 66, f"<p>{c}</p>", eid=f"p8mc{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.4))
    # 下：调研地图/时间线
    els.append(panel(40, 296, 880, 206, eid="p8tl"))
    els.append(T(58, 306, 500, 22, "<p><strong>调研路线与关键节点</strong></p>", eid="p8tlt",
                 fontSize=15, color="#FFFFFF", wrap=False))
    els.append(T(640, 308, 260, 18, "<p>（此处可替换为调研照片墙）</p>", eid="p8tlph",
                 fontSize=10, color=DIM, wrap=False, align=["right", "middle"]))
    nodes = [
        ("2025.09", "北京", "文献与判例\n调研启动"),
        ("2025.11", "线上 21 省", "问卷发放与\n回收分析"),
        ("2026.01", "北京 ×× 区", "消协与律所\n实地访谈"),
        ("2026.03", "4 大电商平台", "新老账号\n对照实测"),
        ("2026.05", "×× 大学", "插件试采集\n158 条数据"),
        ("2026.06", "北京", "调研报告\n定稿立项"),
    ]
    x_start, x_step, yy = 90, 158, 360
    els.append(LN(x_start, yy + 8, x_step * 5, 4, f"0,2 {x_step*5},2", [x_step * 5, 4],
                  curve="sharp", border={"style": "solid", "width": 2, "color": "#3B82F6"}, eid="p8axis"))
    for i, (d, loc, t) in enumerate(nodes):
        x = x_start + i * x_step
        c = GOLD if i in (3, 5) else CYAN
        els.append(S(x - 7, yy, 14, 14, shape="ellipse", fill=solid(c), eid=f"p8n{i}"))
        els.append(T(x - 50, yy - 34, 100, 18, f"<p><strong>{d}</strong></p>", eid=f"p8d{i}",
                     fontSize=11, color=c, wrap=False, align=["center", "middle"]))
        els.append(T(x - 60, yy + 22, 120, 18, f"<p><strong>{loc}</strong></p>", eid=f"p8l{i}",
                     fontSize=11.5, color="#FFFFFF", wrap=False, align=["center", "middle"]))
        lines = t.split("\n")
        els.append(T(x - 60, yy + 42, 120, 34, "".join(f"<p>{s}</p>" for s in lines), eid=f"p8tt{i}",
                     fontSize=10, color=SUB, lineHeight=1.3, align=["center", "top"]))
    els.append(T(58, 466, 844, 24,
                 "<p>调研产出：《电商价格歧视取证需求调研报告》1 份、访谈纪要 42 份、对照观测数据集 1 套 —— 全部留档备查</p>",
                 eid=f"p8out", fontSize=11, color=GOLD_L, wrap=False, align=["center", "middle"]))
    return els

# ---------------- P9 调研发现 ----------------
def p09_findings():
    els = bg_base() + nav("调研发现", 1)
    els += page_title_bar("四个核心发现，一个确定性机会", "需求真实 · 堵点清晰 · 工具缺位 · 标准缺失", y=54)
    finds = [
        ("发现一", "需求真实且普遍", "86.91% 受访者有被杀熟经历，覆盖网购、外卖、打车、在线旅游全场景；超九成受访者认为应加强监管与立法。",
         "需求侧", "fas:users"),
        ("发现二", "取证是最大堵点", "79.53% 受访者认为杀熟“不容易取证”；受访律师一致认为：单个截图难以排除促销干扰，法院采信度低。",
         "供给侧", "fas:magnifying-glass"),
        ("发现三", "技术工具缺位", "市面工具要么面向比价导购（不以取证为目标），要么面向企业风控；面向公益诉讼的公益型取证工具为空白。",
         "工具侧", "fas:toolbox"),
        ("发现四", "证据标准缺失", "消协与检察院均表示：缺乏“群体级、可复现、含检验过程”的标准化证据包，个案难以升级为公益诉讼。",
         "标准侧", "fas:file-contract"),
    ]
    x0, y0, cw, ch, g = 40, 116, 428, 122, 24
    for i, (tag, t, desc, side, ic) in enumerate(finds):
        x, y = x0 + (i % 2) * (cw + g), y0 + (i // 2) * (ch + g)
        els.append(panel(x, y, cw, ch, eid=f"p9f{i}"))
        els.append(S(x + 14, y + 14, 54, 20, shape="roundRect", adjustments=[50000],
                     fill=solid("#FFC00022"), border={"style": "solid", "width": 1, "color": GOLD}, eid=f"p9tag{i}"))
        els.append(T(x + 14, y + 14, 54, 20, f"<p>{tag}</p>", eid=f"p9tagt{i}",
                     fontSize=10.5, color=GOLD, bold=True, wrap=False, align=["center", "middle"]))
        els.append(ICON(x + cw - 46, y + 14, 28, 28, ic, CYAN, eid=f"p9ic{i}"))
        els.append(T(x + 78, y + 12, cw - 140, 26, f"<p><strong>{t}</strong></p>", eid=f"p9t{i}",
                     fontSize=16, color="#FFFFFF", wrap=False, align=["left", "middle"]))
        els.append(T(x + 14, y + 46, cw - 28, 66, f"<p>{desc}</p>", eid=f"p9d{i}",
                     fontSize=11, color=SUB, lineHeight=1.5))
    # 底部机会结论
    els.append(panel(40, 400, 880, 102, fill="#FFC00018", border_c=GOLD, eid="p9op"))
    els.append(ICON(64, 426, 40, 40, "fas:lightbulb", GOLD, eid="p9op_i"))
    els.append(T(122, 412, 780, 26, "<p><strong>确定性机会：公益诉讼取证工具</strong></p>",
                 eid="p9op_t", fontSize=18, color=GOLD_L, wrap=False))
    els.append(T(122, 442, 780, 50,
                 "<p>四个发现共同指向同一空白：把“众包采集的规模优势”与“统计检验的证据效力”结合，为消协、公益律师、检察机关提供<b>开箱即用的群体级取证基础设施</b>——这正是本项目的立项原点。</p>",
                 eid="p9op_b", fontSize=12, color="#FFFFFF", lineHeight=1.5))
    return els

# ---------------- P10 取证困境（问题导向） ----------------
def p10_problem():
    els = bg_base() + nav("问题导向", 1)
    els += page_title_bar("传统取证的四道关卡", "从创意到研发、从问题到方案 —— 我们遵循创新的一般过程定义问题", y=54)
    probs = [
        ("① 数据困在页面里", "价格藏在 React SSR 页面与内嵌 JSON 中，手工抄录效率低、易出错；页面一改版，证据即灭失。",
         "破解思路：双通道自动提取（DOM 选择器 + 内嵌 JSON 回退），页面改版双保险。", "fas:bug"),
        ("② 单点证据没效力", "单次截图无法排除新人券、时段促销等干扰因素，法庭难以采信；需要群体级、可复现的对照数据。",
         "破解思路：众包汇聚 + Mann-Whitney U 检验 + OLS 回归控制变量，结论可复现。", "fas:scale-unbalanced"),
        ("③ 隐私合规红线", "取证必须经本人授权、最小化采集；昵称、cookie 值等敏感信息绝不能碰，否则证据反而有瑕疵。",
         "破解思路：授权优先 + 白名单脱敏，sanitize() 逐字段显式拷贝，敏感字段绝不上传。", "fas:user-shield"),
        ("④ 证据链不完整", "零散文档缺少采集时间、环境、校验值等元数据，无法形成完整证据链，公益诉讼门槛难以跨越。",
         "破解思路：一键导出含 SHA-256 校验清单的标准证据包，对接公益诉讼流程。", "fas:link"),
    ]
    y0, ch, g = 112, 92, 14
    for i, (t, desc, sol, ic) in enumerate(probs):
        y = y0 + i * (ch + g)
        els.append(panel(40, y, 560, ch, eid=f"p10p{i}"))
        els.append(ICON(58, y + 16, 26, 26, ic, "#FF8A8A", eid=f"p10ic{i}"))
        els.append(T(96, y + 10, 490, 22, f"<p><strong>{t}</strong></p>", eid=f"p10t{i}",
                     fontSize=15, color="#FFFFFF", wrap=False))
        els.append(T(96, y + 34, 490, 52, f"<p>{desc}</p>", eid=f"p10d{i}",
                     fontSize=11, color=SUB, lineHeight=1.45))
        els.append(panel(612, y, 308, ch, fill="#123C8F99", border_c="#3B82F6", eid=f"p10s{i}"))
        els.append(T(626, y + 8, 282, ch - 16, f"<p>{sol}</p>", eid=f"p10st{i}",
                     fontSize=11, color="#FFFFFF", lineHeight=1.45, align=["left", "middle"]))
    return els
