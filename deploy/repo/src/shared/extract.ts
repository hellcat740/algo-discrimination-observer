/**
 * 页面数据提取（纯函数模块，不依赖 chrome.* API）
 * 同时被 content script（src/content/index.ts）与页面探针（src/probe/page-probe.ts）复用。
 * DOM 选择器来自 platforms.ts 的平台规则配置；选择器之外另设「内嵌 JSON 回退」策略。
 *
 * 多策略提取框架（v0.3.0）：
 * 真实淘宝/天猫详情页（2025 版 React SSR + CSS Modules）中，价格等数据同时存在于
 *   ① DOM 节点（Price--/priceText/tb-rmb-num 等类名）
 *   ② 内联 script 的初始化 JSON（g_config / __INIT_DATA / pageData 等，含 reservePrice、
 *      priceText、origPrice、finalPrice、couponPrice、shopId、sellerId、deliveryAddress 等键）
 * 每个字段先走 DOM 选择器列表，失败再走 JSON 回退；来源记录在 extractionMeta 中便于排查。
 */
import type { DeviceInfo, DomSnapshot, ExtractedPageData, ExtractionMeta, ExtractionSource, PriceInfo, RawUserContext } from '../types';
import { extractProductId, findPlatformRule } from '../platforms';
import type { PlatformRule } from '../platforms';
import { maskText } from '../utils';

interface PickedNode {
  text: string;
  el: Element;
}

interface PickedValue<T> {
  value: T | null;
  source: ExtractionSource | null;
}

/** 价格合法性区间（元）：过滤 JSON 里 0 / 占位大数等脏值 */
const PRICE_MIN = 0.01;
const PRICE_MAX = 10_000_000;

/** 内嵌 JSON 键名优先级（按平台惯例排序，注释说明各键语义） */
// 售价：priceText 为 2025 版详情页主价格文案；price 为通用兜底
const SALE_PRICE_KEYS = ['priceText', 'promotePrice', 'currentPrice', 'salePrice', 'price'];
// 原价（划线价）：origPrice/originalPrice 为淘宝天猫惯例；reservePrice 在部分版本表示一口价原价，作兜底
const ORIG_PRICE_KEYS = ['origPrice', 'originalPrice', 'reservePrice', 'marketPrice', 'strPrice'];
// 到手价/券后价：finalPrice 最直接；couponPrice/promotePrice 为券后价常见别名
const FINAL_PRICE_KEYS = ['finalPrice', 'couponPrice', 'promotePrice', 'handPrice'];
// 发货地：deliveryAddress 为详情页初始化数据惯例；areaName/sendAddress 为变体
const SHIPPING_KEYS = ['deliveryAddress', 'areaName', 'sendAddress', 'shipFrom', 'deliveryCity'];
// 店铺名：shopName/shopNick 为淘宝天猫惯例；mallName 为拼多多惯例
const SHOP_NAME_KEYS = ['shopName', 'shopNick', 'mallName', 'sellerNick'];
// 店铺 ID：shopId/shop_id 为店铺维度；sellerId/seller_id 为卖家维度（同店唯一，可作替代）
const SHOP_ID_KEYS = ['shopId', 'shop_id', 'sellerId', 'seller_id'];

