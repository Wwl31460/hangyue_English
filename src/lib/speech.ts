// 语音识别封装（Web Speech API），用于“发音测试”
// 仅支持 webkitSpeechRecognition / SpeechRecognition 的浏览器/环境可用；
// 不支持时由调用方回退到手动判定（通过/不通过）。

const _SR: any =
  typeof window !== 'undefined'
    ? (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    : null;

// 当前环境是否支持语音识别
export function speechRecognitionSupported(): boolean {
  return !!_SR;
}

// 一次性识别一句话，返回识别出的原始文本（可能含标点/空格）
export function recognizeOnce(lang = 'en-GB', timeoutMs = 6000): Promise<string> {
  return new Promise((resolve, reject) => {
    if (!_SR) {
      reject(new Error('unsupported'));
      return;
    }
    let rec: any;
    try {
      rec = new _SR();
    } catch (e) {
      reject(e as Error);
      return;
    }
    rec.lang = lang;
    rec.interimResults = false;
    rec.maxAlternatives = 1;
    rec.continuous = false;

    let settled = false;
    const cleanup = () => {
      try {
        rec.onresult = null;
        rec.onerror = null;
        rec.onend = null;
        rec.stop();
      } catch {
        /* 忽略 */
      }
    };
    const done = (fn: () => void) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      cleanup();
      fn();
    };
    const timer = setTimeout(() => done(() => reject(new Error('timeout'))), timeoutMs);

    rec.onresult = (e: any) => {
      const text: string = e?.results?.[0]?.[0]?.transcript ?? '';
      done(() => resolve(text));
    };
    rec.onerror = (e: any) => {
      done(() => reject(new Error(e?.error || 'error')));
    };
    rec.onend = () => {
      // 正常结束但没有识别到结果
      done(() => reject(new Error('no-result')));
    };
    try {
      rec.start();
    } catch (e) {
      done(() => reject(e as Error));
    }
  });
}

// 归一化：转小写、去除非字母，便于比对（忽略大小写与标点）
export function normWord(s: string): string {
  return (s || '')
    .toLowerCase()
    .replace(/[^a-z]/g, '');
}

// 发音是否通过：识别文本里包含目标词（忽略大小写与标点）
export function speakPassed(transcript: string, target: string): boolean {
  const t = normWord(target);
  if (!t) return false;
  return normWord(transcript).includes(t);
}

// 编辑距离（用于拼写容错：允许 1 个字母误差）
export function editDistance(a: string, b: string): number {
  const m = a.length;
  const n = b.length;
  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      dp[i][j] = Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost);
    }
  }
  return dp[m][n];
}
