/**
 * 平台选择器规则配置
 * 新增平台时只需在 PLATFORM_RULES 中追加一条规则，content 脚本不写死任何选择器。
 * 注意：电商页面改版频繁，选择器需定期维护；每个字段提供多个候选选择器，按顺序尝试。
 */
export interface PlatformRule {
  /** 平台标识 */
  id: string;
  /** 中文名 */
  name: string;
  /** hostname 匹配（识别当前页所属平台） */
  hostPatterns: RegExp[];
  /** 商品 ID 提取正则（作用于完整 URL，需含一个捕获组；命中即视为商品详情页） */
  productIdPatterns: RegExp[];
  /** 各字段候选 CSS 选择器（数组，按顺序尝试，取第一个命中且可见文本非空的节点） */
  selectors: {
    title: string[];
    shopName: string[];
    /** 当前展示售价 */
    price: string[];
    /** 到手价 / 券后价（页面直接展示时才取得到） */
    finalPrice: string[];
    coupon: string[];
    originalPrice: string[];
    shippingCity: string[];
    /** 页面可见的登录昵称 / 会员标识节点 */
    userMarker: string[];
  };
  /** 登录态 cookie 键名白名单：只判断「键名是否存在」，绝不读取或上传 cookie 值 */
  loginCookieNames: string[];
}

