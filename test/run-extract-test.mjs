// 页面提取（extract.ts）回归测试：jsdom 加载 e2e/ 下三个高仿真模拟页，
// shim window.location 为对应真实域名 URL，执行编译后的 extract 逻辑（esbuild 现编为 cjs），
// 逐字段断言 原价 / 到手价 / 发货城市 / 店铺名 / 店铺ID 及提取来源（dom/json/null）。
// 注：v0.3.5 的「等完整价格模块」轮询逻辑位于 content/index.ts 的 extractWithPriceWait
// （依赖真实页面异步注水时序），jsdom 静态加载覆盖不到，此处仅测单次同步提取结果。
import { buildSync } from 'esbuild';
import { createRequire } from 'node:module';
import { readFileSync, unlinkSync } from 'node:fs';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const tmpOut = join(root, 'test', '.tmp-extract.cjs');

buildSync({
  entryPoints: [join(root, 'src', 'shared', 'extract.ts')],
  bundle: true,
  format: 'cjs',
  platform: 'node',
  outfile: tmpOut,
  logLevel: 'silent',
});

const require = createRequire(import.meta.url);
const { extractPageData } = require('./.tmp-extract.cjs');
const { JSDOM } = require('jsdom');

// ===== 用例定义：三个模拟页均为真实 2025 版 DOM 结构（highlightPrice--/subPrice-- 等）=====
// 语义规则：subPrice 存在 → subPrice=原价、highlightPrice=到手价；
//           subPrice 不存在 → highlightPrice=原价（售价）、到手价=null
const CASES = [
  {
    file: 'mock-tmall-a.html',
    url: 'https://detail.tmall.com/item.htm?id=982252700443',
    desc: '天猫A（商品 982252700443）· 双价结构（subPrice+highlightPrice 并存）',
    expect: {
      platform: 'tmall',
      productId: '982252700443',
      original: 3799,   // subPrice「优惠前￥3799」
      final: 3188.55,   // highlightPrice「平台加补后￥3188.55」
      shipRaw: '浙江嘉兴 至 北京市 海淀区',
      shipNormalized: '嘉兴', // 「至」前半段提取省市
      shopName: '天猫国际自营全球超级店',
      shopId: '2212833764123', // 内嵌 JSON 的 shopId 键
      meta: {
        price: 'dom', originalPrice: 'dom', finalPrice: 'dom',
        shippingCity: 'dom', shopName: 'dom', shopId: 'json',
      },
    },
  },
  {
    file: 'mock-tmall-b.html',
    url: 'https://detail.tmall.com/item.htm?id=651981565426',
    desc: '天猫B（商品 651981565426）· 双价结构 + data-shopid',
    expect: {
      platform: 'tmall',
      productId: '651981565426',
      original: 18.7,   // subPrice「特价秒杀￥18.7起」
      final: 15.74,     // highlightPrice「秒杀价￥15.74起」
      shipRaw: '重庆 至 北京市 海淀区',
      shipNormalized: '重庆',
      shopName: '厮磨工坊旗舰店',
      shopId: '889977665', // data-shopid 属性
      meta: {
        price: 'dom', originalPrice: 'dom', finalPrice: 'dom',
        shippingCity: 'dom', shopName: 'dom', shopId: 'dom',
      },
    },
  },
  {
    file: 'mock-taobao-c.html',
    url: 'https://item.taobao.com/item.htm?id=836035130704',
    desc: '淘宝C（商品 836035130704）· 单价结构（无 subPrice：original=售价、final=null）+ 店铺名评分后缀清理',
    expect: {
      platform: 'taobao',
      productId: '836035130704',
      original: 3850, // highlightPrice「优惠促销￥3850起」，无优惠时高亮价即原价（售价）
      final: null,    // 无 subPrice → 到手价 null（不回退为售价）
      shipRaw: '广东深圳 至 北京 海淀',
      shipNormalized: '深圳',
      shopName: '明智电脑科技', // 回退选择器命中「明智电脑科技4.690天新增…」，清理截断
      shopId: '110245678', // 店铺链接 href 的 shop_id 参数
      meta: {
        price: 'dom', originalPrice: 'dom', finalPrice: null,
        shippingCity: 'dom', shopName: 'dom', shopId: 'dom',
      },
    },
  },
  {
    file: 'mock-tmall-d.html',
    url: 'https://detail.tmall.com/item.htm?id=1063820538904',
    desc: '天猫D（商品 1063820538904）· 状态A 简化渲染：block2--（unit--+text--）组合 + 排除吸顶栏 ItemHeadFixed-- 干扰价（48 元）',
    expect: {
      platform: 'tmall',
      productId: '1063820538904',
      original: 1029, // 主区域 block2 组合价；吸顶栏同名结构的 48 必须被排除
      final: null,    // 单价格结构：display=该价、final=null
      shipRaw: '广东广州 至 北京市 朝阳区',
      shipNormalized: '广州',
      shopName: 'SANC旗舰店',
      shopId: '123971619', // 内嵌 JSON
      couponAmount: 500,   // 「已享受: ¥500百亿补贴」
      couponType: '百亿补贴',
      meta: {
        price: 'dom', originalPrice: 'dom', finalPrice: null,
        shippingCity: 'dom', shopName: 'dom', shopId: 'json',
      },
    },
  },
  {
    file: 'mock-tmall-e.html',
    url: 'https://detail.tmall.com/item.htm?id=944892186161',
    desc: '天猫E（商品 944892186161）· 标签含数字陷阱：subPrice「超级88￥3119起」须读 ￥ 后的 3119 而非标签里的 88',
    expect: {
      platform: 'tmall',
      productId: '944892186161',
      original: 3119,    // subPrice「超级88￥3119起」：￥ 符号后的数字（88 是活动名，不是价格）
      final: 2615.65,    // highlightPrice「平台加补后￥2615.65起」
      shipRaw: '广东广州 至 北京市 海淀区',
      shipNormalized: '广州',
      shopName: '天猫国际自营全球超级店',
      shopId: '123971619', // 内嵌 JSON
      couponAmount: 461.59, // 「领政府补贴省461.59」
      couponType: '平台补贴',
      meta: {
        price: 'dom', originalPrice: 'dom', finalPrice: 'dom',
        shippingCity: 'dom', shopName: 'dom', shopId: 'json',
      },
    },
  },
];

