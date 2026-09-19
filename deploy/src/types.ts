/**
 * 类型定义：观测数据记录与扩展内部消息协议
 * 所有模块（content / background / popup / options / report）共用本文件。
 */

/** 商品价格信息（单位：元，解析失败为 null） */
export interface PriceInfo {
  /** 划线价 / 原价 */
  original: number | null;
  /** 到手价 / 券后价（仅页面 DOM 或内嵌 JSON 显式存在券后价时才填充；取不到保持 null，不再回退为售价——原价/折扣价需明确区分） */
  final: number | null;
  /** 币种（目标平台均为 CNY） */
  currency: string;
  /** 优惠券金额 */
  couponAmount: number | null;
  /** 优惠券类型（满减券 / 折扣券 / 通用券 等） */
  couponType: string | null;
}

/** content 侧采集到的原始用户上下文（userMarker 为原始文本，原文绝不入库、绝不上报） */
export interface RawUserContext {
  /** 是否登录（保守推断，无法确定为 null） */
  isLoggedIn: boolean | null;
  /** 会员等级关键词（VIP / PLUS / 88VIP 等），未识别为 null */
  memberLevel: string | null;
  /** 是否新用户：页面通常无法可靠判断，默认为 null */
  isNewUser: boolean | null;
  /** 页面可见的登录昵称 / 会员标识原始文本（仅用于后台打码，原文不进入最终记录） */
  userMarker: string | null;
  /** 推断依据说明（便于审计与复核证据效力） */
  evidence: string;
}

/** 入库 / 上报的用户上下文（昵称按设置打码） */
export interface UserContext {
  isLoggedIn: boolean | null;
  memberLevel: string | null;
  isNewUser: boolean | null;
  /** 打码后的用户标识，如「张*」 */
  userMarkerMasked: string | null;
  evidence: string;
}

/** 设备信息与「设备价格指数」估算 */
export interface DeviceInfo {
  userAgent: string;
  screenResolution: string;
  deviceMemory: number | null;
  hardwareConcurrency: number | null;
  platform: string;
  language: string;
  /** 0-100 设备档次估算分（代理指标，计算方式见 content/index.ts 中函数注释） */
  devicePriceIndex: number;
}

/** 网络环境（公网 IP 与地理归属，来自 IP 定位 API） */
export interface NetworkInfo {
  ip: string | null;
  city: string | null;
  region: string | null;
  country: string | null;
  /** 数据来源与降级说明 */
  source: string;
}

export interface ShippingInfo {
  /** 发货地原文（页面展示的配送/发货文本，如「浙江 嘉兴」「配送至 北京市 朝阳区」） */
  shipFromCity: string | null;
  /** 归一化城市名（从原文提取的市级关键词，如「嘉兴」「重庆」；无法归一化时为 null） */
  shipFromCityNormalized: string | null;
}

/**
 * 字段提取来源标注（排查「数据从哪来」用）
 * 'dom' = DOM 选择器命中；'json' = 内嵌 script 的初始化 JSON 回退命中；null = 未取到
 */
export type ExtractionSource = 'dom' | 'json';

export interface ExtractionMeta {
  price: ExtractionSource | null;
  originalPrice: ExtractionSource | null;
  finalPrice: ExtractionSource | null;
  shippingCity: ExtractionSource | null;
  shopName: ExtractionSource | null;
  shopId: ExtractionSource | null;
}

/** 关键节点 DOM 快照（证据留存） */
export interface DomSnapshot {
  /** 字段名：title / price / finalPrice / shopName 等 */
  field: string;
  /** 节点 outerHTML，截取前 2000 字符，已剔除 script/style */
  outerHTML: string;
}

export type UploadStatus = 'pending' | 'success' | 'failed' | 'skipped_no_price';