export const PLATFORM_RULES: PlatformRule[] = [
  {
    id: 'taobao',
    name: '淘宝',
    hostPatterns: [/(^|\.)taobao\.com$/],
    productIdPatterns: [/[?&]id=(\d{5,})/],
    selectors: {
      title: [
        'span[class*="mainTitle--"]', // 2025 版商品主标题内层 span（实测类名 mainTitle--哈希，文本干净）
        '[class*="MainTitle--"]', // 2025 版主标题容器（注意区别于 tabDetailItemTitle 评价页签）
        '#J_Title .tb-main-title', // 旧版详情页标题
        'h1[class*="main-title"]', // 新版详情页标题
        '.tb-item-info .tb-main-title',
        '#J_Title h3',
        'h1[class*="title"]',
      ],
      shopName: [
        'span[class*="shopName--"]', // 2025 版店铺名内层 span（带 title 属性，文本干净）
        '.tb-shop-name',
        '[class*="ShopName--"]', // 新版 CSS Modules 店铺名类名
        '[class*="shopName"]',
        '[class*="ShopName"]',
        '.tb-seller-info .shop-name',
        '.shop-name',
      ],
      price: [
        // 2025 版到手价/售价高亮容器（文本如「平台加补后￥3188.55」）
        // 注意：宽松选择器 [class*="Price--"] / span[class*="priceText"] 已移除——
        // 实测会抓到无关数字（如「48」），价格只允许来自明确容器；
        // 简化渲染（状态A）的 unit--+text-- 组合由 extract.ts 的 pickUnitTextPrice 处理。
        '[class*="highlightPrice--"]',
        '.tb-rmb-num', // 经典价格节点
        '#J_PromoPriceNum .tb-rmb-num',
        '.tb-property .tb-rmb-num',
      ],
      finalPrice: [
        '[class*="finalPrice"]', // 券后到手价（页面直接展示时）
        '[class*="FinalPrice"]',
        '[class*="couponPrice"]',
        '.tb-promo-price .tb-rmb-num',
        '.price-final',
      ],
      coupon: [
        '[class*="couponInfoArea--"]', // 2025 版优惠信息区（「已享受:官方立减38元…」）
        '.tb-coupon',
        '[class*="coupon"]',
        '[class*="Coupon--"]',
        '.coupon-amount',
        '#J_Coupon',
      ],
      originalPrice: [
        '[class*="subPrice--"]', // 2025 版原价容器（文本如「优惠前￥3799」；无优惠时该节点不存在）
        '#J_StrPrice .tb-rmb-num', // 划线价
        '.tb-cancel-price',
        '[class*="originPrice"]',
        'del[class*="price"]',
        '.origin-price',
      ],
      shippingCity: [
        '[class*="deliveryAddrWrap--"]', // 2025 版发货地容器（「浙江嘉兴 至 北京市 海淀区」）
        '#J-From',
        '.tb-location',
        '[class*="deliveryAddress"]',
        '[class*="deliver"]',
        '.tb-deliver-to',
      ],
      userMarker: [
        '#J_SiteNavLogin .site-nav-login-info-nick', // 顶部导航昵称
        '.site-nav-user',
        '[class*="nickname"]',
        '[class*="userNick"]',
        '.member-info',
      ],
    },
    loginCookieNames: ['unb', '_nk_'],
  },
  {
    id: 'tmall',
    name: '天猫',
    hostPatterns: [/(^|\.)tmall\.com$/],
    productIdPatterns: [/[?&]id=(\d{5,})/],
    selectors: {
      title: [
        'span[class*="mainTitle--"]', // 2025 版商品主标题内层 span（实测类名 mainTitle--哈希，文本干净）
        '[class*="MainTitle--"]', // 2025 版主标题容器（注意区别于 tabDetailItemTitle 评价页签）
        '.tb-detail-hd h1', // 天猫详情页标题
        '#J_DetailMeta .tb-detail-hd h1',
        'h1[class*="main-title"]',
        '[class*="ItemTitle--"]',
        'h1[class*="title"]',
      ],
      shopName: [
        'span[class*="shopName--"]', // 2025 版店铺名内层 span（带 title 属性，文本干净）
        '#shopExtra .slogo-shopname', // 天猫店铺招牌
        '.slogo-shopname',
        '[class*="ShopName--"]', // 新版 CSS Modules 店铺名类名
        '[class*="shopName"]',
        '.shopLink',
        '[class*="ShopName"]',
      ],
      price: [
        // 2025 版到手价/售价高亮容器（淘宝天猫同版式）
        // 宽松选择器 [class*="Price--"] / span[class*="priceText"] 已移除（实测抓到无关数字）；
        // 简化渲染（状态A）的 unit--+text-- 组合由 extract.ts 的 pickUnitTextPrice 处理。
        '[class*="highlightPrice--"]',
        '.tm-price', // 天猫价
        '.tm-promo-price .tm-price',
        '.tb-rmb-num',
      ],
      finalPrice: [
        '[class*="finalPrice"]',
        '[class*="FinalPrice"]',
        '[class*="couponPrice"]',
        '.tm-promo-price .tm-price',
        '.price-final',
      ],
      coupon: [
        '[class*="couponInfoArea--"]', // 2025 版优惠信息区（「已享受:官方立减38元…」）
        '.tm-coupon',
        '[class*="coupon"]',
        '[class*="Coupon--"]',
        '.coupon-amount',
        '.tm-shop-coupon',
      ],
      originalPrice: [
        '[class*="subPrice--"]', // 2025 版原价容器（无优惠时该节点不存在）
        '.tm-yprice', // 天猫原价（划线价）
        '.tm-price-panel .tm-yprice',
        '[class*="originPrice"]',
        'del[class*="price"]',
        '.origin-price',
      ],
      shippingCity: [
        '[class*="deliveryAddrWrap--"]', // 2025 版发货地容器（「重庆 至 北京市 海淀区」）
        '#J-From',
        '.tm-location',
        '[class*="deliveryAddress"]',
        '[class*="deliver"]',
        '[class*="delivery"]',
      ],
      userMarker: [
        '#J_SiteNavLogin .site-nav-login-info-nick',
        '.site-nav-user',
        '[class*="nickname"]',
        '[class*="userNick"]',
        '.member-info',
      ],
    },
    loginCookieNames: ['unb', '_nk_'],
  },
  {
    id: 'jd',
    name: '京东',
    hostPatterns: [/(^|\.)jd\.com$/],
    productIdPatterns: [
      /item\.jd\.com\/(\d+)\.html/, // 京东商品页：item.jd.com/<sku>.html
      /[?&]skuId=(\d+)/,
    ],
    selectors: {
      title: [
        '#name h1', // 京东商品名
        '.sku-name',
        '#itemInfo #name h1',
        '.itemInfo-wrap .sku-name',
        'h1[class*="sku"]',
      ],
      shopName: [
        '#shopId', // 店铺链接节点
        '.pop-shop-name',
        '.shopName',
        '[class*="shop-name"]',
        '.crumb-wrap .contact .name',
      ],
      price: [
        '.p-price .price', // 京东价
        '#price .price',
        '.summary-price .price',
        'span.price',
        '[class*="priceJ"]',
      ],
      finalPrice: [
        '[class*="finalPrice"]',
        '.summary-price .p-price .price',
        '[class*="couponPrice"]',
        '.p-price .price',
        '[class*="FinalPrice"]',
      ],
      coupon: [
        '.quan-item', // 优惠券领取区
        '#coupon .quan',
        '[class*="coupon"]',
        '.youhui .quan-item',
        '[class*="Coupon"]',
      ],
      originalPrice: [
        '#page_maprice', // 京东划线价
        '.p-price del',
        '[class*="originPrice"]',
        'del.price',
        '.origin-price',
      ],
      shippingCity: [
        '#store-prompt', // 配送至/发货地（部分页面需展开配送面板才渲染）
        '[class*="sendAddress"]',
        '#summary .dd',
        '[class*="address"]',
        '.summary .dd',
      ],
      userMarker: [
        '#ttbar-login .nickname', // 顶栏昵称
        '.nickname',
        '[class*="userInfo"]',
        '.user-info',
        '[class*="userNick"]',
      ],
    },
    loginCookieNames: ['pin', 'pt_pin', 'pt_key'],
  },
  {
    id: 'pinduoduo',
    name: '拼多多',
    // 拼多多网页版（mobile.yangkeduo.com）页面结构改版频繁，
    // 以下选择器可能随改版失效，需要定期核对更新。
    hostPatterns: [/(^|\.)yangkeduo\.com$/],
    productIdPatterns: [
      /[?&]goods_id=(\d+)/, // 商品页参数 goods_id
      /[?&]goodsId=(\d+)/,
    ],
    selectors: {
      title: [
        '[class*="goods-name"]',
        '[class*="goodsName"]',
        '.goods-name',
        'h1[class*="title"]',
        'h1',
      ],
      shopName: [
        '[class*="mall-name"]', // 拼多多店铺常称「店铺/商场」
        '[class*="mallName"]',
        '[class*="shopName"]',
        '.mall-name',
        '[class*="shop-name"]',
      ],
      price: [
        '[class*="goods-price"]',
        '[class*="goodsPrice"]',
        '.goods-price',
        '[class*="price"]',
        '.price',
      ],
      finalPrice: [
        '[class*="finalPrice"]',
        '[class*="goodsPrice"]',
        '[class*="couponPrice"]',
        '.goods-price',
        '[class*="price"]',
      ],
      coupon: [
        '[class*="coupon"]',
        '[class*="Coupon"]',
        '.coupon-amount',
        '[class*="discount"]',
        '[class*="quan"]',
      ],
      originalPrice: [
        '[class*="originPrice"]',
        '[class*="market-price"]',
        'del[class*="price"]',
        '.origin-price',
        'del',
      ],
      shippingCity: [
        '[class*="delivery"]',
        '[class*="deliver"]',
        '[class*="address"]',
        '[class*="shipping"]',
        '[class*="from"]',
      ],
      userMarker: [
        '[class*="user-name"]',
        '[class*="nickName"]',
        '[class*="userName"]',
        '[class*="avatar"]',
        '[class*="user-info"]',
      ],
    },
    loginCookieNames: ['pdd_user_id', 'pdd_user_token'],
  },
];

/** 按 hostname 匹配平台规则；未命中返回 null */
export function findPlatformRule(hostname: string): PlatformRule | null {
  for (const rule of PLATFORM_RULES) {
    if (rule.hostPatterns.some((re) => re.test(hostname))) return rule;
  }
  return null;
}

/** 从完整 URL 提取商品 ID；全部模式未命中返回 null（即当前不是商品详情页） */
export function extractProductId(rule: PlatformRule, url: string): string | null {
  for (const re of rule.productIdPatterns) {
    const m = url.match(re);
    if (m && m[1]) return m[1];
  }
  return null;
}
