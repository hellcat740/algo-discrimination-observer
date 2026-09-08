/**
 * Service Worker：采集流程编排与对外网络请求
 * START_COLLECTION（手动）/ AUTO_COLLECT（商品页自动）→ 授权校验 →
 * collectAndUpload 共用流水线：向页面要数据（EXTRACT_PAGE_DATA）→ 截图 →
 * 查公网 IP 城市 → 组装 ObservationRecord → 本地脱敏（白名单 sanitize）→
 * mapObservationToBackend 映射为后端扁平 schema → POST 上报（X-API-Key 鉴权）→
 * 无论成败都存 chrome.storage.local → 返回结果给调用方。
 *
 * 隐私前提：自动采集（AUTO_COLLECT）必须在用户已授权（consent=true）
 * 且自动采集开关打开（autoCollect=true）时才执行。
 */
import { DEFAULT_API_ENDPOINT, DEFAULT_API_KEY, MAX_LOCAL_RECORDS, MSG, STORAGE_KEYS } from '../types';
import type {
  AutoCollectPayload,
  BackendObservationPayload,
  CollectionResult,
  ExtensionSettings,
  ExtractedPageData,
  NetworkInfo,
  ObservationRecord,
  RetryResult,
  StartCollectionPayload,
  TestConnectionResult,
  UploadStatus,
} from '../types';
import { mapObservationToBackend } from '../shared/backendMapping';
import { errMsg, maskText } from '../utils';

// ===== 消息路由 =====
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message?.type === MSG.START_COLLECTION) {
    void handleStartCollection((message.payload ?? {}) as StartCollectionPayload, sender).then(sendResponse);
    return true; // 异步响应
  }
  if (message?.type === MSG.AUTO_COLLECT) {
    void handleAutoCollect((message.payload ?? {}) as AutoCollectPayload, sender).then(sendResponse);
    return true; // 异步响应
  }
  if (message?.type === MSG.TEST_CONNECTION) {
    void handleTestConnection().then(sendResponse);
    return true; // 异步响应
  }
  if (message?.type === MSG.RETRY_FAILED) {
    void handleRetryFailed().then(sendResponse);
    return true; // 异步响应
  }
  return false;
});

/**
 * 后端连通测试：fetch 后端 <origin>/health（origin 由 apiEndpoint 推导，去掉 /api/... 路径）
 * /health 为公开接口，不带 X-API-Key；3 秒超时。
 */
async function handleTestConnection(): Promise<TestConnectionResult> {
  const settings = await getSettings();
  let healthUrl: string;
  try {
    healthUrl = `${new URL(settings.apiEndpoint).origin}/health`;
  } catch {
    return { ok: false, detail: `API 端点格式无效：${settings.apiEndpoint}` };
  }
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 3000);
  try {
    const resp = await fetch(healthUrl, { signal: ctrl.signal });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    return { ok: true, detail: '已连通（数据库正常）' };
  } catch (e) {
    return { ok: false, detail: `无法连接 ${healthUrl}：${errMsg(e)}` };
  } finally {
    clearTimeout(timer);
  }
}

// ===== 手动采集入口（popup / 提示条触发） =====

async function handleStartCollection(
  payload: StartCollectionPayload,
  sender: chrome.runtime.MessageSender,
): Promise<CollectionResult> {
  // 1. 授权校验：提示条「仅本次采集」不写入持久授权，但视为本次已授权
  const settings = await getSettings();
  if (!settings.consent && !payload.onceOnly) {
    return { ok: false, error: 'no_consent：尚未获得采集授权' };
  }

  // 2. 定位目标标签页：优先消息来源页（提示条触发），其次当前活动页（popup 触发）
  const tab = sender.tab ?? (await getActiveTab());
  if (!tab?.id) return { ok: false, error: '未找到目标标签页' };

  // 3. 进入采集流水线（手动采集不受自动去重限制）
  return collectAndUpload(tab, 'manual', settings);
}

