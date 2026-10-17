import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { words } from '../data/words';
import { Word } from '../types';
import { useProgress } from '../lib/progress';
import { speak, prefetchSpeech } from '../lib/tts';

const ROUND = 10; // 每轮题量

function shuffle<T>(arr: T[]): T[] {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// 词汇复习：选择题问词义；选对下一题，选错加入错词本。
// 只从“已学单词”中抽题——未学的词不进入测试。
export default function Review() {
  const nav = useNavigate();
  const p = useProgress();

  // 已学单词池（挂载时一次性确定，避免选项乱序）
  const learnedPool = useMemo(
    () => words.filter((w) => p.isLearned(w.id)),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  );

  const [round, setRound] = useState<Word[]>(() => buildRound(learnedPool));
  const [idx, setIdx] = useState(0);
  const [picked, setPicked] = useState<number | null>(null);
  const [correct, setCorrect] = useState(0);
  const [wrong, setWrong] = useState(0);
  const [done, setDone] = useState(false);

  const current = round[idx];

  // 为本词生成 4 个选项（正确 + 3 个干扰），全部来自已学词
  const options = useMemo(() => {
    if (!current) return [];
    const wrongs = shuffle(learnedPool.filter((w) => w.id !== current.id && w.meaning !== current.meaning)).slice(0, 3);
    const opts = shuffle([current, ...wrongs]).map((w) => w.meaning);
    return opts;
  }, [current, learnedPool]);

  // 提前合成当前词与下一词的读音，点「🔊 听」几乎立刻出声
  useEffect(() => {
    prefetchSpeech(
      round.slice(idx, idx + 2).map((x) => x.word),
      {},
      2,
    );
  }, [round, idx, p.settings.voiceName]);

  const answer = (optIdx: number) => {
    if (picked !== null) return; // 已作答
    setPicked(optIdx);
    const isRight = options[optIdx] === current.meaning;
    if (isRight) {
      setCorrect((c) => c + 1);
    } else {
      setWrong((w) => w + 1);
      p.addMistake(current.id); // 答错 → 加入错词本
    }
  };

  const next = () => {
    if (idx + 1 >= round.length) {
      setDone(true);
      return;
    }
    setIdx((i) => i + 1);
    setPicked(null);
  };

  const restart = () => {
    setRound(buildRound(learnedPool));
    setIdx(0);
    setPicked(null);
    setCorrect(0);
    setWrong(0);
    setDone(false);
  };

  // 没有已学单词：引导先去学习
  if (!done && learnedPool.length === 0) {
    return (
      <div className="page pb-6 pt-10 text-center">
        <div className="text-5xl">📚</div>
        <h1 className="mt-3 text-xl font-extrabold text-brand-900">还没有已学单词</h1>
        <p className="mt-2 text-sm text-slate-500">
          测试只考“学习模块里学过的词”。先去背几个单词，再来复习吧～
        </p>
        <button onClick={() => nav('/vocab')} className="btn-primary mt-5 w-full">
          📚 去背单词
        </button>
      </div>
    );
  }

  if (done) {
    return (
      <div className="page pb-6 pt-8">
        <div className="card animate-fadeup text-center">
          <div className="text-5xl">🎉</div>
          <h1 className="mt-3 text-2xl font-extrabold text-brand-900">本轮复习完成</h1>
          <p className="mt-2 text-sm text-slate-500">共 {round.length} 题（仅来自已学单词）</p>
          <div className="mt-4 grid grid-cols-2 gap-3">
            <Stat label="答对" value={correct} color="text-emerald-600" />
            <Stat label="答错（已加入错词本）" value={wrong} color="text-rose-500" />
          </div>
          <button onClick={restart} className="btn-primary mt-5 w-full">
            🔄 再来一轮
          </button>
        </div>
      </div>
    );
  }

  if (!current) return <div className="p-6 text-slate-500">暂无单词。</div>;

  const rightIdx = options.indexOf(current.meaning);

  return (
    <div className="page pb-6 pt-6">
      {/* 进度 */}
      <div className="flex items-center justify-between">
        <span className="text-sm text-slate-500">第 {idx + 1} / {round.length} 题</span>
        <span className="text-xs text-slate-400">答对 {correct} · 答错 {wrong}</span>
      </div>

      {/* 题目卡 */}
      <div className="card mt-3 animate-fadeup">
        <div className="flex items-center justify-between">
          {/* 长单词换行显示，不用省略号截断 */}
          <div className="min-w-0 flex-1 break-words text-3xl font-extrabold leading-tight text-brand-900">
            {current.word}
          </div>
          <button onClick={() => speak(current.word)} className="btn-ghost !py-2 text-sm">
            🔊 听
          </button>
        </div>
        {current.phonetic && <div className="mt-1 text-sm text-slate-500">{current.phonetic}</div>}
        <div className="section-title mt-4">这个单词是什么意思？</div>

        {/* 选项 */}
        <div className="mt-2 space-y-2">
          {options.map((opt, i) => {
            let cls = 'border-slate-200 bg-white hover:border-brand-300';
            if (picked !== null) {
              if (i === rightIdx) cls = 'border-emerald-400 bg-emerald-50 text-emerald-700';
              else if (i === picked) cls = 'border-rose-400 bg-rose-50 text-rose-700';
              else cls = 'border-slate-200 bg-white opacity-60';
            }
            return (
              <button
                key={i}
                disabled={picked !== null}
                onClick={() => answer(i)}
                className={`w-full rounded-2xl border px-4 py-3 text-left text-base font-medium transition active:scale-[0.99] ${cls}`}
              >
                <span className="mr-2 text-slate-400">{String.fromCharCode(65 + i)}.</span>
                {opt}
              </button>
            );
          })}
        </div>

        {/* 反馈 + 下一题 */}
        {picked !== null && (
          <div className="mt-4">
            <div className={`rounded-2xl px-4 py-2 text-sm font-medium ${picked === rightIdx ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'}`}>
              {picked === rightIdx ? '✅ 回答正确！' : `❌ 正确答案：${current.meaning}`}
            </div>
            <button onClick={next} className="btn-primary mt-3 w-full">
              {idx + 1 >= round.length ? '查看结果' : '下一题 →'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

function buildRound(pool: Word[]): Word[] {
  return shuffle(pool).slice(0, Math.min(ROUND, pool.length));
}

function Stat({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="rounded-2xl bg-slate-50 p-4 text-center">
      <div className={`text-3xl font-extrabold ${color}`}>{value}</div>
      <div className="mt-1 text-xs text-slate-500">{label}</div>
    </div>
  );
}
