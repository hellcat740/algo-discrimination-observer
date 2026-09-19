/**
 * 页面探针入口（由 scripts/gen-page-probe.mjs 打包为 dist-test/page-probe.js）
 *
 * 用途：在真实浏览器（如 Edge 的淘宝商品页）中通过 Runtime.evaluate / 控制台执行，
 * 验证「DOM 提取 → ObservationRecord 组装 → 后端字段映射 → POST 上报」的端到端链路。
 *
 * 设计要点：
 *  - 复用与 content script 完全相同的提取逻辑（../shared/extract）与映射逻辑（../shared/backendMapping）；
 *  - 整条文件是一个 async IIFE 表达式语句：脚本完成值是一个 Promise<string>，
 *    Runtime.evaluate 传 awaitPromise:true 时可直接拿到 JSON 字符串结果；
 *  - 截图与 IP 查询属于 service worker 能力，探针中置 null 并在 network.source 标注。
 */
import { extractPageData } from '../shared/extract';
import { mapObservationToBackend } from '../shared/backendMapping';
import type { ObservationRecord } from '../types';

(async function pageProbe(): Promise<string> {
  const data = extractPageData();
  if (!data) {
    return JSON.stringify({ ok: false, error: '当前页未识别为受支持的商品详情页（平台规则或商品 ID 模式未命中）' });
  }

  // 组装 ObservationRecord（与 background 的组装逻辑一致；截图/IP 为探针降级值）
  const record: ObservationRecord = {
    recordId: typeof crypto.randomUUID === 'function' ? crypto.randomUUID() : `probe-${Date.now()}`,
    anonymousUserId: 'page-probe',
    collectedAt: new Date().toISOString(),
    platform: data.platform,
    productId: data.productId,
    productName: data.productName,
    shopName: data.shopName,
    shopId: data.shopId,
    productUrl: data.productUrl,
    price: data.price,
    userContext: {
      isLoggedIn: data.userContext.isLoggedIn,
      memberLevel: data.userContext.memberLevel,
      isNewUser: data.userContext.isNewUser,
      userMarkerMasked: null, // 探针不打码也不上传昵称（映射层本就不含该字段）
      evidence: data.userContext.evidence,
    },
    device: data.device,
    network: { ip: null, city: null, region: null, country: null, source: 'page-probe（探针不查询 IP）' },
    shipping: data.shipping,
    screenshotDataUrl: null, // 探针不截图（且映射层本就不上传截图）
    screenshotError: 'page-probe 不提供截图能力',
    domSnapshots: data.domSnapshots,
    extractionMeta: data.extractionMeta,
    uploadStatus: 'pending',
    observationId: null,
  };

  const payload = mapObservationToBackend(record, 'page-probe');

  try {
    const resp = await fetch('http://127.0.0.1:8000/api/observations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'dev-key-123',
      },
      body: JSON.stringify(payload),
    });
    const body = (await resp.json().catch(() => ({}))) as {
      observation_id?: string;
      created_at?: string;
      warnings?: unknown;
    };
    return JSON.stringify({
      ok: resp.ok,
      status: resp.status,
      observationId: body.observation_id ?? null,
      warnings: Array.isArray(body.warnings) ? body.warnings : [],
      extracted: {
        platform: data.platform,
        productId: data.productId,
        productName: data.productName,
        shopName: data.shopName,
        shopId: data.shopId,
        price: data.price,
        shipFromCity: data.shipping.shipFromCity,
        shipFromCityNormalized: data.shipping.shipFromCityNormalized,
        extractionMeta: data.extractionMeta,
        isLoggedIn: data.userContext.isLoggedIn,
        memberLevel: data.userContext.memberLevel,
        devicePriceIndex: data.device.devicePriceIndex,
        snapshotFields: data.domSnapshots.map((s) => s.field),
        domPriceText: payload.dom_price_text,
      },
    });
  } catch (e) {
    return JSON.stringify({ ok: false, error: String(e), hint: '请确认本地后端已在 127.0.0.1:8000 运行' });
  }
})();
