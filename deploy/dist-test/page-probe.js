// src/platforms.ts
var PLATFORM_RULES = [
  {
    id: "taobao",
    name: "\u6DD8\u5B9D",
    hostPatterns: [/(^|\.)taobao\.com$/],
    productIdPatterns: [/[?&]id=(\d{5,})/],
    selectors: {
      title: [
        'span[class*="mainTitle--"]',
        // 2025 版商品主标题内层 span（实测类名 mainTitle--哈希，文本干净）
        '[class*="MainTitle--"]',
        // 2025 版主标题容器（注意区别于 tabDetailItemTitle 评价页签）
        "#J_Title .tb-main-title",
        // 旧版详情页标题
        'h1[class*="main-title"]',
        // 新版详情页标题
        ".tb-item-info .tb-main-title",
        "#J_Title h3",
        'h1[class*="title"]'
      ],
      shopName: [
        'span[class*="shopName--"]',
        // 2025 版店铺名内层 span（带 title 属性，文本干净）
        ".tb-shop-name",
        '[class*="ShopName--"]',
        // 新版 CSS Modules 店铺名类名
        '[class*="shopName"]',
        '[class*="ShopName"]',
        ".tb-seller-info .shop-name",
        ".shop-name"
      ],
      price: [
        // 2025 版到手价/售价高亮容器（文本如「平台加补后￥3188.55」）
        // 注意：宽松选择器 [class*="Price--"] / span[class*="priceText"] 已移除——
        // 实测会抓到无关数字（如「48」），价格只允许来自明确容器；
        // 简化渲染（状态A）的 unit--+text-- 组合由 extract.ts 的 pickUnitTextPrice 处理。
        '[class*="highlightPrice--"]',
        ".tb-rmb-num",
        // 经典价格节点
        "#J_PromoPriceNum .tb-rmb-num",
        ".tb-property .tb-rmb-num"
      ],
      finalPrice: [
        '[class*="finalPrice"]',
        // 券后到手价（页面直接展示时）
        '[class*="FinalPrice"]',
        '[class*="couponPrice"]',
        ".tb-promo-price .tb-rmb-num",
        ".price-final"
      ],
      coupon: [
        '[class*="couponInfoArea--"]',
        // 2025 版优惠信息区（「已享受:官方立减38元…」）
        ".tb-coupon",
        '[class*="coupon"]',
        '[class*="Coupon--"]',
        ".coupon-amount",
        "#J_Coupon"
      ],
      originalPrice: [
        '[class*="subPrice--"]',
        // 2025 版原价容器（文本如「优惠前￥3799」；无优惠时该节点不存在）
        "#J_StrPrice .tb-rmb-num",
        // 划线价
        ".tb-cancel-price",
        '[class*="originPrice"]',
        'del[class*="price"]',
        ".origin-price"
      ],
      shippingCity: [
        '[class*="deliveryAddrWrap--"]',
        // 2025 版发货地容器（「浙江嘉兴 至 北京市 海淀区」）
        "#J-From",
        ".tb-location",
        '[class*="deliveryAddress"]',
        '[class*="deliver"]',
        ".tb-deliver-to"
      ],
      userMarker: [
        "#J_SiteNavLogin .site-nav-login-info-nick",
        // 顶部导航昵称
        ".site-nav-user",
        '[class*="nickname"]',
        '[class*="userNick"]',
        ".member-info"
      ]
    },
    loginCookieNames: ["unb", "_nk_"]
  },
  {
    id: "tmall",
    name: "\u5929\u732B",
    hostPatterns: [/(^|\.)tmall\.com$/],
    productIdPatterns: [/[?&]id=(\d{5,})/],
    selectors: {
      title: [
        'span[class*="mainTitle--"]',
        // 2025 版商品主标题内层 span（实测类名 mainTitle--哈希，文本干净）
        '[class*="MainTitle--"]',
        // 2025 版主标题容器（注意区别于 tabDetailItemTitle 评价页签）
        ".tb-detail-hd h1",
        // 天猫详情页标题
        "#J_DetailMeta .tb-detail-hd h1",
        'h1[class*="main-title"]',
        '[class*="ItemTitle--"]',
        'h1[class*="title"]'
      ],
      shopName: [
        'span[class*="shopName--"]',
        // 2025 版店铺名内层 span（带 title 属性，文本干净）
        "#shopExtra .slogo-shopname",
        // 天猫店铺招牌
        ".slogo-shopname",
        '[class*="ShopName--"]',
        // 新版 CSS Modules 店铺名类名
        '[class*="shopName"]',
        ".shopLink",
        '[class*="ShopName"]'
      ],
      price: [
        // 2025 版到手价/售价高亮容器（淘宝天猫同版式）
        // 宽松选择器 [class*="Price--"] / span[class*="priceText"] 已移除（实测抓到无关数字）；
        // 简化渲染（状态A）的 unit--+text-- 组合由 extract.ts 的 pickUnitTextPrice 处理。
        '[class*="highlightPrice--"]',
        ".tm-price",
        // 天猫价
        ".tm-promo-price .tm-price",
        ".tb-rmb-num"
      ],
      finalPrice: [
        '[class*="finalPrice"]',
        '[class*="FinalPrice"]',
        '[class*="couponPrice"]',
        ".tm-promo-price .tm-price",
        ".price-final"
      ],
      coupon: [
        '[class*="couponInfoArea--"]',
        // 2025 版优惠信息区（「已享受:官方立减38元…」）
        ".tm-coupon",
        '[class*="coupon"]',
        '[class*="Coupon--"]',
        ".coupon-amount",
        ".tm-shop-coupon"
      ],
      originalPrice: [
        '[class*="subPrice--"]',
        // 2025 版原价容器（无优惠时该节点不存在）
        ".tm-yprice",
        // 天猫原价（划线价）
        ".tm-price-panel .tm-yprice",
        '[class*="originPrice"]',
        'del[class*="price"]',
        ".origin-price"
      ],
      shippingCity: [
        '[class*="deliveryAddrWrap--"]',
        // 2025 版发货地容器（「重庆 至 北京市 海淀区」）
        "#J-From",
        ".tm-location",
        '[class*="deliveryAddress"]',
        '[class*="deliver"]',
        '[class*="delivery"]'
      ],
      userMarker: [
        "#J_SiteNavLogin .site-nav-login-info-nick",
        ".site-nav-user",
        '[class*="nickname"]',
        '[class*="userNick"]',
        ".member-info"
      ]
    },
    loginCookieNames: ["unb", "_nk_"]
  },
  {
    id: "jd",
    name: "\u4EAC\u4E1C",
    hostPatterns: [/(^|\.)jd\.com$/],
    productIdPatterns: [
      /item\.jd\.com\/(\d+)\.html/,
      // 京东商品页：item.jd.com/<sku>.html
      /[?&]skuId=(\d+)/
    ],
    selectors: {
      title: [
        "#name h1",
        // 京东商品名
        ".sku-name",
        "#itemInfo #name h1",
        ".itemInfo-wrap .sku-name",
        'h1[class*="sku"]'
      ],
      shopName: [
        "#shopId",
        // 店铺链接节点
        ".pop-shop-name",
        ".shopName",
        '[class*="shop-name"]',
        ".crumb-wrap .contact .name"
      ],
      price: [
        ".p-price .price",
        // 京东价
        "#price .price",
        ".summary-price .price",
        "span.price",
        '[class*="priceJ"]'
      ],
      finalPrice: [
        '[class*="finalPrice"]',
        ".summary-price .p-price .price",
        '[class*="couponPrice"]',
        ".p-price .price",
        '[class*="FinalPrice"]'
      ],
      coupon: [
        ".quan-item",
        // 优惠券领取区
        "#coupon .quan",
        '[class*="coupon"]',
        ".youhui .quan-item",
        '[class*="Coupon"]'
      ],
      originalPrice: [
        "#page_maprice",
        // 京东划线价
        ".p-price del",
        '[class*="originPrice"]',
        "del.price",
        ".origin-price"
      ],
      shippingCity: [
        "#store-prompt",
        // 配送至/发货地（部分页面需展开配送面板才渲染）
        '[class*="sendAddress"]',
        "#summary .dd",
        '[class*="address"]',
        ".summary .dd"
      ],
      userMarker: [
        "#ttbar-login .nickname",
        // 顶栏昵称
        ".nickname",
        '[class*="userInfo"]',
        ".user-info",
        '[class*="userNick"]'
      ]
    },
    loginCookieNames: ["pin", "pt_pin", "pt_key"]
  },
  {
    id: "pinduoduo",
    name: "\u62FC\u591A\u591A",
    // 拼多多网页版（mobile.yangkeduo.com）页面结构改版频繁，
    // 以下选择器可能随改版失效，需要定期核对更新。
    hostPatterns: [/(^|\.)yangkeduo\.com$/],
    productIdPatterns: [
      /[?&]goods_id=(\d+)/,
      // 商品页参数 goods_id
      /[?&]goodsId=(\d+)/
    ],
    selectors: {
      title: [
        '[class*="goods-name"]',
        '[class*="goodsName"]',
        ".goods-name",
        'h1[class*="title"]',
        "h1"
      ],
      shopName: [
        '[class*="mall-name"]',
        // 拼多多店铺常称「店铺/商场」
        '[class*="mallName"]',
        '[class*="shopName"]',
        ".mall-name",
        '[class*="shop-name"]'
      ],
      price: [
        '[class*="goods-price"]',
        '[class*="goodsPrice"]',
        ".goods-price",
        '[class*="price"]',
        ".price"
      ],
      finalPrice: [
        '[class*="finalPrice"]',
        '[class*="goodsPrice"]',
        '[class*="couponPrice"]',
        ".goods-price",
        '[class*="price"]'
      ],
      coupon: [
        '[class*="coupon"]',
        '[class*="Coupon"]',
        ".coupon-amount",
        '[class*="discount"]',
        '[class*="quan"]'
      ],
      originalPrice: [
        '[class*="originPrice"]',
        '[class*="market-price"]',
        'del[class*="price"]',
        ".origin-price",
        "del"
      ],
      shippingCity: [
        '[class*="delivery"]',
        '[class*="deliver"]',
        '[class*="address"]',
        '[class*="shipping"]',
        '[class*="from"]'
      ],
      userMarker: [
        '[class*="user-name"]',
        '[class*="nickName"]',
        '[class*="userName"]',
        '[class*="avatar"]',
        '[class*="user-info"]'
      ]
    },
    loginCookieNames: ["pdd_user_id", "pdd_user_token"]
  }
];
function findPlatformRule(hostname) {
  for (const rule of PLATFORM_RULES) {
    if (rule.hostPatterns.some((re) => re.test(hostname))) return rule;
  }
  return null;
}
function extractProductId(rule, url) {
  for (const re of rule.productIdPatterns) {
    const m = url.match(re);
    if (m && m[1]) return m[1];
  }
  return null;
}

