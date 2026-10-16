// 将 edge-tts 的 drm.py（v2 Sec-MS-GEC 令牌）移植到 JS，用于 Node 侧比对验证。
const MASK = 0xffffffff;
const WIN_EPOCH = 11644473600;
const TRUSTED_CLIENT_TOKEN = '6A5AA1D4EAFF4E9FB37E23D68491D6F4';

const SHA256_INITIAL = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19];
const SHA256_STATE = [0xfd9fbea2, 0x91243ce7, 0xbe499094, 0xcd2e1e0a, 0x6c006f49, 0x04bd35ab, 0xfeb0a7e4, 0x03effbd2];
const SHA256_SCHEDULE = [0xeb24bf9e, 0x1558691f, 0xa0c09ee2, 0x0cfa32ba, 0xa622ee8c, 0xd1dd9491, 0xc0dd25a0, 0xf9e70ab6, 0xf0c31573, 0x7058ce4e, 0x7188e606, 0x00e5ab33, 0xd258b060, 0x72766564];
const K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2];
const SHA256_ADJUSTMENT = 0xc9dc06a7;
const BLOCK_CONSTANTS = [...K.slice(0, 14), SHA256_ADJUSTMENT, ...K.slice(15)];
const SIGMA0_ADJ = 0x059c0b80;
const SIGMA1_ADJ = 0x000b92c0;
const CS64_COEFFICIENTS = [[0xe82e91b1, 0xb32700d0], [0x44de24c6, 0x88dff51d], [0x3beb65bc, 0x29514038], [0xc89c5933, 0xb328cbdf], [0x8d1ec211, 0xd405b4d5], [0x314ef5d5, 0x26e55f3c], [0xe92491b1, 0x607801c6], [0xf0a5b9d5, 0x82b2c1fb], [0x06064cf3, 0xfa51a3da], [0xda79fa60, 0x207cc464], [0xbed20560, 0x3c3c74f3], [0x89f9c9f8, 0xd2d14b61], [0x35fa38c6, 0xbb04a2c1], [0xcb49e3c6, 0xc5626167]];
const CS64_FACTOR = 0x82893933;
const CS64_ADJ0 = 0xf2f90b1a;
const CS64_ADJ1 = 0x0b1a0000;

const u32 = (x) => x >>> 0;
const rotr = (v, n) => ((v >>> n) | (v << (32 - n))) >>> 0;
const rol16 = (v) => (((v & MASK) << 16) | ((v & MASK) >>> 16)) >>> 0;
const mul = (a, b) => Math.imul(a | 0, b | 0) >>> 0;
const sigma0 = (v) => (rotr(v, 7) ^ rotr(v, 18) ^ (v >>> 3)) >>> 0;
const sigma1 = (v) => (rotr(v, 17) ^ rotr(v, 19) ^ (v >>> 10)) >>> 0;

function sha256Rounds(state, words, firstRound = 0) {
  let [a, b, c, d, e, f, g, h] = state;
  const constants = firstRound === 14 ? BLOCK_CONSTANTS : K;
  for (let i = firstRound; i < 64; i++) {
    const S1 = (rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)) >>> 0;
    const ch = (g ^ (e & (f ^ g))) >>> 0;
    const t1 = (h + S1 + ch + constants[i] + words[i]) >>> 0;
    const S0 = (rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)) >>> 0;
    const maj = ((a & b) | (c & (a | b))) >>> 0;
    const t2 = (S0 + maj) >>> 0;
    h = g; g = f; f = e; e = (d + t1) >>> 0; d = c; c = b; b = a; a = (t1 + t2) >>> 0;
  }
  return [a, b, c, d, e, f, g, h];
}

function expandSchedule(words, firstWord = 16) {
  for (let i = firstWord; i < 64; i++) {
    const x = words[i - 2], y = words[i - 15];
    const s1 = (rotr(x, 17) ^ rotr(x, 19) ^ (x >>> 10)) >>> 0;
    const s0 = (rotr(y, 7) ^ rotr(y, 18) ^ (y >>> 3)) >>> 0;
    words.push((s1 + words[i - 7] + s0 + words[i - 16]) >>> 0);
  }
}