/** 从当前页面提取结构化商品数据；未命中平台规则或非商品详情页返回 null */
export function extractPageData(): ExtractedPageData | null {
  const rule = findPlatformRule(window.location.hostname);
  if (!rule) return null;
  const productId = extractProductId(rule, window.location.href);
  if (!productId) return null;

  // 一次性收集全部内联 script 文本，供各字段的 JSON 回退策略复用
  const scriptText = collectInlineScriptText();

  const title = pickFirst(rule.selectors.title);
  const couponNode = pickFirst(rule.selectors.coupon);

  // 店铺名：DOM → JSON
  const shopNode = pickFirst(rule.selectors.shopName);
  let shopName: PickedValue<string> = shopNode
    ? { value: cleanShopName(shopNode.text), source: 'dom' }
    : { value: null, source: null };
  if (shopName.value === null) {
    const v = pickJsonString(scriptText, SHOP_NAME_KEYS);
    if (v !== null) shopName = { value: v, source: 'json' };
  }

  // 店铺 ID：data-shopid 属性 → 店铺链接 href 参数 → JSON
  const shopId = pickShopId(scriptText);

  // ===== 价格双价归属（2025 版页面实测语义，淘宝天猫同版式）=====
  // 到手价高亮容器 highlightPrice-- 必然存在；原价容器 subPrice-- 仅在有优惠时存在。
  // 规则：subPrice 命中 → subPrice=原价、highlightPrice=到手价；
  //       subPrice 未命中 → highlightPrice=原价（售价）、到手价=null（不再回退为售价）。
  // 状态A（简化渲染）：页面只有 PurchasePanel 内的 block2--（unit--=￥ + text--=数字），
  // 由 pickUnitTextPrice 兜底（吸顶栏 ItemHeadFixed-- 内的同名结构是重复价，必须排除）。
  // 注意：[class*="Price--"] 大容器会把两个价格文本拼接（「…￥3188.55优惠前￥3799」），
  // 严禁用它抓原价；JSON 通道同理，finalPrice/couponPrice 键仅在显式存在时才用作到手价。
  const isTaoFamily = rule.id === 'taobao' || rule.id === 'tmall';
  const sale = pickPrice(
    rule.selectors.price,
    scriptText,
    SALE_PRICE_KEYS,
    isTaoFamily ? pickUnitTextPrice : undefined,
  );
  const sub = pickPrice(rule.selectors.originalPrice, scriptText, ORIG_PRICE_KEYS);
  let original: PickedValue<number> & { domNode: PickedNode | null };
  let finalP: PickedValue<number> & { domNode: PickedNode | null };
  if (sub.value !== null) {
    original = sub;
    // 有原价时高亮价即到手价；高亮价缺失才尝试显式券后价选择器/键
    finalP = sale.value !== null ? sale : pickPrice(rule.selectors.finalPrice, scriptText, FINAL_PRICE_KEYS);
  } else {
    original = sale;
    finalP = pickPrice(rule.selectors.finalPrice, scriptText, FINAL_PRICE_KEYS);
  }
  // 大小关系兜底：到手价不应高于原价；反了说明归属错位，交换两者（含来源与快照节点）
  if (original.value !== null && finalP.value !== null && finalP.value > original.value) {
    [original, finalP] = [finalP, original];
  }
  const coupon = couponNode ? parseCoupon(couponNode.text) : { amount: null, type: null };

  // 发货城市：DOM → JSON；原文保留，另做省市归一化
  const shipNode = pickFirst(rule.selectors.shippingCity);
  let shipRaw: PickedValue<string> = shipNode
    ? { value: shipNode.text, source: 'dom' }
    : { value: null, source: null };
  if (shipRaw.value === null) {
    const v = pickJsonString(scriptText, SHIPPING_KEYS);
    if (v !== null) shipRaw = { value: v, source: 'json' };
  }
  const shipNormalized = shipRaw.value !== null ? normalizeShippingCity(shipRaw.value) : null;

  const markerNode = pickFirst(rule.selectors.userMarker);

  const price: PriceInfo = {
    original: original.value,
    final: finalP.value,
    currency: 'CNY',
    couponAmount: coupon.amount,
    couponType: coupon.type,
  };

  const extractionMeta: ExtractionMeta = {
    price: sale.source,
    originalPrice: original.source,
    finalPrice: finalP.source,
    shippingCity: shipRaw.source,
    shopName: shopName.source,
    shopId: shopId.source,
  };

  // 关键节点 DOM 快照（商品名 / 售价 / 到手价 / 店铺），用于证据留存
  const domSnapshots: DomSnapshot[] = [];
  const snapshotTargets: ReadonlyArray<readonly [string, PickedNode | null]> = [
    ['title', title],
    ['price', sale.domNode],
    ['finalPrice', finalP.domNode],
    ['originalPrice', original.domNode],
    ['shopName', shopNode],
    ['shippingCity', shipNode],
  ];
  for (const [field, node] of snapshotTargets) {
    const snap = node ? snapshotNode(field, node.el) : null;
    if (snap) domSnapshots.push(snap);
  }
  // 提取来源标注同样留存一份，便于事后排查某字段来自哪个通道
  domSnapshots.push({ field: 'extractionMeta', outerHTML: JSON.stringify(extractionMeta) });

  return {
    platform: rule.id,
    productId,
    productName: title?.text ?? null,
    shopName: shopName.value,
    shopId: shopId.value,
    productUrl: window.location.href,
    price,
    userContext: inferUserContext(rule, markerNode?.text ?? null),
    device: collectDeviceInfo(),
    shipping: { shipFromCity: shipRaw.value, shipFromCityNormalized: shipNormalized },
    extractionMeta,
    domSnapshots,
  };
}