// ===== 自动采集入口（content script 在商品详情页触发） =====

/** 同一商品自动采集的最小间隔（10 分钟） */
const AUTO_COLLECT_DEDUP_MS = 10 * 60 * 1000;

async function handleAutoCollect(
  payload: AutoCollectPayload,
  sender: chrome.runtime.MessageSender,
): Promise<CollectionResult> {
  // 1. 纵深防御：content 侧已检查授权与开关，此处再校验一次
  const settings = await getSettings();
  if (!settings.consent || !settings.autoCollect) {
    return { ok: false, error: 'auto_collect_disabled：未授权或自动采集开关未打开' };
  }
  const tab = sender.tab;
  if (!tab?.id) return { ok: false, error: '未找到来源标签页' };

  // 2. 跨页面去重：同一 productId 10 分钟内不重复自动采集（手动采集不受此限）
  const productId = typeof payload?.productId === 'string' ? payload.productId : null;
  if (productId && (await isRecentlyAutoCollected(productId))) {
    return { ok: false, error: 'duplicate：该商品 10 分钟内已自动采集过' };
  }

  // 3. 进入采集流水线；成功后写入去重表
  const result = await collectAndUpload(tab, 'auto', settings);
  if (result.ok && productId) await markAutoCollected(productId);
  return result;
}

/** 读取去重表：该商品是否在最近 10 分钟内已自动采集过 */
async function isRecentlyAutoCollected(productId: string): Promise<boolean> {
  const res = await chrome.storage.local.get(STORAGE_KEYS.LAST_AUTO_COLLECT);
  const map = res[STORAGE_KEYS.LAST_AUTO_COLLECT];
  if (!map || typeof map !== 'object') return false;
  const ts = (map as Record<string, unknown>)[productId];
  return typeof ts === 'number' && Date.now() - ts < AUTO_COLLECT_DEDUP_MS;
}

/** 更新去重表；仅保留最近 200 个商品的时间戳，防止无限膨胀 */
async function markAutoCollected(productId: string): Promise<void> {
  const res = await chrome.storage.local.get(STORAGE_KEYS.LAST_AUTO_COLLECT);
  const raw = res[STORAGE_KEYS.LAST_AUTO_COLLECT];
  const map: Record<string, number> =
    raw && typeof raw === 'object' ? { ...(raw as Record<string, number>) } : {};
  map[productId] = Date.now();
  const trimmed = Object.entries(map)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 200);
  await chrome.storage.local.set({ [STORAGE_KEYS.LAST_AUTO_COLLECT]: Object.fromEntries(trimmed) });
}

// ===== 失败记录重试（popup 手动触发） =====

/**
 * 重试上报所有 uploadStatus === 'failed' 的本地记录：
 * 用已存数据重新映射 + POST，不重新截图/提取；
 * 成功则更新该记录的 uploadStatus 与 observationId（并清除旧的 uploadError）。
 * 注意：skipped_no_price（价格抓空被跳过）不参与重试——价格缺失需回页面重新采集，
 * 重发同一份无价格数据只会再次被跳过。
 */
