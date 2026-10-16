// Edge-TTS（微软 Edge 在线朗读）前端实现：通过 WebSocket 合成自然真人感语音。
// 默认英式女声 en-GB-SoniaNeural —— 单词清晰、语调自然，不机械平板。
// 需联网；合成失败时由 tts.ts 自动回退到系统语音。
//
// 协议（对齐官方 edge-tts）：
//   1) 连接 wss://speech.platform.bing.com/.../edge/v1，URL 带 TrustedClientToken / Sec-MS-GEC / Sec-MS-GEC-Version / ConnectionId
//   2) 先发 speech.config，再发 SSML
//   3) 收二进制音频分片（前 2 字节大端为头长度，头里 Path:audio 才是音频），收到文本 turn.end 即结束
//
// 关键：微软 2025 起把 Sec-MS-GEC 升级为 v2 令牌（"<16位CS64>-<64位SHA256>"），
// 旧版 v1（单纯 SHA256）会被服务端拒绝。v2 用的是自定义混淆 SHA256 + CS64 摘要，
// 下面为 drm.py 的等值纯整数移植（已与官方 Python 逐时间戳比对一致）。

const TRUSTED_CLIENT_TOKEN = '6A5AA1D4EAFF4E9FB37E23D68491D6F4';
const WSS_URL = 'wss://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1';
const CHROMIUM_FULL_VERSION = '143.0.3650.75';
const SEC_MS_GEC_VERSION = `2-${CHROMIUM_FULL_VERSION}`;
const WIN_EPOCH = 11644473600; // Windows 文件时间与 Unix 时间的秒差
const MASK = 0xffffffff;

export const DEFAULT_EDGE_VOICE = 'en-GB-SoniaNeural';

// —— Sec-MS-GEC v2 令牌所需的常量表 ——
const SHA256_INITIAL = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19];
const SHA256_STATE = [0xfd9fbea2, 0x91243ce7, 0xbe499094, 0xcd2e1e0a, 0x6c006f49, 0x04bd35ab, 0xfeb0a7e4, 0x03effbd2];
const SHA256_SCHEDULE = [
  0xeb24bf9e, 0x1558691f, 0xa0c09ee2, 0x0cfa32ba, 0xa622ee8c, 0xd1dd9491, 0xc0dd25a0,
  0xf9e70ab6, 0xf0c31573, 0x7058ce4e, 0x7188e606, 0x00e5ab33, 0xd258b060, 0x72766564,
];
const K = [
  0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
  0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
  0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
  0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
  0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
  0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
  0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
];
const SHA256_ADJUSTMENT = 0xc9dc06a7;
const BLOCK_CONSTANTS = [...K.slice(0, 14), SHA256_ADJUSTMENT, ...K.slice(15)];
const SIGMA0_ADJ = 0x059c0b80;
const SIGMA1_ADJ = 0x000b92c0;
const CS64_COEFFICIENTS: Array<[number, number]> = [
  [0xe82e91b1, 0xb32700d0], [0x44de24c6, 0x88dff51d], [0x3beb65bc, 0x29514038], [0xc89c5933, 0xb328cbdf],
  [0x8d1ec211, 0xd405b4d5], [0x314ef5d5, 0x26e55f3c], [0xe92491b1, 0x607801c6], [0xf0a5b9d5, 0x82b2c1fb],
  [0x06064cf3, 0xfa51a3da], [0xda79fa60, 0x207cc464], [0xbed20560, 0x3c3c74f3], [0x89f9c9f8, 0xd2d14b61],
  [0x35fa38c6, 0xbb04a2c1], [0xcb49e3c6, 0xc5626167],
];
const CS64_FACTOR = 0x82893933;
const CS64_ADJ0 = 0xf2f90b1a;
const CS64_ADJ1 = 0x0b1a0000;

const u32 = (x: number) => x >>> 0;
const mul = (a: number, b: number) => Math.imul(a | 0, b | 0) >>> 0;
const rotr = (v: number, n: number) => ((v >>> n) | (v << (32 - n))) >>> 0;
const rol16 = (v: number) => (((v & MASK) << 16) | ((v & MASK) >>> 16)) >>> 0;
const sigma0 = (v: number) => (rotr(v, 7) ^ rotr(v, 18) ^ (v >>> 3)) >>> 0;
const sigma1 = (v: number) => (rotr(v, 17) ^ rotr(v, 19) ^ (v >>> 10)) >>> 0;

