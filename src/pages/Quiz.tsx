import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { words } from '../data/words';
import { useProgress } from '../lib/progress';
import { speak, prefetchSpeech } from '../lib/tts';

interface Item {
  id: string;
  word: string;
  options: string[];
  answer: number;
}

// 小测：听音选词（纯靠听力）。只从“已学单词”中随机抽题。
export default function Quiz() {
  const nav = useNavigate();
  const p = useProgress();
  const [idx, setIdx] = useState(0);
  const [sel, setSel] = useState<number | null>(null);
  const [correct, setCorrect] = useState(0);
  const [done, setDone] = useState(false);

  // 已学单词池 + 随机抽题（挂载时一次性生成，避免每题乱序）
  const items = useMemo<Item[]>(() => {
    const pool = shuffle(words.filter((w) => p.isLearned(w.id)));
    const out: Item[] = [];
    for (let i = 0; i < Math.min(5, pool.length); i++) {
      const target = pool[i];
      const others = shuffle(pool.filter((w) => w.id !== target.id).map((w) => w.word)).slice(0, 3);
      const options = shuffle([target.word, ...others]);
      out.push({ id: target.id, word: target.word, options, answer: options.indexOf(target.word) });
    }
    return out;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 提前合成当前题与下一题的读音，点喇叭几乎立刻出声
  useEffect(() => {
    if (items.length === 0) return;
    prefetchSpeech(
      items.slice(idx, idx + 2).map((x) => x.word),
      { rate: 0.8 },
      2,
    );
  }, [items, idx, p.settings.voiceName]);

  // 没有已学单词：引导先去学习
  if (items.length === 0) {
    return (
      <div className="page pb-6 pt-10 text-center">
        <div className="text-5xl">🎧</div>
        <h1 className="mt-3 text-xl font-extrabold text-brand-900">还没有已学单词</h1>
        <p className="mt-2 text-sm text-slate-500">
          听音选词只考“学习模块里学过的词”。先去背几个单词，再来听音小测吧～
        </p>
        <button onClick={() => nav('/vocab')} className="btn-primary mt-5 w-full">
          📚 去背单词
        </button>
      </div>
    );
  }

  if (done) {
    const total = items.length;
    const pct = Math.round((correct / total) * 100);
    return (
      <div className="page pb-6 pt-10 text-center">
        <div className="text-6xl">🎉</div>
        <div className="mt-4 text-2xl font-extrabold text-brand-900">
          小测得 {correct} / {total}
        </div>
        <div className="mt-2 text-sm text-slate-500">正确率 {pct}% · 答对 +1 星，错词已入错词本</div>
        <div className="card mx-auto mt-6 max-w-xs">
          <div className="h-3 w-full overflow-hidden rounded-full bg-slate-100">
            <div className="h-full rounded-full bg-gradient-to-r from-accent-500 to-accent-700" style={{ width: `${pct}%` }} />
          </div>
        </div>
        <button onClick={() => nav('/vocab')} className="btn-primary mx-auto mt-8 block">
          返回
        </button>
      </div>
    );
  }

  const cur = items[idx];
  const choose = (i: number) => {
    if (sel !== null) return;
    setSel(i);
    if (i === cur.answer) {
      setCorrect((c) => c + 1);
      p.addStars(1);
    } else {
      p.addMistake(cur.id);
    }
    setTimeout(() => {
      if (idx + 1 >= items.length) setDone(true);
      else {
        setIdx(idx + 1);
        setSel(null);
      }
    }, 1200);
  };

  return (
    <div className="page pb-6 pt-4">
      <div className="mt-1 flex items-center justify-between text-sm">
        <span className="font-semibold text-brand-800">听音选词</span>
        <span className="text-slate-400">
          第 {idx + 1} / {items.length} 题
        </span>
      </div>
      <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-gradient-to-r from-brand-600 to-brand-800 transition-all"
          style={{ width: `${((idx + 1) / items.length) * 100}%` }}
        />
      </div>

      <div className="card mt-5 animate-fadeup text-center">
        <button
          onClick={() => speak(cur.word, { rate: 0.8 })}
          className="mx-auto grid h-24 w-24 place-items-center rounded-full bg-brand-50 text-5xl transition active:scale-95"
        >
          🔊
        </button>
        <p className="mt-3 text-sm text-slate-400">点击喇叭，选出你听到的单词</p>
      </div>

      <div className="mt-4 grid grid-cols-1 gap-3">
        {cur.options.map((o, i) => (
          <button
            key={i}
            onClick={() => choose(i)}
            disabled={sel !== null}
            className={`rounded-2xl border-2 py-3.5 text-lg font-semibold transition ${
              sel === null
                ? 'border-slate-200 bg-white text-slate-800 active:scale-[0.98]'
                : i === cur.answer
                  ? 'border-emerald-400 bg-emerald-50 text-emerald-700'
                  : sel === i
                    ? 'border-rose-400 bg-rose-50 text-rose-700'
                    : 'border-slate-200 bg-white text-slate-800'
            }`}
          >
            {o}
          </button>
        ))}
      </div>
    </div>
  );
}

function shuffle<T>(arr: T[]): T[] {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