/** 按候选选择器顺序尝试，返回第一个命中且可见文本非空的节点 */
function pickFirst(selectors: string[]): PickedNode | null {
  for (const sel of selectors) {
    try {
      const el = document.querySelector(sel);
      const text = el?.textContent?.replace(/\s+/g, ' ').trim() ?? '';
      if (el && text) return { text, el };
    } catch {
      // 非法选择器直接跳过，继续尝试下一个候选
    }
  }
  return null;
}

/** 收集全部内联 script 文本（跳过外链脚本），上限 2MB 防爆内存 */
function collectInlineScriptText(): string {
  const parts: string[] = [];
  let total = 0;
  const scripts = document.querySelectorAll('script:not([src])');
  for (const s of scripts) {
    const t = s.textContent ?? '';
    if (!t) continue;
    parts.push(t);
    total += t.length;
    if (total >= 2_000_000) break;
  }
  return parts.join('\n');
}

/** 价格字段双策略：DOM 选择器（数值须合法）→ 平台专用 DOM 兜底（可选）→ 内嵌 JSON 键值回退 */
function pickPrice(
  domSelectors: string[],
  scriptText: string,
  jsonKeys: string[],
  extraDom?: () => (PickedValue<number> & { domNode: PickedNode | null }) | null,
): PickedValue<number> & { domNode: PickedNode | null } {
  const node = pickFirst(domSelectors);
  if (node) {
    const n = parsePriceNumber(node.text);
    if (n !== null && n >= PRICE_MIN && n <= PRICE_MAX) {
      return { value: n, source: 'dom', domNode: node };
    }
  }
  if (extraDom) {
    const e = extraDom();
    if (e) return e;
  }
  const j = pickJsonPrice(scriptText, jsonKeys);
  if (j !== null) return { value: j, source: 'json', domNode: node };
  return { value: null, source: null, domNode: node };
}

/**
 * 简化渲染（状态A）价格兜底（仅淘系）：
 * PurchasePanel 主区域内 div[class*="block2--"] 的
 * span[class*="unit--"]（￥/¥）+ span[class*="text--"]（数字）组合。
 * 必须排除吸顶栏 [class*="ItemHeadFixed--"] 内部的同名结构——
 * 真实页面实测吸顶栏有一份重复价格，不排除会抓到错误数字。
 */
function pickUnitTextPrice(): (PickedValue<number> & { domNode: PickedNode | null }) | null {
  const blocks = document.querySelectorAll('div[class*="block2--"]');
  for (const b of blocks) {
    if (b.closest('[class*="ItemHeadFixed--"]')) continue; // 排除吸顶栏重复价
    const unit = b.querySelector('span[class*="unit--"]');
    const numEl = b.querySelector('span[class*="text--"]');
    if (!unit || !numEl) continue;
    const unitText = (unit.textContent ?? '').trim();
    if (!/^[¥￥]$/.test(unitText)) continue;
    const numText = (numEl.textContent ?? '').trim();
    const n = parsePriceNumber(numText);
    if (n !== null && n >= PRICE_MIN && n <= PRICE_MAX) {
      return { value: n, source: 'dom', domNode: { text: `${unitText}${numText}`, el: b } };
    }
  }
  return null;
}