// 执行 SHA-256 轮函数；firstRound=14 表示从首块的末段续跑
function sha256Rounds(state: number[], words: number[], firstRound = 0): number[] {
  let [a, b, c, d, e, f, g, h] = state;
  const constants = firstRound === 14 ? BLOCK_CONSTANTS : K;
  for (let i = firstRound; i < 64; i++) {
    const S1 = (rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)) >>> 0;
    const ch = (g ^ (e & (f ^ g))) >>> 0;
    const t1 = (h + S1 + ch + constants[i] + words[i]) >>> 0;
    const S0 = (rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)) >>> 0;
    const maj = ((a & b) | (c & (a | b))) >>> 0;
    h = g; g = f; f = e; e = (d + t1) >>> 0; d = c; c = b; b = a;
    a = (t1 + S0 + maj) >>> 0;
  }
  return [a, b, c, d, e, f, g, h];
}

// 消息扩展：从 firstWord 起补齐到 64 字
function expandSchedule(words: number[], firstWord = 16) {
  for (let i = firstWord; i < 64; i++) {
    words.push((sigma1(words[i - 2]) + words[i - 7] + sigma0(words[i - 15]) + words[i - 16]) >>> 0);
  }
}

// 由前 7 字节推出初始状态（利用预置常量表跳过可预测的轮次）
function sha256Init(head7: Uint8Array): number[] {
  const words: number[] = new Array(14).fill(0);
  words.push(((head7[0] << 16) | (head7[1] << 8) | head7[2]) >>> 0);
  words.push(((head7[3] << 24) | (head7[4] << 16) | (head7[5] << 8) | head7[6]) >>> 0);
  for (let i = 16; i < 30; i++) {
    let value = SHA256_SCHEDULE[i - 16];
    if (i - 2 >= 14) value += i === 16 ? sigma1(words[i - 2]) ^ SIGMA1_ADJ : sigma1(words[i - 2]);
    if (i - 7 >= 14) value += words[i - 7];
    if (i - 15 >= 14) value += i === 29 ? sigma0(words[i - 15]) ^ SIGMA0_ADJ : sigma0(words[i - 15]);
    words.push(value & MASK);
  }
  words.push((sigma1(words[28]) + words[23] + sigma0(words[15]) + words[14] + SHA256_ADJUSTMENT - K[14]) & MASK);
  expandSchedule(words, 31);
  const working = sha256Rounds(SHA256_STATE, words, 14);
  return SHA256_INITIAL.map((x, i) => (x + working[i]) & MASK);
}

// 计算 32 字节摘要（大端序）
function sha256Digest(data: Uint8Array): Uint8Array {
  const length = 57 + data.length;
  const padded: number[] = [...data.subarray(7), 0x80];
  const zeros = (((55 - length) % 64) + 64) % 64;
  for (let i = 0; i < zeros; i++) padded.push(0);
  let bitLen = length * 8;
  const tail: number[] = [];
  for (let i = 0; i < 8; i++) { tail.unshift(bitLen & 0xff); bitLen = Math.floor(bitLen / 256); }
  padded.push(...tail);

  let state = sha256Init(data.subarray(0, 7));
  for (let off = 0; off < padded.length; off += 64) {
    const words: number[] = [];
    for (let i = 0; i < 16; i++) {
      words.push(((padded[off + i * 4] << 24) | (padded[off + i * 4 + 1] << 16) | (padded[off + i * 4 + 2] << 8) | padded[off + i * 4 + 3]) >>> 0);
    }
    expandSchedule(words);
    const working = sha256Rounds(state, words);
    state = state.map((x, i) => (x + working[i]) & MASK);
  }
  const bytes = new Uint8Array(32);
  state.forEach((x, i) => {
    bytes[i * 4] = (x >>> 24) & 0xff;
    bytes[i * 4 + 1] = (x >>> 16) & 0xff;
    bytes[i * 4 + 2] = (x >>> 8) & 0xff;
    bytes[i * 4 + 3] = x & 0xff;
  });
  return bytes;
}

// 把数据切成小端 32 位字（前置一个 0x00，补齐到偶数个）
function wordsLe4Even(data: Uint8Array): number[] {
  const buf = new Uint8Array(1 + data.length);
  buf.set(data, 1);
  const total = buf.length + ((4 - (buf.length % 4)) % 4);
  const words: number[] = [];
  for (let i = 0; i < total; i += 4) {
    words.push(((buf[i] || 0) | ((buf[i + 1] || 0) << 8) | ((buf[i + 2] || 0) << 16) | ((buf[i + 3] || 0) << 24)) >>> 0);
  }
  if (words.length % 2) words.push(0);
  return words;
}

