import { FormEvent, useCallback, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../lib/auth';
import {
  StudentRow,
  StudentDetail,
  fetchStudents,
  fetchStudentDetail,
  setStudentScope,
  clearStudentProgress,
} from '../lib/teacher';
import { grades, GradeStage } from '../data/grades';

// 老师后台：查看学生学习情况 / 设置内容开放范围 / 添加学生 / 清除学习数据
//
// 老师口令只存在于**服务端**（hy_* 函数里），不写在 App 代码里——这个仓库是公开的，
// 口令写在前端等于公开。前端只负责把口令带给服务端，对错由服务端判定：
// 口令错的时候，第一个请求（拉学生列表）就会直接返回「老师口令不正确」。

const SECTIONS: GradeStage['section'][] = ['小学', '初中', '高中'];

type Tab = 'list' | 'add';

export default function Teacher() {
  const { createStudent } = useAuth();
  const [pin, setPin] = useState('');
  const [pinOk, setPinOk] = useState(false);
  const [tab, setTab] = useState<Tab>('list');
  const [students, setStudents] = useState<StudentRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');

  // 进入老师后台：顺便用这个口令拉一次学生列表，等于当场验证口令
  const enter = async (e: FormEvent) => {
    e.preventDefault();
    if (!pin.trim()) return setErr('请输入老师口令');
    setLoading(true);
    setErr('');
    try {
      const list = await fetchStudents(pin);
      setStudents(list);
      setPinOk(true);
    } catch (e: any) {
      setErr(String(e?.message || '进入失败，请重试'));
    } finally {
      setLoading(false);
    }
  };

  const refresh = useCallback(async () => {
    try {
      setStudents(await fetchStudents(pin));
    } catch {
      /* 刷新失败保留旧列表，不打扰老师 */
    }
  }, [pin]);

  if (!pinOk) {
    return (
      <div className="page pb-10 pt-8">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-extrabold text-brand-900">老师后台</h1>
          <Link to="/" className="text-sm text-brand-600">
            ← 返回
          </Link>
        </div>
        <p className="mt-1 text-xs text-slate-500">老师专用，学生会话里看不到入口</p>

        <form onSubmit={enter} className="card mt-5">
          <label className="section-title mb-0">老师口令</label>
          <input
            type="password"
            value={pin}
            onChange={(e) => setPin(e.target.value)}
            placeholder="请输入老师口令"
            className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm outline-none focus:border-brand-400"
          />
          {err && <p className="mt-3 rounded-lg bg-rose-50 px-3 py-2 text-xs text-rose-600">{err}</p>}
          <button type="submit" disabled={loading} className="btn-primary mt-4 w-full !py-2.5 disabled:opacity-60">
            {loading ? '验证中…' : '进入'}
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="page pb-10 pt-8">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-extrabold text-brand-900">老师后台</h1>
        <Link to="/" className="text-sm text-brand-600">
          ← 返回
        </Link>
      </div>

      {/* 两个分区 */}
      <div className="mt-3 flex gap-2">
        <button
          onClick={() => setTab('list')}
          className={`chip flex-1 !px-0 text-center ${tab === 'list' ? 'chip-on' : 'chip-off'}`}
        >
          学生学习情况
        </button>
        <button
          onClick={() => setTab('add')}
          className={`chip flex-1 !px-0 text-center ${tab === 'add' ? 'chip-on' : 'chip-off'}`}
        >
          添加学生
        </button>
      </div>

      {tab === 'add' ? (
        <AddStudent
          pin={pin}
          createStudent={createStudent}
          onDone={refresh}
        />
      ) : (
        <StudentList pin={pin} students={students} loading={loading} onChanged={refresh} />
      )}
    </div>
  );
}

// ---- 学习情况列表 ----
function StudentList({
  pin,
  students,
  loading,
  onChanged,
}: {
  pin: string;
  students: StudentRow[];
  loading: boolean;
  onChanged: () => void;
}) {
  const [openUser, setOpenUser] = useState<string | null>(null);

  if (loading) return <p className="mt-6 text-center text-sm text-slate-400">读取中…</p>;
  if (students.length === 0) {
    return (
      <div className="card mt-4 text-center text-sm text-slate-500">
        还没有学生。切到「添加学生」建一个吧。
      </div>
    );
  }

  return (
    <div className="mt-4 space-y-3">
      <p className="text-xs text-slate-400">共 {students.length} 个学生，点一行看每天学了多少。</p>
      {students.map((s) => (
        <StudentCard
          key={s.username}
          pin={pin}
          s={s}
          open={openUser === s.username}
          onToggle={() => setOpenUser(openUser === s.username ? null : s.username)}
          onChanged={onChanged}
        />
      ))}
    </div>
  );
}

function StudentCard({
  pin,
  s,
  open,
  onToggle,
  onChanged,
}: {
  pin: string;
  s: StudentRow;
  open: boolean;
  onToggle: () => void;
  onChanged: () => void;
}) {
  const [detail, setDetail] = useState<StudentDetail | null>(null);
  const [detailErr, setDetailErr] = useState('');
  const [msg, setMsg] = useState('');

  // 展开时按需拉明细，避免一次拉所有人
  const loadDetail = useCallback(async () => {
    setDetailErr('');
    try {
      setDetail(await fetchStudentDetail(pin, s.username));
    } catch (e: any) {
      setDetailErr(String(e?.message || '读取明细失败'));
    }
  }, [pin, s.username]);

  const toggle = () => {
    if (!open && !detail) void loadDetail();
    onToggle();
  };

  return (
    <div className="card mt-3 !p-0 overflow-hidden">
      <button onClick={toggle} className="w-full px-4 py-3 text-left">
        <div className="flex items-center justify-between">
          <span className="text-sm font-bold text-brand-900">👤 {s.displayName}</span>
          <span className="text-xs text-slate-400">{open ? '收起 ▲' : '详情 ▼'}</span>
        </div>
        <div className="mt-1.5 flex flex-wrap gap-x-3 gap-y-1 text-xs text-slate-600">
          <span>📝 已学 <b className="text-brand-700">{s.learned}</b> 词</span>
          <span>📕 错词 {s.mistakes}</span>
          <span>🎧 听读 {s.readings}</span>
          <span>📅 学习 {s.days} 天</span>
          <span>⏱️ {s.minutes} 分钟</span>
        </div>
        <div className="mt-1 text-xs text-slate-400">
          {s.linked
            ? `今天 ${s.todayWords} 词 · 最近 ${s.lastDay ?? '—'}`
            : '云端还没有学习记录（学生还没登录过）'}
          {s.scope && (
            <span className="ml-2 rounded bg-amber-50 px-1.5 py-0.5 text-amber-700">
              已限制 {s.scope.length} 个年级
            </span>
          )}
        </div>
      </button>

      {open && (
        <div className="border-t border-slate-100 px-4 py-3">
          {msg && <p className="mb-2 rounded-lg bg-emerald-50 px-3 py-2 text-xs text-emerald-700">{msg}</p>}
          {detailErr && <p className="mb-2 rounded-lg bg-rose-50 px-3 py-2 text-xs text-rose-600">{detailErr}</p>}
          {!detail ? (
            <p className="text-xs text-slate-400">读取中…</p>
          ) : (
            <>
              <DailyDetail progress={detail.progress} />
              <ScopeEditor
                pin={pin}
                username={s.username}
                scope={detail.scope}
                onSaved={(newScope) => {
                  setDetail({ ...detail, scope: newScope });
                  setMsg('内容范围已保存，学生下次打开 App 生效');
                  onChanged();
                }}
              />
              <div className="mt-4 border-t border-slate-100 pt-3">
                <button
                  onClick={async () => {
                    if (!confirm(`确定清除「${s.displayName}」的全部学习数据？\n清掉后无法恢复。`)) return;
                    try {
                      await clearStudentProgress(pin, s.username);
                      setMsg('已清除。学生下次打开 App 时，本机进度也会被清空。');
                      setDetail({ ...detail, progress: {} });
                      onChanged();
                    } catch (e: any) {
                      setDetailErr(String(e?.message || '清除失败'));
                    }
                  }}
                  className="w-full rounded-xl bg-rose-50 py-2.5 text-sm font-medium text-rose-600"
                >
                  🗑 清除这个学生的学习数据
                </button>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

// ---- 每日明细 ----
function DailyDetail({ progress }: { progress: any }) {
  const history: Record<string, any> = progress?.history ?? {};
  const rows = useMemo(() => {
    const quiz = progress?.readingScores ?? {};
    const rec = progress?.readingRecordScores ?? {};
    return Object.entries(history)
      .map(([date, d]: [string, any]) => ({
        date,
        words: d?.words ?? 0,
        readings: d?.readings ?? 0,
        minutes: d?.minutes ?? 0,
        stars: starsFor(d, quiz, rec),
      }))
      .filter((d) => d.words > 0 || d.readings > 0 || d.minutes > 0)
      .sort((a, b) => (a.date < b.date ? 1 : -1))
      .slice(0, 14);
  }, [history, progress]);

  const totalWords = progress?.learnedIds?.length ?? 0;
  const totalMistakes = progress?.mistakeIds?.length ?? 0;

  return (
    <div>
      <div className="section-title mb-1">每天学了多少</div>
      {rows.length === 0 ? (
        <p className="py-1 text-xs text-slate-400">云端还没有学习记录。</p>
      ) : (
        <div className="max-h-56 space-y-1.5 overflow-y-auto pr-1">
          {rows.map((d) => (
            <div key={d.date} className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-1.5 text-xs">
              <span className="font-semibold text-slate-600">{d.date}</span>
              <span className="flex items-center gap-2.5 text-slate-500">
                <span className="font-bold text-amber-500">⭐ {d.stars}</span>
                <span>📝 {d.words}</span>
                <span>🎧 {d.readings}</span>
                <span>⏱️ {d.minutes}′</span>
              </span>
            </div>
          ))}
        </div>
      )}
      <p className="mt-1.5 text-[11px] text-slate-400">
        累计已学 {totalWords} 词 · 错词本 {totalMistakes} 个
      </p>
    </div>
  );
}

// 与 lib/progress.tsx 的 starsFor 保持一致：单词星（≤5）+ 听读星（≤5）+ 当日奖励
function starsFor(day: any, quizScores: Record<string, number>, recScores: Record<string, number>): number {
  const w = (Math.min(day?.words ?? 0, 10) / 10) * 5;
  let best = 0;
  for (const id of day?.readingIds ?? []) {
    const parts = [recScores?.[id], quizScores?.[id]].filter((x) => typeof x === 'number');
    if (parts.length) best = Math.max(best, parts.reduce((a, b) => a + b, 0) / parts.length);
  }
  const a = Math.min(1, best / 100) * 5;
  return Math.round((w + a + (day?.bonus ?? 0)) * 10) / 10;
}

// ---- 内容开放范围 ----
function ScopeEditor({
  pin,
  username,
  scope,
  onSaved,
}: {
  pin: string;
  username: string;
  scope: string[] | null;
  onSaved: (s: string[] | null) => void;
}) {
  const [allOpen, setAllOpen] = useState(scope === null);
  const [picked, setPicked] = useState<string[]>(scope ?? []);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');

  const toggleGrade = (id: string) =>
    setPicked((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]));

  // 按学段批量勾选
  const toggleSection = (sec: GradeStage['section']) => {
    const ids = grades.filter((g) => g.section === sec).map((g) => g.id);
    const allOn = ids.every((id) => picked.includes(id));
    setPicked((prev) => (allOn ? prev.filter((x) => !ids.includes(x)) : [...new Set([...prev, ...ids])]));
  };

  const save = async () => {
    setErr('');
    if (!allOpen && picked.length === 0) {
      return setErr('至少勾选一个年级；想全开就打开上面的「全部内容开放」');
    }
    setBusy(true);
    try {
      const next = allOpen ? null : picked;
      await setStudentScope(pin, username, next);
      onSaved(next);
    } catch (e: any) {
      setErr(String(e?.message || '保存失败'));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mt-4 border-t border-slate-100 pt-3">
      <div className="section-title mb-1">内容开放范围</div>
      <label className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2 text-sm text-slate-700">
        <span>全部内容开放</span>
        <input
          type="checkbox"
          checked={allOpen}
          onChange={(e) => setAllOpen(e.target.checked)}
          className="h-4 w-4 accent-brand-600"
        />
      </label>

      {!allOpen && (
        <div className="mt-3 space-y-3">
          <p className="text-[11px] text-slate-400">
            只勾这个学生要学的年级。没勾的年级，学生那里会显示一把锁 🔒，点不进去。
          </p>
          {SECTIONS.map((sec) => {
            const list = grades.filter((g) => g.section === sec);
            const onCount = list.filter((g) => picked.includes(g.id)).length;
            return (
              <div key={sec}>
                <button
                  onClick={() => toggleSection(sec)}
                  className="flex w-full items-center justify-between text-xs font-semibold text-brand-800"
                >
                  <span>
                    {sec}
                    <span className="ml-1.5 font-normal text-slate-400">
                      {onCount}/{list.length}
                    </span>
                  </span>
                  <span className="text-brand-600">{onCount === list.length ? '全不选' : '全选'}</span>
                </button>
                <div className="mt-1.5 grid grid-cols-4 gap-1.5">
                  {list.map((g) => {
                    const on = picked.includes(g.id);
                    return (
                      <button
                        key={g.id}
                        onClick={() => toggleGrade(g.id)}
                        className={`rounded-xl border px-1 py-1.5 text-xs font-medium transition ${
                          on
                            ? 'border-brand-400 bg-brand-50 text-brand-800'
                            : 'border-slate-200 bg-white text-slate-400'
                        }`}
                      >
                        {g.short}
                      </button>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {err && <p className="mt-2 rounded-lg bg-rose-50 px-3 py-2 text-xs text-rose-600">{err}</p>}
      <button onClick={save} disabled={busy} className="btn-primary mt-3 w-full !py-2.5 text-sm disabled:opacity-60">
        {busy ? '保存中…' : '保存内容范围'}
      </button>
    </div>
  );
}

// ---- 添加学生 ----
function AddStudent({
  pin,
  createStudent,
  onDone,
}: {
  pin: string;
  createStudent: (u: string, p: string, pin: string) => Promise<{ isNew: boolean }>;
  onDone: () => void;
}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [err, setErr] = useState('');
  const [msg, setMsg] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setErr('');
    setMsg('');
    if (!username.trim()) return setErr('请填写用户名（中文或英文都可以）');
    if (password.length < 6) return setErr('密码至少 6 位');
    if (password !== confirm) return setErr('两次输入的密码不一致');
    setBusy(true);
    try {
      const r = await createStudent(username.trim(), password, pin);
      setMsg(r.isNew ? `已添加学生：${username.trim()}` : `「${username.trim()}」已存在，已把密码改成新密码`);
      setUsername('');
      setPassword('');
      setConfirm('');
      onDone();
    } catch (e: any) {
      setErr(String(e?.message || '添加失败，请重试'));
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit} className="card mt-4">
      <label className="section-title mb-0">用户名</label>
      <input
        type="text"
        inputMode="text"
        autoComplete="off"
        autoCorrect="off"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="如 小明 或 xiaoming"
        className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm outline-none focus:border-brand-400"
      />
      <p className="mt-1 text-[11px] text-slate-400">中文、英文、数字都行，学生登录时照这个输入。</p>

      <label className="section-title mb-0 mt-4">密码</label>
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="至少 6 位"
        className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm outline-none focus:border-brand-400"
      />

      <label className="section-title mb-0 mt-4">确认密码</label>
      <input
        type="password"
        value={confirm}
        onChange={(e) => setConfirm(e.target.value)}
        placeholder="再输一次密码"
        className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm outline-none focus:border-brand-400"
      />

      {err && <p className="mt-3 rounded-lg bg-rose-50 px-3 py-2 text-xs text-rose-600">{err}</p>}
      {msg && <p className="mt-3 rounded-lg bg-emerald-50 px-3 py-2 text-xs text-emerald-700">{msg}</p>}

      <button type="submit" disabled={busy} className="btn-primary mt-5 w-full !py-2.5 disabled:opacity-60">
        {busy ? '添加中…' : '添加学生'}
      </button>
      <p className="mt-3 text-center text-xs text-slate-400">
        同一个用户名再添加一次，就是把他的密码改成新密码（学生忘密码时用得上）。
      </p>
    </form>
  );
}