// src/utils.ts
function maskText(text) {
  const t = text.trim();
  if (!t) return t;
  return `${t[0]}*`;
}

// src/shared/extract.ts
var PRICE_MIN = 0.01;
var PRICE_MAX = 1e7;
var SALE_PRICE_KEYS = ["priceText", "promotePrice", "currentPrice", "salePrice", "price"];
var ORIG_PRICE_KEYS = ["origPrice", "originalPrice", "reservePrice", "marketPrice", "strPrice"];
var FINAL_PRICE_KEYS = ["finalPrice", "couponPrice", "promotePrice", "handPrice"];
var SHIPPING_KEYS = ["deliveryAddress", "areaName", "sendAddress", "shipFrom", "deliveryCity"];
var SHOP_NAME_KEYS = ["shopName", "shopNick", "mallName", "sellerNick"];
var SHOP_ID_KEYS = ["shopId", "shop_id", "sellerId", "seller_id"];
function extractPageData() {
  const rule = findPlatformRule(window.location.hostname);
  if (!rule) return null;
  const productId = extractProductId(rule, window.location.href);
  if (!productId) return null;
  const scriptText = collectInlineScriptText();
  const title = pickFirst(rule.selectors.title);
  const couponNode = pickFirst(rule.selectors.coupon);
  const shopNode = pickFirst(rule.selectors.shopName);
  let shopName = shopNode ? { value: cleanShopName(shopNode.text), source: "dom" } : { value: null, source: null };
  if (shopName.value === null) {
    const v = pickJsonString(scriptText, SHOP_NAME_KEYS);
    if (v !== null) shopName = { value: v, source: "json" };
  }
  const shopId = pickShopId(scriptText);
  const isTaoFamily = rule.id === "taobao" || rule.id === "tmall";
  const sale = pickPrice(
    rule.selectors.price,
    scriptText,
    SALE_PRICE_KEYS,
    isTaoFamily ? pickUnitTextPrice : void 0
  );
  const sub = pickPrice(rule.selectors.originalPrice, scriptText, ORIG_PRICE_KEYS);
  let original;
  let finalP;
  if (sub.value !== null) {
    original = sub;
    finalP = sale.value !== null ? sale : pickPrice(rule.selectors.finalPrice, scriptText, FINAL_PRICE_KEYS);
  } else {
    original = sale;
    finalP = pickPrice(rule.selectors.finalPrice, scriptText, FINAL_PRICE_KEYS);
  }
  if (original.value !== null && finalP.value !== null && finalP.value > original.value) {
    [original, finalP] = [finalP, original];
  }
  const coupon = couponNode ? parseCoupon(couponNode.text) : { amount: null, type: null };
  const shipNode = pickFirst(rule.selectors.shippingCity);
  let shipRaw = shipNode ? { value: shipNode.text, source: "dom" } : { value: null, source: null };
  if (shipRaw.value === null) {
    const v = pickJsonString(scriptText, SHIPPING_KEYS);
    if (v !== null) shipRaw = { value: v, source: "json" };
  }
  const shipNormalized = shipRaw.value !== null ? normalizeShippingCity(shipRaw.value) : null;
  const markerNode = pickFirst(rule.selectors.userMarker);
  const price = {
    original: original.value,
    final: finalP.value,
    currency: "CNY",
    couponAmount: coupon.amount,
    couponType: coupon.type
  };
  const extractionMeta = {
    price: sale.source,
    originalPrice: original.source,
    finalPrice: finalP.source,
    shippingCity: shipRaw.source,
    shopName: shopName.source,
    shopId: shopId.source
  };
  const domSnapshots = [];
  const snapshotTargets = [
    ["title", title],
    ["price", sale.domNode],
    ["finalPrice", finalP.domNode],
    ["originalPrice", original.domNode],
    ["shopName", shopNode],
    ["shippingCity", shipNode]
  ];
  for (const [field, node] of snapshotTargets) {
    const snap = node ? snapshotNode(field, node.el) : null;
    if (snap) domSnapshots.push(snap);
  }
  domSnapshots.push({ field: "extractionMeta", outerHTML: JSON.stringify(extractionMeta) });
  return {
    platform: rule.id,
    productId,
    productName: title?.text ?? null,
    shopName: shopName.value,
    shopId: shopId.value,
    productUrl: window.location.href,
    price,
    userContext: inferUserContext(rule, markerNode?.text ?? null),
    device: collectDeviceInfo(),
    shipping: { shipFromCity: shipRaw.value, shipFromCityNormalized: shipNormalized },
    extractionMeta,
    domSnapshots
  };
}
function pickFirst(selectors) {
  for (const sel of selectors) {
    try {
      const el = document.querySelector(sel);
      const text = el?.textContent?.replace(/\s+/g, " ").trim() ?? "";
      if (el && text) return { text, el };
    } catch {
    }
  }
  return null;
}
function collectInlineScriptText() {
  const parts = [];
  let total = 0;
  const scripts = document.querySelectorAll("script:not([src])");
  for (const s of scripts) {
    const t = s.textContent ?? "";
    if (!t) continue;
    parts.push(t);
    total += t.length;
    if (total >= 2e6) break;
  }
  return parts.join("\n");
}
function pickPrice(domSelectors, scriptText, jsonKeys, extraDom) {
  const node = pickFirst(domSelectors);
  if (node) {
    const n = parsePriceNumber(node.text);
    if (n !== null && n >= PRICE_MIN && n <= PRICE_MAX) {
      return { value: n, source: "dom", domNode: node };
    }
  }
  if (extraDom) {
    const e = extraDom();
    if (e) return e;
  }
  const j = pickJsonPrice(scriptText, jsonKeys);
  if (j !== null) return { value: j, source: "json", domNode: node };
  return { value: null, source: null, domNode: node };
}
function pickUnitTextPrice() {
  const blocks = document.querySelectorAll('div[class*="block2--"]');
  for (const b of blocks) {
    if (b.closest('[class*="ItemHeadFixed--"]')) continue;
    const unit = b.querySelector('span[class*="unit--"]');
    const numEl = b.querySelector('span[class*="text--"]');
    if (!unit || !numEl) continue;
    const unitText = (unit.textContent ?? "").trim();
    if (!/^[¥￥]$/.test(unitText)) continue;
    const numText = (numEl.textContent ?? "").trim();
    const n = parsePriceNumber(numText);
    if (n !== null && n >= PRICE_MIN && n <= PRICE_MAX) {
      return { value: n, source: "dom", domNode: { text: `${unitText}${numText}`, el: b } };
    }
  }
  return null;
}
function pickJsonPrice(text, keys) {
  if (!text) return null;
  for (const key of keys) {
    const re = new RegExp(`"${key}"\\s*:\\s*"?(-?\\d+(?:\\.\\d+)?)"?`);
    const m = re.exec(text);
    if (!m) continue;
    const n = Number(m[1]);
    if (Number.isFinite(n) && n >= PRICE_MIN && n <= PRICE_MAX) return n;
  }
  return null;
}
function pickJsonString(text, keys, maxLen = 80) {
  if (!text) return null;
  for (const key of keys) {
    const re = new RegExp(`"${key}"\\s*:\\s*"([^"]{1,${maxLen}})"`);
    const m = re.exec(text);
    if (m && m[1].trim()) return m[1].trim();
  }
  return null;
}
function pickShopId(scriptText) {
  const attrEl = document.querySelector("[data-shopid],[data-sellerid]");
  const attr = attrEl?.getAttribute("data-shopid")?.trim() ?? attrEl?.getAttribute("data-sellerid")?.trim() ?? null;
  if (attr && /^\d{3,}$/.test(attr)) return { value: attr, source: "dom" };
  const links = document.querySelectorAll('a[href*="shop"]');
  for (const a of links) {
    const href = a.getAttribute("href") ?? "";
    const m = href.match(/[?&](?:shopId|shop_id|sellerId|seller_id)=(\d{3,})/);
    if (m) return { value: m[1], source: "dom" };
  }
  const v = pickJsonString(scriptText, SHOP_ID_KEYS, 40);
  if (v !== null && /^\d{3,}$/.test(v)) return { value: v, source: "json" };
  return { value: null, source: null };
}
function cleanShopName(text) {
  const m = text.match(/^[^\d]{2,}(?=\d)/);
  return m ? m[0].trim() : text;
}
var MUNICIPALITIES = ["\u5317\u4EAC", "\u4E0A\u6D77", "\u5929\u6D25", "\u91CD\u5E86"];
var PROVINCES = [
  "\u6CB3\u5317",
  "\u5C71\u897F",
  "\u8FBD\u5B81",
  "\u5409\u6797",
  "\u9ED1\u9F99\u6C5F",
  "\u6C5F\u82CF",
  "\u6D59\u6C5F",
  "\u5B89\u5FBD",
  "\u798F\u5EFA",
  "\u6C5F\u897F",
  "\u5C71\u4E1C",
  "\u6CB3\u5357",
  "\u6E56\u5317",
  "\u6E56\u5357",
  "\u5E7F\u4E1C",
  "\u6D77\u5357",
  "\u56DB\u5DDD",
  "\u8D35\u5DDE",
  "\u4E91\u5357",
  "\u9655\u897F",
  "\u7518\u8083",
  "\u9752\u6D77",
  "\u53F0\u6E7E",
  "\u5185\u8499\u53E4",
  "\u5E7F\u897F",
  "\u897F\u85CF",
  "\u5B81\u590F",
  "\u65B0\u7586",
  "\u9999\u6E2F",
  "\u6FB3\u95E8"
];
function normalizeShippingCity(raw) {
  const segs = raw.split("\u81F3").map((s) => s.replace(/\s+/g, ""));
  let t = segs[0];
  if (!t || t === "\u914D\u9001" || t === "\u53D1\u8D27" || t === "\u5FEB\u9012") t = segs[1] ?? "";
  if (!t) return null;
  for (const m of MUNICIPALITIES) {
    if (t.includes(m)) return m;
  }
  for (const p of PROVINCES) {
    const idx = t.indexOf(p);
    if (idx === -1) continue;
    const rest = t.slice(idx + p.length).replace(/^(特别行政区|壮族自治区|回族自治区|维吾尔自治区|自治区|省|市)/, "");
    const cm2 = rest.match(/^([一-龥]{1,4}?)(?:市|区|县|盟|地区|自治州|$)/);
    if (cm2 && cm2[1]) return cm2[1];
    return p;
  }
  const cm = t.match(/([一-龥]{2,4})市/);
  if (cm) return cm[1];
  return null;
}
function parsePriceNumber(text) {
  const t = text.replace(/,/g, "");
  const afterSymbol = t.match(/[¥￥]\s*(\d+(?:\.\d{1,2})?)/);
  const m = afterSymbol ?? t.match(/(\d+(?:\.\d{1,2})?)/);
  if (!m) return null;
  const n = Number(m[1]);
  return Number.isFinite(n) ? n : null;
}
function parseCoupon(text) {
  const t = text.trim();
  if (!t) return { amount: null, type: null };
  for (const st of ["\u767E\u4EBF\u8865\u8D34", "\u5E73\u53F0\u8865\u8D34", "\u653F\u5E9C\u8865\u8D34"]) {
    const idx = t.indexOf(st);
    if (idx === -1) continue;
    const before = t.slice(0, idx).match(/[¥￥]\s*(\d+(?:\.\d+)?)\s*$/);
    const after = t.slice(idx + st.length).match(/^(?:已?抵|立?省|减)?\s*[¥￥]?\s*(\d+(?:\.\d+)?)/);
    const amount = before?.[1] ?? after?.[1];
    return { amount: amount ? Number(amount) : null, type: st === "\u767E\u4EBF\u8865\u8D34" ? "\u767E\u4EBF\u8865\u8D34" : "\u5E73\u53F0\u8865\u8D34" };
  }
  let type = null;
  if (/满.*减/.test(t)) type = "\u6EE1\u51CF\u5238";
  else if (/折/.test(t)) type = "\u6298\u6263\u5238";
  else if (/券|优惠/.test(t)) type = "\u901A\u7528\u5238";
  const m = t.match(/减\s*(\d+(?:\.\d+)?)/) ?? t.match(/(\d+(?:\.\d+)?)\s*元/);
  return { amount: m ? Number(m[1]) : null, type };
}
function inferUserContext(rule, markerText) {
  const cookieKeys = new Set(
    document.cookie.split(";").map((kv) => kv.split("=")[0].trim()).filter(Boolean)
  );
  const hitCookie = rule.loginCookieNames.find((name) => cookieKeys.has(name)) ?? null;
  const evidence = [];
  let isLoggedIn = null;
  if (hitCookie) {
    isLoggedIn = true;
    evidence.push(`\u5B58\u5728\u767B\u5F55\u6001 cookie \u952E\u540D\u300C${hitCookie}\u300D\uFF08\u4EC5\u5224\u65AD\u5B58\u5728\u6027\uFF0C\u672A\u8BFB\u53D6\u503C\uFF09`);
  }
  const marker = markerText?.trim() || null;
  if (marker) {
    if (/请登录|立即登录|^登录$|注册/.test(marker)) {
      if (isLoggedIn === null) isLoggedIn = false;
      evidence.push("\u9875\u9762\u7528\u6237\u8282\u70B9\u5C55\u793A\u300C\u767B\u5F55/\u6CE8\u518C\u300D\u5165\u53E3\uFF0C\u63A8\u65AD\u672A\u767B\u5F55");
    } else {
      if (isLoggedIn === null) isLoggedIn = true;
      evidence.push(`\u9875\u9762\u5C55\u793A\u7528\u6237\u6807\u8BC6\u300C${maskText(marker)}\u300D`);
    }
  }
  if (isLoggedIn === null) {
    evidence.push("\u672A\u627E\u5230\u53EF\u9760\u767B\u5F55\u6001\u8BC1\u636E\uFF0C\u6309\u672A\u77E5\u5904\u7406");
  }
  let memberLevel = null;
  const levelMatch = marker?.match(/(88VIP|PLUS|超级会员|钻石会员|黄金会员|VIP\d{0,2}|会员)/i);
  if (levelMatch) memberLevel = levelMatch[1];
  return {
    isLoggedIn,
    memberLevel,
    isNewUser: null,
    // 页面无法可靠判断是否新用户，保持 null
    userMarker: marker,
    evidence: `${evidence.join("\uFF1B")}\uFF1BisNewUser \u9875\u9762\u65E0\u53EF\u9760\u5224\u65AD\u4F9D\u636E\uFF0C\u8BB0\u4E3A null`
  };
}
function collectDeviceInfo() {
  const nav = navigator;
  const memory = typeof nav.deviceMemory === "number" ? nav.deviceMemory : null;
  const cores = typeof navigator.hardwareConcurrency === "number" ? navigator.hardwareConcurrency : null;
  const pixels = window.screen.width * window.screen.height;
  return {
    userAgent: navigator.userAgent,
    screenResolution: `${window.screen.width}x${window.screen.height}`,
    deviceMemory: memory,
    hardwareConcurrency: cores,
    platform: navigator.platform,
    language: navigator.language,
    devicePriceIndex: estimateDevicePriceIndex(memory, cores, pixels)
  };
}
function estimateDevicePriceIndex(memory, cores, pixels) {
  const memScore = memory === null ? 0.5 : Math.min(memory / 16, 1);
  const cpuScore = cores === null ? 0.5 : Math.min(cores / 8, 1);
  const screenScore = Math.min(pixels / (2560 * 1440), 1);
  return Math.round((memScore * 0.4 + cpuScore * 0.3 + screenScore * 0.3) * 100);
}
function snapshotNode(field, el) {
  const clone = el.cloneNode(true);
  clone.querySelectorAll("script,style").forEach((n) => n.remove());
  const html = (clone.outerHTML ?? "").slice(0, 2e3);
  return html ? { field, outerHTML: html } : null;
}