// CS64 摘要：取摘要前 8 字节作两个密钥，做两轮混合
function cs64Digest(data: Uint8Array, digest: Uint8Array): [number, number] {
  const keyA = ((digest[0] | (digest[1] << 8) | (digest[2] << 16) | (digest[3] << 24)) | 1) >>> 0;
  const keyB = ((digest[4] | (digest[5] << 8) | (digest[6] << 16) | (digest[7] << 24)) | 1) >>> 0;
  const factors = [mul(keyA, CS64_FACTOR), mul(keyB, CS64_FACTOR)];
  const terms = CS64_COEFFICIENTS.map(([c], i) => mul(c, factors[i % 2]));
  const offsets = CS64_COEFFICIENTS.map(([, o]) => u32(o));

  wordsLe4Even(data).forEach((word, index) => {
    let term = mul(word, index % 2 === 0 ? keyA : keyB);
    let offset = mul(rol16(word), index % 2 === 0 ? 0xef0569fb : 0xc31713db);
    if (index === 0) {
      term = u32(term + mul(CS64_ADJ0, factors[0]));
      offset = u32(offset + CS64_ADJ1);
    }
    terms.push(term);
    offsets.push(offset);
  });

  let swapAcc = 0, swapLast = 0, state = 0, acc = 0;
  for (let i = 0; i < terms.length; i += 2) {
    const x = terms[i], y = terms[i + 1];
    let t = rol16(u32(offsets[i] + x));
    let q = mul(t, 0x76f50f34);
    swapAcc = u32(swapAcc + u32(mul(rol16(q), 0xc3efea97) + q));
    t = rol16(u32(offsets[i + 1] + y));
    q = mul(t, 0x1881ce3c);
    swapLast = u32(mul(rol16(q), 0x35bd1ec9) + q);
    swapAcc = u32(swapAcc + swapLast);

    state = u32(mul(state, keyA) + x);
    state = mul(rol16(state), 0xcf98b111);
    state = mul(rol16(state), 0x87085b9f);
    state = mul(rol16(state), 0x12ceb96d);
    state = mul(rol16(state), 0x257e1d83);
    acc = u32(acc + state);
    t = u32(mul(state, keyB) + y);
    t = mul(rol16(t), 0xa27416f5);
    t = mul(rol16(t), 0xd38396ff);
    state = mul(rol16(mul(rol16(t), 0x7c932b89)), 0xbfa49f69);
    acc = u32(acc + state);
  }
  return [u32(swapLast ^ state), u32(swapAcc ^ acc)];
}

const hexLE32 = (v: number) =>
  [v & 0xff, (v >>> 8) & 0xff, (v >>> 16) & 0xff, (v >>> 24) & 0xff]
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('')
    .toUpperCase();

// 生成 v2 令牌；同一 5 分钟窗口内复用（与官方 lru_cache 行为一致）
let gecCache = { key: '', value: '' };
function secMsGec(now = Date.now() / 1000): string {
  let ticks = now + WIN_EPOCH;
  ticks -= ticks % 300; // 向下取整到 5 分钟
  ticks *= 1e7;
  const key = ticks.toFixed(0);
  if (gecCache.key === key) return gecCache.value;
  const data = new TextEncoder().encode(key + TRUSTED_CLIENT_TOKEN);
  const digest = sha256Digest(data);
  const [w0, w1] = cs64Digest(data, digest);
  const sha = Array.from(digest).map((x) => x.toString(16).padStart(2, '0')).join('').toUpperCase();
  const value = `${hexLE32(w0)}${hexLE32(w1)}-${sha}`;
  gecCache = { key, value };
  return value;
}

// 生成无连字符的 32 位十六进制 UUID。
// 服务端要求 X-RequestId / ConnectionId 必须是这种"无连字符 UUID"，否则直接以 1002 断开。
function uuid(): string {
  const bytes = new Uint8Array(16);
  if (globalThis.crypto?.getRandomValues) globalThis.crypto.getRandomValues(bytes);
  else for (let i = 0; i < 16; i++) bytes[i] = (Math.random() * 256) | 0;
  bytes[6] = (bytes[6] & 0x0f) | 0x40; // 版本 4
  bytes[8] = (bytes[8] & 0x3f) | 0x80; // 变体 10xx
  return Array.from(bytes, (b) => b.toString(16).padStart(2, '0')).join('');
}

// 微软要求的时间戳格式（JS Date.toString 风格，但固定为 GMT）
function jsDateString(): string {
  const d = new Date();
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const mons = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const p = (n: number) => String(n).padStart(2, '0');
  return `${days[d.getUTCDay()]} ${mons[d.getUTCMonth()]} ${p(d.getUTCDate())} ${d.getUTCFullYear()} ` +
    `${p(d.getUTCHours())}:${p(d.getUTCMinutes())}:${p(d.getUTCSeconds())} GMT+0000 (Coordinated Universal Time)`;
}

function escapeXml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

