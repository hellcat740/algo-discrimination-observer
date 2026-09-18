# ⚙️ 算法歧视观测数据后端（backend/）

本地后端服务：接收浏览器插件上传的「算法歧视观测数据」，清洗校验后存入 PostgreSQL，
并提供鉴权查询 API 与一个内置的数据库查看页面（`/admin`）。

> 本目录与插件源码（`../src/`）完全独立，互不依赖。

## 📑 目录

- [📁 目录结构](#-目录结构)
- [🚀 运行方式](#-运行方式)
- [🔐 鉴权](#-鉴权)
- [🌐 CORS（跨域）](#-cors跨域)
- [📡 接口一览](#-接口一览)
- [🗄️ 数据模型变更记录](#-数据模型变更记录)
- [📦 数据格式冻结声明](#-数据格式冻结声明)
- [🧹 数据清洗规则](#-数据清洗规则appcleaningpy)
- [🔗 插件字段映射（对接说明）](#-插件字段映射对接说明)
- [🧪 快速自测（curl）](#-快速自测curl)
- [🖥️ 统一控制台（/）](#-统一控制台)
- [📊 统计分析（价格歧视推断引擎）](#-统计分析价格歧视推断引擎)
- [⚠️ 已知限制](#️-已知限制)

## 📁 目录结构

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI 入口：路由注册、启动建表、静态页面托管
│   ├── database.py        # engine/session/Base；DATABASE_URL 从环境变量读
│   ├── models.py          # SQLAlchemy 模型：observations / users / tasks / evidence_bundles
│   ├── schemas.py         # Pydantic v2：ObservationIn / ObservationOut / 分页响应等
│   ├── cleaning.py        # 数据清洗与校验（独立于路由，便于测试）
│   ├── auth.py            # X-API-Key 鉴权依赖（/health、/admin 不鉴权）
│   ├── analysis_api.py    # 统计分析 API 路由（/api/analysis/*）
│   ├── admin_api.py       # 演示数据管理接口（seed-demo / clear-demo）
│   ├── transfer.py        # 数据打包导出/导入核心（bundle 格式 v1.0，已冻结）
│   ├── transfer_api.py    # 数据打包导出/导入接口（/api/export|import/bundle）
│   ├── seed.py            # 演示数据生成核心逻辑（⚠️ 仅供演示联调）
│   └── static/
│       ├── index.html     # 统一控制台（单页应用，原生 JS + 手写 SVG）
│       ├── admin.html     # 数据库查看前端（原生 JS，无框架）
│       └── analysis.html  # 统计分析页面（旧版入口）
├── analysis/
│   ├── discrimination.py  # 统计推断引擎（CLI / API / 测试三处复用）
│   └── cli.py             # 命令行入口：python -m analysis.cli
├── scripts/
│   └── seed_demo.py       # 灌演示数据 CLI（python -m scripts.seed_demo）
├── requirements.txt
├── Dockerfile             # python:3.12-slim
├── docker-compose.yml     # db(postgres:16-alpine，健康检查) + api(8000 端口)
├── .env.example
└── README.md
```

## 🚀 运行方式

> 💡 **Windows 一键启动**：双击项目根目录的 `启动本地服务.bat` 即可（自动创建/修复虚拟环境、
> 启动服务并打开控制台页面）；停止用 `停止本地服务.bat`。

### 方式一：Docker Compose（推荐，一键起 PostgreSQL + API）

```bash
cd backend
docker compose up -d --build
# 查看状态（等 db healthy 后 api 才会启动）
docker compose ps
```

- API：<http://localhost:8000>
- 管理页面：<http://localhost:8000/admin>
- 接口文档（Swagger）：<http://localhost:8000/docs>
- 停止：`docker compose down`（数据保留在 `pgdata` 卷中；加 `-v` 则连数据一起删）

### 方式二：本地 Python（无 Docker 时）

```bash
cd backend
python -m venv .venv
# Windows：
.venv\Scripts\pip install -r requirements.txt
# 依赖源慢的话加镜像：-i https://pypi.tuna.tsinghua.edu.cn/simple

# 没有本地 PostgreSQL 时用 SQLite 兜底（仅调试）：
#   Windows cmd:      set DATABASE_URL=sqlite:///./local_test.db
#   Git Bash/Linux:   export DATABASE_URL=sqlite:///./local_test.db
# 有本地 PostgreSQL 则保持默认连接串或指向你的实例。

.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000
```

启动时会自动建表（`Base.metadata.create_all`），无需手动迁移。

## 🔐 鉴权

- 所有 `/api/*` 数据接口需要 `X-API-Key` 请求头（默认 `dev-key-123`，用 `API_KEY` 环境变量覆盖）。
- 浏览器访问不便设请求头，数据 API 同时兼容 `?api_key=` 查询参数。
- `/health`、`/`、`/admin`、`/analysis` 页面本身不鉴权（页面内的数据请求仍需 Key）。

## 🌐 CORS（跨域）

- `main.py` 已挂载 `CORSMiddleware`：`allow_origins=["*"]`、`allow_methods=["*"]`、
  `allow_headers=["*"]`（含自定义头 `X-API-Key`），浏览器插件（`chrome-extension://…`）
  与任意来源页面可直调后端。

> [!WARNING]
> 这是**本地演示**配置；生产部署应收敛 `allow_origins` 到具体来源（插件 ID 对应的
> `chrome-extension://<id>` 与控制台域名），并按需限制 methods/headers。

## 📡 接口一览

### 观测数据

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/health` | 健康检查（实际执行 SELECT 1） |
| POST | `/api/observations` | 写入一条观测，201 返回 `{observation_id, created_at, warnings}` |
| GET | `/api/observations` | 分页查询：`page/page_size(≤200)`，筛选：`product_id / platform_code / ip_city / is_login / is_new_user / start_ts / end_ts / min_price / max_price`（价格单位：分） |
| GET | `/api/observations/{id}` | 单条详情 |
| DELETE | `/api/observations/{id}` | 删除一条观测：成功 204（无 body），不存在 404；带 `user_ref` 的记录会把 users 表计数减 1（下限 0） |
| GET | `/api/stats/summary` | 总数、按平台分组计数、最近 7 天每日计数 |

### 统计分析

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/analysis/products` | 可分析商品列表（观测 ≥2 条；进入分析还要求 ≥2 个不同匿名用户） |
| GET | `/api/analysis/product-users?product_id=` | 商品下的匿名用户列表（user_ref、观测数、均价） |
| GET | `/api/analysis/price-discrimination` | 单商品分析；自动选取价差最大的匿名用户对（`user_a`/`user_b` 可手动指定用户对的两个 user_ref） |
| GET | `/api/analysis/platform` | 平台级批量分析（全部商品自动选对）+ 跨商品复现检验 |

### 演示数据（⚠️ 仅供开发调试）

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/admin/seed-demo` | 灌入演示数据，body `{"clear": true/false}`（⚠️ 正式环境勿用） |
| POST | `/api/admin/clear-demo` | 清空 DEMO- 前缀演示数据 |

### 数据包导出 / 导入

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/export/bundle` | 导出全部观测为 zip 数据包（支持 `?api_key=` 浏览器直接下载） |
| POST | `/api/import/bundle` | multipart 上传 zip 导入（版本/SHA-256 校验，幂等跳过已有记录） |

### 页面

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/` | 统一控制台（单页应用） |
| GET | `/admin` | 数据库查看页面（旧版入口） |
| GET | `/analysis` | 统计分析页面（旧版入口） |

## 🗄️ 数据模型变更记录

- **2026-09：observations 新增 `user_ref` 列（一次性变更）**。应项目所有者要求，
  观测记录需要能归属到匿名用户（「只要是两个不同的用户 id 就可以进行分析」，
  支撑 user_pair 按用户对比分析）。`user_ref` = 插件上报的 `anonymous_id` 明文。
  隐私口径：`anonymous_id` 是插件安装时生成的随机 UUID，不含任何个人信息，
  且 users 表本就明文存储该值，两处隐私等级一致。老库由启动时的轻量迁移自动补列
  （SQLAlchemy inspect，SQLite 底层 PRAGMA table_info / PostgreSQL 底层 information_schema），
  老数据该列为 NULL。

## 📦 数据格式冻结声明

> [!CAUTION]
> **导出数据包格式 v1.0 已冻结**：`app/transfer.py` 中 `EXPORT_FORMAT_VERSION = "1.0"`，
> 未经项目所有者明确要求不得修改格式；任何变更必须升版本号。

zip 包结构：

```text
observations-bundle-YYYYMMDD-HHMMSS.zip
├── observations.json   # 观测记录数组，字段与 ObservationOut 完全一致（见下）
└── manifest.json       # {format_version, exported_at, observation_count, sha256}
                        # sha256 = observations.json 原始字节的 SHA-256
```

observations.json 每条记录的完整字段清单（金额单位均为分，时间为 UTC ISO8601）：

```text
observation_id, task_id, user_ref, platform_code, source_type,
product_id, product_name, seller_id, product_url,
display_price_cents, actual_pay_price_cents, currency,
discount_coupon_amount_cents, promo_type, promo_label,
is_login, membership_level, is_new_user, register_days,
user_agent, platform, language, device_memory, hardware_concurrency,
screen_resolution, device_price_score_estimate,
ip_city, shipping_city, peak_hour, stock_hint,
fetch_ts, screenshot_path, dom_price_text, dom_snapshot_path,
source_code_version, created_at
```

**导入规则**：校验 `format_version == "1.0"` 与 SHA-256 → 逐条走 `ObservationIn` 校验 +
cleaning 清洗复用 → `observation_id` 已存在的跳过（幂等）→ 同步维护 users 表。
返回 `{imported, skipped, errors}`。

## 🧹 数据清洗规则（app/cleaning.py）

| 规则 | 说明 |
| --- | --- |
| 价格单位 | 接受「分」(int) 或「元」(float / 含小数的字符串)，元自动 ×100 四舍五入转分并记 warning；金额范围 `1 ~ 1,000,000` 分，越界返回 422 |
| `platform_code` 白名单 | `meituan, taobao, tmall, jd, pinduoduo, yangkeduo, eleme, dianping, ctrip, didi`，不在名单返回 422 并列出合法值 |
| 字符串超长 | 自动截断并记 warning（user_agent ≤500、product_name ≤300、product_url ≤1000、其余 ≤200） |
| `currency` | 统一大写，默认 CNY |
| `fetch_ts` | 缺省用服务端当前 UTC 并记 warning |

## 🔗 插件字段映射（对接说明）

插件（`../src/types.ts` 的 `ObservationRecord`）上报的是**嵌套结构**，本后端接收**扁平字段**。
对接时在插件侧做一次展开即可，映射关系如下：

| 插件字段（嵌套） | 后端字段（扁平） | 说明 |
| --- | --- | --- |
| `platform` | `platform_code` | 直接对应 |
| `productId` / `productName` / `productUrl` | `product_id` / `product_name` / `product_url` | 直接对应 |
| `shopName` | `seller_id` | 语义近似（店铺标识） |
| `price.original`（元） | `display_price_cents` | 插件传元浮点即可，后端自动转分 |
| `price.final`（元） | `actual_pay_price_cents` | 同上 |
| `price.currency` | `currency` | 统一大写 |
| `price.couponAmount`（元） | `discount_coupon_amount_cents` | 同上换算 |
| `price.couponType` | `promo_type` | — |
| `userContext.isLoggedIn` | `is_login` | — |
| `userContext.memberLevel` | `membership_level` | — |
| `userContext.isNewUser` | `is_new_user` | — |
| `device.userAgent` | `user_agent` | — |
| `device.platform` | `platform` | — |
| `device.language` | `language` | — |
| `device.deviceMemory` | `device_memory` | — |
| `device.hardwareConcurrency` | `hardware_concurrency` | — |
| `device.screenResolution` | `screen_resolution` | — |
| `device.devicePriceIndex` | `device_price_score_estimate` | 0–100 估算分 |
| `network.city` | `ip_city` | — |
| `shipping.shipFromCity` | `shipping_city` | — |
| `collectedAt` | `fetch_ts` | ISO8601 UTC |
| `anonymousUserId` | `anonymous_id` | 仅用于维护 users 表，**不存入 observations**（隐私隔离） |
| `screenshotDataUrl` | —（暂无） | 后端只存 `screenshot_path` 路径，dataUrl 上传需后续加文件接口 |
| `domSnapshots[]` | `dom_snapshot_path` / `dom_price_text` | 后端存路径；价格节点文本可取 `domSnapshots` 中 `field=price` 的摘要 |
| `recordId` / `uploadStatus` 等 | — | 插件本地状态，不上报 |

> 注：插件设置里默认请求头是 `X-Observation-Token`，本后端用 `X-API-Key`，对接时需在插件 options 页把上报头改为 `X-API-Key`（或在后端 auth.py 加一行兼容）。

## 🧪 快速自测（curl）

```bash
# 健康检查
curl http://localhost:8000/health

# 写入一条观测（价格用元浮点，验证自动转分）
curl -X POST http://localhost:8000/api/observations \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-key-123" \
  -d '{"platform_code":"taobao","product_id":"TB123456","product_name":"测试商品","product_url":"https://item.taobao.com/item.htm?id=TB123456","display_price_cents":89.9,"user_agent":"Mozilla/5.0","is_login":true,"ip_city":"北京"}'

# 分页查询
curl "http://localhost:8000/api/observations?platform_code=taobao&page=1&page_size=20" \
  -H "X-API-Key: dev-key-123"

# 统计
curl http://localhost:8000/api/stats/summary -H "X-API-Key: dev-key-123"
```

## 🖥️ 统一控制台（`/`）

`backend/app/static/index.html` 是把「数据查看」与「统计分析」整合后的单页应用，
覆盖「从抓取数据查看到最后验证是否存在歧视」的完整流程。原生 JS + 手写 SVG，
无任何外部 CDN/框架依赖，离线可用。

- 访问：<http://localhost:8000/>（旧版 `/admin`、`/analysis` 保留作为深链入口，互不影响）。
- Hash 路由：`#/overview`（总览，默认）、`#/observations`（观测数据）、
  `#/analysis`（歧视分析）、`#/about`（关于/方法说明），支持浏览器前进后退与深链。
- 顶部栏：API Key 一次输入全控制台生效（沿用 localStorage 键 `obs_api_key`，
  与旧版 admin / analysis 页面共用，401 时顶部红色提示）+ 数据库连通状态指示灯（/health）。
- 四个视图：
  1. **总览**：统计卡片（总观测数/覆盖商品数/平台数/最近上报时间/7 天趋势）、分析流水线步骤条
     （采集 → 入库 → 统计检验 → 判定）、平台级批量分析按钮与判定徽章、
     flagged 商品清单（带「查看分析」「查看数据」跳转）、商品表格；
  2. **观测数据**：筛选栏 + 分页表格 + 全字段详情抽屉（移植自 admin.html，
     抽屉内新增「分析此商品」按钮）；
  3. **歧视分析**：选择商品（自动选取价差最大的匿名用户对）→ 六步计算过程展示（移植自 analysis.html）；
  4. **关于/方法说明**：数据用途与隐私声明、reason_code 中文释义表、统计方法局限性。
- 跨视图跳转（全流程串联的核心交互）：
  - 总览/分析页点「查看数据」→ 切到观测数据视图并自动带入该 `product_id` 筛选；
  - 观测详情抽屉点「分析此商品」→ 切到歧视分析视图并自动选中该商品立即运行分析。

## 📊 统计分析（价格歧视推断引擎）

在观测数据之上提供统计推断：判断**同一商品对不同匿名用户是否存在系统性价差**。
核心模块 `analysis/discrimination.py` 与路由/前端完全解耦，可被 CLI、API、测试三处复用。

### 方法说明

1. **数据加载**：取同一 `product_id`（可选 `seller_id`）的全部观测；分析优先基于
   `display_price_cents`（原价/页面展示价），原价缺失的记录逐条回退
   `actual_pay_price_cents`（到手价），并在结果的 `price_basis`（如
   `display_price_cents (3条回退actual_pay)`）与 `notes` 中如实标注。
   详见下文「按原价分析与假折扣标注」。
2. **对比用户对选取**（不再按 is_new_user / is_login / membership 属性分组）：
   - 准入条件：同一商品存在 **≥2 个不同匿名用户**（`user_ref`）的观测，否则返回 `INSUFFICIENT_DATA`；
   - 自动选对：按每个用户的中位价排序，选取**价差最大的一对**——用户A = 低价侧
     （中位价最低，并列取观测数更多者），用户B = 高价侧（中位价最高）；
   - 也可通过 `user_a` / `user_b` 参数手动指定两个 user_ref（指定后仍会按中位价自动
     交换，保证 A 低 B 高）；
   - 输出中 `user_a` / `user_b` 含 `user_ref`（完整值）、`user_ref_short`（前 8 位）与各自 `n`。
3. **检验与度量**（作用在用户对上）：
   - 描述性统计：两用户各自 n / 均值 / 中位数 / 标准差 / min / max（分）；
   - 中位数价差百分比：`(median_B - median_A) / median_A × 100`（相对低价侧），附方向描述；
   - Mann-Whitney U（`scipy.stats.mannwhitneyu`，双侧）：非参数检验，不要求正态分布；
     **小样本降级**：任一用户仅 1 条观测时 MWU 不运行，结果为 null 并记 `SMALL_SAMPLE`，
     分析照常返回描述性结果（不报错）；两用户各 ≥2 条但理论最小 p 值 `2/C(n_A+n_B, n_A)`
     已 >0.05 时，照常报告实际 p 值但 `significant` 强制为 false 并记 `SMALL_SAMPLE`；
   - OLS 回归：`log(价格) ~ is_user_b + 控制变量`，核心变量为「是否高价侧用户B」虚拟变量，
     `fit(cov_type='HC3')` 稳健标准误。
     控制变量：`C(ip_city)`、`C(peak_hour)`、`C(shipping_city)`、`C(stock_hint)`、
     `device_price_score_estimate`、`C(platform_code)`；缺失率 >60% 或取值无变异的控制列
     自动剔除并记入 `controls_dropped`。样本 <30 或核心变量无变异时回归置 null 并给原因。
     输出系数、标准误、t、p、95% CI 及换算百分比影响 `(exp(coef)-1)×100`。
4. **判定规则**（逐条体现在 `reason_code`）：

   | reason_code | 含义 |
   | --- | --- |
   | `MWU_SIGNIFICANT` | MWU p < 0.05 |
   | `PRICE_DIFF_OVER_5PCT` | 中位数价差 > 5%（相对低价侧） |
   | `REGRESSION_SIGNIFICANT` | 回归核心变量 p < 0.05 |
   | `REGRESSION_NOT_APPLICABLE` | 回归不适用（不计入否决） |
   | `SMALL_SAMPLE` | MWU 因小样本降级（见上），不作为否决项 |

   - 单商品 `flag`（疑似歧视）= 价差>5% 且（MWU显著 或 回归显著）且（回归已运行则必须回归显著）
   - `LOW_CONFIDENCE`（疑似低置信）：检验降级或 MWU 不显著，但价差>5% 且无回归否定——
     即「价差存在，统计证据不足」，结果单独标记、不计入 `flag`
   - 平台级：`analyze_platform` 批量分析所有商品，`flag` 商品数 ≥2 →
     `platform_suspected=true`，记 `REPLICATED_ACROSS_PRODUCTS(n=k)`；
     低置信商品单独列入 `low_confidence_products`，不触发平台级判定

### 按原价分析与假折扣标注

**为什么按原价分析**：`display_price_cents`（原价/页面展示价）是平台对不同用户群体
定价的载体——「大数据杀熟」发生在标价环节；而 `actual_pay_price_cents`（到手价）
叠加了用户个人优惠券、红包等个体因素，噪声大，不适合作为群体间定价差异的判据。

**价格基准规则**：

- 逐条记录取价：有原价用原价；原价缺失的记录回退到手价，回退条数写进
  `price_basis`（如 `display_price_cents (3条回退actual_pay)`）并记入 `notes`；
- 原价与到手价均缺失的记录剔除并计数标注；
- 「按用户对比」下拉中的均价口径同步为 `coalesce(display, actual)`，与分析一致。

**假折扣特别标注**（`fake_discount`）：

- 商品级折扣深度：对有原价与到手价双值的记录计算
  `discount_depth_percent = median((display − actual) / display) × 100`；
- 当单商品 `flag=true` 且 `discount_depth_percent > 10`（阈值
  `FAKE_DISCOUNT_DEPTH_THRESHOLD_PCT`）时：输出 `fake_discount: true` 与
  `discount_depth_percent`，`reason_code` 追加 `FAKE_DISCOUNT_PATTERN`——
  原价存在群体差异又挂着深折扣，属「先区别定价、再用折扣掩饰」的典型形态；
- 其余情况 `fake_discount: false`；无 display/actual 双值记录时
  `discount_depth_percent` 为 null 并在 `notes` 注明无法计算；
- 平台级批量分析（`/api/analysis/platform`）的每个商品结果均携带
  `fake_discount` / `discount_depth_percent` 字段；
- 控制台呈现：分析视图主徽章旁出现红色副徽章
  「⚠ 假折扣型歧视（折扣深度 xx.x%）」，总览平台级 flagged 商品表格带「假折扣」列。

### 运行方式

```bash
# CLI（在 backend/ 下；--db 可覆盖连接串；自动选取价差最大的用户对）
python -m analysis.cli --product-id 1063820538904
python -m analysis.cli --product-id 1063820538904 --user-a <user_ref> --user-b <user_ref>  # 手动指定用户对
python -m analysis.cli --all                              # 平台级批量

# 灌演示数据（⚠️ 仅供开发调试，seed 固定 42 可复现；正式证据库勿用）
python -m scripts.seed_demo --clear

# API（需 X-API-Key）
GET /api/analysis/products                              # 可分析商品列表（观测 ≥2 条）
GET /api/analysis/price-discrimination?product_id=1063820538904
GET /api/analysis/platform
GET /analysis                                           # 分析前端页面
```

### 示例输出 JSON（历史运行：旧版 `python -m analysis.cli --product-id DEMO-A --group-by new_user`，SQLite 演示数据）

> ⚠️ 本示例为**旧分组口径**（按 is_new_user 分组）与价格基准切换前（旧口径
> `actual_pay_price_cents`）的历史输出；现行版本已改为「价差最大匿名用户对」模式
> （无 `group_by`，输出含 `mode: "max_gap_user_pair"` 与 `user_a` / `user_b` 字段），
> `price_basis` 以 `display_price_cents` 为准，并含 `fake_discount` / `discount_depth_percent`
> 与 `low_confidence` 字段。字段结构仅作参考。

```json
{
  "product_id": "DEMO-A",
  "seller_id": "SELLER-001",
  "product_name": "演示商品A 便携电热水杯",
  "group_by": "new_user",
  "price_basis": "actual_pay_price_cents",
  "analyzed_at": "2026-09-08T12:49:33.378503+00:00",
  "notes": [],
  "groups": [
    {
      "name": "新用户组",
      "key": "is_new_user=true",
      "n": 30,
      "mean_cents": 8895.5,
      "median_cents": 8900.5,
      "std_cents": 100.64,
      "min_cents": 8745.0,
      "max_cents": 9073.0,
      "prices_cents": [8745.0, 8763.0, 8763.0, 8769.0, 8780.0, 8782.0, 8794.0, 8797.0, 8807.0, 8809.0, 8825.0, 8858.0, 8867.0, 8876.0, 8884.0, 8917.0, 8918.0, 8931.0, 8934.0, 8958.0, 8961.0, 8962.0, 8970.0, 8988.0, 8993.0, 9013.0, 9025.0, 9049.0, 9054.0, 9073.0]
    },
    {
      "name": "老用户组",
      "key": "is_new_user=false",
      "n": 30,
      "mean_cents": 9547.03,
      "median_cents": 9564.5,
      "std_cents": 138.27,
      "min_cents": 9284.0,
      "max_cents": 9778.0,
      "prices_cents": [9284.0, 9326.0, 9346.0, 9356.0, 9361.0, 9361.0, 9401.0, 9401.0, 9445.0, 9467.0, 9479.0, 9483.0, 9496.0, 9502.0, 9512.0, 9541.0, 9588.0, 9608.0, 9629.0, 9634.0, 9639.0, 9649.0, 9655.0, 9656.0, 9667.0, 9674.0, 9692.0, 9703.0, 9716.0, 9723.0, 9778.0]
    }
  ],
  "mann_whitney": {
    "u_stat": 0.0,
    "p_value": 0.0,
    "significant": true
  },
  "median_price_diff_percent": -6.94,
  "diff_direction": "老用户组比新用户组贵 6.94%",
  "regression": {
    "n": 52,
    "r_squared": 0.9158,
    "core_variable": "is_new_user_true",
    "coef": -0.072208,
    "std_err": 0.004746,
    "t": -15.2136,
    "p_value": 0.0,
    "ci_95": [-0.08151, -0.062905],
    "approx_percent_effect": -6.97,
    "controls_used": ["C(ip_city)", "C(peak_hour)", "C(shipping_city)", "C(stock_hint)", "device_price_score_estimate"],
    "controls_dropped": ["C(platform_code)（取值无变异）"],
    "cov_type": "HC3"
  },
  "regression_not_applicable_reason": null,
  "flag": true,
  "reason_code": ["MWU_SIGNIFICANT", "PRICE_DIFF_OVER_5PCT", "REGRESSION_SIGNIFICANT"],
  "insufficient_reason": null,
  "sample_total": 60
}
```

> 说明：`p_value` 实际值为 3.016e-11，JSON 中经 `round(..., 6)` 显示为 0.0。
> `groups[].prices_cents` 为排序后的原始价格数组，供前端绘制分布对比图（契约字段之外的附加字段）。

## ⚠️ 已知限制

- 截图 / DOM 快照只登记路径（`screenshot_path` / `dom_snapshot_path`），暂未提供文件上传接口；
  插件的 `screenshotDataUrl`（base64）需要后续新增上传接口对接。
- 未使用 Alembic 迁移，启动时 `create_all` 仅建表不迁移字段；改模型后需手工处理。
- `API_KEY` 默认值仅供本地开发，部署前务必修改。
- SQLite 兜底模式仅供调试，并发与 JSON/时区行为以 PostgreSQL 为准。

### 统计分析的已知限制

- **观测关联 ≠ 因果歧视**：价差可能由未观测因素（优惠券领取行为、入口渠道、活动时段）
  驱动，回归只能控制已采集字段；flag 结果应作为「优先固定证据」的线索，而非结论。
- **小样本功效**：每用户仅 1~2 条观测时 MWU 降级为描述性输出（记 `SMALL_SAMPLE`），
  「未发现差异」不能排除歧视；此时若价差>5% 会单独标记为「疑似（低置信）」供优先补采数据。
- **多重比较未校正**：平台级批量分析逐个商品检验，未做 Bonferroni / FDR 校正，
  商品越多越容易出现假阳性；`REPLICATED_ACROSS_PRODUCTS` 复现规则用于缓解该问题。
- **p 值舍入**：输出 p 值保留 6 位小数，极小 p（如 3e-11）显示为 0.0。
- **价格基准回退**：实际支付价缺失率 >50% 时回退展示价，两种基准的结果不可直接比较。
