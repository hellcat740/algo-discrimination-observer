"""
合成演示数据生成器（CLI 薄壳）—— ⚠️ 仅用于演示与联调，严禁当作真实证据使用 ⚠️

核心逻辑在 app/seed.py（seed / clear_demo，可被 API 复用），本文件仅负责
命令行参数解析与数据库连接。

用法（在 backend/ 目录下）：
    python -m scripts.seed_demo            # 灌入演示数据
    python -m scripts.seed_demo --clear    # 先删除全部演示数据再重新灌入
    python -m scripts.seed_demo --db sqlite:///./local_test.db

随机种子固定为 42，两次运行生成的数据完全一致（可复现）。
"""
import argparse
import os
import sys

# 允许直接运行（python scripts/seed_demo.py）时也能 import app / analysis
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.discrimination import create_engine_from_url  # noqa: E402
from app.seed import seed  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="灌入合成演示数据（仅演示用途）")
    parser.add_argument("--clear", action="store_true", help="先删除全部演示数据再灌入")
    parser.add_argument("--db", default=None, help="覆盖 DATABASE_URL")
    args = parser.parse_args()

    db_url = args.db or os.environ.get(
        "DATABASE_URL", "sqlite:///./local_test.db"
    )
    engine = create_engine_from_url(db_url)

    result = seed(engine, clear=args.clear)
    if args.clear:
        print(f"已清除演示数据 {result['cleared']} 行")
    print(f"已灌入 {result['inserted']} 条演示观测：{result['per_product']}")
    print("⚠️ 以上数据为合成演示数据，仅用于功能演示与联调。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
