// UA 对照实验：验证 Bing Edge-TTS 服务端是否要求 User-Agent 含 "Edg/"
// 用法：electron _ua_ab_test.cjs "<UA 字符串>"
const { app, BrowserWindow, protocol, session } = require('electron');
const path = require('path');

const TEST_UA = process.argv[2] || 'DEFAULT';
const DIST = path.join(__dirname, '..', 'dist');

const TOKEN = '6A5AA1D4EAFF4E9FB37E23D68491D6F4';
const GEC_VER = '2-143.0.3650.75';

if (TEST_UA !== 'DEFAULT') app.userAgentFallback = TEST_UA;

protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true, supportFetchAPI: true, stream: true } },
]);

const hardTimer = setTimeout(() => {
  console.log('RESULT: HARD_TIMEOUT');
  app.exit(9);
}, 60000);

app.whenReady().then(async () => {
  if (TEST_UA !== 'DEFAULT') session.defaultSession.setUserAgent(TEST_UA);

  protocol.registerFileProtocol('app', (request, callback) => {
    let rel = request.url.replace(/^app:\/\//, '').replace(/#.*$/, '').replace(/\?.*$/, '');
    rel = rel.replace(/^\/+/, '').replace(/^localhost\//, '').replace(/^\.\//, '');
    callback({ path: path.join(DIST, rel || 'index.html') });
  });

  const win = new BrowserWindow({ show: false, webPreferences: { contextIsolation: true } });
  await win.loadURL('app://localhost/index.html');

  const mod = await import('file://' + path.join(__dirname, '_drm_port.mjs').replace(/\\/g, '/'));
  const gec = mod.secMsGecV2();

  console.log('测试 UA: ' + TEST_UA);
  console.log('  UA 含 Edg/ ? ' + /Edg\//.test(TEST_UA));

  const script = `(async () => {
    const ua = navigator.userAgent;
    const cid = Array.from({length: 32}, () => '0123456789abcdef'[Math.floor(Math.random()*16)]).join('');
    const url = 'wss://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1'
      + '?TrustedClientToken=${TOKEN}&Sec-MS-GEC=${gec}&Sec-MS-GEC-Version=${GEC_VER}&ConnectionId=' + cid;
    return await new Promise((resolve) => {
      let bytes = 0, settled = false;
      const ws = new WebSocket(url);
      ws.binaryType = 'arraybuffer';
      const tail = ' | 实际UA含Edg/=' + /Edg\\//.test(ua);
      const done = (m) => { if (settled) return; settled = true; try { ws.close(); } catch(e){} resolve(m + tail); };
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
      ws.onerror = () => { clearTimeout(timer); done('ERROR(握手被拒)'); };
      ws.onclose = (e) => { if (!settled) { clearTimeout(timer); done('CLOSE code=' + e.code); } };
    });
  })()`;

  try {
    const r = await win.webContents.executeJavaScript(script);
    console.log('  → 合成结果: ' + r);
  } catch (e) {
    console.log('  执行出错: ' + e.message);
  }
  clearTimeout(hardTimer);
  app.exit(0);
});
