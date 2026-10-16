// 无缝性验证：在真实 Electron 渲染进程里
//   1) 合成 3 句真实语音并解码
//   2) 统计首尾静音裁剪量
//   3) 用 OfflineAudioContext 把 3 句按时间轴排布后离线渲染，
//      扫描渲染出的 PCM，看句与句之间还有多长的静默空档
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
const hardTimer = setTimeout(() => { console.log('STEP: HARD_TIMEOUT'); app.exit(9); }, 90000);

app.whenReady().then(async () => {
  session.defaultSession.setUserAgent(EDGE_UA);
  protocol.registerFileProtocol('app', (request, callback) => {
    let rel = request.url.replace(/^app:\/\//, '');
    rel = rel.replace(/^\/+/, '').replace(/^localhost\//, '').replace(/^\.\//, '');
    callback({ path: path.join(__dirname, '..', 'dist', rel || 'index.html') });
  });
  const win = new BrowserWindow({ show: false, webPreferences: { contextIsolation: true, nodeIntegration: false } });
  await win.loadURL('app://localhost/index.html');
  console.log('STEP: page loaded');

  const mod = await import('file://' + path.join(__dirname, '_drm_port.mjs').replace(/\\/g, '/'));
  const gec = mod.secMsGecV2();

  const script = `(async () => {
    const TOKEN = '${TOKEN}', GEC = '${gec}', VER = '${GEC_VER}';
    const cid = () => crypto.randomUUID().replace(/-/g, '');
    function synth(text) {
      return new Promise((resolve, reject) => {
        const chunks = []; let settled = false;
        const ws = new WebSocket('wss://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1'
          + '?TrustedClientToken=' + TOKEN + '&Sec-MS-GEC=' + GEC + '&Sec-MS-GEC-Version=' + VER + '&ConnectionId=' + cid());
        ws.binaryType = 'arraybuffer';
        const done = (ok, v) => { if (settled) return; settled = true; try { ws.close(); } catch (e) {} ok ? resolve(v) : reject(v); };
        setTimeout(() => done(false, new Error('timeout')), 15000);
        ws.onopen = () => {
          ws.send('X-Timestamp:' + new Date().toString() + '\\r\\nContent-Type:application/json; charset=utf-8\\r\\nPath:speech.config\\r\\n\\r\\n'
            + '{"context":{"synthesis":{"audio":{"metadataoptions":{"sentenceBoundaryEnabled":"false","wordBoundaryEnabled":"false"},"outputFormat":"audio-24khz-48kbitrate-mono-mp3"}}}}\\r\\n');
          ws.send('X-RequestId:' + cid() + '\\r\\nContent-Type:application/ssml+xml\\r\\nX-Timestamp:' + new Date().toString()
            + 'Z\\r\\nPath:ssml\\r\\n\\r\\n<speak version=\\'1.0\\' xmlns=\\'http://www.w3.org/2001/10/synthesis\\' xml:lang=\\'en-GB\\'><voice name=\\'en-GB-SoniaNeural\\'><prosody pitch=\\'+0Hz\\' rate=\\'+0%\\' volume=\\'+0%\\'>' + text + '</prosody></voice></speak>');
        };
        ws.onmessage = (ev) => {
          if (typeof ev.data === 'string') { if (ev.data.includes('Path:turn.end')) done(true, new Blob(chunks, {type:'audio/mpeg'})); return; }
          const b = ev.data; if (!b || b.byteLength < 2) return;
          const hl = new DataView(b).getUint16(0, false);
          if (new TextDecoder().decode(new Uint8Array(b, 2, hl)).includes('Path:audio')) chunks.push(b.slice(2 + hl));
        };
        ws.onerror = () => done(false, new Error('ws error'));
        ws.onclose = () => { if (!settled) done(chunks.length ? true : false, chunks.length ? new Blob(chunks, {type:'audio/mpeg'}) : new Error('closed')); };
      });
    }

    const TH = 0.005, HEAD_PAD = 0.008, TAIL_PAD = 0.025, FADE = 0.006, MIN_KEEP = 0.12;
    function bounds(buf) {
      const chs = buf.numberOfChannels, len = buf.length, d = [];
      for (let c = 0; c < chs; c++) d.push(buf.getChannelData(c));
      const loud = (i) => { let m = 0; for (let c = 0; c < chs; c++) { const v = Math.abs(d[c][i]); if (v > m) m = v; } return m; };
      let s = 0, e = len - 1;
      while (s < len && loud(s) < TH) s++;
      while (e > s && loud(e) < TH) e--;
      return [s, e];
    }
    function trim(ctx, buf) {
      const sr = buf.sampleRate, chs = buf.numberOfChannels, len = buf.length;
      const [s0, e0] = bounds(buf);
      if (s0 >= e0) return { buf, head: 0, tail: 0 };
      const s = Math.max(0, s0 - Math.round(HEAD_PAD * sr));
      const e = Math.min(len - 1, e0 + Math.round(TAIL_PAD * sr));
      const segLen = e - s + 1;
      if (segLen / sr < MIN_KEEP) return { buf, head: 0, tail: 0 };
      const out = ctx.createBuffer(chs, segLen, sr);
      const fade = Math.min(Math.round(FADE * sr), Math.floor(segLen / 8));
      for (let c = 0; c < chs; c++) {
        const src = buf.getChannelData(c).subarray(s, e + 1), dst = out.getChannelData(c);
        dst.set(src);
        for (let i = 0; i < fade; i++) { const k = i / fade; dst[i] *= k; dst[segLen - 1 - i] *= k; }
      }
      return { buf: out, head: (s0 - s) / sr, tail: (e - e0) / sr, raw: { s: s0 / sr, e: (len - 1 - e0) / sr } };
    }
    // 扫描 PCM 中长于 minMs 的静默段（用于证明确实没有空档）
    function silentRuns(buf, minMs) {
      const chs = buf.numberOfChannels, len = buf.length, sr = buf.sampleRate, d = [];
      for (let c = 0; c < chs; c++) d.push(buf.getChannelData(c));
      const runs = []; let run = 0;
      for (let i = 0; i < len; i++) {
        let m = 0; for (let c = 0; c < chs; c++) { const v = Math.abs(d[c][i]); if (v > m) m = v; }
        if (m < TH) { run++; } else { if (run / sr * 1000 >= minMs) runs.push({ at: (i - run) / sr, ms: run / sr * 1000 }); run = 0; }
      }
      if (run / sr * 1000 >= minMs) runs.push({ at: (len - run) / sr, ms: run / sr * 1000 });
      return runs;
    }

    const texts = ['Good morning, everyone.', 'This is my new school.', 'I like my English teacher very much.'];
    const dec = new AudioContext();
    const blobs = [];
    for (const t of texts) blobs.push(await synth(t));

    // —— 原始（未裁）时长 ——
    const raws = [];
    for (const b of blobs) raws.push(await dec.decodeAudioData(await b.arrayBuffer()));
    const trims = raws.map((r) => trim(dec, r));

    const report = trims.map((t, i) => ({
      i, rawSec: +raws[i].duration.toFixed(3), trimmedSec: +t.buf.duration.toFixed(3),
      leadSilenceMs: t.raw ? +(t.raw.s * 1000).toFixed(0) : 0,
      tailSilenceMs: t.raw ? +(t.raw.e * 1000).toFixed(0) : 0,
      cutHeadMs: +(t.head * 1000).toFixed(0), cutTailMs: +(t.tail * 1000).toFixed(0),
    }));

    // —— A: 不裁、按各自原始时长紧凑排布（等价于旧行为里"拼起来"的理想情况）——
    const totalRaw = raws.reduce((s, r) => s + r.duration, 0) + 0.12 * (raws.length - 1);
    const oacA = new OfflineAudioContext(1, Math.ceil(totalRaw * dec.sampleRate), dec.sampleRate);
    { let cur = 0.06; for (const r of raws) { const s = oacA.createBufferSource(); s.buffer = r; s.connect(oacA.destination); s.start(cur); cur += r.duration + 0.12; } }
    const outA = await oacA.startRendering();

    // —— B: 裁剪后按音频时间轴紧密排布（本次修复的方案）——
    const totalB = trims.reduce((s, t) => s + t.buf.duration, 0) + 0.35 * (trims.length - 1);
    const oacB = new OfflineAudioContext(1, Math.ceil((totalB + 0.2) * dec.sampleRate), dec.sampleRate);
    { let cur = 0.06; trims.forEach((t, i) => { const s = oacB.createBufferSource(); s.buffer = t.buf; s.connect(oacB.destination); s.start(cur); cur += t.buf.duration + (i < trims.length - 1 ? 0.35 : 0); }); }
    const outB = await oacB.startRendering();

    return JSON.stringify({
      report,
      gapsA: silentRuns(outA, 20).map((r) => +r.at.toFixed(2) + 's/' + +r.ms.toFixed(0) + 'ms'),
      gapsB: silentRuns(outB, 20).map((r) => +r.at.toFixed(2) + 's/' + +r.ms.toFixed(0) + 'ms'),
      junctionB: (() => { const js = []; let cur = 0.06; trims.forEach((t, i) => { cur += t.buf.duration + (i < trims.length - 1 ? 0.35 : 0); if (i < trims.length - 1) js.push(+(cur - 0.35).toFixed(3)); }); return js; })(),
      junctionA: (() => { const js = []; let cur = 0.06; for (const r of raws) { cur += r.duration; js.push(+cur.toFixed(3)); } return js.slice(0, -1); })(),
      totalA: +outA.duration.toFixed(2), totalB: +outB.duration.toFixed(2),
    });
  })()`;

  try {
    const r = await win.webContents.executeJavaScript(script);
    const o = JSON.parse(r);
    console.log('E2E: 每句裁剪情况');
    for (const x of o.report) {
      console.log(`  #${x.i + 1} 原始 ${x.rawSec}s → 裁剪后 ${x.trimmedSec}s | 原首静音 ${x.leadSilenceMs}ms 原尾静音 ${x.tailSilenceMs}ms | 保留首 ${x.cutHeadMs}ms 尾 ${x.cutTailMs}ms`);
    }
    console.log('E2E: 20ms 以上的静默段（位置/时长）');
    console.log('  修复前: ' + JSON.stringify(o.gapsA));
    console.log('  修复后: ' + JSON.stringify(o.gapsB));
    console.log('  句间留白起点: ' + JSON.stringify(o.junctionB));
    console.log('  修复后全部静默段: ' + JSON.stringify(o.gapsB));
    console.log('E2E: 总时长 ' + o.totalA + 's → ' + o.totalB + 's');
    const atJ = (list, js) => list.filter((s) => { const t = parseFloat(s); return js.some((j) => Math.abs(j - t) < 0.12); });
    const gab = atJ(o.gapsB, o.junctionB);
    console.log('E2E_VERDICT: 句间(junction)静默 ' + (gab.length ? JSON.stringify(gab) : '均已 <20ms') );
  } catch (e) {
    console.log('E2E_ERROR: ' + e.message);
  }
  clearTimeout(hardTimer);
  app.exit(0);
});
