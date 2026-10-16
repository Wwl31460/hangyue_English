// 朗读引擎：优先使用 Edge 在线真人语音（英式 en-GB-SoniaNeural，语调自然、不机械）；
// 离线或合成失败时自动回退到浏览器 SpeechSynthesis 系统语音。
//
// 播放层用 Web Audio 实现，解决两个"小停顿"来源：
//   1) Edge 合成的 mp3 首尾各有一小段静音 —— 解码后按采样点裁掉，单词起音干脆；
//   2) 逐句播放时"读完这一句才去取下一句"的空档 —— 多句直接按音频时间轴排布，无缝衔接。
//
// 说明：如需更换音色/语速，可在设置里指定 settings.voiceName（形如 en-GB-SoniaNeural）。

import { synthesizeEdge, DEFAULT_EDGE_VOICE } from './edgeTts';

export interface SpeakOptions {
  rate?: number; // 0.5 ~ 1.2
  lang?: string;
  name?: string | null; // 指定发音人；形如 en-GB-SoniaNeural 时走 Edge，否则作为系统语音名
  pitch?: number; // 0 ~ 2，默认 1（中性，最自然）；仅系统语音回退时使用
  volume?: number; // 0 ~ 1，默认 1
  onstart?: () => void; // 开始朗读
  onend?: () => void; // 朗读结束
  onError?: (msg: string) => void; // 完全无法发声时的原因（页面可选）
}

export interface SequenceOptions {
  rate?: number;
  name?: string | null;
  volume?: number;
  loop?: boolean; // 读完最后一句后回到第一句继续
  onIndex?: (i: number) => void; // 第 i 句开始朗读（用于高亮跟读位置）
  onDone?: () => void; // 全部读完（loop 模式下不会触发）
}

// 给系统语音打“自然度分”，优先在线神经语音（最像人）——仅在回退系统语音时用
function voiceScore(v: SpeechSynthesisVoice): number {
  const n = (v.name || '').toLowerCase();
  const l = (v.lang || '').toLowerCase();
  let s = 0;
  if (/online|neural|natural/.test(n)) s += 4;
  if (/aria|jenny|guy|davis|sara|zira|mark|xiaoxiao|yunyang/.test(n)) s += 2;
  if (/^en[-_]us/i.test(l)) s += 1.5;
  else if (/^en/i.test(l)) s += 0.5;
  return s;
}

// 选择一个系统英文发音人：优先指定 name，否则挑最自然的一个
export function pickVoice(lang = 'en-US', name?: string | null): SpeechSynthesisVoice | null {
  if (typeof window === 'undefined' || !('speechSynthesis' in window)) return null;
  const vs = window.speechSynthesis.getVoices();
  if (vs.length === 0) return null;
  if (name) {
    const hit = vs.find((v) => v.name === name);
    if (hit) return hit;
  }
  const en = vs.filter((v) => /^en/i.test(v.lang));
  if (en.length === 0) return null;
  return en.slice().sort((a, b) => voiceScore(b) - voiceScore(a))[0];
}

// 供“设置-发音人”下拉使用：英文语音按自然度从高到低排序
export function englishVoicesSorted(): SpeechSynthesisVoice[] {
  if (typeof window === 'undefined' || !('speechSynthesis' in window)) return [];
  return window.speechSynthesis
    .getVoices()
    .filter((v) => /^en/i.test(v.lang))
    .sort((a, b) => voiceScore(b) - voiceScore(a));
}

export function hasBritishVoice(): boolean {
  if (typeof window === 'undefined' || !('speechSynthesis' in window)) return false;
  return window.speechSynthesis.getVoices().some((v) => /en[-_]GB/i.test(v.lang));
}

export function getVoices(): SpeechSynthesisVoice[] {
  if (typeof window === 'undefined' || !('speechSynthesis' in window)) return [];
  return window.speechSynthesis.getVoices();
}

const DEFAULT_LANG = 'en-US';
const DEFAULT_RATE = 0.9;
const DEFAULT_PITCH = 1.0;

// 合成连续失败达到阈值后先冷却一段时间再重试。
// 注意不能用"一次失败就整场静音"的策略：安卓机在移动网络下抖动一下，
// 整个会话就再也读不出来了，用户体验比多试几次糟糕得多。
let edgeFailCount = 0;
let edgeFailAt = 0;
const EDGE_FAIL_LIMIT = 3;
const EDGE_COOLDOWN = 20000; // 冷却 20 秒，之后允许再试

function edgeBlocked(): boolean {
  return edgeFailCount >= EDGE_FAIL_LIMIT && Date.now() - edgeFailAt < EDGE_COOLDOWN;
}

function markEdgeFail(): void {
  edgeFailCount++;
  edgeFailAt = Date.now();
}

