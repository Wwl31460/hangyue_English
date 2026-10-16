// _cloud_probe.mjs —— 云服务连通性/来源(Origin)探针
// 目的：确认客户端能不能真的调通新后端；并单独验证「带 Origin 头」时服务端是否放行，
// 这决定安卓 WebView（Origin=https://localhost）与 Electron（file://）能否使用。
// 用法：node scripts/_cloud_probe.mjs            → 不带 Origin
//       node scripts/_cloud_probe.mjs <origin>   → 带上指定 Origin 头
import { createWorkBuddyCloud } from '@tencent-ai/workbuddy-cloud-sdk';

const ENDPOINT = 'https://hangyue-english.app.workbuddy.host';
const KEY = 'wbpk_ax6EubsOCr5M7E3MzPNr23_96r7HJritKmoevSoc6w69ucURYYtri82';
const origin = process.argv[2] || '';

// 浏览器会自动带 Origin；Node 不会。这里把 fetch 包一层，手动加上以模拟 WebView/浏览器环境。
const rawFetch = globalThis.fetch;
globalThis.fetch = (input, init = {}) => {
  if (origin) {
    const h = new Headers(init.headers || {});
    h.set('Origin', origin);
    init = { ...init, headers: h };
  }
  return rawFetch(input, init);
};

const cloud = createWorkBuddyCloud({ endpoint: ENDPOINT, publishableKey: KEY });

console.log('Origin 头      :', origin || '(不发送)');
try {
  const r = await cloud.database.rpc('hy_login', {
    p_username: '测试同学',
    p_password: 'test123456',
  });
  console.log('error          :', r?.error ? JSON.stringify(r.error) : 'null');
  console.log('data           :', JSON.stringify(r?.data));
} catch (e) {
  console.log('抛异常         :', String(e?.message || e));
}