async function handleRetryFailed(): Promise<RetryResult> {
  const settings = await getSettings();
  const res = await chrome.storage.local.get(STORAGE_KEYS.OBSERVATIONS);
  const list: ObservationRecord[] = Array.isArray(res[STORAGE_KEYS.OBSERVATIONS])
    ? (res[STORAGE_KEYS.OBSERVATIONS] as ObservationRecord[])
    : [];

  const failedIndexes = list
    .map((r, i) => (r.uploadStatus === 'failed' ? i : -1))
    .filter((i) => i >= 0);

  let succeeded = 0;
  let failed = 0;
  let changed = false;
  for (const i of failedIndexes) {
    const record = list[i];
    const payload = mapObservationToBackend(record, chrome.runtime.getManifest().version);
    // 存量无价格记录（旧版本可能已存本地）：重发必被后端 422，直接改标 skipped_no_price
    if (payload.display_price_cents === null) {
      list[i] = {
        ...record,
        uploadStatus: 'skipped_no_price',
        uploadError: '未抓取到价格，已取消上报。页面可能未加载完成或选择器失效，请刷新重试',
      };
      failed++;
      changed = true;
      continue;
    }
    const upload = await uploadObservation(settings, payload);
    if (upload.status === 'success') {
      const updated: ObservationRecord = {
        ...record,
        uploadStatus: 'success',
        observationId: upload.observationId ?? record.observationId,
      };
      delete updated.uploadError; // 成功即清除旧的错误信息
      if (upload.warnings && upload.warnings.length > 0) updated.uploadWarnings = upload.warnings;
      list[i] = updated;
      succeeded++;
    } else {
      list[i] = { ...record, uploadStatus: 'failed', uploadError: upload.error };
      failed++;
    }
    changed = true;
  }
  if (changed) {
    await chrome.storage.local.set({ [STORAGE_KEYS.OBSERVATIONS]: list });
  }
  return { retried: failedIndexes.length, succeeded, failed };
}

// ===== 采集流水线（手动 / 自动共用） =====

/**
 * @param trigger manual=用户点击触发；auto=商品页自动触发。
 *                auto 场景无用户手势，截图大概率因权限不足失败，
 *                走 screenshotError 降级即可，不影响其余字段。
 */
async function collectAndUpload(
  tab: chrome.tabs.Tab,
  trigger: 'manual' | 'auto',
  settings: ExtensionSettings,
): Promise<CollectionResult> {
  // 1. 让 content script 提取页面数据
  let page: ExtractedPageData;
  try {
    const resp = await chrome.tabs.sendMessage(tab.id as number, { type: MSG.EXTRACT_PAGE_DATA });
    if (!resp?.ok) return { ok: false, error: resp?.error ?? '页面数据提取失败' };
    page = resp.data as ExtractedPageData;
  } catch (e) {
    return { ok: false, error: `无法与页面通信（请确认当前是受支持平台的商品详情页，且页面已加载完成）：${errMsg(e)}` };
  }

  // 2. 截图（PNG dataUrl）
  // manual：popup / 提示条点击构成用户手势，配合 activeTab 权限与站点 host 权限可用；
  // auto：无用户手势，可能失败；失败时降级为无截图并在记录里标注 screenshotError。
  let screenshotDataUrl: string | null = null;
  let screenshotError: string | undefined;
  try {
    screenshotDataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, { format: 'png' });
  } catch (e) {
    screenshotError = errMsg(e);
  }

  // 3. 公网 IP 与城市（5 秒超时，失败降级为 null 并标注）
  const network = await lookupIpCity();

  // 4. 匿名用户 ID（首次使用生成 crypto.randomUUID() 并持久化）
  const anonymousUserId = await ensureAnonymousUserId();

  // 5. 组装完整观测记录（UTC ISO 时间戳）
  const record: ObservationRecord = {
    recordId: crypto.randomUUID(),
    anonymousUserId,
    collectedAt: new Date().toISOString(),
    platform: page.platform,
    productId: page.productId,
    productName: page.productName,
    shopName: page.shopName,
    shopId: page.shopId,
    productUrl: page.productUrl,
    price: page.price,
    userContext: {
      isLoggedIn: page.userContext.isLoggedIn,
      memberLevel: page.userContext.memberLevel,
      isNewUser: page.userContext.isNewUser,
      userMarkerMasked: page.userContext.userMarker, // 暂存原文，sanitize 时按设置打码
      evidence: page.userContext.evidence,
    },
    device: page.device,
    network,
    shipping: page.shipping,
    screenshotDataUrl,
    screenshotError,
    domSnapshots: page.domSnapshots,
    extractionMeta: page.extractionMeta,
    uploadStatus: 'pending',
    observationId: null,
  };

  // 6. 本地脱敏（白名单字段过滤，见 sanitizeRecord 注释）
  const safe = sanitizeRecord(record, settings);

  // 7. 映射为后端扁平 schema 并上报（失败不阻断本地留存）
  //    source_code_version 取自扩展 manifest 版本号
  const backendPayload = mapObservationToBackend(safe, chrome.runtime.getManifest().version);
  // 本地上报前校验：原价（display_price_cents）为 null 说明页面价格抓空，
  // 直接上报会被后端 422 拒绝，无意义——跳过上报并标注 skipped_no_price。
  // 到手价为 null 不阻断（无优惠商品原价即可分析）。
  if (backendPayload.display_price_cents === null) {
    safe.uploadStatus = 'skipped_no_price';
    safe.uploadError = '未抓取到价格，已取消上报。页面可能未加载完成或选择器失效，请刷新重试';
  } else {
    const upload = await uploadObservation(settings, backendPayload);
    safe.uploadStatus = upload.status;
    if (upload.observationId !== undefined) safe.observationId = upload.observationId;
    if (upload.error) safe.uploadError = upload.error;
    if (upload.warnings && upload.warnings.length > 0) safe.uploadWarnings = upload.warnings;
  }

  // 8. 本地留存（上限 MAX_LOCAL_RECORDS 条滚动删除；配额不足时降级去掉本地截图副本）
  await persistRecord(safe);

  // 9. 记录最近一次结果，供 popup 展示
  const result: CollectionResult = {
    ok: true,
    recordId: safe.recordId,
    platform: safe.platform,
    uploadStatus: safe.uploadStatus,
    uploadError: safe.uploadError,
    observationId: safe.observationId,
    warningCount: safe.uploadWarnings?.length ?? 0,
    collectedAt: safe.collectedAt,
  };
  await chrome.storage.local.set({ [STORAGE_KEYS.LAST_RESULT]: result });
  return result;
}

