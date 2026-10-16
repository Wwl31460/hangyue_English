import { useNavigate } from 'react-router-dom';
import { words } from '../data/words';
import { grades, GradeStage } from '../data/grades';
import { useProgress } from '../lib/progress';

const SECTION_ORDER: GradeStage['section'][] = ['小学', '初中', '高中'];

// 背单词首页：按人教版年级阶段展示图标，点图标进入该阶段单词学习
export default function Vocabulary() {
  const nav = useNavigate();
  const p = useProgress();
  const countOf = (gid: string) => words.filter((w) => w.grade === gid).length;

  return (
    <div className="page pb-6 pt-4">
      {/* 标题 + 错词本（返回栏在顶部全局固定） */}
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-extrabold text-brand-900">背单词 · 按年级</h1>
        <button
          onClick={() => nav('/vocab/mistakes')}
          className="relative rounded-2xl bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700"
        >
          错词本
          {p.mistakeIds.length > 0 && (
            <span className="absolute -right-1.5 -top-1.5 grid h-5 min-w-5 place-items-center rounded-full bg-rose-500 px-1 text-xs text-white">
              {p.mistakeIds.length}
            </span>
          )}
        </button>
      </div>
      <p className="mt-1 text-xs text-slate-400">点开对应年级，开始该阶段单词学习。</p>

      {/* 各学段 */}
      <div className="mt-4 space-y-5">
        {SECTION_ORDER.map((sec) => (
          <div key={sec}>
            <div className="section-title">{sec}</div>
            <div className="mt-2 grid grid-cols-2 gap-3">
              {grades
                .filter((g) => g.section === sec)
                .map((g) => (
                  <button
                    key={g.id}
                    onClick={() => nav(`/vocab/grade/${g.id}`)}
                    className="group flex items-center gap-3 rounded-2xl border border-slate-200 bg-white p-3 text-left transition hover:-translate-y-0.5 hover:border-brand-300 hover:shadow-soft active:scale-[0.98]"
                  >
                    <span className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-brand-50 text-3xl">
                      {g.emoji}
                    </span>
                    <div className="min-w-0">
                      <div className="truncate text-sm font-bold text-brand-900">{g.label}</div>
                      <div className="text-xs text-slate-500">{countOf(g.id)} 个词</div>
                    </div>
                    <span className="ml-auto text-slate-300 transition group-hover:translate-x-0.5">›</span>
                  </button>
                ))}
            </div>
          </div>
        ))}
      </div>

      {/* 测试 / 复习 入口 */}
      <button
        onClick={() => nav('/vocab/test')}
        className="btn-primary mt-6 w-full"
      >
        🎯 章节测试（按单元评分，满分 100）
      </button>
      <div className="mt-3 grid grid-cols-2 gap-3">
        <button
          onClick={() => nav('/vocab/quiz')}
          className="rounded-2xl border border-slate-200 bg-white py-3 text-sm font-medium text-slate-700"
        >
          🎧 听音选词小测
        </button>
        <button
          onClick={() => nav('/vocab/review')}
          className="rounded-2xl border border-slate-200 bg-white py-3 text-sm font-medium text-slate-700"
        >
          📝 词汇复习
        </button>
      </div>
    </div>
  );
}
