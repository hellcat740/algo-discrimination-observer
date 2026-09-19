/**
 * 弹窗页：当前页识别状态、授权状态、采集按钮、最近一次采集结果
 */
import { DEFAULT_API_ENDPOINT, MSG, STORAGE_KEYS } from '../types';
import type { CollectionResult, ObservationRecord, RetryResult, TestConnectionResult } from '../types';
import { extractProductId, findPlatformRule } from '../platforms';
import { errMsg, escapeHtml } from '../utils';

function $(id: string): HTMLElement {
  const el = document.getElementById(id);
  if (!el) throw new Error(`缺少节点 #${id}`);
  return el;
}

async function getActiveTab(): Promise<chrome.tabs.Tab | undefined> {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

/** 判断当前页是否为受支持平台的商品详情页 */
function describePage(url: string | undefined): string {
  if (!url) return '无法读取当前页地址';
  try {
    const u = new URL(url);
    const rule = findPlatformRule(u.hostname);
    if (!rule) return '非受支持平台（支持：淘宝 / 天猫 / 京东 / 拼多多）';
    const pid = extractProductId(rule, u.href);
    if (!pid) return `已识别平台「${rule.name}」，但当前不是商品详情页`;
    return `${rule.name} 商品页（商品 ID：${pid}）`;
  } catch {
    return '无法解析当前页地址';
  }
}

function renderConsent(consent: boolean): void {
  $('consent-status').innerHTML = consent
    ? '<span class="badge ok">已授权参与</span>'
    : '<span class="badge no">未授权</span>';
  $('consent-panel').hidden = consent;
}

/** 自动采集开关渲染：未授权时禁用并提示先同意授权 */
function renderAuto(consent: boolean, autoCollect: boolean): void {
  const ck = $('ck-auto') as HTMLInputElement;
  ck.checked = autoCollect;
  ck.disabled = !consent;
  $('auto-row').classList.toggle('off', !consent);
  $('auto-hint').textContent = consent
    ? '进入商品详情页时自动抓取并上报（同一商品 10 分钟内不重复采集）'
    : '需先同意授权后才能开启自动采集';
}

/** 上报状态文案：有后端清洗提示时带条数 */
function formatUploadStatus(result: CollectionResult): string {
  if (result.uploadStatus === 'success') {
    const n = result.warningCount ?? 0;
    return n > 0 ? `已上报（${n} 条清洗提示）` : '已上报';
  }
  if (result.uploadStatus === 'failed') return '上报失败（已存本地）';
  if (result.uploadStatus === 'skipped_no_price') return '未上报（未抓到价格）';
  return '待上报';
}

/** 截断长 ID 便于弹窗展示 */
function truncateId(id: string | null | undefined): string {
  if (!id) return '-';
  return id.length > 16 ? `${id.slice(0, 16)}…` : id;
}

/** 截断过长的端点 URL 便于弹窗展示 */
function truncateEndpoint(endpoint: string): string {
  return endpoint.length > 42 ? `${endpoint.slice(0, 42)}…` : endpoint;
}

function renderLast(result: CollectionResult | undefined): void {
  if (!result) return;
  $('last-card').hidden = false;
  const lines = [
    `时间：${result.collectedAt ? new Date(result.collectedAt).toLocaleString('zh-CN') : '-'}`,
    `状态：${formatUploadStatus(result)}`,
    `本地记录 ID：${truncateId(result.recordId)}`,
    `后端观测 ID：${truncateId(result.observationId)}`,
  ];
  const n = result.warningCount ?? 0;
  if (result.uploadStatus === 'success' && n > 0) {
    lines.push(`清洗提示：${n} 条（详见 report 页记录或后端日志）`);
  }
  if ((result.uploadStatus === 'failed' || result.uploadStatus === 'skipped_no_price') && result.uploadError) {
    // 失败/跳过时展示具体错误（后端 422 detail / 网络错误中文提示 / 未抓到价格提示）
    lines.push(`上报错误：<span style="color:#991b1b">${escapeHtml(result.uploadError)}</span>`);
  }
  $('last-result').innerHTML = lines.join('<br>');
}

/** 统计本地待重试的失败记录数并刷新重试卡片（N=0 时隐藏） */
async function refreshRetryCount(): Promise<void> {
  const res = await chrome.storage.local.get(STORAGE_KEYS.OBSERVATIONS);
  const list = (
    Array.isArray(res[STORAGE_KEYS.OBSERVATIONS]) ? res[STORAGE_KEYS.OBSERVATIONS] : []
  ) as ObservationRecord[];
  const n = list.filter((r) => r.uploadStatus === 'failed').length; // skipped_no_price 不参与重试（需回页面重新采集）
  $('retry-card').hidden = n === 0;
  $('retry-count').textContent = String(n);
}

async function main(): Promise<void> {
  const tab = await getActiveTab();
  $('page-status').textContent = describePage(tab?.url);

  const stored = await chrome.storage.local.get([
    STORAGE_KEYS.CONSENT,
    STORAGE_KEYS.AUTO_COLLECT,
    STORAGE_KEYS.LAST_RESULT,
    STORAGE_KEYS.API_ENDPOINT,
  ]);
  let consent = stored[STORAGE_KEYS.CONSENT] === true;
  let autoCollect = stored[STORAGE_KEYS.AUTO_COLLECT] === true;
  renderConsent(consent);
  renderAuto(consent, autoCollect);
  renderLast(stored[STORAGE_KEYS.LAST_RESULT] as CollectionResult | undefined);

  // 自动采集开关（与 options 页读写同一 storage 键）
  $('ck-auto').addEventListener('change', async () => {
    autoCollect = ($('ck-auto') as HTMLInputElement).checked;
    await chrome.storage.local.set({ [STORAGE_KEYS.AUTO_COLLECT]: autoCollect });
  });

  // 与 options 页保持同步（任一处修改，另一处即时刷新）
  chrome.storage.onChanged.addListener((changes, area) => {
    if (area !== 'local') return;
    if (STORAGE_KEYS.CONSENT in changes) {
      consent = changes[STORAGE_KEYS.CONSENT].newValue === true;
      renderConsent(consent);
      renderAuto(consent, autoCollect);
    }
    if (STORAGE_KEYS.AUTO_COLLECT in changes) {
      autoCollect = changes[STORAGE_KEYS.AUTO_COLLECT].newValue === true;
      renderAuto(consent, autoCollect);
    }
    if (STORAGE_KEYS.LAST_RESULT in changes) {
      renderLast(changes[STORAGE_KEYS.LAST_RESULT].newValue as CollectionResult | undefined);
    }
    if (STORAGE_KEYS.OBSERVATIONS in changes) {
      void refreshRetryCount();
    }
  });

  // 打开弹窗时统计失败记录数（有失败记录时提示用户点重试，不做自动静默重试）
  void refreshRetryCount();

  // 重试上报：失败记录用已存数据重新映射 + POST（不重新截图/提取）
  $('btn-retry').addEventListener('click', async () => {
    const btn = $('btn-retry') as HTMLButtonElement;
    const out = $('retry-result');
    btn.disabled = true;
    btn.textContent = '重试中…';
    try {
      const r = (await chrome.runtime.sendMessage({ type: MSG.RETRY_FAILED })) as RetryResult;
      out.textContent = `重试 ${r.retried} 条：成功 ${r.succeeded} 失败 ${r.failed}`;
    } catch (e) {
      out.textContent = `重试失败：${errMsg(e)}`;
    } finally {
      btn.disabled = false;
      btn.textContent = '重试上报';
    }
    await refreshRetryCount();
  });

  // ===== 后端连接区 =====
  const endpoint =
    typeof stored[STORAGE_KEYS.API_ENDPOINT] === 'string' && stored[STORAGE_KEYS.API_ENDPOINT]
      ? stored[STORAGE_KEYS.API_ENDPOINT]
      : DEFAULT_API_ENDPOINT;
  $('endpoint-display').textContent = truncateEndpoint(endpoint);
  // 控制台链接指向 health 同源根路径
  let origin = 'http://127.0.0.1:8000';
  try {
    origin = new URL(endpoint).origin;
  } catch {
    // 端点格式异常时保持默认本地地址
  }
  ($('link-console') as HTMLAnchorElement).href = `${origin}/`;

  $('btn-test-conn').addEventListener('click', async () => {
    const btn = $('btn-test-conn') as HTMLButtonElement;
    const out = $('conn-result');
    btn.disabled = true;
    btn.textContent = '测试中…';
    out.style.display = 'block';
    out.innerHTML = '';
    try {
      const res = (await chrome.runtime.sendMessage({ type: MSG.TEST_CONNECTION })) as TestConnectionResult;
      out.innerHTML = res.ok
        ? `<span style="color:#166534">● ${escapeHtml(res.detail)}</span>`
        : `<span style="color:#991b1b">● ${escapeHtml(res.detail)}</span><br /><span style="color:#6b7280">请先启动后端：cd backend &amp;&amp; uvicorn app.main:app --port 8000</span>`;
    } catch (e) {
      out.innerHTML = `<span style="color:#991b1b">● ${escapeHtml(errMsg(e))}</span>`;
    } finally {
      btn.disabled = false;
      btn.textContent = '测试连接';
    }
  });

  $('btn-consent').addEventListener('click', async () => {
    await chrome.storage.local.set({ [STORAGE_KEYS.CONSENT]: true });
    consent = true;
    renderConsent(true);
    renderAuto(true, autoCollect);
  });

  $('btn-collect').addEventListener('click', async () => {
    if (!consent) {
      // 未授权：先展示授权说明，而不是直接采集
      $('consent-panel').hidden = false;
      return;
    }
    const btn = $('btn-collect') as HTMLButtonElement;
    const out = $('collect-result');
    btn.disabled = true;
    btn.textContent = '采集中…';
    out.style.display = 'block';
    try {
      const result = (await chrome.runtime.sendMessage({
        type: MSG.START_COLLECTION,
        payload: {},
      })) as CollectionResult;
      if (result.ok) {
        if (result.uploadStatus === 'skipped_no_price') {
          // 价格抓空：未上报，提示刷新重试（不参与「待重试」，重发无价格数据无意义）
          out.innerHTML = `<span style="color:#b45309">⚠ 未抓取到价格，已取消上报</span>${
            result.uploadError ? `<br /><span style="color:#991b1b">${escapeHtml(result.uploadError)}</span>` : ''
          }`;
        } else if (result.uploadStatus === 'failed') {
          // 上报失败：展示具体错误（如后端 422 detail、网络错误中文提示）
          out.innerHTML = `<span style="color:#b45309">⚠ 已存本地，待重试</span>${
            result.uploadError ? `<br /><span style="color:#991b1b">${escapeHtml(result.uploadError)}</span>` : ''
          }`;
        } else {
          out.innerHTML = `<span style="color:#166534">✓ 采集完成（${formatUploadStatus(result)}）</span>`;
        }
        renderLast(result);
        void refreshRetryCount();
      } else {
        out.innerHTML = `<span style="color:#991b1b">✗ ${escapeHtml(errMsg(result.error ?? '采集失败'))}</span>`;
      }
    } catch (e) {
      out.innerHTML = `<span style="color:#991b1b">✗ ${errMsg(e)}</span>`;
    } finally {
      btn.disabled = false;
      btn.textContent = '采集本页数据';
    }
  });

  $('link-report').addEventListener('click', () => {
    void chrome.tabs.create({ url: chrome.runtime.getURL('report/report.html') });
  });
  $('link-options').addEventListener('click', () => {
    void chrome.runtime.openOptionsPage();
  });
}

void main();