// ===== 设置与状态 =====

async function getSettings(): Promise<ExtensionSettings> {
  const res = await chrome.storage.local.get([
    STORAGE_KEYS.CONSENT,
    STORAGE_KEYS.AUTO_COLLECT,
    STORAGE_KEYS.API_ENDPOINT,
    STORAGE_KEYS.API_KEY,
    STORAGE_KEYS.MASK_SHOP,
    STORAGE_KEYS.MASK_USER,
  ]);
  return {
    consent: res[STORAGE_KEYS.CONSENT] === true,
    autoCollect: res[STORAGE_KEYS.AUTO_COLLECT] === true, // 默认关闭
    apiEndpoint:
      typeof res[STORAGE_KEYS.API_ENDPOINT] === 'string' && res[STORAGE_KEYS.API_ENDPOINT]
        ? res[STORAGE_KEYS.API_ENDPOINT]
        : DEFAULT_API_ENDPOINT,
    apiKey:
      typeof res[STORAGE_KEYS.API_KEY] === 'string' && res[STORAGE_KEYS.API_KEY]
        ? res[STORAGE_KEYS.API_KEY]
        : DEFAULT_API_KEY,
    maskShopName: res[STORAGE_KEYS.MASK_SHOP] !== false, // 默认开启脱敏
    maskUserMarker: res[STORAGE_KEYS.MASK_USER] !== false, // 默认开启脱敏
  };
}

