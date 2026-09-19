# -*- coding: utf-8 -*-
"""第三章 个人成长：P25-P30；第四章 产业价值：P32-P38"""
from core import *
from skeletons import nav, page_title_bar, panel, kpi, chip, feature_row

# ---------------- P25 立德树人 ----------------
def p25_values():
    els = bg_base() + nav("立德树人", 3)
    els += page_title_bar("科技向善：把论文写在祖国大地上", "项目弘扬正确价值观 · 厚植家国情怀 · 恪守伦理规范", y=54)
    # 左：公益初心
    els.append(panel(40, 112, 440, 240, fill="#123C8F99", border_c=GOLD, eid="p25heart"))
    els.append(T(58, 124, 400, 24, "<p><strong>为什么是我们？为什么是现在？</strong></p>",
                 eid="p25heart_t", fontSize=16, color=GOLD_L, wrap=False))
    els.append(T(58, 156, 404, 188,
                 "<p>“国家完善法律法规，我们为法律装上‘眼睛’。”</p>"
                 "<p style=\"margin-top:8px\">项目萌芽于一堂《电子商务法》研讨课：老师讲到公益诉讼“取证难”时，我们意识到——<b>计算机技术能做的事，远比吐槽更多</b>。</p>"
                 "<p style=\"margin-top:8px\">从课堂问题到社会方案，我们选择把专业能力对准 9.74 亿网购者的公平交易权，这正是新时代青年“把论文写在祖国大地上”的具体行动。</p>",
                 eid="p25heart_b", fontSize=12, color="#FFFFFF", lineHeight=1.6))
    # 左下：伦理规范
    els.append(panel(40, 366, 440, 136, eid="p25ethic"))
    els.append(T(58, 376, 400, 22, "<p><strong>恪守伦理规范的三条底线</strong></p>", eid="p25ethic_t",
                 fontSize=14, color="#FFFFFF", wrap=False))
    els.append(T(58, 402, 404, 92,
                 "<p>· 只做<b>经本人授权</b>的最小化采集，技术能力让位于伦理约束</p>"
                 "<p>· 只输出<b>群体级统计结论</b>，不针对任何具体个人或商家定性</p>"
                 "<p>· 坚持<b>公益属性</b>：核心代码 MIT 开源，接受全社会审计</p>",
                 eid="p25ethic_b", fontSize=11, color=SUB, lineHeight=1.6))
    # 右：价值观三卡
    vals = [
        ("家国情怀", "响应平台经济常态化监管部署，用技术服务国家算法治理大局", "fas:flag", GOLD),
        ("公平正义", "守护消费者知情权与公平交易权，让数字红利人人共享", "fas:scale-balanced", CYAN),
        ("创新精神", "敢闯无人区：全国首个面向公益诉讼的众包取证开源工具", "fas:lightbulb", "#7EE2A8"),
    ]
    yy = 112
    for i, (t, d, ic, c) in enumerate(vals):
        els.append(panel(496, yy, 424, 120, eid=f"p25v{i}"))
        els.append(S(512, yy + 16, 52, 52, shape="roundRect", adjustments=[24000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1.2, "color": c}, eid=f"p25vi{i}"))
        els.append(ICON(525, yy + 29, 26, 26, ic, c, eid=f"p25vic{i}"))
        els.append(T(580, yy + 16, 324, 26, f"<p><strong>{t}</strong></p>", eid=f"p25vt{i}",
                     fontSize=17, color="#FFFFFF", wrap=False))
        els.append(T(580, yy + 48, 324, 58, f"<p>{d}</p>", eid=f"p25vd{i}",
                     fontSize=11.5, color=SUB, lineHeight=1.5))
        yy += 134
    return els

