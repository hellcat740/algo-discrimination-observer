// 生成浏览器页面探针 dist-test/page-probe.js
// 用 esbuild（vite 自带依赖）把 src/probe/page-probe.ts 连同 platforms.ts、
// shared/extract.ts、shared/backendMapping.ts 打包成一个自包含纯 JS 文件。
//
// 产物形态说明：打包用 ESM 格式（bundle 后实际不含任何 import/export 语句），
// 入口末尾是 async IIFE 表达式语句，因此整个文件的脚本完成值是一个
// Promise<string> —— Runtime.evaluate(expression, awaitPromise:true) 可直接拿到结果。
import { buildSync } from 'esbuild';
import { mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const outFile = join(root, 'dist-test', 'page-probe.js');

mkdirSync(join(root, 'dist-test'), { recursive: true });

buildSync({
  entryPoints: [join(root, 'src', 'probe', 'page-probe.ts')],
  bundle: true,
  format: 'esm', // bundle 后无 import/export；保持顶层语句以保留完成值（iife 格式会丢失完成值）
  platform: 'browser',
  target: 'chrome100',
  minify: false, // 保持可读，便于人工核查探针行为
  outfile: outFile,
  logLevel: 'silent',
});

const code = readFileSync(outFile, 'utf8');
const fail = (msg) => {
  console.error(`FAIL ${msg}`);
  process.exit(1);
};

// 核验 1：产物无 import/export 语句（自包含，可直接 evaluate）
if (/^\s*import\s/m.test(code)) fail('产物含顶层 import 语句');
if (/^\s*export\s/m.test(code)) fail('产物含顶层 export 语句');
// 核验 2：包含淘宝选择器（平台规则确实被打包进来）
if (!code.includes('#J_Title .tb-main-title')) fail('产物缺少淘宝选择器规则');
// 核验 3：包含 POST 上报逻辑与鉴权头
if (!code.includes('http://127.0.0.1:8000/api/observations')) fail('产物缺少上报端点');
if (!code.includes('X-API-Key')) fail('产物缺少 X-API-Key 头');

console.log(`OK   已生成 ${outFile}（${(code.length / 1024).toFixed(1)} KB）`);
console.log('OK   无 import/export 语句，包含淘宝选择器与 POST 上报逻辑');
console.log('用法：在商品详情页 Runtime.evaluate(探针源码, { awaitPromise: true })，返回 JSON 字符串');