async function getActiveTab(): Promise<chrome.tabs.Tab | undefined> {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

/** 匿名用户 ID：首次使用生成 uuid 并持久化，不含任何注册信息 */
async function ensureAnonymousUserId(): Promise<string> {
  const res = await chrome.storage.local.get(STORAGE_KEYS.ANON_ID);
  if (typeof res[STORAGE_KEYS.ANON_ID] === 'string' && res[STORAGE_KEYS.ANON_ID]) {
    return res[STORAGE_KEYS.ANON_ID];
  }
  const id = crypto.randomUUID();
  await chrome.storage.local.set({ [STORAGE_KEYS.ANON_ID]: id });
  return id;
}

// ===== 网络环境查询 =====

/** 查询公网 IP 与城市（ipapi.co，5 秒超时；失败降级为全 null 并标注来源说明） */
async function lookupIpCity(): Promise<NetworkInfo> {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 5000);
  try {
    const resp = await fetch('https://ipapi.co/json/', { signal: ctrl.signal });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const j = (await resp.json()) as Record<string, unknown>;
    const str = (v: unknown): string | null => (typeof v === 'string' && v ? v : null);
    return {
      ip: str(j.ip),
      city: str(j.city),
      region: str(j.region),
      country: str(j.country) ?? str(j.country_name),
      source: 'ipapi.co',
    };
  } catch (e) {
    return {
      ip: null,
      city: null,
      region: null,
      country: null,
      source: `ipapi.co 查询失败（已降级为 null）：${errMsg(e)}`,
    };
  } finally {
    clearTimeout(timer);
  }
}

// ===== 脱敏 =====

/**
 * 【隐私关键】白名单脱敏过滤
 * 逐字段显式拷贝，任何未列出的字段都不会进入最终记录；
 * 本扩展从不读取 cookie 值 / localStorage，此处再做一次结构级兜底。
 * 店铺名 / 用户标识按设置做「张*」式打码。
 */
function sanitizeRecord(r: ObservationRecord, s: ExtensionSettings): ObservationRecord {
  const safe: ObservationRecord = {
    recordId: r.recordId,
    anonymousUserId: r.anonymousUserId,
    collectedAt: r.collectedAt,
    platform: r.platform,
    productId: r.productId,
    productName: r.productName,
    shopName: r.shopName && s.maskShopName ? maskText(r.shopName) : r.shopName,
    shopId: r.shopId,
    productUrl: r.productUrl,
    price: {
      original: r.price.original,
      final: r.price.final,
      currency: r.price.currency,
      couponAmount: r.price.couponAmount,
      couponType: r.price.couponType,
    },
    userContext: {
      isLoggedIn: r.userContext.isLoggedIn,
      memberLevel: r.userContext.memberLevel,
      isNewUser: r.userContext.isNewUser,
      userMarkerMasked:
        r.userContext.userMarkerMasked && s.maskUserMarker
          ? maskText(r.userContext.userMarkerMasked)
          : r.userContext.userMarkerMasked,
      evidence: r.userContext.evidence,
    },
    device: {
      userAgent: r.device.userAgent,
      screenResolution: r.device.screenResolution,
      deviceMemory: r.device.deviceMemory,
      hardwareConcurrency: r.device.hardwareConcurrency,
      platform: r.device.platform,
      language: r.device.language,
      devicePriceIndex: r.device.devicePriceIndex,
    },
    network: {
      ip: r.network.ip,
      city: r.network.city,
      region: r.network.region,
      country: r.network.country,
      source: r.network.source,
    },
    shipping: {
      shipFromCity: r.shipping.shipFromCity,
      shipFromCityNormalized: r.shipping.shipFromCityNormalized ?? null,
    },
    screenshotDataUrl: r.screenshotDataUrl,
    domSnapshots: r.domSnapshots.map((d) => ({ field: d.field, outerHTML: d.outerHTML })),
    uploadStatus: r.uploadStatus,
    observationId: r.observationId,
  };
  if (r.extractionMeta) safe.extractionMeta = { ...r.extractionMeta };
  if (r.screenshotError) safe.screenshotError = r.screenshotError;
  return safe;
}

// ===== 上报 =====

/**
 * POST 上报到配置的后端 API（10 秒超时；失败仅标记，本地留存兜底）。
 * 载荷为后端扁平 schema（BackendObservationPayload），鉴权头 X-API-Key。
 * 本地后端默认 http://127.0.0.1:8000（manifest 已加 127.0.0.1/localhost host 权限）；
 * 若改用其他域名，需把该域名加入 manifest 的 host_permissions 后重新构建，
 * 或由后端响应头 Access-Control-Allow-Origin 放行扩展来源。
 */