/** 一条完整的观测记录（入库与上报的唯一数据结构） */
export interface ObservationRecord {
  /** 本地记录 ID（uuid） */
  recordId: string;
  /** 匿名用户 ID（首次安装时生成的 uuid，不含任何注册信息） */
  anonymousUserId: string;
  /** 采集时间（UTC ISO8601） */
  collectedAt: string;
  /** 平台标识：taobao / tmall / jd / pinduoduo */
  platform: string;
  /** 商品 ID（从 URL 提取） */
  productId: string;
  productName: string | null;
  shopName: string | null;
  /** 店铺 ID（店铺链接 shopId 参数 / data-shopid / 内嵌 JSON 的 shopId|sellerId；取不到为 null） */
  shopId: string | null;
  productUrl: string;
  price: PriceInfo;
  userContext: UserContext;
  device: DeviceInfo;
  network: NetworkInfo;
  shipping: ShippingInfo;
  /** 各字段提取来源（dom/json/null），旧记录可能缺此字段 */
  extractionMeta?: ExtractionMeta;
  /** 页面截图（PNG dataUrl），失败时为 null 并标注 screenshotError */
  screenshotDataUrl: string | null;
  screenshotError?: string;
  domSnapshots: DomSnapshot[];
  uploadStatus: UploadStatus;
  uploadError?: string;
  /** 后端返回的清洗/转换提示（如「浮点价格已转分」「字段超长已截断」） */
  uploadWarnings?: string[];
  /** 后端返回的观测 ID */
  observationId: string | null;
}

/** content 侧提取结果（EXTRACT_PAGE_DATA 消息的响应载荷） */
export interface ExtractedPageData {
  platform: string;
  productId: string;
  productName: string | null;
  shopName: string | null;
  /** 店铺 ID（DOM 链接/data 属性或内嵌 JSON 提取；取不到为 null） */
  shopId: string | null;
  productUrl: string;
  price: PriceInfo;
  userContext: RawUserContext;
  device: DeviceInfo;
  shipping: ShippingInfo;
  /** 各字段提取来源标注 */
  extractionMeta: ExtractionMeta;
  domSnapshots: DomSnapshot[];
}

/** 扩展设置（存于 chrome.storage.local） */
export interface ExtensionSettings {
  /** 是否已同意参与采集 */
  consent: boolean;
  /** 商品页自动采集开关（默认 false；隐私前提：仅在 consent=true 时生效） */
  autoCollect: boolean;
  /** 上报 API 端点 */
  apiEndpoint: string;
  /** 上报鉴权 key（X-API-Key 请求头） */
  apiKey: string;
  /** 是否对店铺名打码 */
  maskShopName: boolean;
  /** 是否对昵称/会员标识打码 */
  maskUserMarker: boolean;
}

/** 消息类型常量 */
export const MSG = {
  START_COLLECTION: 'START_COLLECTION',
  EXTRACT_PAGE_DATA: 'EXTRACT_PAGE_DATA',
  TEST_CONNECTION: 'TEST_CONNECTION',
  AUTO_COLLECT: 'AUTO_COLLECT',
  RETRY_FAILED: 'RETRY_FAILED',
} as const;

export interface StartCollectionPayload {
  /** 提示条「仅本次采集」：本次视为已授权，但不改写持久授权状态 */
  onceOnly?: boolean;
}

export interface AutoCollectPayload {
  /** content 侧提取到的商品 ID（用于 background 跨页面去重） */
  productId?: string;
}

export interface ExtensionMessage<T = unknown> {
  type: string;
  payload?: T;
}

/** START_COLLECTION 的处理结果（回给 popup / 提示条） */
export interface CollectionResult {
  ok: boolean;
  error?: string;
  recordId?: string;
  platform?: string;
  uploadStatus?: UploadStatus;
  /** 上报失败的具体原因（后端 422 detail / 网络错误的中文翻译等） */
  uploadError?: string;
  observationId?: string | null;
  /** 后端返回的清洗提示条数（0 表示无提示） */
  warningCount?: number;
  collectedAt?: string;
}

