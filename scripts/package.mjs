// 发布打包：dist/ → release/算法歧视观测-edge插件-v<version>.zip
// 用 Windows 自带 PowerShell Compress-Archive（Node 无内置 zip）。
// 关键要求：zip 第一层就是 manifest.json（-Path 'dist\*' 只打包内容，不含 dist 目录本身），
// 打包后自动解压自验（根层 manifest + 文件数与 dist 一致），验证完删除临时目录。
import { execFileSync } from 'node:child_process';
import {
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  rmSync,
  statSync,
} from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');
const release = join(root, 'release');

const fail = (msg) => {
  console.error(`FAIL ${msg}`);
  process.exit(1);
};

// PowerShell 可执行文件：优先 PATH，其次系统绝对路径（部分受限环境 PATH 不含其目录）
const PS_ABS = join(
  process.env.SystemRoot || 'C:\\Windows',
  'System32',
  'WindowsPowerShell',
  'v1.0',
  'powershell.exe',
);
const POWERSHELL = existsSync(PS_ABS) ? PS_ABS : 'powershell.exe';

if (!existsSync(join(dist, 'manifest.json'))) {
  fail('dist/manifest.json 不存在，请先运行 npm run build');
}

const manifest = JSON.parse(readFileSync(join(root, 'public', 'manifest.json'), 'utf8'));
const zipName = `算法歧视观测-edge插件-v${manifest.version}.zip`;
const zipPath = join(release, zipName);

mkdirSync(release, { recursive: true });
if (existsSync(zipPath)) rmSync(zipPath);

// PowerShell 单引号字符串转义：' → ''
const psq = (s) => s.replace(/'/g, "''");

console.log(`打包：${dist}\\* → ${zipPath}`);
execFileSync(
  POWERSHELL,
  [
    '-NoProfile',
    '-NonInteractive',
    '-Command',
    // -Path 以 \* 结尾：zip 根层直接是 manifest.json 等内容，不嵌套 dist 目录
    `Compress-Archive -Path '${psq(dist)}\\*' -DestinationPath '${psq(zipPath)}' -Force`,
  ],
  { stdio: 'inherit' },
);

if (!existsSync(zipPath)) fail('zip 未生成');

// ===== 自验：解压到临时目录，核对根层 manifest 与文件数 =====
const tmp = join(release, '.tmp-verify');
if (existsSync(tmp)) rmSync(tmp, { recursive: true, force: true });
mkdirSync(tmp, { recursive: true });
execFileSync(
  POWERSHELL,
  [
    '-NoProfile',
    '-NonInteractive',
    '-Command',
    `Expand-Archive -Path '${psq(zipPath)}' -DestinationPath '${psq(tmp)}' -Force`,
  ],
  { stdio: 'inherit' },
);

const countFiles = (dir) => {
  let n = 0;
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    n += statSync(p).isDirectory() ? countFiles(p) : 1;
  }
  return n;
};

const distCount = countFiles(dist);
const zipCount = countFiles(tmp);
const rootHasManifest = existsSync(join(tmp, 'manifest.json'));
const nestedDist = existsSync(join(tmp, 'dist'));

// 清理临时解压目录
rmSync(tmp, { recursive: true, force: true });

const sizeKB = (statSync(zipPath).size / 1024).toFixed(1);
console.log(`OK   zip 已生成：${zipPath}（${sizeKB} KB）`);
console.log(rootHasManifest ? 'OK   manifest.json 位于 zip 根层' : 'FAIL zip 根层缺少 manifest.json');
console.log(!nestedDist ? 'OK   zip 内未嵌套 dist 目录' : 'FAIL zip 内嵌套了 dist 目录');
console.log(
  zipCount === distCount
    ? `OK   文件数一致（dist ${distCount} 个 = zip 内 ${zipCount} 个）`
    : `FAIL 文件数不一致（dist ${distCount} 个 ≠ zip 内 ${zipCount} 个）`,
);

if (!rootHasManifest || nestedDist || zipCount !== distCount) {
  process.exit(1);
}
console.log('\n打包与自验全部通过 ✅');
