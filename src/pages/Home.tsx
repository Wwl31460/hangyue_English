import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { useProgress } from '../lib/progress';
import { useAuth } from '../lib/auth';
import { gradeById, unitTitles } from '../data/grades';

export default function Home() {
  const p = useProgress();
  const { user, ready, syncState, logout, canOpen } = useAuth();

  // “继续学习”入口：登录且记录了当前单元时显示
  const contGrade = p.currentGrade ? gradeById[p.currentGrade] : undefined;
  const contTitle = p.currentGrade && p.currentUnit ? unitTitles[p.currentGrade]?.[p.currentUnit] : undefined;
  // 今日听读最好成绩（仅统计今日首次听到的文章）
  const bestArticle = p.daily.readingIds.reduce((m, id) => Math.max(m, p.getReadingScore(id) ?? 0), 0);

  return (
    <div className="page pb-24 pt-8">
      {/* 品牌头 + 登录态 */}
      <div className="animate-fadeup">
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="grid h-10 w-10 place-items-center rounded-2xl bg-gradient-to-br from-brand-600 to-brand-800 text-xl shadow-soft">
              📖
            </span>
            <div>
              <h1 className="text-2xl font-extrabold tracking-tight text-brand-900">航悦英语</h1>
              <p className="text-xs text-slate-500">K12 单词 · 听读训练</p>
            </div>
          </div>
          {/* 右上角：登录 / 已登录 */}
          {ready && user ? (
            <div className="flex flex-col items-end gap-1">
              <button
                onClick={() => logout()}
                className="rounded-full bg-brand-50 px-3 py-1 text-xs font-medium text-brand-700"
                title="退出后本机进度保留，云端进度仍在"
              >
                👤 {user.name} · 退出
              </button>
              <SyncChip state={syncState} />
            </div>
          ) : (
            <Link
              to="/login"
              className="rounded-full bg-brand-600 px-4 py-1.5 text-sm font-medium text-white shadow-soft"
            >
              登录
            </Link>
          )}
        </div>
        <p className="mt-3 text-sm text-slate-500">
          每天 10 分钟，单词听得懂、说得出。今天也要加油 💪
        </p>
      </div>

      {/* 继续学习：跳到上次所在的单元（该年级被老师锁住时不显示） */}
      {ready && user && contGrade && p.currentUnit && p.currentGrade && canOpen(p.currentGrade) ? (
        <Link
          to={`/vocab/grade/${p.currentGrade}/unit/${p.currentUnit}`}
          className="mt-4 flex items-center justify-between rounded-2xl border border-brand-200 bg-brand-50 p-3.5 shadow-soft"
        >
          <div>
            <div className="text-xs font-medium text-brand-600">继续学习</div>
            <div className="text-sm font-bold text-brand-900">
              {contGrade.short} · Unit {p.currentUnit}
              {contTitle ? `（${contTitle}）` : ''}
            </div>
          </div>
          <span className="text-brand-400">→</span>
        </Link>
      ) : null}

      {/* 两个大入口 */}
      <div className="mt-6 grid grid-cols-1 gap-4">
        <Link
          to="/vocab"
          className="group animate-fadeup rounded-3xl bg-gradient-to-br from-brand-600 to-brand-900 p-6 text-white shadow-soft transition hover:-translate-y-0.5"
        >
          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-bold">背单词</div>
              <div className="mt-1 text-sm text-white/80">按年级 · 词根词缀网络 · 错词本</div>
            </div>
            <span className="text-5xl transition group-hover:scale-110">📚</span>
          </div>
        </Link>
        <Link
          to="/listen"
          className="group animate-fadeup rounded-3xl bg-gradient-to-br from-accent-500 to-accent-700 p-6 text-white shadow-glow transition hover:-translate-y-0.5"
        >
          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-bold">听读训练</div>
              <div className="mt-1 text-sm text-white/80">分级材料 · 逐句跟读 · 理解小测</div>
            </div>
            <span className="text-5xl transition group-hover:scale-110">🎧</span>
          </div>
        </Link>
      </div>

      {/* 测试 / 复习 / 错词本 / 困难本 / 我的 入口 */}
      <div className="mt-4 grid grid-cols-2 gap-4">
        <Link
          to="/vocab/test"
          className="group flex items-center justify-between rounded-3xl border border-slate-200 bg-white p-4 shadow-soft transition hover:-translate-y-0.5"
        >
          <div>
            <div className="text-lg font-bold text-brand-900">章节测试</div>
            <div className="mt-1 text-xs text-slate-500">按单元测·满分 100</div>
          </div>
          <span className="text-4xl transition group-hover:scale-110">🎯</span>
        </Link>
        <Link
          to="/vocab/review"
          className="group flex items-center justify-between rounded-3xl border border-slate-200 bg-white p-4 shadow-soft transition hover:-translate-y-0.5"
        >
          <div>
            <div className="text-lg font-bold text-brand-900">词汇复习</div>
            <div className="mt-1 text-xs text-slate-500">选择题测词义</div>
          </div>
          <span className="text-4xl transition group-hover:scale-110">📝</span>
        </Link>
        <Link
          to="/vocab/mistakes"
          className="group flex items-center justify-between rounded-3xl border border-slate-200 bg-white p-4 shadow-soft transition hover:-translate-y-0.5"
        >
          <div>
            <div className="text-lg font-bold text-brand-900">错词本</div>
            <div className="mt-1 text-xs text-slate-500">常复习就能记住</div>
          </div>
          <span className="text-4xl transition group-hover:scale-110">📕</span>
        </Link>
        <Link
          to="/vocab/hard"
          className="group flex items-center justify-between rounded-3xl border border-slate-200 bg-white p-4 shadow-soft transition hover:-translate-y-0.5"
        >
          <div>
            <div className="text-lg font-bold text-brand-900">困难单词本</div>
            <div className="mt-1 text-xs text-slate-500">记起来很吃力的词</div>
          </div>
          <span className="text-4xl transition group-hover:scale-110">😣</span>
        </Link>
        <Link
          to="/me"
          className="group col-span-2 flex items-center justify-between rounded-3xl border border-slate-200 bg-white p-4 shadow-soft transition hover:-translate-y-0.5"
        >
          <div>
            <div className="text-lg font-bold text-brand-900">我的</div>
            <div className="mt-1 text-xs text-slate-500">进度 / 错词本 / 困难本</div>
          </div>
          <span className="text-4xl transition group-hover:scale-110">⭐</span>
        </Link>
      </div>

      {/* 今日进度：满 10 颗星 = 背 10 个新单词 + 听读 1 篇未听文章并测满分 */}
      <div className="card mt-5 animate-fadeup">
        <div className="flex items-center justify-between">
          <span className="section-title mb-0">今日进度</span>
          <span className="text-sm font-bold text-brand-700">{p.todayStars()} / 10 ⭐</span>
        </div>
        <div className="mt-2 h-2.5 w-full overflow-hidden rounded-full bg-slate-100">
          <div
            className="h-full rounded-full bg-gradient-to-r from-brand-500 to-brand-800"
            style={{ width: `${Math.min(100, p.todayStars() * 10)}%` }}
          />
        </div>
        <p className="mt-2 text-xs text-slate-500">
          背 10 个新单词 + 听读 1 篇未听文章测满分 = 10 颗星；单词少背按比例扣。
        </p>
        <div className="mt-3 grid grid-cols-3 gap-3">
          <Stat icon="📝" label="新单词" value={`${p.daily.words}/10`} sub={`${p.todayWordStars().toFixed(1)} 星`} />
          <Stat
            icon="🎧"
            label="听读"
            value={bestArticle > 0 ? `${bestArticle}分` : '未测'}
            sub={`${p.todayArticleStars().toFixed(2)} 星`}
          />
          <Stat icon="⏱️" label="分钟" value={p.daily.minutes} />
        </div>
      </div>
    </div>
  );
}

function Stat({ icon, label, value, sub }: { icon: string; label: string; value: ReactNode; sub?: string }) {
  return (
    <div className="rounded-2xl bg-gradient-to-b from-slate-50 to-white p-3 text-center ring-1 ring-slate-100">
      <div className="text-lg">{icon}</div>
      <div className="mt-1 text-2xl font-extrabold text-brand-700">{value}</div>
      <div className="text-xs text-slate-500">{label}</div>
      {sub && <div className="mt-0.5 text-[11px] text-slate-400">{sub}</div>}
    </div>
  );
}

// 同步状态小标签：登录后显示进度与云端的同步情况
function SyncChip({ state }: { state: 'local' | 'loading' | 'saving' | 'saved' | 'error' }) {
  const map = {
    local: { t: '仅本机', c: 'text-slate-400' },
    loading: { t: '同步中…', c: 'text-brand-500' },
    saving: { t: '保存中…', c: 'text-brand-500' },
    saved: { t: '☁️ 已同步', c: 'text-emerald-600' },
    error: { t: '同步失败', c: 'text-rose-500' },
  } as const;
  const m = map[state];
  return <span className={`text-[11px] font-medium ${m.c}`}>{m.t}</span>;
}