// src/shared/backendMapping.ts
var PLATFORM_CODE_MAP = {
  yangkeduo: "pinduoduo",
  pinduoduo: "pinduoduo",
  taobao: "taobao",
  tmall: "tmall",
  jd: "jd"
};
function isPeakHour(collectedAt) {
  const d = new Date(collectedAt);
  if (Number.isNaN(d.getTime())) return null;
  const h = d.getHours();
  return h >= 11 && h <= 13 || h >= 19 && h <= 23;
}
function snapshotToText(outerHTML) {
  return outerHTML.replace(/<script[\s\S]*?<\/script>/gi, " ").replace(/<style[\s\S]*?<\/style>/gi, " ").replace(/<[^>]+>/g, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/\s+/g, " ").trim().slice(0, 500);
}
function pickDomPriceText(record) {
  const snap = record.domSnapshots.find((s) => s.field === "price") ?? record.domSnapshots.find((s) => s.field === "finalPrice");
  if (!snap) return null;
  const text = snapshotToText(snap.outerHTML);
  return text || null;
}
function yuanToCents(yuan) {
  if (yuan === null || yuan === void 0) return null;
  return Math.round(yuan * 100);
}
function mapObservationToBackend(record, extVersion) {
  const couponType = record.price.couponType;
  const couponAmount = record.price.couponAmount;
  return {
    platform_code: PLATFORM_CODE_MAP[record.platform] ?? record.platform,
    product_id: record.productId,
    product_name: record.productName,
    seller_id: record.shopId ?? record.shopName,
    // 优先真实店铺 ID；取不到回退店铺名（后端 schema 已冻结，seller_id 语义为「卖家标识」）
    product_url: record.productUrl,
    display_price_cents: yuanToCents(record.price.original),
    // 插件侧换算为整数分（见 yuanToCents 注释）
    actual_pay_price_cents: yuanToCents(record.price.final),
    currency: record.price.currency,
    discount_coupon_amount_cents: yuanToCents(couponAmount),
    promo_type: couponType,
    promo_label: couponType !== null && couponAmount !== null ? `${couponType}\uFF08\u51CF${couponAmount}\u5143\uFF09` : couponType,
    is_login: record.userContext.isLoggedIn,
    membership_level: record.userContext.memberLevel,
    is_new_user: record.userContext.isNewUser,
    register_days: null,
    // 插件无法获取注册天数
    user_agent: record.device.userAgent,
    platform: record.device.platform,
    language: record.device.language,
    device_memory: record.device.deviceMemory,
    hardware_concurrency: record.device.hardwareConcurrency,
    screen_resolution: record.device.screenResolution,
    device_price_score_estimate: record.device.devicePriceIndex,
    ip_city: record.network.city,
    shipping_city: record.shipping.shipFromCityNormalized ?? record.shipping.shipFromCity,
    peak_hour: isPeakHour(record.collectedAt),
    stock_hint: null,
    // 插件未采集库存提示
    fetch_ts: record.collectedAt,
    dom_price_text: pickDomPriceText(record),
    source_code_version: extVersion,
    anonymous_id: record.anonymousUserId
  };
}

