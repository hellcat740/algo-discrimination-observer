// dist 产物核验脚本：
//  1. manifest.json 中引用的文件是否全部存在
//  2. content script 产物是否为纯 IIFE（顶层无 import/export 语句，Chrome MV3 硬性要求）
//  3. service worker 是否以 module 类型声明
// 用法：npm run verify（需先 npm run build）
import { readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');
let fail = 0;
const check = (ok, label) => {
  console.log(`${ok ? 'OK  ' : 'FAIL'} ${label}`);
  if (!ok) fail++;
};

if (!existsSync(join(dist, 'manifest.json'))) {
  console.error('FAIL dist/manifest.json 不存在，请先运行 npm run build');
  process.exit(1);
}

const manifest = JSON.parse(readFileSync(join(dist, 'manifest.json'), 'utf8'));
const refs = new Set(
  [
    manifest.action?.default_popup,
    manifest.options_page,
    manifest.background?.service_worker,
    ...(manifest.content_scripts ?? []).flatMap((c) => c.js ?? []),
    ...(manifest.web_accessible_resources ?? []).flatMap((w) => w.resources ?? []),
    ...Object.values(manifest.icons ?? {}),
    ...Object.values(manifest.action?.default_icon ?? {}),
  ].filter(Boolean),
);
for (const p of refs) {
  check(existsSync(join(dist, p)), `manifest 引用文件存在：${p}`);
}

// content script 必须是 IIFE：顶层不得出现 import/export 语句
const contentPath = join(dist, 'content/index.js');
if (existsSync(contentPath)) {
  const content = readFileSync(contentPath, 'utf8');
  check(!/^\s*import\s/m.test(content), 'content/index.js 无顶层 import 语句');
  check(!/^\s*export\s/m.test(content), 'content/index.js 无顶层 export 语句');
  check(/^\s*var\s+\w+\s*=\s*\(?function|^\s*\(function/.test(content), 'content/index.js 为 IIFE 形态');
}

// service worker 声明为 module
check(manifest.background?.type === 'module', 'manifest background.type = "module"');

// popup / options / report 的 HTML 引用的脚本文件存在
for (const html of ['popup/popup.html', 'options/options.html', 'report/report.html']) {
  const htmlPath = join(dist, html);
  if (!existsSync(htmlPath)) continue;
  const text = readFileSync(htmlPath, 'utf8');
  for (const m of text.matchAll(/src="([^"]+\.js)"/g)) {
    // 以 / 开头视为相对 dist 根目录，否则相对 HTML 所在目录
    const scriptPath = m[1].startsWith('/')
      ? join(dist, m[1].slice(1))
      : join(dist, dirname(html), m[1]);
    check(existsSync(scriptPath), `${html} 引用的脚本存在：${m[1]}`);
  }
}

console.log(fail === 0 ? '\n全部核验通过 ✅' : `\n${fail} 项核验失败 ❌`);
process.exit(fail ? 1 : 0);