// ————— 失败反馈 —————
// 安卓 WebView 等环境没有 Web Speech API，Edge 又连不上时就没有任何声音。
// 这时必须让界面能提示用户，否则表现就是"点了没反应"。
const FAIL_MSG = '朗读失败：连不上在线语音服务，且本机没有离线语音。请检查网络后再试。';

let errorNotifier: ((msg: string) => void) | null = null;

export function setSpeechErrorNotifier(fn: ((msg: string) => void) | null): void {
  errorNotifier = fn;
}

function reportFail(opts?: SpeakOptions): void {
  opts?.onError?.(FAIL_MSG);
  try {
    errorNotifier?.(FAIL_MSG);
  } catch {
    /* 通知方自己出错不影响朗读流程 */
  }
}

// 系统语音是否可用（安卓 WebView、部分精简内核没有 Web Speech API）
function canSpeakSystem(): boolean {
  return (
    typeof window !== 'undefined' &&
    'speechSynthesis' in window &&
    'SpeechSynthesisUtterance' in window
  );
}

// ————— 回退：系统语音 —————
// 返回是否真的开始发声；不可用时返回 false，由调用方决定怎么提示
function speakSystem(text: string, opts: SpeakOptions): boolean {
  if (!canSpeakSystem()) return false;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = opts.lang ?? DEFAULT_LANG;
  u.rate = opts.rate ?? DEFAULT_RATE;
  u.pitch = opts.pitch ?? DEFAULT_PITCH;
  u.volume = opts.volume ?? 1;
  const v = pickVoice(u.lang, opts.name);
  if (v) u.voice = v;
  u.onstart = () => opts.onstart?.();
  u.onend = () => opts.onend?.();
  window.speechSynthesis.speak(u);
  return true;
}

// ————— Web Audio 播放层 —————
const SILENCE_TH = 0.005; // 静音判定阈值（≈ -46 dBFS）
const HEAD_PAD = 0.008; // 句首保留 8ms，避免削掉起音
const TAIL_PAD = 0.025; // 句尾保留 25ms，避免结尾被切
const FADE = 0.006; // 首尾各 6ms 淡入淡出，避免爆音
const MIN_KEEP = 0.12; // 裁完不足 120ms 就不裁，防止误伤短词
const START_DELAY = 0.012; // 起播预留，尽量短——点下去就出声
const SENTENCE_GAP = 0.35; // 连读时句与句之间的停顿（秒），像真人朗读那样换口气
const LOOKAHEAD = 4; // 连续播放时最多提前排入的音频秒数

let ctx: AudioContext | null = null;