/** 从内嵌 script 文本按键名优先级提取价格：取第一个命中且落在合法区间的值 */
function pickJsonPrice(text: string, keys: string[]): number | null {
  if (!text) return null;
  for (const key of keys) {
    const re = new RegExp(`"${key}"\\s*:\\s*"?(-?\\d+(?:\\.\\d+)?)"?`);
    const m = re.exec(text);
    if (!m) continue;
    const n = Number(m[1]);
    if (Number.isFinite(n) && n >= PRICE_MIN && n <= PRICE_MAX) return n;
  }
  return null;
}

/** 从内嵌 script 文本按键名优先级提取字符串值 */
function pickJsonString(text: string, keys: string[], maxLen = 80): string | null {
  if (!text) return null;
  for (const key of keys) {
    const re = new RegExp(`"${key}"\\s*:\\s*"([^"]{1,${maxLen}})"`);
    const m = re.exec(text);
    if (m && m[1].trim()) return m[1].trim();
  }
  return null;
}

/** 店铺 ID 三策略：data-shopid 属性 → 店铺链接 href 的 shopId/shop_id/sellerId 参数 → JSON */
function pickShopId(scriptText: string): PickedValue<string> {
  // ① data-shopid / data-sellerid 属性
  const attrEl = document.querySelector('[data-shopid],[data-sellerid]');
  const attr =
    attrEl?.getAttribute('data-shopid')?.trim() ?? attrEl?.getAttribute('data-sellerid')?.trim() ?? null;
  if (attr && /^\d{3,}$/.test(attr)) return { value: attr, source: 'dom' };

  // ② 店铺链接 href 参数
  const links = document.querySelectorAll('a[href*="shop"]');
  for (const a of links) {
    const href = a.getAttribute('href') ?? '';
    const m = href.match(/[?&](?:shopId|shop_id|sellerId|seller_id)=(\d{3,})/);
    if (m) return { value: m[1], source: 'dom' };
  }

  // ③ 内嵌 JSON（g_config.shopId / __INIT_DATA 的 shopId/sellerId 等）
  const v = pickJsonString(scriptText, SHOP_ID_KEYS, 40);
  if (v !== null && /^\d{3,}$/.test(v)) return { value: v, source: 'json' };
  return { value: null, source: null };
}

/**
 * 店铺名清理：回退选择器（如外层 wrapper [class*="shopName"]）命中的文本可能混入评分后缀
 * （真实页实测：「明智电脑科技4.690天新增…」）。
 * 仅当文本以 ≥2 个非数字字符开头、其后出现数字尾巴时，截断取第一个连续非数字段；
 * 数字开头的店铺名（如「360官方旗舰店」）不做处理，避免误伤。
 */
function cleanShopName(text: string): string {
  const m = text.match(/^[^\d]{2,}(?=\d)/);
  return m ? m[0].trim() : text;
}

/** 中国大陆直辖市 */
const MUNICIPALITIES = ['北京', '上海', '天津', '重庆'];
/** 省 / 自治区 / 特别行政区名（不含后缀） */
const PROVINCES = [
  '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西',
  '山东', '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西',
  '甘肃', '青海', '台湾', '内蒙古', '广西', '西藏', '宁夏', '新疆', '香港', '澳门',
];

/**
 * 发货地归一化：先按「至」切分取前半段（发货侧；2025 版文本形如
 * 「浙江嘉兴 至 北京市 海淀区」「重庆 至 北京市 海淀区」），再做省市关键词提取。
 * 规则：直辖市直接返回；省名命中后取其后的市名（1-4 汉字，止于 市/区/县/州/盟/地区 或结尾）；
 * 只有省份信息时返回省名；无省份信息时尝试「xx市」；都不行返回 null。
 */