async function uploadObservation(
  settings: ExtensionSettings,
  payload: BackendObservationPayload,
): Promise<{ status: UploadStatus; observationId?: string | null; warnings?: string[]; error?: string }> {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 10_000);
  try {
    const resp = await fetch(settings.apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 本地 FastAPI 后端鉴权头（默认 dev-key-123，可在 options 页修改）
        'X-API-Key': settings.apiKey,
      },
      body: JSON.stringify(payload),
      signal: ctrl.signal,
    });
    if (!resp.ok) {
      // 提取后端返回的具体错误（FastAPI 422 的 detail 等），便于 popup 展示
      let detail = '';
      try {
        const errBody = (await resp.json()) as { detail?: unknown };
        if (errBody && errBody.detail !== undefined) {
          detail = typeof errBody.detail === 'string' ? errBody.detail : JSON.stringify(errBody.detail);
        }
      } catch {
        // 错误响应无 JSON body 时仅保留状态码
      }
      throw new Error(`HTTP ${resp.status}${detail ? `：${detail}` : ''}`);
    }
    // 后端返回 {"observation_id","created_at","warnings"}；兼容驼峰写法
    const body = (await resp.json().catch(() => ({}))) as {
      observation_id?: string;
      observationId?: string;
      id?: string;
      warnings?: unknown;
    };
    const warnings = Array.isArray(body.warnings) ? body.warnings.map((w) => String(w)) : [];
    return {
      status: 'success',
      observationId: body.observation_id ?? body.observationId ?? body.id ?? null,
      warnings,
    };
  } catch (e) {
    return { status: 'failed', error: translateUploadError(e, settings.apiEndpoint) };
  } finally {
    clearTimeout(timer);
  }
}

/**
 * 把底层错误翻译成用户可执行的中文提示：
 * - TypeError / Failed to fetch：后端未启动或网络不通（最常见：用户曾在后端未启动时采集）；
 * - AbortError：10 秒超时；
 * - 其余原样返回（已含 HTTP 状态码与后端 detail）。
 */
function translateUploadError(e: unknown, endpoint: string): string {
  const msg = errMsg(e);
  let origin = endpoint;
  try {
    origin = new URL(endpoint).origin;
  } catch {
    // 端点格式异常时保留原文
  }
  if (e instanceof TypeError || /failed to fetch|networkerror/i.test(msg)) {
    return `无法连接 ${origin}（后端未启动或网络不通），请先双击 启动本地服务.bat 启动后端`;
  }
  if ((e instanceof DOMException && e.name === 'AbortError') || /abort/i.test(msg)) {
    return `连接后端超时（10 秒无响应），请确认后端正常运行：${endpoint}`;
  }
  return msg;
}

// ===== 本地留存 =====

/**
 * 本地留存：上限 MAX_LOCAL_RECORDS 条，溢出滚动删除最早记录。
 * chrome.storage.local 默认配额约 10MB，全屏 PNG dataUrl 较占空间；
 * 配额不足时先去掉本地副本中的截图（上报载荷不受影响），仍超限则继续删最早记录。
 */
async function persistRecord(record: ObservationRecord): Promise<void> {
  const key = STORAGE_KEYS.OBSERVATIONS;
  const res = await chrome.storage.local.get(key);
  const list: ObservationRecord[] = Array.isArray(res[key]) ? res[key] : [];
  list.unshift(record);
  while (list.length > MAX_LOCAL_RECORDS) list.pop();

  try {
    await chrome.storage.local.set({ [key]: list });
    return;
  } catch {
    list[0] = {
      ...record,
      screenshotDataUrl: null,
      screenshotError: `${record.screenshotError ? `${record.screenshotError}；` : ''}本地留存因配额限制未保存截图`,
    };
  }
  while (list.length > 0) {
    try {
      await chrome.storage.local.set({ [key]: list });
      return;
    } catch {
      list.pop();
    }
  }
}
