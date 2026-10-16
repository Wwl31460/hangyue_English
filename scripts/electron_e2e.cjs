// 端到端验证（走真实生产路径）：完全复刻 main.cjs 的协议注册 + UA 覆盖，
// 加载 dist 的 app://localhost/index.html，在真实渲染进程环境里跑一次 Edge-TTS 合成。
const { app, BrowserWindow, protocol, session } = require('electron');
const path = require('path');

const EDGE_UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
  '(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0';
app.userAgentFallback = EDGE_UA;

protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true, supportFetchAPI: true, stream: true } },
]);

const TOKEN = '6A5AA1D4EAFF4E9FB37E23D68491D6F4';
const GEC_VER = '2-143.0.3650.75';

const hardTimer = setTimeout(() => { console.log('STEP: HARD_TIMEOUT'); app.exit(9); }, 60000);

app.whenReady().then(async () => {
  const distDir = path.join(__dirname, '..', 'dist');
  session.defaultSession.setUserAgent(EDGE_UA);
  protocol.registerFileProtocol('app', (request, callback) => {
    let rel = request.url.replace(/^app:\/\//, '');
    rel = rel.replace(/^\/+/, '').replace(/^localhost\//, '').replace(/^\.\//, '');
    callback({ path: path.join(distDir, rel || 'index.html') });
  });

  const win = new BrowserWindow({ show: false, webPreferences: { contextIsolation: true, nodeIntegration: false } });
  await win.loadURL('app://localhost/index.html');
  console.log('STEP: app page loaded');

  const mod = await import('file://' + path.join(__dirname, '_drm_port.mjs').replace(/\\/g, '/'));
  const gec = mod.secMsGecV2();
  console.log('STEP: token generated');

  const script = `(async () => {
    const ua = navigator.userAgent;
    const secure = window.isSecureContext;
    const hasRU = !!(crypto && crypto.randomUUID);
    const cid = (hasRU ? crypto.randomUUID() : String(Math.random())).replace(/-/g, '');
    const url = 'wss://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1'
      + '?TrustedClientToken=${TOKEN}&Sec-MS-GEC=${gec}&Sec-MS-GEC-Version=${GEC_VER}&ConnectionId=' + cid;
    return await new Promise((resolve) => {
      let bytes = 0, settled = false;
      const ws = new WebSocket(url);
      ws.binaryType = 'arraybuffer';
      const tail = ' || isSecureContext=' + secure + ' hasRandomUUID=' + hasRU
        + ' cidOK=' + /^[0-9a-f]{32}$/i.test(cid) + ' hasEdg=' + /Edg\\//.test(ua);
      const done = (m) => { if (settled) return; settled = true; try { ws.close(); } catch (e) {} resolve(m + tail); };
      const timer = setTimeout(() => done('TIMEOUT'), 15000);
      ws.onopen = () => {
        ws.send('X-Timestamp:' + new Date().toString() + '\\r\\nContent-Type:application/json; charset=utf-8\\r\\nPath:speech.config\\r\\n\\r\\n'
          + '{"context":{"synthesis":{"audio":{"metadataoptions":{"sentenceBoundaryEnabled":"false","wordBoundaryEnabled":"false"},"outputFormat":"audio-24khz-48kbitrate-mono-mp3"}}}}\\r\\n');
        ws.send('X-RequestId:' + cid + '\\r\\nContent-Type:application/ssml+xml\\r\\nX-Timestamp:' + new Date().toString()
          + 'Z\\r\\nPath:ssml\\r\\n\\r\\n<speak version=\\'1.0\\' xmlns=\\'http://www.w3.org/2001/10/synthesis\\' xml:lang=\\'en-GB\\'><voice name=\\'en-GB-SoniaNeural\\'><prosody pitch=\\'+0Hz\\' rate=\\'+0%\\' volume=\\'+0%\\'>Welcome to English class.</prosody></voice></speak>');
      };
      ws.onmessage = (ev) => {
        if (typeof ev.data === 'string') { if (ev.data.includes('Path:turn.end')) { clearTimeout(timer); done('OK bytes=' + bytes); } return; }
        const buf = ev.data;
        if (!buf || buf.byteLength < 2) return;
        const hl = new DataView(buf).getUint16(0, false);
        const head = new TextDecoder().decode(new Uint8Array(buf, 2, hl));
        if (head.includes('Path:audio')) bytes += buf.byteLength - 2 - hl;
      };
      ws.onerror = () => { clearTimeout(timer); done('ERROR'); };
      ws.onclose = (e) => { if (!settled) { clearTimeout(timer); done('CLOSE code=' + e.code + ' reason=' + e.reason); } };
    });
  })()`;

  try {
    const result = await win.webContents.executeJavaScript(script);
    console.log('E2E_RESULT: ' + result);
    console.log('E2E_VERDICT: ' + (String(result).startsWith('OK') ? 'PASS' : 'FAIL'));
  } catch (e) {
    console.log('E2E_ERROR: ' + e.message);
  }
  clearTimeout(hardTimer);
  app.exit(0);
});