function normalizeShippingCity(raw: string): string | null {
  // 「至」前为发货地，后为收货地（收货侧是用户地址，必须排除）；
  // 兼容「配送至 北京市 朝阳区」这类左侧只有动词前缀的旧格式：左侧为纯前缀词时取右侧。
  const segs = raw.split('至').map((s) => s.replace(/\s+/g, ''));
  let t = segs[0];
  if (!t || t === '配送' || t === '发货' || t === '快递') t = segs[1] ?? '';
  if (!t) return null;
  for (const m of MUNICIPALITIES) {
    if (t.includes(m)) return m;
  }
  for (const p of PROVINCES) {
    const idx = t.indexOf(p);
    if (idx === -1) continue;
    const rest = t
      .slice(idx + p.length)
      .replace(/^(特别行政区|壮族自治区|回族自治区|维吾尔自治区|自治区|省|市)/, '');
    // 终止符不含「州」：广州/杭州/苏州等市名以州结尾，把州当终止符会截出「广」
    const cm = rest.match(/^([一-龥]{1,4}?)(?:市|区|县|盟|地区|自治州|$)/);
    if (cm && cm[1]) return cm[1];
    return p;
  }
  const cm = t.match(/([一-龥]{2,4})市/);
  if (cm) return cm[1];
  return null;
}

/**
 * 从文本中解析价格数字（容忍 ¥/￥ 符号与千分位逗号）
 * 规则：文本含 ¥/￥ 时，读取符号**后面**的数字（价格容器文案形如「超级88￥3119起」，
 * 标签里的 88 是活动名而非价格）；无符号时才回退到首个数字。
 */
function parsePriceNumber(text: string): number | null {
  const t = text.replace(/,/g, '');
  const afterSymbol = t.match(/[¥￥]\s*(\d+(?:\.\d{1,2})?)/);
  const m = afterSymbol ?? t.match(/(\d+(?:\.\d{1,2})?)/);
  if (!m) return null;
  const n = Number(m[1]);
  return Number.isFinite(n) ? n : null;
}

/** 从优惠券/补贴文本解析金额与类型，如「满199减30」「8.5折」「10元券」「已享受: ¥500百亿补贴」 */
function parseCoupon(text: string): { amount: number | null; type: string | null } {
  const t = text.trim();
  if (!t) return { amount: null, type: null };
  // 平台补贴类文案（金额可在类型词前「¥500百亿补贴」或后「领政府补贴省562.69」），提不到金额不报错
  for (const st of ['百亿补贴', '平台补贴', '政府补贴'] as const) {
    const idx = t.indexOf(st);
    if (idx === -1) continue;
    const before = t.slice(0, idx).match(/[¥￥]\s*(\d+(?:\.\d+)?)\s*$/);
    const after = t.slice(idx + st.length).match(/^(?:已?抵|立?省|减)?\s*[¥￥]?\s*(\d+(?:\.\d+)?)/);
    const amount = before?.[1] ?? after?.[1];
    return { amount: amount ? Number(amount) : null, type: st === '百亿补贴' ? '百亿补贴' : '平台补贴' };
  }
  let type: string | null = null;
  if (/满.*减/.test(t)) type = '满减券';
  else if (/折/.test(t)) type = '折扣券';
  else if (/券|优惠/.test(t)) type = '通用券';
  const m = t.match(/减\s*(\d+(?:\.\d+)?)/) ?? t.match(/(\d+(?:\.\d+)?)\s*元/);
  return { amount: m ? Number(m[1]) : null, type };
}

/**
 * 登录状态保守推断
 * 隐私红线：cookie 只判断「白名单键名是否存在」，值绝不读取、绝不上报。
 * 无法确定的维度一律填 null，并在 evidence 中说明依据。
 */
