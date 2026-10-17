import { useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { words } from '../data/words';
import { gradeById, unitTitles } from '../data/grades';
import { useProgress } from '../lib/progress';
import { useAuth } from '../lib/auth';

// 某年级的导航：
// - 无 unit 参数 -> 显示该年级的单元列表（Unit 1..N），点单元进入单词
// - 带 unit 参数 -> 显示该单元单词
// - 带 ?all=1 -> 显示该年级全部单词
export default function WordList() {
  const { gid, uid } = useParams();
  const [params] = useSearchParams();
  const nav = useNavigate();
  const p = useProgress();
  const { canOpen } = useAuth(); // 老师未开放的年级禁止进入
  // 进入某个单元即记为“当前学习单元”，登录后可用于首页续学 / 云端同步
  useEffect(() => {
    if (gid && uid) p.setCurrent(gid, Number(uid));
  }, [gid, uid, p]);
  const stage = gid ? gradeById[gid] : undefined;
  if (!stage) return <div className="p-6 text-slate-500">未找到该年级。</div>;

  // 老师没开放这个年级：即使从收藏/续学直接进来也挡住
  if (!canOpen(gid!)) {
    return (
      <div className="page pb-6 pt-16 text-center">
        <div className="text-5xl">🔒</div>
        <p className="mt-3 text-sm font-semibold text-slate-700">{stage.label} 还没开放</p>
        <p className="mt-1 text-xs text-slate-400">需要学习这一册，请让老师在「老师后台」里给你开放。</p>
        <button onClick={() => nav('/vocab')} className="btn-primary mt-5 !px-6 !py-2.5 text-sm">
          返回选年级
        </button>
      </div>
    );
  }

  const gradeWords = words.filter((w) => w.grade === gid);
  const units = [...new Set(gradeWords.map((w) => w.unit ?? 0))].sort((a, b) => a - b);
  const titleOf = (u: number) => unitTitles[gid!]?.[u];

  // 1) 单元内的单词
  if (uid) {
    const u = Number(uid);
    const list = gradeWords.filter((w) => w.unit === u);
    return (
      <div className="page pb-6 pt-4">
        <div className="flex items-center gap-3">
          <span className="grid h-11 w-11 place-items-center rounded-2xl bg-brand-50 text-3xl">{stage.emoji}</span>
          <div>
            <h1 className="text-xl font-extrabold text-brand-900">{stage.short} · Unit {u}</h1>
            <p className="text-xs text-slate-500">{titleOf(u) ?? `第 ${u} 单元`} · 共 {list.length} 个词</p>
          </div>
        </div>
        <WordGrid list={list} nav={nav} p={p} />
      </div>
    );
  }

  // 2) 全部单词
  if (params.get('all') === '1') {
    return (
      <div className="page pb-6 pt-4">
        <div className="flex items-center gap-3">
          <span className="grid h-11 w-11 place-items-center rounded-2xl bg-brand-50 text-3xl">{stage.emoji}</span>
          <div>
            <h1 className="text-xl font-extrabold text-brand-900">{stage.label} · 全部</h1>
            <p className="text-xs text-slate-500">共 {gradeWords.length} 个词</p>
          </div>
        </div>
        <WordGrid list={gradeWords} nav={nav} p={p} />
      </div>
    );
  }

  // 3) 单元列表
  return (
    <div className="page pb-6 pt-4">
      <div className="flex items-center gap-3">
        <span className="grid h-11 w-11 place-items-center rounded-2xl bg-brand-50 text-3xl">{stage.emoji}</span>
        <div>
          <h1 className="text-xl font-extrabold text-brand-900">{stage.label}</h1>
          <p className="text-xs text-slate-500">共 {gradeWords.length} 个词 · 点单元开始学习</p>
        </div>
      </div>

      <div className="mt-4 space-y-2.5">
        {units.map((u) => {
          const n = gradeWords.filter((w) => w.unit === u).length;
          return (
            <button
              key={u}
              onClick={() => nav(`/vocab/grade/${gid}/unit/${u}`)}
              className="group flex w-full items-center gap-3 rounded-2xl border border-slate-200 bg-white p-3.5 text-left transition hover:-translate-y-0.5 hover:border-brand-300 hover:shadow-soft active:scale-[0.98]"
            >
              <span className="grid h-11 w-11 shrink-0 place-items-center rounded-2xl bg-brand-50 text-lg font-extrabold text-brand-700">
                {u}
              </span>
              <div className="min-w-0">
                <div className="text-sm font-bold text-brand-900">Unit {u}</div>
                <div className="truncate text-xs text-slate-500">{titleOf(u) ?? `第 ${u} 单元`} · {n} 个词</div>
              </div>
              <span className="ml-auto text-slate-300 transition group-hover:translate-x-0.5">›</span>
            </button>
          );
        })}
        <button
          onClick={() => nav(`/vocab/grade/${gid}?all=1`)}
          className="flex w-full items-center justify-center gap-1.5 rounded-2xl border border-dashed border-slate-300 bg-white/60 p-3 text-sm font-medium text-slate-500"
        >
          📖 查看全部单词（{gradeWords.length}）
        </button>
      </div>
    </div>
  );
}

function WordGrid({ list, nav, p }: { list: typeof words; nav: (s: string) => void; p: ReturnType<typeof useProgress> }) {
  return (
    <div className="mt-4 grid grid-cols-2 gap-2.5 sm:grid-cols-3">
      {list.map((w) => (
        <button
          key={w.id}
          onClick={() => nav(`/vocab/study/${w.id}`)}
          className="group flex flex-col items-center gap-1 rounded-2xl border border-slate-200 bg-white p-3 text-center transition hover:-translate-y-0.5 hover:border-brand-300 hover:shadow-soft active:scale-[0.98]"
        >
          <span className="grid h-12 w-12 place-items-center rounded-2xl bg-brand-50 text-3xl">{w.image ?? '🔤'}</span>
          <span className="text-sm font-bold text-brand-900">{w.word}</span>
          <span className="line-clamp-1 text-xs text-slate-500">{w.meaning}</span>
          {p.isMistake(w.id) && <span className="rounded-full bg-rose-100 px-2 py-0.5 text-[10px] text-rose-600">错词</span>}
        </button>
      ))}
      {list.length === 0 && (
        <div className="col-span-2 rounded-2xl bg-slate-50 p-6 text-center text-sm text-slate-400">该单元暂未录入单词。</div>
      )}
    </div>
  );
}
