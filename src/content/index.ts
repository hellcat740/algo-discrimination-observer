/**
 * 内容脚本：运行于受支持电商平台的商品详情页
 * 职责：
 *  1. 命中平台规则且是商品详情页时，按授权状态决定是否注入提示条（Shadow DOM 隔离样式）
 *  2. 响应 background 的 EXTRACT_PAGE_DATA 消息（提取逻辑在 ../shared/extract.ts，与页面探针复用）
 *  3. 商品页自动采集：用户已授权（consent=true）且开关打开（autoCollect=true）时，
 *     进入商品详情页自动触发 AUTO_COLLECT，无需手动点工具栏按钮；
 *     兼容 SPA 前端路由（pushState/replaceState/popstate + URL 轮询），
 *     同一次页面会话内同一 productId 只触发一次，background 侧另有 10 分钟跨页面去重。
 *
 * 隐私前提：自动采集只在已获得用户明确授权（consent）后发生；未授权或开关关闭时
 * 行为与旧版完全一致（仅提示条，不会自动采集）。
 */
import { MSG, STORAGE_KEYS } from '../types';
import type {
  AutoCollectPayload,
  CollectionResult,
  ExtensionMessage,
  StartCollectionPayload,
} from '../types';
import { extractProductId, findPlatformRule } from '../platforms';
import { extractPageData } from '../shared/extract';
import type { ExtractedPageData } from '../types';
import { errMsg, escapeHtml } from '../utils';

const BANNER_HOST_ID = '__algo_obs_banner_host__';
const TOAST_HOST_ID = '__algo_obs_toast_host__';

/** 本次页面会话内已触发过自动采集的商品 ID（内存去重；跨页面去重由 background 负责） */
const triggeredProductIds = new Set<string>();

// ===== 初始化：检测 + SPA 路由监听 =====
(function init(): void {
  detectAndAct();
  watchSpaNavigation();
})();

/** 检测当前页：是商品详情页则按授权/开关状态执行提示条或自动采集 */
function detectAndAct(): void {
  const rule = findPlatformRule(window.location.hostname);
  if (!rule) return;
  const productId = extractProductId(rule, window.location.href);
  if (!productId) return; // 只有能提取到商品 ID 的详情页才处理

  chrome.storage.local.get([STORAGE_KEYS.CONSENT, STORAGE_KEYS.AUTO_COLLECT], (res) => {
    const consent = res[STORAGE_KEYS.CONSENT] === true;
    const autoCollect = res[STORAGE_KEYS.AUTO_COLLECT] === true;

    if (!consent) {
      injectBanner(); // 未授权：维持原有提示条逻辑（重复注入由 injectBanner 内部去重）
      return;
    }
    // 隐私前提：自动采集必须已授权且开关打开
    if (autoCollect && !triggeredProductIds.has(productId)) {
      triggeredProductIds.add(productId);
      void triggerAutoCollect(productId);
    }
    // 已授权但未开自动采集：静默，由用户点工具栏按钮手动采集
  });
}

/** 触发一次自动采集；成功弹 toast，失败静默不打扰 */
async function triggerAutoCollect(productId: string): Promise<void> {
  try {
    // 时机保护：页面资源未加载完时先等 window load（最多 3 秒兜底），
    // 避免在价格模块仍处于状态A（简化渲染）的早期就触发提取
    if (document.readyState !== 'complete') {
      await new Promise<void>((resolve) => {
        const timer = window.setTimeout(resolve, 3000);
        window.addEventListener(
          'load',
          () => {
            window.clearTimeout(timer);
            resolve();
          },
          { once: true },
        );
      });
    }
    const payload: AutoCollectPayload = { productId };
    const result = (await chrome.runtime.sendMessage({
      type: MSG.AUTO_COLLECT,
      payload,
    })) as CollectionResult;
    if (result?.ok) {
      showToast('✅ 已自动采集本页观测数据');
    }
    // 失败（含 10 分钟去重跳过、截图降级失败等）：静默不打扰
  } catch {
    // 与 background 通信失败：静默不打扰
  }
}

