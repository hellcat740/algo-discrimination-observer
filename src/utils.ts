/** 通用小工具：错误消息提取、HTML 转义、文本打码 */

/** 把 unknown 异常转成可读消息 */
export function errMsg(e: unknown): string {
  return e instanceof Error ? e.message : String(e);
}

/** HTML 转义，防止页面文本注入破坏报告页结构 */
export function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/** 文本打码：保留首字符，其余替换为 *，如「张*」（昵称 / 店铺名脱敏用） */
export function maskText(text: string): string {
  const t = text.trim();
  if (!t) return t;
  return `${t[0]}*`;
}