export interface EdgeSynthOptions {
  voice?: string; // 形如 en-GB-SoniaNeural；非法值回退默认音色
  rate?: number; // 1 = 正常语速；0.9 → -10%
}

// 会话内缓存：同一句/词只合成一次（保存对象 URL）
const cache = new Map<string, string>();
const CACHE_MAX = 600;

// 同一句并发请求时共用同一次合成，避免重复建连（预热与正式播放会同时触发）
const inflight = new Map<string, Promise<string>>();

function cacheSet(key: string, url: string) {
  if (cache.size >= CACHE_MAX) {
    const first = cache.keys().next().value;
    if (first !== undefined) {
      const old = cache.get(first);
      if (old) URL.revokeObjectURL(old);
      cache.delete(first);
    }
  }
  cache.set(key, url);
}

export function clearEdgeCache() {
  for (const u of cache.values()) URL.revokeObjectURL(u);
  cache.clear();
}

// 合成一段文本，返回可播放的音频对象 URL
export function synthesizeEdge(text: string, opts: EdgeSynthOptions = {}): Promise<string> {
  const voice = opts.voice && /Neural$/i.test(opts.voice) ? opts.voice : DEFAULT_EDGE_VOICE;
  const rate = opts.rate ?? 0.9;
  const key = `${voice}|${rate}|${text}`;
  const hit = cache.get(key);
  if (hit) return Promise.resolve(hit);
  const pending = inflight.get(key);
  if (pending) return pending;

  const endpoint =
    `${WSS_URL}?TrustedClientToken=${TRUSTED_CLIENT_TOKEN}` +
    `&Sec-MS-GEC=${secMsGec()}&Sec-MS-GEC-Version=${SEC_MS_GEC_VERSION}&ConnectionId=${uuid()}`;

  const p = new Promise<string>((resolve, reject) => {
    let settled = false;
    const chunks: ArrayBuffer[] = [];
    // 注意：不能请求子协议，服务端不会回显，浏览器会因此判定握手失败
    const ws = new WebSocket(endpoint);
    ws.binaryType = 'arraybuffer';

    const timer = window.setTimeout(() => finish(false, new Error('Edge-TTS 超时')), 12000);

    function finish(ok: boolean, val?: unknown) {
      if (settled) return;
      settled = true;
      window.clearTimeout(timer);
      try { ws.close(); } catch { /* ignore */ }
      if (ok) {
        const blob = new Blob(chunks, { type: 'audio/mpeg' });
        const objUrl = URL.createObjectURL(blob);
        cacheSet(key, objUrl);
        resolve(objUrl);
      } else {
        reject(val instanceof Error ? val : new Error('Edge-TTS 失败'));
      }
    }

    ws.onopen = () => {
      ws.send(
        `X-Timestamp:${jsDateString()}\r\nContent-Type:application/json; charset=utf-8\r\nPath:speech.config\r\n\r\n` +
          '{"context":{"synthesis":{"audio":{"metadataoptions":{"sentenceBoundaryEnabled":"false","wordBoundaryEnabled":"false"},"outputFormat":"audio-24khz-48kbitrate-mono-mp3"}}}}\r\n',
      );
      const ratePct = Math.round((rate - 1) * 100);
      const ssml =
        `<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-GB'>` +
        `<voice name='${voice}'><prosody pitch='+0Hz' rate='${ratePct >= 0 ? '+' : ''}${ratePct}%' volume='+0%'>` +
        `${escapeXml(text)}</prosody></voice></speak>`;
      ws.send(
        `X-RequestId:${uuid()}\r\nContent-Type:application/ssml+xml\r\n` +
          `X-Timestamp:${jsDateString()}Z\r\nPath:ssml\r\n\r\n${ssml}`,
      );
    };

    ws.onmessage = (ev) => {
      if (typeof ev.data === 'string') {
        if (ev.data.includes('Path:turn.end')) finish(true);
        return;
      }
      const buf = ev.data as ArrayBuffer;
      if (!buf || buf.byteLength < 2) return;
      const headerLen = new DataView(buf).getUint16(0, false);
      const header = new TextDecoder().decode(new Uint8Array(buf, 2, headerLen));
      if (!header.includes('Path:audio')) return; // 跳过 turn.start 等无音频分片
      const payload = buf.slice(2 + headerLen);
      if (payload.byteLength > 0) chunks.push(payload);
    };

    ws.onerror = () => finish(false, new Error('Edge-TTS 连接错误'));
    ws.onclose = () => {
      if (settled) return;
      if (chunks.length > 0) finish(true);
      else finish(false, new Error('Edge-TTS 连接关闭'));
    };
  });

  inflight.set(key, p);
  p.then(
    () => inflight.delete(key),
    () => inflight.delete(key),
  );
  return p;
}
