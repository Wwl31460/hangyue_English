// 在真实浏览器环境（Electron/Chromium）里用 SDK 调一次 hy_login，
// 用来验证 CORS 预检 + 来源校验是否放行——这决定安卓 WebView 能不能用。
import { createWorkBuddyCloud } from '@tencent-ai/workbuddy-cloud-sdk';

const ENDPOINT = 'https://hangyue-english.app.workbuddy.host';
const KEY = 'wbpk_ax6EubsOCr5M7E3MzPNr23_96r7HJritKmoevSoc6w69ucURYYtri82';

const w = window as any;
const out = document.getElementById('out')!;
w.probeState = 'running';

const cloud = createWorkBuddyCloud({ endpoint: ENDPOINT, publishableKey: KEY });

(async () => {
  try {
    w.probeOrigin = location.origin;
    const r: any = await (cloud.database as any).rpc('hy_login', {
      p_username: '测试同学',
      p_password: 'test123456',
    });
    w.probeResult = JSON.stringify({ error: r?.error ?? null, data: r?.data ?? null });
    out.textContent = 'error: ' + JSON.stringify(r?.error) + '\ndata: ' + JSON.stringify(r?.data);
  } catch (e: any) {
    w.probeResult = 'THROW: ' + String(e?.message || e);
    out.textContent = 'throw: ' + String(e?.message || e);
  } finally {
    w.probeState = 'done';
  }
})();