/** RETRY_FAILED 的处理结果（回给 popup） */
export interface RetryResult {
  /** 本次重试的记录总数 */
  retried: number;
  /** 重试成功数 */
  succeeded: number;
  /** 重试后仍失败数 */
  failed: number;
}

/** TEST_CONNECTION 的处理结果（回给 popup） */
export interface TestConnectionResult {
  ok: boolean;
  /** 人类可读的连接结果描述（成功/失败原因） */
  detail: string;
}

/** chrome.storage.local 的键名集中管理 */
export const STORAGE_KEYS = {
  CONSENT: 'consent',
  AUTO_COLLECT: 'autoCollect',
  API_ENDPOINT: 'apiEndpoint',
  API_KEY: 'apiKey',
  MASK_SHOP: 'maskShopName',
  MASK_USER: 'maskUserMarker',
  OBSERVATIONS: 'observations',
  ANON_ID: 'anonymousUserId',
  LAST_RESULT: 'lastCollectionResult',
  /** 自动采集跨页面去重：{ [productId]: 时间戳 } */
  LAST_AUTO_COLLECT: 'lastAutoCollect',
} as const;

/** 默认上报端点（本地 FastAPI 后端，可在 options 页修改） */
export const DEFAULT_API_ENDPOINT = 'http://127.0.0.1:8000/api/observations';

/** 默认上报鉴权 key（X-API-Key 请求头，与本地后端开发默认值一致，可在 options 页修改） */
export const DEFAULT_API_KEY = 'dev-key-123';

/** 本地观测记录上限（溢出滚动删除最早记录） */
export const MAX_LOCAL_RECORDS = 500;

/**
 * 本地后端（FastAPI）扁平 schema 的观测上报载荷
 * 由 src/shared/backendMapping.ts 的 mapObservationToBackend() 从 ObservationRecord 映射生成。
 * 注意：价格字段（*_cents）由插件侧换算为「整数分」后上报（避免 JSON 整数/浮点跨语言解析歧义）。
 */
export interface BackendObservationPayload {
  /** 平台代码（白名单：meituan/taobao/tmall/jd/pinduoduo/yangkeduo/eleme/dianping/ctrip/didi） */
  platform_code: string;
  product_id: string;
  product_name: string | null;
  /** 卖家标识：插件无独立卖家 ID 时以店铺名代替 */
  seller_id: string | null;
  product_url: string;
  /** 划线价/原价（整数分，插件侧换算） */
  display_price_cents: number | null;
  /** 到手价（整数分，插件侧换算） */
  actual_pay_price_cents: number | null;
  currency: string;
  /** 优惠券金额（整数分，插件侧换算） */
  discount_coupon_amount_cents: number | null;
  /** 促销类型（满减券/折扣券/通用券） */
  promo_type: string | null;
  /** 促销可读标签 */
  promo_label: string | null;
  is_login: boolean | null;
  membership_level: string | null;
  is_new_user: boolean | null;
  /** 注册天数：插件无法获取，固定 null */
  register_days: number | null;
  user_agent: string;
  /** 设备平台（navigator.platform） */
  platform: string;
  language: string;
  device_memory: number | null;
  hardware_concurrency: number | null;
  screen_resolution: string;
  /** 设备价格指数估算（0-100 代理指标） */
  device_price_score_estimate: number;
  /** IP 归属城市 */
  ip_city: string | null;
  /** 发货地 */
  shipping_city: string | null;
  /** 本地时段粗粒度高峰估计：11-13 点或 19-23 点为 true */
  peak_hour: boolean | null;
  /** 库存提示：插件未采集，固定 null */
  stock_hint: string | null;
  /** 采集时间（UTC ISO8601） */
  fetch_ts: string;
  /** 价格相关第一条 DOM 快照的纯文本（去标签，≤500 字符） */
  dom_price_text: string | null;
  /** 插件版本号（chrome.runtime.getManifest().version） */
  source_code_version: string;
  /** 匿名用户 ID */
  anonymous_id: string;
}