# ---------------- P26 负责人成长档案 ----------------
def p26_leader():
    els = bg_base() + nav("负责人成长档案", 3)
    els += page_title_bar("项目负责人：从课堂学生到开源项目维护者", "个人成长 · 过程性经历（照片与信息可替换）", y=54)
    # 左：照片 + 基本信息
    els.append(IMG(56, 120, 168, 224, "media/portrait.png", fit={"mode": "cover"},
                   cropShape={"shapeName": "roundRect", "adjustments": [5000]},
                   border={"style": "solid", "width": 2, "color": GOLD},
                   shadow={"blur": 16, "color": "#00000066", "offset": [0, 6]}, eid="p26photo"))
    els.append(T(56, 352, 168, 26, "<p><strong>×××（替换姓名）</strong></p>", eid="p26name",
                 fontSize=16, color=GOLD_L, wrap=False, align=["center", "middle"]))
    els.append(T(56, 380, 168, 40, "<p>×× 大学 ×× 学院\n计算机科学与技术 · 大二在读</p>", eid="p26info",
                 fontSize=10.5, color=SUB, lineHeight=1.4, align=["center", "top"]))
    # 中：成长经历
    els.append(panel(248, 112, 400, 390, eid="p26grow"))
    els.append(T(266, 122, 360, 22, "<p><strong>成长轨迹（过程性经历）</strong></p>", eid="p26grow_t",
                 fontSize=15, color="#FFFFFF", wrap=False))
    grows = [
        ("2024.09", "入学 ×× 大学计算机系，加入学院科技创新协会"),
        ("2025.03", "《电子商务法》研讨课上确立选题，组建 5 人团队"),
        ("2025.06", "完成插件 v0.1：只会“抄价格”的粗糙原型"),
        ("2025.11", "主导 1,286 份问卷调研，学会把社会问题翻译成技术指标"),
        ("2026.03", "攻克 2025 版淘系页面双渲染态适配，提取准确率从 62% 提升至 98%"),
        ("2026.06", "独立完成后端统计引擎，MWU + OLS 管线全通"),
        ("2026.09", "发布 v0.4.0 公网版，项目进入市赛备战阶段"),
    ]
    yy = 152
    for i, (d, t) in enumerate(grows):
        c = GOLD if i in (4, 6) else CYAN
        els.append(S(272, yy + 4, 9, 9, shape="ellipse", fill=solid(c), eid=f"p26gn{i}"))
        if i < 6:
            els.append(S(276, yy + 15, 2, 30, fill=solid("#2D4E8F"), eid=f"p26gl{i}"))
        els.append(T(292, yy - 2, 70, 20, f"<p><strong>{d}</strong></p>", eid=f"p26gd{i}",
                     fontSize=11, color=c, wrap=False))
        els.append(T(366, yy - 2, 268, 40, f"<p>{t}</p>", eid=f"p26gt{i}",
                     fontSize=10.5, color="#FFFFFF", lineHeight=1.3))
        yy += 48
    # 右：成果与标签
    els.append(panel(664, 112, 256, 240, eid="p26ach"))
    els.append(T(682, 122, 220, 22, "<p><strong>已取得成果</strong></p>", eid="p26ach_t",
                 fontSize=14, color="#FFFFFF", wrap=False))
    achs = ["校级大学生创新训练计划立项（负责人）", "×× 竞赛校级 × 等奖（替换）", "GPA ×.× / 4.0 · 专业前 ××%", "GitHub 开源项目维护者（8 个版本迭代）", "×× 奖学金（替换）"]
    for i, a in enumerate(achs):
        y = 150 + i * 38
        els.append(ICON(682, y, 16, 16, "fas:award", GOLD, eid=f"p26a{i}"))
        els.append(T(706, y - 2, 200, 36, f"<p>{a}</p>", eid=f"p26at{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.3))
    els.append(panel(664, 366, 256, 136, fill="#FFC00018", border_c=GOLD, eid="p26sum"))
    els.append(T(682, 376, 220, 116,
                 '<p><strong>评委请看这里：</strong></p>'
                 '<p style="margin-top:6px">负责人独立完成全部核心代码 <b>1.2 万行</b>、撰写调研报告 <b>2.6 万字</b>，完成了从“写课程作业”到“维护真实开源项目”的跃迁。</p>',
                 eid="p26sum_b", fontSize=11, color="#FFFFFF", lineHeight=1.5))
    return els

# ---------------- P27 知识转化 ----------------
def p27_knowledge():
    els = bg_base() + nav("知识转化", 3)
    els += page_title_bar("把课堂知识炼成项目能力", "学以致用：六门课程知识在项目中逐一落地", y=54)
    rows = [
        ("《程序设计基础 / TypeScript》", "浏览器插件全栈开发", "MV3 插件架构、content/background 通信、Shadow DOM 提示条", "fas:code"),
        ("《数据结构与算法》", "采集管线设计", "平台选择器规则引擎、去重哈希表、滚动淘汰队列（500 条上限）", "fas:diagram-project"),
        ("《概率论与数理统计》", "歧视判定引擎", "Mann-Whitney U 检验、p 值解读、小样本降级策略", "fas:chart-line"),
        ("《回归分析 / 计量方法》", "混杂因素控制", "OLS + HC3 稳健标准误，控制城市/时段/设备等协变量", "fas:square-root-variable"),
        ("《电子商务法 / 消费者权益保护法》", "证据规则设计", "自动化决策条款适用、证据链完整性、公益诉讼证据标准", "fas:gavel"),
        ("《软件工程》", "工程质量保障", "19+29 项自动化测试、版本管理、两段式构建核验", "fas:list-check"),
    ]
    y0, ch, g = 112, 62, 6
    for i, (course, ability, detail, ic) in enumerate(rows):
        y = y0 + i * (ch + g)
        els.append(panel(40, y, 880, ch, eid=f"p27r{i}"))
        els.append(S(54, y + 13, 36, 36, shape="roundRect", adjustments=[24000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1, "color": "#3B82F6"}, eid=f"p27ic{i}"))
        els.append(ICON(63, y + 22, 18, 18, ic, CYAN, eid=f"p27iic{i}"))
        els.append(T(104, y + 8, 250, 44, f"<p><strong>{course}</strong></p>", eid=f"p27c{i}",
                     fontSize=12, color="#FFFFFF", lineHeight=1.3, align=["left", "middle"]))
        els.append(ICON(362, y + 22, 18, 18, "fas:angles-right", GOLD, eid=f"p27ar{i}"))
        els.append(T(392, y + 8, 160, 44, f"<p><strong>{ability}</strong></p>", eid=f"p27a{i}",
                     fontSize=12, color=GOLD_L, lineHeight=1.3, align=["left", "middle"]))
        els.append(T(560, y + 8, 348, 44, f"<p>{detail}</p>", eid=f"p27d{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.35, align=["left", "middle"]))
    els.append(T(40, 508, 880, 18,
                 "<p>知识掌握与应用能力：每一行代码都能回溯到一门课程、每一门课程都在项目中找到了真实问题</p>",
                 eid="p27note", fontSize=11, color=DIM, wrap=False, align=["center", "middle"]))
    return els

# ---------------- P28 能力跃迁（雷达图） ----------------
def p28_growth():
    els = bg_base() + nav("能力跃迁", 3)
    els += page_title_bar("一年前的我们，写不出今天的一行代码", "项目成长对团队成员创新精神、创新意识、创新能力的锻炼和提升", y=54)
    # 左：雷达图
    els.append(panel(40, 112, 420, 390, eid="p28radar"))
    els.append(T(58, 122, 380, 22, "<p><strong>团队能力雷达（立项前 → 现在）</strong></p>",
                 eid="p28radar_t", fontSize=14, color="#FFFFFF", wrap=False))
    els.append({"elementId": "p28rchart", "elementType": "chart", "bounds": [70, 150, 360, 340],
                "data": {"cols": ["dim", "before", "now"],
                         "rows": [["工程实现", 2, 5], ["数据与统计", 1, 4], ["法律素养", 1, 4],
                                  ["调研与沟通", 2, 5], ["产品与商业", 1, 4], ["协作与领导", 2, 4]]},
                "series": [
                    {"type": "radar", "name": "立项前（2025.03）", "encode": {"category": "dim", "y": "before"},
                     "areaColor": "#8FAADC40", "lineColor": "#8FAADC"},
                    {"type": "radar", "name": "现在（2026.09）", "encode": {"category": "dim", "y": "now"},
                     "areaColor": "#FFC0004D", "lineColor": "#FFC000"},
                ],
                "spokeAxis": {"max": 5, "label": {"fontSize": 10, "color": "#C7D7F2"}},
                "legend": {"fontSize": 10, "color": "#FFFFFF"}})
    # 右：跃迁故事
    stories = [
        ("从“调不通”到“架构师”", "第一个版本连 manifest 都写错；现在能独立设计端云协同架构、制定字段 schema 与鉴权体系。", "fas:code"),
        ("从“背公式”到“用公式”", "统计课上的 U 检验曾是考题；现在它是判定歧视的引擎，我们懂了 p 值背后的证据逻辑。", "fas:square-root-variable"),
        ("从“法条读者”到“规则译者”", "把《个保法》第 24 条翻译成六条隐私红线写进代码，法律素养变成了产品约束。", "fas:gavel"),
        ("从“社恐”到“访谈 42 人”", "敲门走进消协与律所，学会把技术语言翻译成对方听得懂的价值主张。", "fas:comments"),
    ]
    yy = 112
    for i, (t, d, ic) in enumerate(stories):
        els.append(panel(476, yy, 444, 90, eid=f"p28s{i}"))
        els.append(ICON(494, yy + 16, 26, 26, ic, GOLD, eid=f"p28ic{i}"))
        els.append(T(534, yy + 10, 370, 22, f"<p><strong>{t}</strong></p>", eid=f"p28t{i}",
                     fontSize=13.5, color="#FFFFFF", wrap=False))
        els.append(T(534, yy + 36, 372, 46, f"<p>{d}</p>", eid=f"p28d{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.4))
        yy += 100
    return els

# ---------------- P29 学校支持 ----------------
def p29_school():
    els = bg_base() + nav("人才培养成效", 3)
    els += page_title_bar("项目背后，是学校完整的育人体系", "新工科建设成果 · 产教融合 · 专创融合 —— 院校给予的关键支持", y=54)
    sups = [
        ("课程土壤", "《电子商务法》《回归分析》等课程为项目提供跨学科知识底座；研讨课上的真实问题成为选题原点", "fas:book-open", "课程"),
        ("导师引路", "计算机学院 ××× 副教授（技术导师）与法学院 ××× 教授（法律顾问）双导师制，每两周一次例会", "fas:chalkboard-user", "导师"),
        ("平台支撑", "学校大学生创新训练计划立项资助 × 万元；学院开放实验室与服务器资源供压测使用", "fas:school", "平台"),
        ("孵化加速", "校产业孵化园提供办公工位与法务咨询，协助对接 ×× 区消协与两家律师事务所", "fas:rocket", "孵化"),
    ]
    x0, y0, cw, ch, g = 40, 116, 428, 140, 24
    for i, (t, d, ic, tag) in enumerate(sups):
        x, y = x0 + (i % 2) * (cw + g), y0 + (i // 2) * (ch + g)
        els.append(panel(x, y, cw, ch, eid=f"p29s{i}"))
        els.append(ICON(x + 18, y + 16, 30, 30, ic, GOLD, eid=f"p29ic{i}"))
        els.append(T(x + 62, y + 14, 200, 26, f"<p><strong>{t}</strong></p>", eid=f"p29t{i}",
                     fontSize=16, color="#FFFFFF", wrap=False))
        els.append(S(x + cw - 74, y + 16, 56, 22, shape="roundRect", adjustments=[50000],
                     fill=solid("#FFC00022"), border={"style": "solid", "width": 1, "color": GOLD}, eid=f"p29tag{i}"))
        els.append(T(x + cw - 74, y + 16, 56, 22, f"<p>{tag}</p>", eid=f"p29tagt{i}",
                     fontSize=10.5, color=GOLD, bold=True, wrap=False, align=["center", "middle"]))
        els.append(T(x + 18, y + 52, cw - 36, 76, f"<p>{d}</p>", eid=f"p29d{i}",
                     fontSize=11, color=SUB, lineHeight=1.5))
    # 底：育人模式
    els.append(panel(40, 428, 880, 74, fill="#123C8F99", border_c="#3B82F6", eid="p29model"))
    els.append(T(58, 436, 844, 58,
                 '<p><strong>育人模式印证：</strong>项目完整经历了“课程学习 → 大创立项 → 竞赛打磨 → 孵化落地”的学校双创培养链路，</p>'
                 '<p>是 <b>专创融合、产教融合、多学科交叉</b>（计算机 × 法学 × 统计学）在本科人才培养中的一次集中检验。</p>',
                 eid="p29model_b", fontSize=11.5, color="#FFFFFF", lineHeight=1.5, align=["left", "middle"]))
    return els

# ---------------- P30 反哺学校 ----------------
def p30_feedback():
    els = bg_base() + nav("反哺学校", 3)
    els += page_title_bar("项目走出课堂，成果回到课堂", "以项目反哺教学、科研与双创生态", y=54)
    backs = [
        ("反哺教学", "插件源码与 4 个真实页面测试用例进入《Web 开发》课程案例库；面向新生开展 3 场“从课堂到开源”分享会", "fas:chalkboard", "覆盖 300+ 人次"),
        ("反哺科研", "158 条真实观测数据已脱敏共享给法学院 ××× 教授团队，支撑其算法治理课题的实证分析", "fas:microscope", "1 个校级课题"),
        ("反哺双创", "以老带新组建 8 人竞赛梯队，2 名大一成员已成为插件 v0.5 的核心开发者", "fas:people-group", "梯队 8 人"),
        ("反哺社会", "面向校园与社区开展“防范大数据杀熟”科普宣讲，发放自研《消费者自我保护手册》", "fas:hand-holding-heart", "宣讲 5 场"),
    ]
    x0, y0, cw, ch, g = 40, 116, 428, 180, 24
    for i, (t, d, ic, num) in enumerate(backs):
        x, y = x0 + (i % 2) * (cw + g), y0 + (i // 2) * (ch + g)
        els.append(panel(x, y, cw, ch, eid=f"p30b{i}"))
        els.append(S(x + 16, y + 16, 48, 48, shape="roundRect", adjustments=[24000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1, "color": GOLD}, eid=f"p30ic{i}"))
        els.append(ICON(x + 28, y + 28, 24, 24, ic, GOLD, eid=f"p30iic{i}"))
        els.append(T(x + 78, y + 20, 200, 26, f"<p><strong>{t}</strong></p>", eid=f"p30t{i}",
                     fontSize=16, color="#FFFFFF", wrap=False))
        els.append(T(x + 16, y + 76, cw - 32, 68, f"<p>{d}</p>", eid=f"p30d{i}",
                     fontSize=11, color=SUB, lineHeight=1.5))
        els.append(S(x + 16, y + 148, 90, 22, shape="roundRect", adjustments=[50000],
                     fill=solid("#7EE2A822"), border={"style": "solid", "width": 1, "color": "#7EE2A8"}, eid=f"p30n{i}"))
        els.append(T(x + 16, y + 148, 90, 22, f"<p>{num}</p>", eid=f"p30nt{i}",
                     fontSize=10.5, color="#7EE2A8", bold=True, wrap=False, align=["center", "middle"]))
    return els

# ---------------- P32 产业认知 ----------------
def p32_industry():
    els = bg_base() + nav("产业认知", 4)
    els += page_title_bar("算法治理：政策驱动的朝阳赛道", "产业规模 · 增长速度 · 竞争格局 · 产业趋势 · 产业政策", y=54)
    # 左：产业链
    els.append(panel(40, 112, 440, 250, eid="p32chain"))
    els.append(T(58, 122, 400, 22, "<p><strong>算法治理产业链图谱</strong></p>", eid="p32chain_t",
                 fontSize=15, color="#FFFFFF", wrap=False))
    chain = [
        ("上游 · 数据与工具", "众包采集插件、数据清洗、证据固定（本项目所在环节）", GOLD),
        ("中游 · 监管科技", "算法审计、合规检测、歧视判定、监管报送", CYAN),
        ("下游 · 应用主体", "消协组织、检察机关、市场监管、律所、平台合规部", "#7EE2A8"),
    ]
    yy = 152
    for i, (t, d, c) in enumerate(chain):
        els.append(S(58, yy, 404, 56, shape="roundRect", adjustments=[14000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1.2, "color": c}, eid=f"p32c{i}"))
        els.append(T(72, yy + 6, 380, 20, f"<p><strong>{t}</strong></p>", eid=f"p32ct{i}",
                     fontSize=12.5, color=c, wrap=False))
        els.append(T(72, yy + 28, 380, 24, f"<p>{d}</p>", eid=f"p32cd{i}",
                     fontSize=10, color=SUB, wrap=False))
        if i < 2:
            els.append(ICON(248, yy + 58, 16, 12, "fas:angle-down", DIM, eid=f"p32ca{i}"))
        yy += 68
    # 左下：趋势
    els.append(panel(40, 376, 440, 126, fill="#0A2A63DD", eid="p32trend"))
    els.append(T(58, 386, 400, 22, "<p><strong>四大产业趋势</strong></p>", eid="p32trend_t",
                 fontSize=14, color="#FFFFFF", wrap=False))
    els.append(T(58, 412, 404, 84,
                 "<p>① 监管从“专项整治”走向“常态化制度”　② 算法备案与审计成为平台合规刚需</p>"
                 "<p>③ 公益诉讼案件量持续增长，消费者保护为重点领域　④ 证据电子化、检验标准化成为司法新需求</p>",
                 eid="p32trend_b", fontSize=11, color=SUB, lineHeight=1.6))
    # 右：产业政策时间线
    els.append(panel(496, 112, 424, 250, eid="p32pol"))
    els.append(T(514, 122, 390, 22, "<p><strong>产业政策演进（监管持续加码）</strong></p>",
                 eid="p32pol_t", fontSize=15, color="#FFFFFF", wrap=False))
    pols = [
        ("2021", "《个人信息保护法》施行", "自动化决策不得不合理差别待遇"),
        ("2022", "《算法推荐管理规定》施行", "首部算法专项规章，剑指杀熟"),
        ("2024", "《网络反不正当竞争暂行规定》", "细化杀熟认定与处罚原则"),
        ("2025→", "“十五五”数字经济治理部署", "平台经济常态化监管走向纵深"),
    ]
    yy = 152
    for i, (y_, t, d) in enumerate(pols):
        els.append(T(514, yy, 52, 22, f"<p><strong>{y_}</strong></p>", eid=f"p32py{i}",
                     fontSize=13, color=GOLD if i == 3 else CYAN, wrap=False))
        els.append(T(574, yy, 330, 20, f"<p><strong>{t}</strong></p>", eid=f"p32pt{i}",
                     fontSize=11.5, color="#FFFFFF", wrap=False))
        els.append(T(574, yy + 20, 330, 18, f"<p>{d}</p>", eid=f"p32pd{i}",
                     fontSize=10, color=SUB, wrap=False))
        yy += 52
    # 右下：规模数据
    els += kpi(496, 376, 204, 126, "15.52", "万亿元", "2024 全国网上零售额", "同比增长 7.2%，连续 12 年全球第一")
    els += kpi(716, 376, 204, 126, "9.74", "亿人", "网络购物用户规模", "CNNIC：占网民整体 87.9%")
    return els

# ---------------- P33 市场规模 ----------------
def p33_market():
    els = bg_base() + nav("市场规模", 4)
    els += page_title_bar("从 9.74 亿人的痛点里长出的市场", "TAM → SAM → SOM 三层测算（团队基于公开数据测算）", y=54)
    layers = [
        ("TAM", "算法治理与监管科技总市场", "≈ 1,200 亿元/年", "以网络零售额 15.52 万亿元为基数，参照合规与审计服务渗透率 0.7‰~1‰ 估算", "#0A2A63", 880, 74),
        ("SAM", "电商价格合规与取证服务", "≈ 120 亿元/年", "聚焦电商价格歧视细分：消协/检察/律所/平台合规部的取证与检验服务预算", "#123C8F", 640, 74),
        ("SOM", "本项目 3 年可获取市场", "≈ 3,000 万元", "首期覆盖 30 家消协/检察机构 + 100 家律所 + 2 家平台合规试点，客单价 20~50 万元", "#1D4ED8", 400, 74),
    ]
    yy = 116
    for i, (tag, t, num, basis, c, w, h) in enumerate(layers):
        x = (960 - w) / 2
        els.append(S(x, yy, w, h, shape="roundRect", adjustments=[16000],
                     fill=solid(c), border={"style": "solid", "width": 1.5, "color": GOLD if i == 2 else "#3B82F6"}, eid=f"p33l{i}"))
        els.append(T(x + 24, yy + 10, 70, 30, f"<p><strong>{tag}</strong></p>", eid=f"p33tag{i}",
                     fontSize=20, color=GOLD, wrap=False, align=["left", "middle"]))
        els.append(T(x + 104, yy + 8, w - 130, 24, f"<p><strong>{t}　<span style=\"color:#FFC000\">{num}</span></strong></p>",
                     eid=f"p33t{i}", fontSize=15, color="#FFFFFF", wrap=False))
        els.append(T(x + 104, yy + 36, w - 130, 32, f"<p>{basis}</p>", eid=f"p33b{i}",
                     fontSize=10, color=SUB, lineHeight=1.35))
        yy += h + 16
    # 底：增长驱动
    drivers = [("政策驱动", "常态化监管带来机构侧刚需预算", "fas:landmark"),
               ("案件驱动", "公益诉讼案件持续增长，证据服务先行", "fas:gavel"),
               ("技术驱动", "浏览器插件形态零部署成本，可快速规模化", "fas:microchip")]
    for i, (t, d, ic) in enumerate(drivers):
        x = 40 + i * 300
        els.append(panel(x, 392, 284, 110, eid=f"p33d{i}"))
        els.append(ICON(x + 16, 408, 26, 26, ic, CYAN, eid=f"p33dic{i}"))
        els.append(T(x + 52, 404, 216, 24, f"<p><strong>{t}</strong></p>", eid=f"p33dt{i}",
                     fontSize=14, color="#FFFFFF", wrap=False))
        els.append(T(x + 16, 438, 252, 52, f"<p>{d}</p>", eid=f"p33dd{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.45))
    return els

# ---------------- P34 竞品分析 ----------------
def p34_compete():
    els = bg_base() + nav("竞品分析", 4)
    els += page_title_bar("与四类现有方案的正面比较", "我们不与比价工具竞争，我们开创“公益取证”新品类", y=54)
    headers = ["对比维度", "个人截图 / 录屏", "公证处电子公证", "商业比价工具", "本项目（众包观测）"]
    rows = [
        ["核心目标", "留证自用", "司法级留证", "帮用户省钱", "群体级歧视判定与公益诉讼支撑"],
        ["样本规模", "单点 1 条", "单点 1 条", "海量但不可用于证据", "众包海量 + 可复现检验"],
        ["证据效力", "低：易被促销解释推翻", "高但仅限当次页面", "不具备证据定位", "高：含检验过程与校验清单"],
        ["单次成本", "0 元", "约 800~1,500 元/次", "免费（导购分成盈利）", "近 0 元（公益开源）"],
        ["隐私合规", "易含个人信息", "规范", "过度采集争议多", "白名单脱敏，六条红线"],
        ["统计检验", "无", "无", "无", "MWU + OLS + 平台级复现"],
    ]
    els.append({"elementId": "p34table", "elementType": "table", "bounds": [40, 116, 880, 300],
                "columnWidths": [0.14, 0.20, 0.20, 0.20, 0.26],
                "rowHeights": [0.14, 0.172, 0.172, 0.172, 0.172, 0.172],
                "rows": [
                    [{"text": h, "bold": True, "fontSize": 12,
                      "color": "#FFFFFF" if j < 4 else "#FFC000",
                      "fill": {"type": "solid", "color": "#1D4ED8" if j < 4 else "#B45309"}}
                     for j, h in enumerate(headers)],
                ] + [
                    [{"text": r[0], "bold": True, "fontSize": 11, "color": GOLD_L},
                     {"text": r[1], "fontSize": 10.5, "color": SUB},
                     {"text": r[2], "fontSize": 10.5, "color": SUB},
                     {"text": r[3], "fontSize": 10.5, "color": SUB},
                     {"text": r[4], "fontSize": 10.5, "color": "#FFFFFF", "bold": True,
                      "fill": {"type": "solid", "color": "#7EE2A81A"}}]
                    for r in rows
                ],
                "style": {"cellStyle": {"color": "#FFFFFF", "fontSize": 10.5, "border": {"style": "solid", "width": 0.75, "color": "#2D4E8F"},
                                        "align": ["center", "middle"], "fill": {"type": "solid", "color": "#0C2B66B3"}}}})
    # 底：差异化结论
    cards = [("品类空白", "面向公益诉讼的取证工具在国内尚属空白", "fas:compass"),
             ("代际优势", "以统计检验替代单点留证，证据效力实现代际跨越", "fas:arrow-trend-up"),
             ("成本优势", "边际成本趋近于零，可覆盖长尾投诉场景", "fas:coins")]
    for i, (t, d, ic) in enumerate(cards):
        x = 40 + i * 300
        els.append(panel(x, 432, 284, 70, fill="#123C8F99", border_c=GOLD, eid=f"p34c{i}"))
        els.append(ICON(x + 14, 444, 24, 24, ic, GOLD, eid=f"p34ic{i}"))
        els.append(T(x + 48, 440, 224, 20, f"<p><strong>{t}</strong></p>", eid=f"p34ct{i}",
                     fontSize=13, color=GOLD_L, wrap=False))
        els.append(T(x + 48, 462, 224, 34, f"<p>{d}</p>", eid=f"p34cd{i}",
                     fontSize=10, color="#FFFFFF", lineHeight=1.35))
    return els

# ---------------- P35 商业模式 ----------------
def p35_business():
    els = bg_base() + nav("商业模式", 4)
    els += page_title_bar("公益为核，三层价值闭环", "C 端免费聚数据 · G/B 端服务创收入 · 收入反哺公益运营", y=54)
    tiers = [
        ("C 端 · 消费者（免费）", "浏览器插件永久免费开源", "汇聚观测数据、扩大覆盖网络", "数据贡献者", "fas:users", "#38BDF8"),
        ("G 端 · 消协 / 检察 / 市监", "取证 SaaS + 定制化数据分析", "年费 20~50 万元/机构：辖区歧视监测、批量证据包、检验报告", "核心收入", "fas:building-columns", GOLD),
        ("B 端 · 律所 / 研究机构", "证据包与 API 服务", "按案计费 0.5~2 万元/案；研究数据集授权 5~10 万元/年", "增长收入", "fas:briefcase", "#7EE2A8"),
    ]
    x0, cw, g = 40, 285, 16
    for i, (t, s, d, tag, ic, c) in enumerate(tiers):
        x = x0 + i * (cw + g)
        els.append(panel(x, 116, cw, 210, eid=f"p35t{i}"))
        els.append(S(x + 16, 130, 46, 46, shape="roundRect", adjustments=[24000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1.2, "color": c}, eid=f"p35ic{i}"))
        els.append(ICON(x + 27, 141, 24, 24, ic, c, eid=f"p35iic{i}"))
        els.append(T(x + 74, 132, cw - 90, 42, f"<p><strong>{t}</strong></p>", eid=f"p35tt{i}",
                     fontSize=14, color="#FFFFFF", lineHeight=1.2, align=["left", "middle"]))
        els.append(T(x + 16, 184, cw - 32, 20, f"<p>{s}</p>", eid=f"p35ts{i}",
                     fontSize=11, color=GOLD_L, wrap=False))
        els.append(T(x + 16, 208, cw - 32, 60, f"<p>{d}</p>", eid=f"p35td{i}",
                     fontSize=10.5, color=SUB, lineHeight=1.45))
        els.append(S(x + 16, 286, 80, 24, shape="roundRect", adjustments=[50000],
                     fill=solid("#FFC00022" if tag == "核心收入" else "#2D4E8F55"),
                     border={"style": "solid", "width": 1, "color": GOLD if tag == "核心收入" else "#2D4E8F"}, eid=f"p35tag{i}"))
        els.append(T(x + 16, 286, 80, 24, f"<p>{tag}</p>", eid=f"p35tagt{i}",
                     fontSize=10.5, color=GOLD if tag == "核心收入" else SUB, bold=True, wrap=False, align=["center", "middle"]))
    # 下：闭环图
    els.append(panel(40, 342, 880, 160, fill="#0A2A63DD", eid="p35loop"))
    els.append(T(58, 352, 400, 22, "<p><strong>价值闭环：公益与可持续的平衡术</strong></p>",
                 eid="p35loop_t", fontSize=15, color="#FFFFFF", wrap=False))
    loop = [("免费插件", "用户增长"), ("数据网络", "覆盖扩大"), ("检验能力", "结论可信"), ("机构付费", "收入形成"), ("反哺运营", "更好产品")]
    xx = 74
    for i, (t, d) in enumerate(loop):
        els.append(S(xx, 392, 130, 62, shape="roundRect", adjustments=[18000],
                     fill=solid("#123C8F"), border={"style": "solid", "width": 1, "color": "#3B82F6"}, eid=f"p35l{i}"))
        els.append(T(xx, 398, 130, 24, f"<p><strong>{t}</strong></p>", eid=f"p35lt{i}",
                     fontSize=13, color="#FFFFFF", wrap=False, align=["center", "middle"]))
        els.append(T(xx, 424, 130, 18, f"<p>{d}</p>", eid=f"p35ld{i}",
                     fontSize=9.5, color=SUB, wrap=False, align=["center", "middle"]))
        if i < 4:
            els.append(ICON(xx + 134, 414, 18, 18, "fas:angle-right", GOLD, eid=f"p35ar{i}"))
        xx += 158
    els.append(T(74, 466, 812, 24,
                 "<p>财务纪律：机构收入的 ≥30% 固定用于插件维护、数据合规审计与公益科普，确保公益属性不被商业稀释</p>",
                 eid="p35note", fontSize=11, color=GOLD_L, wrap=False, align=["center", "middle"]))
    return els

# ---------------- P36 落地进展 ----------------
def p36_landing():
    els = bg_base() + nav("落地进展", 4)
    els += page_title_bar("不是 PPT 项目：系统已真实运行", "公网部署 · 真实数据 · 真实用户旅程（截图均为系统实拍）", y=54)
    # 左：落地清单
    feats = [
        ("公网版上线", "后端 + 门户部署至 Vercel，插件 v0.4.0 内置服务器地址，解压即用", "fas:cloud-arrow-up", "已完成"),
        ("数据资产形成", "158 条真实观测入库，覆盖 2 平台 3 个可分析商品，跑通平台级检验", "fas:database", "已完成"),
        ("双登录体系", "用户免密 UUID 一键登录 + 管理员密钥哈希校验，生产级鉴权", "fas:key", "已完成"),
        ("机构对接", "与 ×× 区消协、×× 律师事务所开展试用对接（意向阶段）", "fas:handshake", "进行中"),
        ("试点城市", "拟在 ×× 高校社团与 ×× 社区招募首批 200 名志愿者", "fas:location-dot", "进行中"),
    ]
    yy = 112
    for i, (t, d, ic, st) in enumerate(feats):
        els.append(panel(40, yy, 470, 68, eid=f"p36f{i}"))
        els.append(ICON(56, yy + 20, 26, 26, ic, "#7EE2A8" if st == "已完成" else GOLD, eid=f"p36ic{i}"))
        els.append(T(94, yy + 8, 320, 22, f"<p><strong>{t}</strong></p>", eid=f"p36t{i}",
                     fontSize=13.5, color="#FFFFFF", wrap=False))
        els.append(T(94, yy + 32, 400, 30, f"<p>{d}</p>", eid=f"p36d{i}",
                     fontSize=10, color=SUB, lineHeight=1.3))
        stc = "#7EE2A8" if st == "已完成" else GOLD
        els.append(S(428, yy + 22, 66, 24, shape="roundRect", adjustments=[50000],
                     fill=solid(stc + "22"), border={"style": "solid", "width": 1, "color": stc}, eid=f"p36st{i}"))
        els.append(T(428, yy + 22, 66, 24, f"<p>{st}</p>", eid=f"p36stt{i}",
                     fontSize=10.5, color=stc, bold=True, wrap=False, align=["center", "middle"]))
        yy += 80
    # 右：门户 + 用户看板截图
    els.append(IMG(530, 112, 390, 190, "media/landing.png", fit={"mode": "cover"},
                   crop={"bottom": 0.25},
                   cropShape={"shapeName": "roundRect", "adjustments": [3000]},
                   border={"style": "solid", "width": 1.5, "color": "#3B82F6"}, eid=f"p36s1"))
    els.append(T(530, 306, 390, 18, "<p>▲ 门户首页：用户 / 管理员 / 下载 三入口</p>", eid=f"p36s1c",
                 fontSize=9.5, color=DIM, wrap=False, align=["center", "middle"]))
    els.append(IMG(530, 332, 390, 172, "media/me.png", fit={"mode": "cover"},
                   crop={"top": 0, "bottom": 0.35},
                   cropShape={"shapeName": "roundRect", "adjustments": [3000]},
                   border={"style": "solid", "width": 1.5, "color": "#3B82F6"}, eid=f"p36s2"))
    els.append(T(530, 508, 390, 16, "<p>▲ 用户看板：41 条个人观测 · 近 7 天趋势 · 明细分页</p>", eid=f"p36s2c",
                 fontSize=9.5, color=DIM, wrap=False, align=["center", "middle"]))
    return els

# ---------------- P37 财务预测 ----------------
def p37_finance():
    els = bg_base() + nav("财务预测", 4)
    els += page_title_bar("三年财务展望（团队测算）", "对目标客户与收入的合理预测 · 盈利潜力与公益可持续性兼备", y=54)
    # 左：收入预测图
    els.append(panel(40, 112, 500, 390, eid="p37chart"))
    els.append(T(58, 122, 460, 22, "<p><strong>收入与成本预测（万元）</strong></p>", eid="p37chart_t",
                 fontSize=14, color="#FFFFFF", wrap=False))
    els.append({"elementId": "p37c", "elementType": "chart", "bounds": [56, 150, 470, 340],
                "data": {"cols": ["year", "rev", "cost", "profit"],
                         "rows": [["2026", 12, 18, -6], ["2027", 86, 52, 34], ["2028", 300, 120, 180]]},
                "series": [
                    {"type": "bar", "name": "营业收入", "encode": {"x": "year", "y": "rev"},
                     "fill": "#38BDF8", "dataLabels": {"show": True, "fontSize": 9, "color": "#FFFFFF"}},
                    {"type": "bar", "name": "运营成本", "encode": {"x": "year", "y": "cost"},
                     "fill": "#8FAADC", "dataLabels": {"show": True, "fontSize": 9, "color": "#FFFFFF"}},
                    {"type": "line", "name": "净利润", "encode": {"x": "year", "y": "profit"},
                     "lineColor": "#FFC000", "dataLabels": {"show": True, "fontSize": 9, "color": "#FFC000"}},
                ],
                "xAxis": {"label": {"fontSize": 11, "color": "#C7D7F2"}},
                "yAxis": {"label": {"fontSize": 9, "color": "#C7D7F2"}},
                "legend": {"fontSize": 10, "color": "#FFFFFF"}})
    # 右：测算假设
    els.append(panel(556, 112, 364, 240, eid="p37asm"))
    els.append(T(574, 122, 330, 22, "<p><strong>核心测算假设</strong></p>", eid="p37asm_t",
                 fontSize=14, color="#FFFFFF", wrap=False))
    asms = [
        ("2026 试点年", "2 家机构试点 × 6 万元 = 12 万元；以免费换案例与口碑"),
        ("2027 复制年", "12 家机构 × 6 万元 + 8 个案证据包 × 1.5 万元 ≈ 86 万元"),
        ("2028 规模年", "30 家机构 × 8 万元 + API 与数据授权 60 万元 ≈ 300 万元"),
        ("成本结构", "服务器与合规审计 40% · 研发 35% · 科普运营 25%"),
    ]
    for i, (t, d) in enumerate(asms):
        y = 152 + i * 48
        els.append(S(574, y + 2, 10, 10, shape="ellipse", fill=solid(GOLD if i < 3 else CYAN), eid=f"p37a{i}"))
        els.append(T(594, y - 2, 110, 20, f"<p><strong>{t}</strong></p>", eid=f"p37at{i}",
                     fontSize=11.5, color="#FFFFFF", wrap=False))
        els.append(T(594, y + 18, 312, 28, f"<p>{d}</p>", eid=f"p37ad{i}",
                     fontSize=9.5, color=SUB, lineHeight=1.3))
    # 右下：盈亏平衡
    els.append(panel(556, 366, 364, 136, fill="#FFC00018", border_c=GOLD, eid="p37be"))
    els.append(T(574, 378, 330, 110,
                 '<p><span style="font-size:26px;color:#FFC000"><strong>2027 Q4</strong></span><span style="font-size:12px;color:#C7D7F2">　预计实现盈亏平衡</span></p>'
                 '<p style="margin-top:8px">轻资产模式：无硬件投入，主要成本为研发与合规；机构年费制带来稳定现金流。</p>'
                 '<p>国际化潜力：浏览器插件天然跨语言，方案可复制至海外电商平台的算法审计场景。</p>',
                 eid="p37be_b", fontSize=11, color="#FFFFFF", lineHeight=1.5))
    return els

# ---------------- P38 社会影响 ----------------
def p38_social():
    els = bg_base() + nav("社会影响", 4)
    els += page_title_bar("让技术红利公平地抵达每一个人", "区域发展 · 就业带动 · 民生改善 · 生态文明", y=54)
    cards = [
        ("民生福祉", "守护 9.74 亿网购者的公平交易权：让“千人千价”可被发现、可被检验、可被追责，降低弱势群体的信息不对称", "fas:heart", "9.74 亿人受益面", GOLD),
        ("就业带动", "项目直接创造算法审计、数据合规、公益法律服务等新职业入口；未来三年带动数据标注、合规审计等岗位", "fas:briefcase", "3 年带动 50+ 岗位", CYAN),
        ("区域发展", "以 ×× 市为试点枢纽，向消协网络辐射；助力地方市场监管数字化升级，服务全国统一大市场建设", "fas:city", "1 个试点枢纽", "#7EE2A8"),
        ("生态文明", "全程无纸化电子取证，替代传统打印公证流程；按 10 万条观测估算，减少纸张消耗约 40 万张", "fas:leaf", "减纸 40 万张", "#A3E635"),
    ]
    x0, y0, cw, ch, g = 40, 116, 428, 152, 24
    for i, (t, d, ic, num, c) in enumerate(cards):
        x, y = x0 + (i % 2) * (cw + g), y0 + (i // 2) * (ch + g)
        els.append(panel(x, y, cw, ch, eid=f"p38c{i}"))
        els.append(ICON(x + 16, y + 16, 28, 28, ic, c, eid=f"p38ic{i}"))
        els.append(T(x + 56, y + 14, 200, 26, f"<p><strong>{t}</strong></p>", eid=f"p38t{i}",
                     fontSize=16, color="#FFFFFF", wrap=False))
        els.append(T(x + 16, y + 52, cw - 32, 62, f"<p>{d}</p>", eid=f"p38d{i}",
                     fontSize=11, color=SUB, lineHeight=1.5))
        els.append(T(x + 16, y + 118, cw - 32, 24,
                     f'<p><span style="color:{c}"><strong>{num}</strong></span></p>', eid=f"p38n{i}",
                     fontSize=14, wrap=False))
    # 底：社会价值升华
    els.append(panel(40, 464, 880, 52, fill="#FFC00018", border_c=GOLD, eid="p38sum"))
    els.append(T(58, 464, 844, 52,
                 "<p><strong>社会价值总述：</strong>项目以青年之力补上算法治理的“取证短板”——既保护消费者权益，也帮助合规平台自证清白，让良币驱逐劣币。</p>",
                 eid="p38sum_b", fontSize=12, color="#FFFFFF", wrap=False, align=["left", "middle"]))
    return els
