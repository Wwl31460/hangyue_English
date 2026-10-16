import { useNavigate } from 'react-router-dom';
import { words } from '../data/words';
import { familyWords } from '../data/families';
import { useProgress } from '../lib/progress';

// 困难单词本：统计所有“记起来很困难”的单词，可反复复习。
// 困难词可能来自课本单元（words），也可能来自词根词缀拓展页（familyWords），故合并检索。
const ALL = [...words, ...familyWords];

export default function Hard() {
  const nav = useNavigate();
  const p = useProgress();
  const list = p.hardIds
    .map((id) => ALL.find((w) => w.id === id))
    .filter(Boolean) as typeof words;

  return (
    <div className="page pb-6 pt-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-extrabold text-brand-900">困难单词本</h1>
        {list.length > 0 && (
          <button
            onClick={() => confirm('确定清空困难单词本？') && p.clearHard()}
            className="text-sm text-rose-500"
          >
            清空
          </button>
        )}
      </div>
      <p className="mt-1 text-xs text-slate-400">挑出来的难点词，常复习就能攻克。</p>

      <div className="mt-4 space-y-3">
        {list.map((w) => (
          <div key={w.id} className="card flex items-center gap-3">
            <span className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-brand-50 text-3xl">
              {w.image ?? '🔤'}
            </span>
            <button onClick={() => nav(`/vocab/study/${w.id}`)} className="flex-1 text-left">
              <div className="text-lg font-bold text-slate-800">{w.word}</div>
              <div className="text-xs text-slate-500">
                {w.phonetic} · {w.meaning}
              </div>
            </button>
            <button
              onClick={() => p.removeHard(w.id)}
              className="rounded-full bg-slate-100 px-3 py-1.5 text-xs text-slate-500"
            >
              移除
            </button>
          </div>
        ))}
        {list.length === 0 && (
          <div className="card text-center text-sm text-slate-400">还没有困难单词，加油记！💪</div>
        )}
      </div>
    </div>
  );
}
