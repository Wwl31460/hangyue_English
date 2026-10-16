import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { readings } from '../data/readings';
import type { Reading } from '../types';
import { useProgress } from '../lib/progress';

// 学段顺序与各学段内的年级顺序（与背单词一致）
const SECTION_ORDER: Array<'小学' | '初中' | '高中'> = ['小学', '初中', '高中'];
const GRADE_ORDER = ['三年级', '四年级', '五年级', '六年级', '七年级', '八年级', '九年级', '高一', '高二', '高三'];
const GRADE_SECTION: Record<string, '小学' | '初中' | '高中'> = {
  三年级: '小学', 四年级: '小学', 五年级: '小学', 六年级: '小学',
  七年级: '初中', 八年级: '初中', 九年级: '初中',
  高一: '高中', 高二: '高中', 高三: '高中',
};
const SEM_ORDER: Array<'上' | '下'> = ['上', '下'];

// 单元角标：优先取标题里的 U 编号（如 U8）；Starter → S，Welcome → W
function unitLabel(m: Reading): string {
  const t = m.title;
  const um = t.match(/U\s*(\d+)/i);
  if (um) return `U${um[1]}`;
  if (/starter/i.test(t)) return 'S';
  if (/welcome/i.test(t)) return 'W';
  return `U${m.textbook!.unit}`;
}
// 去掉标题里的 “U1 ” 前缀，只留课题
const cleanTitle = (t: string) => t.replace(/^U\s*\d+\s*/i, '');

export default function Listen() {
  const p = useProgress();
  const nav = useNavigate();
  const [grade, setGrade] = useState<string | null>(null);

  // 教材课文：按 年级 → 学期 → Unit 分组
  const byGrade: Record<string, Record<string, Reading[]>> = {};
  for (const r of readings) {
    const t = r.textbook;
    if (!t || !GRADE_SECTION[t.grade]) continue;
    byGrade[t.grade] = byGrade[t.grade] || {};
    (byGrade[t.grade][t.semester] = byGrade[t.grade][t.semester] || []).push(r);
  }
  for (const g of Object.keys(byGrade)) {
    for (const s of Object.keys(byGrade[g])) {
      byGrade[g][s].sort((a, b) => (a.textbook!.unit || 0) - (b.textbook!.unit || 0));
    }
  }

  // 年级详情：上/下学期 + 全部单元
  if (grade && byGrade[grade]) {
    const sems = SEM_ORDER.filter((s) => byGrade[grade][s]?.length);
    return (
      <div className="page pb-24 pt-6">
        <button onClick={() => setGrade(null)} className="text-sm text-slate-500">
          ← 返回年级
        </button>
        <h1 className="mt-2 text-xl font-extrabold text-brand-900">{grade}</h1>
        <p className="mt-1 text-xs text-slate-400">选一个单元开始 · 听读 / 跟读 / 理解小测</p>

        {sems.map((sem) => (
          <div key={sem} className="mt-5">
            <div className="mb-2 flex items-center gap-2">
              <span className="h-3 w-3 rounded-full bg-gradient-to-br from-brand-500 to-brand-800" />
              <span className="text-sm font-bold text-slate-600">{sem === '上' ? '上学期' : '下学期'}</span>
            </div>
            <div className="space-y-3">
              {byGrade[grade][sem].map((m) => {
                const sc = p.getReadingScore(m.id);
                return (
                  <button
                    key={m.id}
                    onClick={() => nav(`/listen/train/${m.id}`)}
                    className="card flex w-full items-center gap-3 text-left transition hover:-translate-y-0.5 hover:shadow-soft"
                  >
                    <span className="grid h-11 w-11 shrink-0 place-items-center rounded-2xl bg-brand-50 text-sm font-extrabold text-brand-700">
                      {unitLabel(m)}
                    </span>
                    <div className="flex-1">
                      <div className="font-bold text-slate-800">{cleanTitle(m.title)}</div>
                      <div className="text-xs text-slate-500">人教版 · {m.duration}</div>
                    </div>
                    <ScoreBadge score={sc} done={p.isReadingDone(m.id)} />
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    );
  }

  // 主视图：按学段分组，列出全部年级（小学 ~ 高中）
  return (
    <div className="page pb-24 pt-6">
      <h1 className="text-xl font-extrabold text-brand-900">听读训练</h1>
      <p className="mt-1 text-xs text-slate-400">人教版课文 · 小学到高中全部单元，点开即可听读 / 跟读 / 小测</p>

      {SECTION_ORDER.map((sec) => {
        const gs = GRADE_ORDER.filter((g) => GRADE_SECTION[g] === sec && byGrade[g]);
        if (gs.length === 0) return null;
        return (
          <div key={sec} className="mt-6">
            <div className="mb-2 flex items-center gap-2">
              <span className="text-sm font-bold text-slate-500">{sec}</span>
              <span className="h-px flex-1 bg-slate-100" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              {gs.map((g) => {
                const sems = SEM_ORDER.filter((s) => byGrade[g][s]?.length);
                const total = sems.reduce((n, s) => n + byGrade[g][s].length, 0);
                return (
                  <button
                    key={g}
                    onClick={() => setGrade(g)}
                    className="group card flex items-center gap-3 !p-4 text-left transition hover:-translate-y-0.5 hover:shadow-soft"
                  >
                    <span className="grid h-10 w-10 shrink-0 place-items-center rounded-2xl bg-gradient-to-br from-accent-500 to-accent-700 text-xl shadow-soft transition group-hover:scale-110">
                      🎧
                    </span>
                    <div>
                      <div className="text-base font-extrabold text-brand-900">{g}</div>
                      <div className="text-xs text-slate-500">{total} 课</div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}

// 列表里的分数徽标：本章总评（录音分 + 测试分合计）；没测显示已完成 / 未测
function ScoreBadge({ score, done }: { score?: number; done: boolean }) {
  if (score != null) {
    const c =
      score >= 80
        ? 'bg-emerald-100 text-emerald-600'
        : score >= 60
          ? 'bg-amber-100 text-amber-600'
          : 'bg-rose-100 text-rose-600';
    return <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${c}`}>总 {score}分</span>;
  }
  if (done) return <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-xs text-emerald-600">已完成</span>;
  return <span className="text-slate-300">未测 ›</span>;
}
