// 跟读评分：原型阶段用模拟评分，预留真实 ASR 接口
export interface ASRResult {
  text: string; // 识别出的文本
}

/**
 * 预留 ASR 接口：真实接入时在此调用语音识别云服务
 * （如腾讯云/讯飞等），把录音音频转写为文本，再做发音比对。
 * 当前未接入，调用会抛错以提示对接位置。
 */
export async function asrTranscribe(_audioBlob: Blob): Promise<ASRResult> {
  throw new Error('ASR 未接入：请在此处对接语音识别云服务（如腾讯云/讯飞），将录音转写为文本');
}

/**
 * 模拟评分：基于录音时长与参考文本长度，给出一个 60~100 的友好分数。
 * 不惩罚、鼓励完成：分数整体偏友好。
 */
export function mockScore(referenceText: string, audioDurationSec: number): { score: number; feedback: string } {
  const words = referenceText.trim().split(/\s+/).filter(Boolean).length;
  const expected = Math.max(1.2, words * 0.45); // 期望朗读时长（秒）
  const ratio = audioDurationSec / expected;
  let score: number;
  if (ratio >= 0.8 && ratio <= 1.4) score = 92;
  else if (ratio >= 0.6 && ratio <= 1.8) score = 82;
  else score = 68;
  score = Math.min(100, Math.max(60, score));
  const feedback =
    score >= 90 ? '发音流畅，很棒！' : score >= 80 ? '不错，再多练几遍会更自然。' : '慢慢来，注意每个音节。';
  return { score, feedback };
}

/**
 * 跟读评分统一入口：当前返回模拟结果，预留 ASR 实时评分。
 * 接入真实 ASR 后，可改为：
 *   const asr = await asrTranscribe(audioBlob);
 *   return realScore(asr.text, referenceText);
 */
export async function evaluateReadAloud(
  referenceText: string,
  audioBlob: Blob,
  durationSec: number,
): Promise<{ score: number; feedback: string; asrText?: string }> {
  const { score, feedback } = mockScore(referenceText, durationSec);
  return { score, feedback };
}
