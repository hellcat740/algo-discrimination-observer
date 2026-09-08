// content script 独立构建配置
// Chrome MV3 的 content_scripts 不接受 ES module（顶层 import/export 会直接报错），
// 因此这里用 lib 模式产出 IIFE 单文件，保证 dist/content/index.js 顶层无 import 语句。
import { defineConfig } from 'vite';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  publicDir: false, // 静态资源已由主构建拷贝，避免重复
  build: {
    outDir: resolve(__dirname, 'dist'),
    emptyOutDir: false, // 追加到主构建产物中，不清空 dist
    minify: false, // 保持可读，便于人工核验
    lib: {
      entry: resolve(__dirname, 'src/content/index.ts'),
      // IIFE 格式要求一个全局占位名；本模块无导出，该名仅满足 rollup 要求
      name: 'AlgoObsContent',
      formats: ['iife'],
    },
    rollupOptions: {
      output: {
        entryFileNames: 'content/index.js',
      },
    },
  },
});
