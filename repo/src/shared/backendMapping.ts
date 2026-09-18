/**
 * 插件嵌套 ObservationRecord → 本地后端（FastAPI）扁平 schema 的字段映射
 *
 * 本模块为纯函数，不依赖 chrome.* / DOM，可在 Node 环境直接单元测试。
 *
 * 映射表（插件字段 → 后端字段）：
 * ┌ 插件 ObservationRecord ────────────────┬ 后端扁平字段 ───────────────────┬ 备注 ─────────────────────────────┐
 * │ platform                               │ platform_code                   │ 插件 id「yangkeduo」→「pinduoduo」， │
 * │                                        │                                 │ taobao/tmall/jd 直通              │
 * │ productId                              │ product_id                      │                                   │
 * │ productName                            │ product_name                    │                                   │
 * │ shopId（优先）/ shopName（回退）       │ seller_id                       │ 有店铺 ID 用 ID，否则店铺名代替  │
 * │ productUrl                             │ product_url                     │                                   │
 * │ price.original（元，浮点）             │ display_price_cents             │ 插件侧 ×100 四舍五入为整数分      │
 * │ price.final（元，浮点）                │ actual_pay_price_cents          │ 同上                              │
 * │ price.currency                         │ currency                        │                                   │
 * │ price.couponAmount（元，浮点）         │ discount_coupon_amount_cents    │ 同上                              │
 * │ price.couponType                       │ promo_type / promo_label        │ label 带金额组成可读标签          │
 * │ userContext.isLoggedIn                 │ is_login                        │                                   │
 * │ userContext.memberLevel                │ membership_level                │                                   │
 * │ userContext.isNewUser                  │ is_new_user                     │ 无法确定时为 null                 │
 * │ （无）                                 │ register_days                   │ 插件无法获取，固定 null           │
 * │ device.userAgent / platform / language │ user_agent / platform / language│                                   │
 * │ device.deviceMemory                    │ device_memory                   │                                   │
 * │ device.hardwareConcurrency             │ hardware_concurrency            │                                   │
 * │ device.screenResolution                │ screen_resolution               │                                   │
 * │ device.devicePriceIndex                │ device_price_score_estimate     │ 0-100 代理估算指标                │
 * │ network.city                           │ ip_city                         │                                   │
 * │ shipping.shipFromCityNormalized        │ shipping_city                   │ 归一化市级关键词；为空回退原文    │
 * │ collectedAt（UTC ISO）                 │ fetch_ts                        │                                   │
 * │ collectedAt 的本地小时                 │ peak_hour                       │ 11-13 或 19-23 点 → true          │
 * │ domSnapshots 价格相关第一条（纯文本）  │ dom_price_text                  │ 去标签后 ≤500 字符                │
 * │ （无）                                 │ stock_hint                      │ 插件未采集库存提示，固定 null     │
 * │ 调用方传入 extVersion                  │ source_code_version             │ chrome.runtime.getManifest().version│
 * │ anonymousUserId                        │ anonymous_id                    │                                   │
 * └────────────────────────────────────────┴─────────────────────────────────┴───────────────────────────────────┘
 *
 * 隐私红线（以下字段绝不上传）：
 *  - userContext.userMarker / userMarkerMasked（昵称与打码昵称都不上传，memberLevel 等群体维度已足够）
 *  - userContext.evidence（推断依据仅供本地审计）
 *  - screenshotDataUrl（体积大，后续走独立文件上传接口）
 *  - domSnapshots 整份快照（体积大，同上；仅提取价格相关第一条的纯文本 ≤500 字符）
 */
import type { BackendObservationPayload, ObservationRecord } from '../types';

/** 插件平台 id → 后端 platform_code（后端白名单外的值原样透传，由后端校验拒绝） */
const PLATFORM_CODE_MAP: Record<string, string> = {
  yangkeduo: 'pinduoduo',
  pinduoduo: 'pinduoduo',
  taobao: 'taobao',
  tmall: 'tmall',
  jd: 'jd',
};

