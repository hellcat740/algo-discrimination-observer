// backendMapping 单元测试（纯 Node 运行，不依赖浏览器）
// 做法：用 esbuild（vite 自带依赖）把 src/shared/backendMapping.ts 临时编译为 cjs，
// 再 require 进来跑断言。backendMapping.ts 本身是纯函数模块，不依赖 chrome.*/DOM。
import { buildSync } from 'esbuild';
import { createRequire } from 'node:module';
import { unlinkSync } from 'node:fs';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const tmpOut = join(root, 'test', '.tmp-mapping.cjs');

buildSync({
  entryPoints: [join(root, 'src', 'shared', 'backendMapping.ts')],
  bundle: true,
  format: 'cjs',
  platform: 'node',
  outfile: tmpOut,
  logLevel: 'silent',
});

const require = createRequire(import.meta.url);
const { mapObservationToBackend, isPeakHour, snapshotToText, yuanToCents } = require('./.tmp-mapping.cjs');

// ===== 构造一份完整 ObservationRecord fixture =====
// collectedAt 用本地 20:30 构造（断言本机时区无关：创建与读取同为本地时区）
const localEvening = new Date(2026, 5, 15, 20, 30, 0); // 2026-06-15 20:30 本地
const localAfternoon = new Date(2026, 5, 15, 15, 0, 0); // 2026-06-15 15:00 本地

const baseRecord = {
  recordId: '11111111-2222-3333-4444-555555555555',
  anonymousUserId: 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
  collectedAt: localEvening.toISOString(),
  platform: 'yangkeduo', // 插件平台 id（应映射为后端 pinduoduo）
  productId: '987654321',
  productName: '测试商品名称',
  shopName: '张三的店铺',
  shopId: null, // 无店铺 ID 时 seller_id 回退店铺名
  productUrl: 'https://mobile.yangkeduo.com/goods.html?goods_id=987654321',
  price: {
    original: 99.9,
    final: 79.9,
    currency: 'CNY',
    couponAmount: 20,
    couponType: '满减券',
  },
  userContext: {
    isLoggedIn: true,
    memberLevel: 'VIP',
    isNewUser: null,
    userMarkerMasked: '张*', // 绝不应进入 payload
    evidence: '存在登录态 cookie 键名「unb」…', // 绝不应进入 payload
  },
  device: {
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0',
    screenResolution: '1920x1080',
    deviceMemory: 8,
    hardwareConcurrency: 8,
    platform: 'Win32',
    language: 'zh-CN',
    devicePriceIndex: 62,
  },
  network: { ip: '1.2.3.4', city: '北京', region: '北京', country: 'CN', source: 'ipapi.co' },
  shipping: { shipFromCity: '上海', shipFromCityNormalized: null },
  screenshotDataUrl: 'data:image/png;base64,SCREENSHOT_SHOULD_NEVER_UPLOAD',
  domSnapshots: [
    { field: 'title', outerHTML: '<h1>测试商品名称</h1>' },
    { field: 'price', outerHTML: '<div class="p"><span>¥</span><b>79.9</b></div>' },
  ],
  uploadStatus: 'pending',
  observationId: null,
};

let passed = 0;
function check(name, fn) {
  fn();
  passed++;
  console.log(`OK   ${name}`);
}

// ===== 断言 =====
const payload = mapObservationToBackend(baseRecord, '0.1.0');
const payloadJson = JSON.stringify(payload);

check('platform_code：yangkeduo → pinduoduo', () => {
  assert.equal(payload.platform_code, 'pinduoduo');
});

check('platform_code：jd/taobao/tmall 直通', () => {
  assert.equal(mapObservationToBackend({ ...baseRecord, platform: 'jd' }, '0.1.0').platform_code, 'jd');
  assert.equal(mapObservationToBackend({ ...baseRecord, platform: 'taobao' }, '0.1.0').platform_code, 'taobao');
  assert.equal(mapObservationToBackend({ ...baseRecord, platform: 'tmall' }, '0.1.0').platform_code, 'tmall');
});

check('shopName → seller_id（店铺名代替卖家 ID）', () => {
  assert.equal(payload.seller_id, '张三的店铺');
});

check('shopId 优先 → seller_id（有店铺 ID 时不用店铺名）', () => {
  const p = mapObservationToBackend({ ...baseRecord, shopId: '2212833764123' }, '0.1.0');
  assert.equal(p.seller_id, '2212833764123');
});

check('productId / productName / productUrl 透传', () => {
  assert.equal(payload.product_id, '987654321');
  assert.equal(payload.product_name, '测试商品名称');
  assert.equal(payload.product_url, 'https://mobile.yangkeduo.com/goods.html?goods_id=987654321');
});

check('价格换算为整数分（fixture：99.9→9990、79.9→7990、券20→2000）', () => {
  assert.equal(payload.display_price_cents, 9990);
  assert.equal(payload.actual_pay_price_cents, 7990);
  assert.equal(payload.discount_coupon_amount_cents, 2000);
  assert.equal(payload.currency, 'CNY');
});

