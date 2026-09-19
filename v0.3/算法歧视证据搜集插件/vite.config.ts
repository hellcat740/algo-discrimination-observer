// 主构建配置：background（service worker，ES module）+ popup / options / report 页面
// content script 必须是 IIFE 产物（Chrome MV3 的 content_scripts 不接受 ESM），
// 因此由 vite.content.config.ts 独立构建，见该文件注释。
import { defineConfig } from 'vite';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  // 以 src 为根目录：保证 popup/options/report 的输出路径与 manifest 中的引用一致
  root: resolve(__dirname, 'src'),
  // 扩展页面使用相对路径引用资源，避免绝对路径在 chrome-extension:// 下解析歧义
  base: './',
  // manifest.json 与 icons 原样拷贝到 dist/
  publicDir: resolve(__dirname, 'public'),
  build: {
    outDir: resolve(__dirname, 'dist'),
    emptyOutDir: true,
    minify: false, // 公益审计友好：构建产物保持可读，便于核查隐私行为
    rollupOptions: {
      input: {
        'popup/popup': resolve(__dirname, 'src/popup/popup.html'),
        'options/options': resolve(__dirname, 'src/options/options.html'),
        'report/report': resolve(__dirname, 'src/report/report.html'),
        'background/index': resolve(__dirname, 'src/background/index.ts'),
      },
      output: {
        // service worker 以 ES module 运行（manifest 中 background.type = "module"）
        format: 'es',
        entryFileNames: '[name].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash][extname]',
      },
    },
  },
});