let passed = 0;
function check(name, fn) {
  fn();
  passed++;
  console.log(`OK   ${name}`);
}

/** 价格断言：数值容差 0.001；期望 null 时必须严格为 null */
function assertPrice(name, actual, expected) {
  if (expected === null) {
    assert.equal(actual, null, `${name}：期望 null，实际 ${actual}`);
  } else {
    assert.ok(typeof actual === 'number', `${name}：期望数值 ${expected}，实际 ${actual}`);
    assert.ok(Math.abs(actual - expected) <= 0.001, `${name}：期望 ${expected}，实际 ${actual}`);
  }
}

for (const c of CASES) {
  const html = readFileSync(join(root, 'e2e', c.file), 'utf8');
  const dom = new JSDOM(html, { url: c.url });
  // shim 浏览器全局：extract.ts 以裸 window/document/navigator 引用
  for (const [key, value] of [
    ['window', dom.window],
    ['document', dom.window.document],
    ['navigator', dom.window.navigator],
  ]) {
    Object.defineProperty(globalThis, key, { value, configurable: true, writable: true });
  }

  const data = extractPageData();
  assert.ok(data, `${c.desc}：extractPageData 应返回非 null`);
  const e = c.expect;
  const tag = `${c.file}`;

  check(`${tag} 平台与商品ID`, () => {
    assert.equal(data.platform, e.platform);
    assert.equal(data.productId, e.productId);
  });
  check(`${tag} 原价 = ${e.original}（期望来源 ${e.meta.originalPrice}）`, () => {
    assertPrice('原价', data.price.original, e.original);
  });
  check(`${tag} 到手价 = ${e.final}（期望来源 ${e.meta.finalPrice}）`, () => {
    assertPrice('到手价', data.price.final, e.final);
  });
  check(`${tag} 发货地 原文「${e.shipRaw}」→ 归一化「${e.shipNormalized}」`, () => {
    assert.equal(data.shipping.shipFromCity, e.shipRaw);
    assert.equal(data.shipping.shipFromCityNormalized, e.shipNormalized);
  });
  check(`${tag} 店铺名 = ${e.shopName}`, () => {
    assert.equal(data.shopName, e.shopName);
  });
  check(`${tag} 店铺ID = ${e.shopId}`, () => {
    assert.equal(data.shopId, e.shopId);
  });
  if ('couponAmount' in e || 'couponType' in e) {
    check(`${tag} 补贴/优惠 = ${e.couponType} ${e.couponAmount}元`, () => {
      assertPrice('couponAmount', data.price.couponAmount, e.couponAmount ?? null);
      assert.equal(data.price.couponType, e.couponType ?? null);
    });
  }
  check(`${tag} 提取来源标注 extractionMeta`, () => {
    assert.deepEqual(data.extractionMeta, e.meta);
  });
}

// 清理临时编译产物
try {
  unlinkSync(tmpOut);
} catch {
  /* 忽略清理失败 */
}

console.log(`\n全部 ${passed} 项断言通过 ✅`);