function sha256Init(head7) {
  const words = new Array(14).fill(0);
  words.push(((head7[0] << 16) | (head7[1] << 8) | head7[2]) >>> 0);
  words.push(((head7[3] << 24) | (head7[4] << 16) | (head7[5] << 8) | head7[6]) >>> 0);
  for (let index = 16; index < 30; index++) {
    let value = SHA256_SCHEDULE[index - 16];
    if (index - 2 >= 14) value += index === 16 ? (sigma1(words[index - 2]) ^ SIGMA1_ADJ) : sigma1(words[index - 2]);
    if (index - 7 >= 14) value += words[index - 7];
    if (index - 15 >= 14) value += index === 29 ? (sigma0(words[index - 15]) ^ SIGMA0_ADJ) : sigma0(words[index - 15]);
    words.push(value & MASK);
  }
  words.push((sigma1(words[28]) + words[23] + sigma0(words[15]) + words[14] + SHA256_ADJUSTMENT - K[14]) & MASK);
  expandSchedule(words, 31);
  const working = sha256Rounds(SHA256_STATE, words, 14);
  return SHA256_INITIAL.map((x, i) => (x + working[i]) & MASK);
}

function sha256Digest(data) {
  if (data.length < 7) throw new Error('need >=7 bytes');
  const length = 57 + data.length;
  const padded = [...data.subarray(7), 0x80];
  const zeros = ((55 - length) % 64 + 64) % 64;
  for (let i = 0; i < zeros; i++) padded.push(0);
  let bitLen = length * 8;
  const tail = [];
  for (let i = 0; i < 8; i++) { tail.unshift(bitLen & 0xff); bitLen = Math.floor(bitLen / 256); }
  padded.push(...tail);

  let state = sha256Init(data.subarray(0, 7));
  for (let off = 0; off < padded.length; off += 64) {
    const block = padded.slice(off, off + 64);
    const words = [];
    for (let i = 0; i < 16; i++) {
      words.push(((block[i * 4] << 24) | (block[i * 4 + 1] << 16) | (block[i * 4 + 2] << 8) | block[i * 4 + 3]) >>> 0);
    }
    expandSchedule(words);
    const working = sha256Rounds(state, words);
    state = state.map((x, i) => (x + working[i]) & MASK);
  }
  // struct.pack('>8I', *state) → 32 字节大端
  const bytes = new Uint8Array(32);
  state.forEach((x, i) => {
    bytes[i * 4] = (x >>> 24) & 0xff;
    bytes[i * 4 + 1] = (x >>> 16) & 0xff;
    bytes[i * 4 + 2] = (x >>> 8) & 0xff;
    bytes[i * 4 + 3] = x & 0xff;
  });
  return bytes;
}

function wordsLe4Even(data) {
  const buf = new Uint8Array(1 + data.length);
  buf[0] = 0;
  buf.set(data, 1);
  const total = buf.length + ((4 - (buf.length % 4)) % 4);
  if (total === 0) return [];
  const words = [];
  for (let i = 0; i < total; i += 4) {
    words.push(((buf[i] || 0) | ((buf[i + 1] || 0) << 8) | ((buf[i + 2] || 0) << 16) | ((buf[i + 3] || 0) << 24)) >>> 0);
  }
  if (words.length % 2) words.push(0);
  return words;
}

function cs64Digest(data, digest) {
  const keyA = u32(((digest[0] & 0xff) | ((digest[1] & 0xff) << 8) | ((digest[2] & 0xff) << 16) | ((digest[3] & 0xff) << 24)) | 1);
  const keyB = u32(((digest[4] & 0xff) | ((digest[5] & 0xff) << 8) | ((digest[6] & 0xff) << 16) | ((digest[7] & 0xff) << 24)) | 1);
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
  for (let index = 0; index < terms.length; index += 2) {
    const x = terms[index], y = terms[index + 1];
    let t = rol16(u32(offsets[index] + x));
    let q = mul(t, 0x76f50f34);
    swapAcc = u32(swapAcc + u32(mul(rol16(q), 0xc3efea97) + q));
    t = rol16(u32(offsets[index + 1] + y));
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

const hexLE32 = (v) => [v & 0xff, (v >>> 8) & 0xff, (v >>> 16) & 0xff, (v >>> 24) & 0xff].map((b) => b.toString(16).padStart(2, '0')).join('').toUpperCase();

export function secMsGecV2(unixTimestamp) {
  let ticks = unixTimestamp === undefined ? Date.now() / 1000 : unixTimestamp;
  ticks += WIN_EPOCH;
  ticks -= ticks % 300;
  ticks *= 1e7;
  const str = ticks.toFixed(0) + TRUSTED_CLIENT_TOKEN;
  const data = new TextEncoder().encode(str);
  const digest = sha256Digest(data);
  const [w0, w1] = cs64Digest(data, digest);
  const sha = Array.from(digest).map((x) => x.toString(16).padStart(2, '0')).join('').toUpperCase();
  return `${hexLE32(w0)}${hexLE32(w1)}-${sha}`;
}

if (process.argv[2]) console.log(secMsGecV2(parseFloat(process.argv[2])));