function inferUserContext(rule: PlatformRule, markerText: string | null): RawUserContext {
  const cookieKeys = new Set(
    document.cookie
      .split(';')
      .map((kv) => kv.split('=')[0].trim())
      .filter(Boolean),
  );
  const hitCookie = rule.loginCookieNames.find((name) => cookieKeys.has(name)) ?? null;

  const evidence: string[] = [];
  let isLoggedIn: boolean | null = null;
  if (hitCookie) {
    isLoggedIn = true;
    evidence.push(`存在登录态 cookie 键名「${hitCookie}」（仅判断存在性，未读取值）`);
  }

  const marker = markerText?.trim() || null;
  if (marker) {
    if (/请登录|立即登录|^登录$|注册/.test(marker)) {
      if (isLoggedIn === null) isLoggedIn = false;
      evidence.push('页面用户节点展示「登录/注册」入口，推断未登录');
    } else {
      if (isLoggedIn === null) isLoggedIn = true;
      // 证据文本中的昵称先打码，避免原文进入记录
      evidence.push(`页面展示用户标识「${maskText(marker)}」`);
    }
  }
  if (isLoggedIn === null) {
    evidence.push('未找到可靠登录态证据，按未知处理');
  }

  // 会员等级关键词（页面可见文本）
  let memberLevel: string | null = null;
  const levelMatch = marker?.match(/(88VIP|PLUS|超级会员|钻石会员|黄金会员|VIP\d{0,2}|会员)/i);
  if (levelMatch) memberLevel = levelMatch[1];

  return {
    isLoggedIn,
    memberLevel,
    isNewUser: null, // 页面无法可靠判断是否新用户，保持 null
    userMarker: marker,
    evidence: `${evidence.join('；')}；isNewUser 页面无可靠判断依据，记为 null`,
  };
}

/** 采集设备信息（均为浏览器主动暴露的通用字段，不含指纹级追踪参数） */
function collectDeviceInfo(): DeviceInfo {
  const nav = navigator as Navigator & { deviceMemory?: number };
  const memory = typeof nav.deviceMemory === 'number' ? nav.deviceMemory : null;
  const cores = typeof navigator.hardwareConcurrency === 'number' ? navigator.hardwareConcurrency : null;
  const pixels = window.screen.width * window.screen.height;
  return {
    userAgent: navigator.userAgent,
    screenResolution: `${window.screen.width}x${window.screen.height}`,
    deviceMemory: memory,
    hardwareConcurrency: cores,
    platform: navigator.platform,
    language: navigator.language,
    devicePriceIndex: estimateDevicePriceIndex(memory, cores, pixels),
  };
}

/**
 * 设备价格指数估算（0-100）
 * 说明：这是「设备档次」的代理估算指标，并非设备真实售价。
 * 用途：分析平台是否对不同设备档次的用户差异化定价（例如高价设备用户看到更高价格）。
 * 加权方式：内存 40% + CPU 核心数 30% + 屏幕像素 30%，各分量按经验上限归一化后加权求和。
 */
function estimateDevicePriceIndex(memory: number | null, cores: number | null, pixels: number): number {
  const memScore = memory === null ? 0.5 : Math.min(memory / 16, 1); // 16GB 视为满配
  const cpuScore = cores === null ? 0.5 : Math.min(cores / 8, 1); // 8 核视为满配
  const screenScore = Math.min(pixels / (2560 * 1440), 1); // 2K 屏视为满配
  return Math.round((memScore * 0.4 + cpuScore * 0.3 + screenScore * 0.3) * 100);
}

/** 生成关键节点 DOM 快照：克隆后剔除 script/style，截取前 2000 字符 */
function snapshotNode(field: string, el: Element): DomSnapshot | null {
  const clone = el.cloneNode(true) as Element;
  clone.querySelectorAll('script,style').forEach((n) => n.remove());
  const html = (clone.outerHTML ?? '').slice(0, 2000);
  return html ? { field, outerHTML: html } : null;
}