check('价格换算边界（回归：JSON 整数/浮点跨语言歧义导致的 100 倍错误）', () => {
  // 整数元值 5999.0 序列化为 5999 时，Python 侧会解析为 int；插件侧必须直接给整数分
  assert.equal(yuanToCents(89.9), 8990);
  assert.equal(yuanToCents(5999), 599900);
  assert.equal(yuanToCents(5999.0), 599900);
  assert.equal(yuanToCents(null), null);
  assert.equal(yuanToCents(300), 30000); // coupon 300 元 → 30000 分
  // 浮点精度：79.9 * 100 = 7990.000000000002，Math.round 必须归整
  assert.equal(yuanToCents(79.9), 7990);
  // 端到端：null 价格字段在 payload 中保持 null
  const p = mapObservationToBackend(
    { ...baseRecord, price: { original: null, final: 5999, currency: 'CNY', couponAmount: 300, couponType: null } },
    '0.1.0',
  );
  assert.equal(p.display_price_cents, null);
  assert.equal(p.actual_pay_price_cents, 599900);
  assert.equal(p.discount_coupon_amount_cents, 30000);
});

check('couponType → promo_type / promo_label', () => {
  assert.equal(payload.promo_type, '满减券');
  assert.ok(payload.promo_label.includes('满减券'));
});

check('用户上下文字段映射（is_login / membership_level / is_new_user）', () => {
  assert.equal(payload.is_login, true);
  assert.equal(payload.membership_level, 'VIP');
  assert.equal(payload.is_new_user, null);
});

check('隐私：userMarker / evidence 不出现在 payload', () => {
  assert.ok(!('userMarker' in payload));
  assert.ok(!('userMarkerMasked' in payload));
  assert.ok(!('evidence' in payload));
  assert.ok(!payloadJson.includes('张*'), 'payload 不应包含打码昵称');
  assert.ok(!payloadJson.includes('unb'), 'payload 不应包含 cookie 键名证据');
});

check('隐私：screenshotDataUrl / domSnapshots 整份不上传', () => {
  assert.ok(!('screenshotDataUrl' in payload));
  assert.ok(!('domSnapshots' in payload));
  assert.ok(!payloadJson.includes('SCREENSHOT_SHOULD_NEVER_UPLOAD'));
});

check('设备字段映射（user_agent / platform / language / device_memory / hardware_concurrency / screen_resolution / device_price_score_estimate）', () => {
  assert.equal(payload.user_agent, baseRecord.device.userAgent);
  assert.equal(payload.platform, 'Win32');
  assert.equal(payload.language, 'zh-CN');
  assert.equal(payload.device_memory, 8);
  assert.equal(payload.hardware_concurrency, 8);
  assert.equal(payload.screen_resolution, '1920x1080');
  assert.equal(payload.device_price_score_estimate, 62);
});

check('network.city → ip_city、shipping → shipping_city（归一化优先，无归一化回退原文）', () => {
  assert.equal(payload.ip_city, '北京');
  assert.equal(payload.shipping_city, '上海');
  // 有归一化值时优先于原文
  const p = mapObservationToBackend(
    { ...baseRecord, shipping: { shipFromCity: '配送至 浙江 嘉兴', shipFromCityNormalized: '嘉兴' } },
    '0.1.0',
  );
  assert.equal(p.shipping_city, '嘉兴');
});

check('fetch_ts = collectedAt（UTC ISO）', () => {
  assert.equal(payload.fetch_ts, baseRecord.collectedAt);
});

check('peak_hour：本地 20:30 → true；本地 15:00 → false', () => {
  assert.equal(payload.peak_hour, true);
  const p2 = mapObservationToBackend({ ...baseRecord, collectedAt: localAfternoon.toISOString() }, '0.1.0');
  assert.equal(p2.peak_hour, false);
  // 边界：11 点与 13 点为 true，14 点 false，19 点 true，23 点 true
  assert.equal(isPeakHour(new Date(2026, 5, 15, 11, 0, 0).toISOString()), true);
  assert.equal(isPeakHour(new Date(2026, 5, 15, 13, 59, 0).toISOString()), true);
  assert.equal(isPeakHour(new Date(2026, 5, 15, 14, 0, 0).toISOString()), false);
  assert.equal(isPeakHour(new Date(2026, 5, 15, 19, 0, 0).toISOString()), true);
  assert.equal(isPeakHour(new Date(2026, 5, 15, 23, 30, 0).toISOString()), true);
  assert.equal(isPeakHour(new Date(2026, 5, 15, 0, 0, 0).toISOString()), false);
});

check('dom_price_text：取价格快照纯文本（去标签 ≤500 字符）', () => {
  assert.equal(payload.dom_price_text, '¥ 79.9');
  const long = '<div>' + 'x'.repeat(600) + '</div>';
  assert.equal(snapshotToText(long).length, 500);
});

check('register_days / stock_hint 固定为 null（插件未采集）', () => {
  assert.equal(payload.register_days, null);
  assert.equal(payload.stock_hint, null);
});

check('source_code_version 来自 extVersion 参数', () => {
  assert.equal(payload.source_code_version, '0.1.0');
});

check('anonymous_id = anonymousUserId', () => {
  assert.equal(payload.anonymous_id, 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee');
});

// 清理临时编译产物
try {
  unlinkSync(tmpOut);
} catch {
  /* 忽略清理失败 */
}

console.log(`\n全部 ${passed} 项断言通过 ✅`);