function getCtx(): AudioContext | null {
  if (typeof window === 'undefined') return null;
  const AC: typeof AudioContext | undefined =
    window.AudioContext ?? (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
  if (!AC) return null;
  if (!ctx) ctx = new AC();
  if (ctx.state === 'suspended') void ctx.resume().catch(() => undefined);
  return ctx;
}

// 预热音频上下文：AudioContext 首次创建有几十毫秒开销，进应用就建好，第一次朗读不被拖慢
export function warmupAudio(): void {
  getCtx();
}

// 裁掉首尾静音：静音部分会让单词起音发闷、句子之间显得有停顿
function trimSilence(c: AudioContext, buf: AudioBuffer): AudioBuffer {
  const sr = buf.sampleRate;
  const chs = buf.numberOfChannels;
  const len = buf.length;
  const data: Float32Array[] = [];
  for (let ch = 0; ch < chs; ch++) data.push(buf.getChannelData(ch));

  const loud = (i: number) => {
    let m = 0;
    for (let ch = 0; ch < chs; ch++) {
      const v = Math.abs(data[ch][i]);
      if (v > m) m = v;
    }
    return m;
  };

  let start = 0;
  let end = len - 1;
  while (start < len && loud(start) < SILENCE_TH) start++;
  while (end > start && loud(end) < SILENCE_TH) end--;
  if (start >= end) return buf;

  start = Math.max(0, start - Math.round(HEAD_PAD * sr));
  end = Math.min(len - 1, end + Math.round(TAIL_PAD * sr));
  const segLen = end - start + 1;
  if (segLen / sr < MIN_KEEP) return buf;

  const out = c.createBuffer(chs, segLen, sr);
  const fade = Math.min(Math.round(FADE * sr), Math.floor(segLen / 8));
  for (let ch = 0; ch < chs; ch++) {
    const src = data[ch].subarray(start, end + 1);
    const dst = out.getChannelData(ch);
    dst.set(src);
    for (let i = 0; i < fade; i++) {
      const k = i / fade;
      dst[i] *= k;
      dst[segLen - 1 - i] *= k;
    }
  }
  return out;
}

// 解码后的音频缓存（键为 edgeTts 返回的对象 URL，同一句只解码裁剪一次）
const bufCache = new Map<string, AudioBuffer>();
const BUF_MAX = 400;

async function getBuffer(url: string): Promise<AudioBuffer | null> {
  const hit = bufCache.get(url);
  if (hit) return hit;
  const c = getCtx();
  if (!c) return null;
  const data = await (await fetch(url)).arrayBuffer();
  const decoded = await c.decodeAudioData(data);
  const trimmed = trimSilence(c, decoded);
  if (bufCache.size >= BUF_MAX) {
    const first = bufCache.keys().next().value;
    if (first !== undefined) bufCache.delete(first);
  }
  bufCache.set(url, trimmed);
  return trimmed;
}

let activeSources: AudioBufferSourceNode[] = [];

function stopAllSources() {
  for (const s of activeSources) {
    try {
      s.stop();
    } catch {
      /* 已结束的源再 stop 会抛错，忽略 */
    }
    try {
      s.disconnect();
    } catch {
      /* ignore */
    }
  }
  activeSources = [];
}

function startSource(
  c: AudioContext,
  buf: AudioBuffer,
  when: number,
  volume: number,
  onEnded?: () => void,
): void {
  const src = c.createBufferSource();
  src.buffer = buf;
  const gain = c.createGain();
  gain.gain.value = volume;
  src.connect(gain);
  gain.connect(c.destination);
  src.onended = () => {
    const k = activeSources.indexOf(src);
    if (k >= 0) activeSources.splice(k, 1);
    onEnded?.();
  };
  src.start(when);
  activeSources.push(src);
}

// 统一入口：播放时先停掉上一次，并用递增序号丢弃过期结果
function beginPlayback(): number {
  playSeq++;
  if (seqState) {
    if (seqState.timer) window.clearInterval(seqState.timer);
    seqState = null;
  }
  stopAllSources();
  if (typeof window !== 'undefined' && 'speechSynthesis' in window) window.speechSynthesis.cancel();
  return playSeq;
}

// 用户在「设置」里选的发音人：由 ProgressProvider 同步进来。
// 这样所有 speak() 调用（含以后新增的页面）都会自动尊重这个选择，不必逐处传参。
let preferredVoice: string | null = null;

export function setPreferredVoice(name?: string | null): void {
  preferredVoice = name || null;
}

function pickVoiceName(name?: string | null): string {
  const n = name ?? preferredVoice;
  return n && /Neural$/i.test(n) ? n : DEFAULT_EDGE_VOICE;
}

function isOnline(): boolean {
  return typeof navigator === 'undefined' || navigator.onLine !== false;
}

// ————— 单段朗读（单词 / 句子 / 全文）—————
let playSeq = 0;

export function speak(text: string, opts: SpeakOptions = {}): void {
  if (!text) return;
  const seq = beginPlayback();
  const volume = opts.volume ?? 1;
  const rate = opts.rate ?? DEFAULT_RATE;

  const c = getCtx();
  if (!c || !isOnline() || edgeBlocked()) {
    if (!speakSystem(text, opts)) reportFail(opts);
    return;
  }

  synthesizeEdge(text, { voice: pickVoiceName(opts.name), rate })
    .then((url) => getBuffer(url))
    .then((buf) => {
      if (seq !== playSeq) return;
      if (!buf) {
        if (!speakSystem(text, opts)) reportFail(opts);
        return;
      }
      edgeFailCount = 0;
      edgeFailAt = 0;
      opts.onstart?.();
      startSource(c, buf, c.currentTime + START_DELAY, volume, () => opts.onend?.());
    })
    .catch(() => {
      if (seq !== playSeq) return;
      markEdgeFail();
      if (!speakSystem(text, opts)) reportFail(opts);
    });
}

// 预合成：进入页面时先备好前几句，首次连播也能无缝
export function prefetchSpeech(texts: string[], opts: { name?: string | null; rate?: number } = {}, limit = 4): void {
  if (!isOnline() || edgeBlocked()) return;
  const voice = pickVoiceName(opts.name);
  const rate = opts.rate ?? DEFAULT_RATE;
  texts.slice(0, limit).forEach((t, i) => {
    if (!t) return;
    // 轻微错开，避免同时开太多连接
    window.setTimeout(() => {
      synthesizeEdge(t, { voice, rate })
        .then((url) => getBuffer(url))
        .catch(() => undefined);
    }, i * 60);
  });
}

// ————— 连续朗读：句与句之间按音频时间轴紧密排布，没有空档 —————
interface SeqState {
  seq: number;
  texts: string[];
  from: number;
  to: number;
  loop: boolean;
  voice: string;
  rate: number;
  volume: number;
  next: number; // 下一句待排入的下标
  cursor: number; // 音频时间轴上"下一句的起点"
  scheduled: number; // 已排入的句数
  busy: boolean; // 正在等待合成，避免重复排入
  finished: boolean;
  timer: number | null;
  onIndex?: (i: number) => void;
  onDone?: () => void;
}

let seqState: SeqState | null = null;

function finishSeq(st: SeqState) {
  if (st.timer) window.clearInterval(st.timer);
  st.timer = null;
  if (seqState === st) seqState = null;
  st.onDone?.();
}

// 把"下一句"排入时间轴：只要排入量还没超出 lookahead 就继续
async function pump() {
  const st = seqState;
  if (!st) return;
  const c = getCtx();
  if (!c || st.busy) return;

  if (st.cursor < c.currentTime) st.cursor = c.currentTime + 0.02;

  if (st.finished) {
    if (st.cursor - c.currentTime <= 0.02) finishSeq(st);
    return;
  }
  if (st.cursor - c.currentTime > LOOKAHEAD) return; // 已经排得够远，等播完再排

  const idx = st.next;
  st.busy = true;
  let buf: AudioBuffer | null = null;
  try {
    const url = await synthesizeEdge(st.texts[idx], { voice: st.voice, rate: st.rate });
    if (seqState !== st) {
      st.busy = false;
      return;
    }
    buf = await getBuffer(url);
  } catch {
    buf = null;
    markEdgeFail(); // 计入熔断，避免整篇每句都白白等一次超时
  }
  st.busy = false;
  if (seqState !== st) return;

  // 首句就失败 → 整段退回系统语音顺序朗读，保证能听
  if (!buf && st.scheduled === 0) {
    fallbackSequence(st);
    return;
  }

  if (buf) {
    const when = Math.max(st.cursor, c.currentTime + 0.02);
    startSource(c, buf, when, st.volume);
    // 后面还有句子才留停顿；最后一句不留，读完即结束
    const hasNext = idx < st.to || st.loop;
    st.cursor = when + buf.duration + (hasNext ? SENTENCE_GAP : 0);
    st.scheduled++;
    const at = idx;
    window.setTimeout(() => {
      if (seqState === st) st.onIndex?.(at);
    }, Math.max(0, (when - c.currentTime) * 1000));
  } else {
    st.cursor += 0.2; // 该句合成失败：略过，不中断整篇
  }

  if (idx >= st.to) {
    if (st.loop) {
      st.next = st.from;
    } else {
      st.finished = true;
    }
  } else {
    st.next = idx + 1;
  }

  void pump(); // 还没排满 lookahead 就继续排
}

// Edge 不可用时的降级：逐句交给系统语音，读完自动续下一句
function fallbackSequence(st: SeqState) {
  if (st.timer) window.clearInterval(st.timer);
  st.timer = null;
  if (seqState === st) seqState = null;
  // 本机没有系统语音（安卓 WebView 常见）→ 无法朗读，明确告知并结束，不要静默空转
  if (!canSpeakSystem()) {
    reportFail();
    st.onDone?.();
    return;
  }
  const { texts, from, to, loop, rate } = st;
  const step = (i: number) => {
    if (st.seq !== playSeq) return;
    st.onIndex?.(i);
    speakSystem(texts[i], {
      rate,
      name: st.voice,
      onend: () => {
        if (st.seq !== playSeq) return;
        if (i >= to) {
          if (loop) step(from);
          else st.onDone?.();
        } else step(i + 1);
      },
    });
  };
  step(from);
}

// 连续朗读 texts[from..to]；loop=true 时循环播放
export function speakSequence(texts: string[], opts: SequenceOptions & { from?: number; to?: number } = {}): void {
  const from = Math.max(0, opts.from ?? 0);
  const to = Math.min(texts.length - 1, opts.to ?? texts.length - 1);
  if (to < from) return;

  const seq = beginPlayback();
  const c = getCtx();
  const volume = opts.volume ?? 1;
  const rate = opts.rate ?? DEFAULT_RATE;
  const voice = pickVoiceName(opts.name);

  const st: SeqState = {
    seq,
    texts,
    from,
    to,
    loop: !!opts.loop,
    voice,
    rate,
    volume,
    next: from,
    cursor: c ? c.currentTime + START_DELAY : 0,
    scheduled: 0,
    busy: false,
    finished: false,
    timer: null,
    onIndex: opts.onIndex,
    onDone: opts.onDone,
  };

  if (!c || !isOnline() || edgeBlocked()) {
    fallbackSequence(st);
    return;
  }

  seqState = st;
  // 预热前几句，让首句之后立刻衔接
  prefetchSpeech(texts.slice(from, to + 1), { name: opts.name, rate }, 3);
  st.timer = window.setInterval(() => void pump(), 200);
  void pump();
}

export function stopSpeak(): void {
  beginPlayback();
}
