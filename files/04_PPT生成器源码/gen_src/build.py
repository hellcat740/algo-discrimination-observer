# -*- coding: utf-8 -*-
"""主入口：生成 48 页 .page 文件 + .pptd 清单"""
import sys
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).parent))

from core import ROOT, DECK
from skeletons import cover_page, toc_page, divider_page, final_page
from pages_a import p02_research, p05_policy, p06_cases, p07_data, p08_process, p09_findings, p10_problem
from pages_b import (p12_overview, p13_solution, p14_arch, p15_innov1, p16_innov2, p17_innov3,
                     p18_innov4, p19_demo1, p20_demo2, p21_demo3, p22_verify, p23_ip)
from pages_c import (p25_values, p26_leader, p27_knowledge, p28_growth, p29_school, p30_feedback,
                     p32_industry, p33_market, p34_compete, p35_business, p36_landing,
                     p37_finance, p38_social)
from pages_d import (p40_structure, p41_members, p42_mentors, p43_collab,
                     p45_roadmap, p46_risks, p47_promise)

# (序号, 文件名, 页面函数) —— 页面函数返回元素列表
PAGES = [
    (1,  "01_cover",     cover_page),
    (2,  "02_research",  p02_research),
    (3,  "03_toc",       toc_page),
    (4,  "04_div1",      lambda: divider_page("壹", "项目缘起", "ORIGIN · POLICY · RESEARCH", 1)),
    (5,  "05_policy",    p05_policy),
    (6,  "06_cases",     p06_cases),
    (7,  "07_data",      p07_data),
    (8,  "08_process",   p08_process),
    (9,  "09_findings",  p09_findings),
    (10, "10_problem",   p10_problem),
    (11, "11_div2",      lambda: divider_page("贰", "项目创新", "INNOVATION · SOLUTION · PRODUCT", 2)),
    (12, "12_overview",  p12_overview),
    (13, "13_solution",  p13_solution),
    (14, "14_arch",      p14_arch),
    (15, "15_innov1",    p15_innov1),
    (16, "16_innov2",    p16_innov2),
    (17, "17_innov3",    p17_innov3),
    (18, "18_innov4",    p18_innov4),
    (19, "19_demo1",     p19_demo1),
    (20, "20_demo2",     p20_demo2),
    (21, "21_demo3",     p21_demo3),
    (22, "22_verify",    p22_verify),
    (23, "23_ip",        p23_ip),
    (24, "24_div3",      lambda: divider_page("叁", "个人成长", "GROWTH · EDUCATION · FEEDBACK", 3)),
    (25, "25_values",    p25_values),
    (26, "26_leader",    p26_leader),
    (27, "27_knowledge", p27_knowledge),
    (28, "28_growth",    p28_growth),
    (29, "29_school",    p29_school),
    (30, "30_feedback",  p30_feedback),
    (31, "31_div4",      lambda: divider_page("肆", "产业价值", "VALUE · MARKET · IMPACT", 4)),
    (32, "32_industry",  p32_industry),
    (33, "33_market",    p33_market),
    (34, "34_compete",   p34_compete),
    (35, "35_business",  p35_business),
    (36, "36_landing",   p36_landing),
    (37, "37_finance",   p37_finance),
    (38, "38_social",    p38_social),
    (39, "39_div5",      lambda: divider_page("伍", "团队协作", "TEAM · STRUCTURE · EFFICIENCY", 5)),
    (40, "40_structure", p40_structure),
    (41, "41_members",   p41_members),
    (42, "42_mentors",   p42_mentors),
    (43, "43_collab",    p43_collab),
    (44, "44_div6",      lambda: divider_page("陆", "未来规划", "ROADMAP · RISK · COMMITMENT", 6)),
    (45, "45_roadmap",   p45_roadmap),
    (46, "46_risks",     p46_risks),
    (47, "47_promise",   p47_promise),
    (48, "48_final",     final_page),
]

def main():
    pages_dir = DECK / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    page_names = []
    for num, name, fn in PAGES:
        elements = fn()
        page = {"pageType": "content", "elements": elements}
        out = pages_dir / f"{num:02d}_{name}.page"
        with open(out, "w", encoding="utf-8") as f:
            yaml.safe_dump(page, f, allow_unicode=True, sort_keys=False, width=4096)
        page_names.append(f"pages/{num:02d}_{name}.page")
        print(f"[{num:02d}/48] {name}: {len(elements)} elements")

    pptd = {
        "version": "v2",
        "size": [960, 540],
        "customFonts": [
            {"fontFamily": "飞波正点体",
             "src": "https://statics.kimi.ai/neo-design-static/p-font/飞波正点体.ttf"},
        ],
        "theme": {
            "colors": {
                "primary": "#4472C4",
                "gold": "#FFC000",
                "cyan": "#38BDF8",
                "sub": "#C7D7F2",
                "dk1": "#000000",
                "lt1": "#FFFFFF",
                "dk2": "#44546A",
                "lt2": "#E7E6E6",
                "accent1": "#4472C4",
                "accent2": "#ED7D31",
                "accent3": "#A5A5A5",
                "accent4": "#FFC000",
                "accent5": "#5B9BD5",
                "accent6": "#70AD47",
                "hlink": "#0563C1",
                "folHlink": "#954F72",
                "text1": "#FFFFFF",
                "text2": "#FFFFFF",
            }
        },
        "pages": page_names,
    }
    pptd_path = DECK / "算法歧视众包观测.pptd"
    with open(pptd_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(pptd, f, allow_unicode=True, sort_keys=False, width=4096)
    print(f"\npptd written: {pptd_path} ({len(page_names)} pages)")

if __name__ == "__main__":
    main()