// src/probe/page-probe.ts
(async function pageProbe() {
  const data = extractPageData();
  if (!data) {
    return JSON.stringify({ ok: false, error: "\u5F53\u524D\u9875\u672A\u8BC6\u522B\u4E3A\u53D7\u652F\u6301\u7684\u5546\u54C1\u8BE6\u60C5\u9875\uFF08\u5E73\u53F0\u89C4\u5219\u6216\u5546\u54C1 ID \u6A21\u5F0F\u672A\u547D\u4E2D\uFF09" });
  }
  const record = {
    recordId: typeof crypto.randomUUID === "function" ? crypto.randomUUID() : `probe-${Date.now()}`,
    anonymousUserId: "page-probe",
    collectedAt: (/* @__PURE__ */ new Date()).toISOString(),
    platform: data.platform,
    productId: data.productId,
    productName: data.productName,
    shopName: data.shopName,
    shopId: data.shopId,
    productUrl: data.productUrl,
    price: data.price,
    userContext: {
      isLoggedIn: data.userContext.isLoggedIn,
      memberLevel: data.userContext.memberLevel,
      isNewUser: data.userContext.isNewUser,
      userMarkerMasked: null,
      // 探针不打码也不上传昵称（映射层本就不含该字段）
      evidence: data.userContext.evidence
    },
    device: data.device,
    network: { ip: null, city: null, region: null, country: null, source: "page-probe\uFF08\u63A2\u9488\u4E0D\u67E5\u8BE2 IP\uFF09" },
    shipping: data.shipping,
    screenshotDataUrl: null,
    // 探针不截图（且映射层本就不上传截图）
    screenshotError: "page-probe \u4E0D\u63D0\u4F9B\u622A\u56FE\u80FD\u529B",
    domSnapshots: data.domSnapshots,
    extractionMeta: data.extractionMeta,
    uploadStatus: "pending",
    observationId: null
  };
  const payload = mapObservationToBackend(record, "page-probe");
  try {
    const resp = await fetch("http://127.0.0.1:8000/api/observations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": "dev-key-123"
      },
      body: JSON.stringify(payload)
    });
    const body = await resp.json().catch(() => ({}));
    return JSON.stringify({
      ok: resp.ok,
      status: resp.status,
      observationId: body.observation_id ?? null,
      warnings: Array.isArray(body.warnings) ? body.warnings : [],
      extracted: {
        platform: data.platform,
        productId: data.productId,
        productName: data.productName,
        shopName: data.shopName,
        shopId: data.shopId,
        price: data.price,
        shipFromCity: data.shipping.shipFromCity,
        shipFromCityNormalized: data.shipping.shipFromCityNormalized,
        extractionMeta: data.extractionMeta,
        isLoggedIn: data.userContext.isLoggedIn,
        memberLevel: data.userContext.memberLevel,
        devicePriceIndex: data.device.devicePriceIndex,
        snapshotFields: data.domSnapshots.map((s) => s.field),
        domPriceText: payload.dom_price_text
      }
    });
  } catch (e) {
    return JSON.stringify({ ok: false, error: String(e), hint: "\u8BF7\u786E\u8BA4\u672C\u5730\u540E\u7AEF\u5DF2\u5728 127.0.0.1:8000 \u8FD0\u884C" });
  }
})();