// ===== SPA 兼容：捕获前端路由跳转，URL 变化后延迟 2 秒等 DOM 稳定再重新检测 =====

let detectTimer: number | null = null;

function scheduleDetect(): void {
  if (detectTimer !== null) window.clearTimeout(detectTimer);
  detectTimer = window.setTimeout(() => detectAndAct(), 2000);
}

function watchSpaNavigation(): void {
  // 包装 history.pushState / replaceState（淘宝/京东部分页面为前端路由，不触发整页刷新）
  const wrap =
    (orig: History['pushState']) =>
    function (this: History, ...args: Parameters<History['pushState']>): void {
      orig.apply(this, args);
      scheduleDetect();
    };
  history.pushState = wrap(history.pushState);
  history.replaceState = wrap(history.replaceState);
  window.addEventListener('popstate', () => scheduleDetect());

  // URL 轮询兜底：1.5s 比对 location.href，覆盖不走上述钩子的路由实现
  let lastUrl = window.location.href;
  window.setInterval(() => {
    if (window.location.href !== lastUrl) {
      lastUrl = window.location.href;
      scheduleDetect();
    }
  }, 1500);
}

// ===== 响应 background 的提取请求 =====

/**
 * 提取（等待完整价格模块）：2025 版详情页价格模块异步注水，
 * 存在「状态A（简化渲染）→ 状态B（完整渲染）」的过渡。
 *
 * 淘系（taobao/tmall）：状态A 的 block2-- 单价格 / 早期 JSON 回退值可能是
 * 过渡态或无关数值（真实案例：自动采集抓到 48 元，同页手动采集为 1029/528.84）。
 * 因此轮询期间只要 highlightPrice--/subPrice-- 容器未出现就继续等（20×500ms≈10 秒），
 * 即使 block2/JSON 已给出价格；容器出现（状态B）才立即返回——双价归属语义由
 * extract.ts 现有逻辑处理。超时才接受 block2-- 单价格或 JSON 回退结果
 * （页面可能真的只有状态A）；超时仍无价格按 null 返回（走「价格为 null 不上报」）。
 *
 * 其他平台（京东等）：维持原逻辑，任一价格非 null 即返回（16×500ms≈8 秒）。
 */
async function extractWithPriceWait(): Promise<ExtractedPageData | null> {
  const FULL_PRICE_SELECTOR = '[class*="highlightPrice--"], [class*="subPrice--"]';
  const rule = findPlatformRule(window.location.hostname);
  const isTaoFamily = rule?.id === 'taobao' || rule?.id === 'tmall';
  const MAX_TRIES = isTaoFamily ? 20 : 16;
  let data = extractPageData();
  for (let i = 0; i < MAX_TRIES && data !== null; i++) {
    if (isTaoFamily) {
      if (document.querySelector(FULL_PRICE_SELECTOR)) return data; // 状态B 完整价格模块已渲染
    } else if (data.price.original !== null || data.price.final !== null) {
      return data;
    }
    await new Promise((r) => window.setTimeout(r, 500));
    data = extractPageData();
  }
  return data; // 超时：接受状态A/JSON 结果（可能为 null）
}

chrome.runtime.onMessage.addListener((message: ExtensionMessage, _sender, sendResponse) => {
  if (message?.type !== MSG.EXTRACT_PAGE_DATA) return false;
  void (async () => {
    try {
      const data = await extractWithPriceWait();
      if (!data) {
        sendResponse({ ok: false, error: '当前页未识别为受支持的商品详情页' });
      } else {
        sendResponse({ ok: true, data });
      }
    } catch (e) {
      sendResponse({ ok: false, error: `页面数据提取异常：${errMsg(e)}` });
    }
  })();
  return true; // 异步响应
});

// ===== 自动采集成功 toast（右上角 3 秒自动消失，Shadow DOM 隔离样式） =====

