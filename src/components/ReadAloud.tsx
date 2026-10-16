import { useEffect, useState } from 'react';
import { useRecorder } from '../lib/recorder';
import { evaluateReadAloud } from '../lib/asr';
import { speak } from '../lib/tts';

interface Props {
  text: string;
  onScore?: (score: number) => void;
}

// 跟读录音 + 评分（原型用模拟评分，ASR 接口已预留）
export default function ReadAloud({ text, onScore }: Props) {
  const rec = useRecorder();
  const [result, setResult] = useState<{ score: number; feedback: string } | null>(null);

  useEffect(() => {
    if (rec.audioUrl && rec.blob && rec.duration > 0.3) {
      evaluateReadAloud(text, rec.blob, rec.duration).then((r) => {
        setResult(r);
        onScore?.(r.score);
      });
    }
    // 仅在生成新录音时评分
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [rec.audioUrl]);

  return (
    <div className="rounded-2xl bg-white p-4 shadow-sm border border-slate-100">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-600">跟读录音</span>
        <button onClick={() => speak(text, { rate: 0.8 })} className="text-xs text-brand-600">
          🔊 听示范
        </button>
      </div>
      <p className="mt-2 text-slate-800">{text}</p>

      <div className="mt-3 flex items-center gap-2">
        {!rec.recording ? (
          <button
            onClick={rec.start}
            className="rounded-full bg-brand-600 px-4 py-2 text-sm text-white"
          >
            ● 开始录音
          </button>
        ) : (
          <button
            onClick={rec.stop}
            className="animate-pulse rounded-full bg-rose-500 px-4 py-2 text-sm text-white"
          >
            ■ 停止 {rec.duration.toFixed(1)}s
          </button>
        )}
        {rec.audioUrl && <audio src={rec.audioUrl} controls className="h-9" />}
        {rec.audioUrl && (
          <button onClick={rec.reset} className="text-xs text-slate-400">
            重录
          </button>
        )}
      </div>

      {result && (
        <div className="mt-3 rounded-xl bg-emerald-50 p-3 text-sm">
          <span className="font-semibold text-emerald-700">
            得分 {result.score} · {result.feedback}
          </span>
        </div>
      )}
      <p className="mt-2 text-[11px] text-slate-400">
        评分为原型模拟值，真实发音评测需接入 ASR 服务。
      </p>
    </div>
  );
}
