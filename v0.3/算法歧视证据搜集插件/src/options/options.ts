/**
 * 设置页：数据用途说明、授权开关、上报配置、脱敏选项、历史记录管理
 */
import { DEFAULT_API_ENDPOINT, DEFAULT_API_KEY, STORAGE_KEYS } from '../types';
import type { ObservationRecord } from '../types';
import { errMsg, escapeHtml } from '../utils';

function $(id: string): HTMLElement {
  const el = document.getElementById(id);
  if (!el) throw new Error(`缺少节点 #${id}`);
  return el;
}
const $input = (id: string): HTMLInputElement => $(id) as HTMLInputElement;

async function load(): Promise<void> {
  const res = await chrome.storage.local.get([
    STORAGE_KEYS.CONSENT,
    STORAGE_KEYS.AUTO_COLLECT,
    STORAGE_KEYS.API_ENDPOINT,
    STORAGE_KEYS.API_KEY,
    STORAGE_KEYS.MASK_SHOP,
    STORAGE_KEYS.MASK_USER,
    STORAGE_KEYS.OBSERVATIONS,
  ]);
  $input('ck-consent').checked = res[STORAGE_KEYS.CONSENT] === true;
  $input('ck-auto-collect').checked = res[STORAGE_KEYS.AUTO_COLLECT] === true;
  $input('inp-endpoint').value =
    typeof res[STORAGE_KEYS.API_ENDPOINT] === 'string' && res[STORAGE_KEYS.API_ENDPOINT]
      ? res[STORAGE_KEYS.API_ENDPOINT]
      : DEFAULT_API_ENDPOINT;
  $input('inp-apikey').value =
    typeof res[STORAGE_KEYS.API_KEY] === 'string' && res[STORAGE_KEYS.API_KEY]
      ? res[STORAGE_KEYS.API_KEY]
      : DEFAULT_API_KEY;
  // 脱敏选项默认开启（未显式设置为 false 即为开启）
  $input('ck-mask-shop').checked = res[STORAGE_KEYS.MASK_SHOP] !== false;
  $input('ck-mask-user').checked = res[STORAGE_KEYS.MASK_USER] !== false;
  renderHistory(
    Array.isArray(res[STORAGE_KEYS.OBSERVATIONS]) ? (res[STORAGE_KEYS.OBSERVATIONS] as ObservationRecord[]) : [],
  );
}

async function save(): Promise<void> {
  await chrome.storage.local.set({
    [STORAGE_KEYS.CONSENT]: $input('ck-consent').checked,
    [STORAGE_KEYS.AUTO_COLLECT]: $input('ck-auto-collect').checked,
    [STORAGE_KEYS.API_ENDPOINT]: $input('inp-endpoint').value.trim() || DEFAULT_API_ENDPOINT,
    [STORAGE_KEYS.API_KEY]: $input('inp-apikey').value.trim() || DEFAULT_API_KEY,
    [STORAGE_KEYS.MASK_SHOP]: $input('ck-mask-shop').checked,
    [STORAGE_KEYS.MASK_USER]: $input('ck-mask-user').checked,
  });
  const hint = $('saved-hint');
  hint.textContent = '✓ 已保存';
  window.setTimeout(() => {
    hint.textContent = '';
  }, 2000);
}

function renderHistory(list: ObservationRecord[]): void {
  $('history-count').textContent = `本地共 ${list.length} 条观测记录（最多保留 500 条，溢出滚动删除最早记录）`;
  if (list.length === 0) {
    $('history-list').innerHTML = '<div class="muted">暂无记录</div>';
    return;
  }
  const rows = list
    .slice(0, 10)
    .map((r) => {
      const time = new Date(r.collectedAt).toLocaleString('zh-CN');
      const status =
        r.uploadStatus === 'success'
          ? '✅ 已上报'
          : r.uploadStatus === 'failed'
            ? '⚠️ 上报失败'
            : r.uploadStatus === 'skipped_no_price'
              ? '⏭️ 无价格未上报'
              : '⏳ 待上报';
      return `<div class="row">${escapeHtml(time)} · ${escapeHtml(r.platform)} · ${escapeHtml(
        r.productName ?? '(未取到商品名)',
      )} · ${status}</div>`;
    })
    .join('');
  $('history-list').innerHTML =
    rows + (list.length > 10 ? `<div class="muted">… 其余 ${list.length - 10} 条见「数据报告」页</div>` : '');
}

async function clearHistory(): Promise<void> {
  if (!window.confirm('确定清空全部历史观测记录吗？该操作不可恢复。')) return;
  await chrome.storage.local.set({ [STORAGE_KEYS.OBSERVATIONS]: [] });
  renderHistory([]);
}

function main(): void {
  void load();
  $('btn-save').addEventListener('click', () => void save().catch((e) => window.alert(errMsg(e))));
  // 授权与自动采集开关即时生效，不必等「保存设置」
  $('ck-consent').addEventListener('change', () => void save());
  $('ck-auto-collect').addEventListener('change', () => void save());
  $('btn-clear').addEventListener('click', () => void clearHistory());

  // 与弹窗内的开关保持同步（任一处修改，另一处即时刷新）
  chrome.storage.onChanged.addListener((changes, area) => {
    if (area !== 'local') return;
    if (STORAGE_KEYS.CONSENT in changes) {
      $input('ck-consent').checked = changes[STORAGE_KEYS.CONSENT].newValue === true;
    }
    if (STORAGE_KEYS.AUTO_COLLECT in changes) {
      $input('ck-auto-collect').checked = changes[STORAGE_KEYS.AUTO_COLLECT].newValue === true;
    }
  });
}

main();
