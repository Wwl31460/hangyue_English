import { useNavigate } from 'react-router-dom';
import { words } from '../data/words';
import { useProgress } from '../lib/progress';

export default function Mistakes() {
  const nav = useNavigate();
  const p = useProgress();
  const list = p.mistakeIds
    .map((id) => words.find((w) => w.id === id))
    .filter(Boolean) as typeof words;

  return (
    <div className="page pb-6 pt-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-extrabold text-brand-900">错词本</h1>
        {list.length > 0 && (
          <button
            onClick={() => confirm('确定清空错词本？') && p.clearMistakes()}
            className="text-sm text-rose-500"
          >
            清空
          </button>
        )}
      </div>
      <p className="mt-1 text-xs text-slate-400">不惩罚，常复习就能记住。</p>

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
              onClick={() => p.removeMistake(w.id)}
              className="rounded-full bg-slate-100 px-3 py-1.5 text-xs text-slate-500"
            >
              移除
            </button>
          </div>
        ))}
        {list.length === 0 && (
          <div className="card text-center text-sm text-slate-400">还没有错词，真棒！🌟</div>
        )}
      </div>
    </div>
  );
}