/**
 * 本地时段高峰粗粒度估计：11-13 点（午间）或 19-23 点（晚间）视为高峰。
 * 说明：这是基于采集时刻本地小时的粗略口径，仅作分析协变量；后端字段可空。
 */
export function isPeakHour(collectedAt: string): boolean | null {
  const d = new Date(collectedAt);
  if (Number.isNaN(d.getTime())) return null;
  const h = d.getHours(); // 本地小时
  return (h >= 11 && h <= 13) || (h >= 19 && h <= 23);
}

/** 把快照 outerHTML 转为纯文本：去标签、合并空白、截断到 ≤500 字符 */
export function snapshotToText(outerHTML: string): string {
  return outerHTML
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 500);
}

/** 取价格相关第一条快照（优先 price，其次 finalPrice）的纯文本；无快照返回 null */
function pickDomPriceText(record: ObservationRecord): string | null {
  const snap =
    record.domSnapshots.find((s) => s.field === 'price') ??
    record.domSnapshots.find((s) => s.field === 'finalPrice');
  if (!snap) return null;
  const text = snapshotToText(snap.outerHTML);
  return text || null;
}

/**
 * 元 → 整数分换算（null 保持 null）
 * 为什么由插件侧换算：JSON 序列化不区分整数/浮点（5999.0 序列化为 5999），
 * Python 侧会把整数值解析为 int，后端按「整数=已经是分」处理，导致 ¥5999.00
 * 被错存为 5999 分（¥59.99），差 100 倍。字段名本来就是 *_cents，
 * 由插件侧用 Math.round(x * 100) 输出整数分语义最清晰，也不再触发后端换算 warning。
 */
export function yuanToCents(yuan: number | null): number | null {
  if (yuan === null || yuan === undefined) return null;
  return Math.round(yuan * 100);
}

/** ObservationRecord → 后端扁平 payload（extVersion 由调用方传入，保持本函数无 chrome 依赖） */
export function mapObservationToBackend(
  record: ObservationRecord,
  extVersion: string,
): BackendObservationPayload {
  const couponType = record.price.couponType;
  const couponAmount = record.price.couponAmount;
  return {
    platform_code: PLATFORM_CODE_MAP[record.platform] ?? record.platform,
    product_id: record.productId,
    product_name: record.productName,
    seller_id: record.shopId ?? record.shopName, // 优先真实店铺 ID；取不到回退店铺名（后端 schema 已冻结，seller_id 语义为「卖家标识」）
    product_url: record.productUrl,
    display_price_cents: yuanToCents(record.price.original), // 插件侧换算为整数分（见 yuanToCents 注释）
    actual_pay_price_cents: yuanToCents(record.price.final),
    currency: record.price.currency,
    discount_coupon_amount_cents: yuanToCents(couponAmount),
    promo_type: couponType,
    promo_label:
      couponType !== null && couponAmount !== null ? `${couponType}（减${couponAmount}元）` : couponType,
    is_login: record.userContext.isLoggedIn,
    membership_level: record.userContext.memberLevel,
    is_new_user: record.userContext.isNewUser,
    register_days: null, // 插件无法获取注册天数
    user_agent: record.device.userAgent,
    platform: record.device.platform,
    language: record.device.language,
    device_memory: record.device.deviceMemory,
    hardware_concurrency: record.device.hardwareConcurrency,
    screen_resolution: record.device.screenResolution,
    device_price_score_estimate: record.device.devicePriceIndex,
    ip_city: record.network.city,
    shipping_city: record.shipping.shipFromCityNormalized ?? record.shipping.shipFromCity,
    peak_hour: isPeakHour(record.collectedAt),
    stock_hint: null, // 插件未采集库存提示
    fetch_ts: record.collectedAt,
    dom_price_text: pickDomPriceText(record),
    source_code_version: extVersion,
    anonymous_id: record.anonymousUserId,
  };
}
