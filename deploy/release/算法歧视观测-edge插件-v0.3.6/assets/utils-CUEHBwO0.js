const MSG = {
  START_COLLECTION: "START_COLLECTION",
  EXTRACT_PAGE_DATA: "EXTRACT_PAGE_DATA",
  TEST_CONNECTION: "TEST_CONNECTION",
  AUTO_COLLECT: "AUTO_COLLECT",
  RETRY_FAILED: "RETRY_FAILED"
};
const STORAGE_KEYS = {
  CONSENT: "consent",
  AUTO_COLLECT: "autoCollect",
  API_ENDPOINT: "apiEndpoint",
  API_KEY: "apiKey",
  MASK_SHOP: "maskShopName",
  MASK_USER: "maskUserMarker",
  OBSERVATIONS: "observations",
  ANON_ID: "anonymousUserId",
  LAST_RESULT: "lastCollectionResult",
  /** 自动采集跨页面去重：{ [productId]: 时间戳 } */
  LAST_AUTO_COLLECT: "lastAutoCollect"
};
const DEFAULT_API_ENDPOINT = "http://127.0.0.1:8000/api/observations";
const DEFAULT_API_KEY = "dev-key-123";
const MAX_LOCAL_RECORDS = 500;
function errMsg(e) {
  return e instanceof Error ? e.message : String(e);
}
function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}
function maskText(text) {
  const t = text.trim();
  if (!t) return t;
  return `${t[0]}*`;
}
export {
  DEFAULT_API_KEY as D,
  MSG as M,
  STORAGE_KEYS as S,
  DEFAULT_API_ENDPOINT as a,
  MAX_LOCAL_RECORDS as b,
  escapeHtml as c,
  errMsg as e,
  maskText as m
};