function showToast(text: string): void {
  document.getElementById(TOAST_HOST_ID)?.remove();
  const host = document.createElement('div');
  host.id = TOAST_HOST_ID;
  host.style.cssText = 'position:fixed;top:12px;right:12px;z-index:2147483647;';
  const shadow = host.attachShadow({ mode: 'open' });
  shadow.innerHTML = `
    <style>
      .toast { padding:8px 14px; background:#166534; color:#fff; border-radius:8px;
               box-shadow:0 2px 10px rgba(0,0,0,.3);
               font:13px/1.5 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }
    </style>
    <div class="toast">${escapeHtml(text)}</div>`;
  (document.body ?? document.documentElement).appendChild(host);
  window.setTimeout(() => host.remove(), 3000);
}

// ===== 顶部提示条（Shadow DOM 隔离页面样式） =====

function injectBanner(): void {
  if (document.getElementById(BANNER_HOST_ID)) return;
  const host = document.createElement('div');
  host.id = BANNER_HOST_ID;
  // 宿主节点用内联样式固定定位，避免被页面布局影响
  host.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:2147483647;';
  const shadow = host.attachShadow({ mode: 'open' });
  shadow.innerHTML = `
    <style>
      .bar { display:flex; align-items:center; gap:8px; padding:8px 14px; flex-wrap:wrap;
             background:#1e293b; color:#f8fafc; box-shadow:0 2px 8px rgba(0,0,0,.25);
             font:13px/1.5 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }
      .txt { flex:1; min-width:220px; }
      button { border:none; border-radius:6px; padding:5px 12px; font-size:13px; cursor:pointer; }
      button:disabled { opacity:.6; cursor:default; }
      .agree { background:#4f46e5; color:#fff; }
      .once { background:#0ea5e9; color:#fff; }
      .dismiss { background:transparent; color:#94a3b8; }
      .ok { color:#4ade80; }
      .err { color:#f87171; }
    </style>
    <div class="bar">
      <span class="txt">🔍 算法歧视众包观测：是否为本页面贡献一条算法比价观测数据？仅采集页面公开价格信息，不含账号密码与 cookie 值。</span>
      <button class="agree" data-act="consent">同意并采集</button>
      <button class="once" data-act="once">仅本次采集</button>
      <button class="dismiss" data-act="dismiss">忽略</button>
    </div>`;
  (document.body ?? document.documentElement).appendChild(host);
  shadow.querySelectorAll('button').forEach((btn) => {
    btn.addEventListener('click', () => {
      const act = (btn as HTMLElement).dataset.act ?? '';
      void onBannerAction(shadow, act);
    });
  });
}

async function onBannerAction(shadow: ShadowRoot, act: string): Promise<void> {
  const host = document.getElementById(BANNER_HOST_ID);
  if (act === 'dismiss') {
    host?.remove();
    return;
  }
  if (act === 'consent') {
    // 「同意并采集」：写入持久授权，以后商品页不再提示
    await chrome.storage.local.set({ [STORAGE_KEYS.CONSENT]: true });
  }
  const bar = shadow.querySelector('.bar');
  const txt = shadow.querySelector('.txt');
  bar?.querySelectorAll('button').forEach((b) => {
    (b as HTMLButtonElement).disabled = true;
  });
  if (txt) txt.textContent = '正在采集本页观测数据…';
  const payload: StartCollectionPayload = { onceOnly: act === 'once' };
  try {
    const result = (await chrome.runtime.sendMessage({
      type: MSG.START_COLLECTION,
      payload,
    })) as CollectionResult;
    if (txt) {
      txt.innerHTML = result.ok
        ? `<span class="ok">✓ 已采集（${formatUploadStatus(result)}），感谢参与！</span>`
        : `<span class="err">✗ 采集失败：${escapeHtml(result.error ?? '未知错误')}</span>`;
    }
  } catch (e) {
    if (txt) txt.innerHTML = `<span class="err">✗ 采集失败：${escapeHtml(errMsg(e))}</span>`;
  }
  window.setTimeout(() => host?.remove(), 4000);
}

/** 上报状态文案：有后端清洗提示时带条数 */
function formatUploadStatus(result: CollectionResult): string {
  if (result.uploadStatus === 'success') {
    const n = result.warningCount ?? 0;
    return n > 0 ? `已上报（${n} 条清洗提示）` : '已上报';
  }
  return '已存本地，待重试';
}
