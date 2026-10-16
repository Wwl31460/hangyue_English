import { FormEvent, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../lib/auth';

// 老师口令：打开“添加学生”前先验证，避免学生自行添加账号。
// 想改口令就改下面这个常量（建议换个只有你知道的 4 位以上数字）。
const TEACHER_PIN = 'wwl31460';

// 老师后台：用“用户名 + 密码”添加学生账号（邮箱由系统自动生成，无需填写）
export default function Teacher() {
  const { createStudent } = useAuth();
  const nav = useNavigate();
  const [pin, setPin] = useState('');
  const [pinOk, setPinOk] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [err, setErr] = useState('');
  const [msg, setMsg] = useState('');
  const [busy, setBusy] = useState(false);

  const verifyPin = (e: FormEvent) => {
    e.preventDefault();
    if (pin === TEACHER_PIN) {
      setPinOk(true);
      setErr('');
    } else {
      setErr('口令不正确');
    }
  };

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setErr('');
    setMsg('');
    if (!username.trim()) return setErr('请填写用户名（中文或英文都可以）');
    if (password.length < 6) return setErr('密码至少 6 位');
    if (password !== confirm) return setErr('两次输入的密码不一致');
    setBusy(true);
    try {
      await createStudent(username.trim(), password);
      setMsg(`已添加学生：${username.trim()}`);
      setUsername('');
      setPassword('');
      setConfirm('');
    } catch {
      setErr('添加失败：该用户名可能已存在，或网络异常，请重试');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="page pb-10 pt-8">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-extrabold text-brand-900">老师后台</h1>
        <Link to="/" className="text-sm text-brand-600">
          ← 返回
        </Link>
      </div>
      <p className="mt-1 text-xs text-slate-500">添加学生账号（用户名支持中文或英文，无需邮箱）</p>

      {!pinOk ? (
        <form onSubmit={verifyPin} className="card mt-5">
          <label className="section-title mb-0">老师口令</label>
          <input
            type="password"
            value={pin}
            onChange={(e) => setPin(e.target.value)}
            placeholder="请输入老师口令"
            className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm outline-none focus:border-brand-400"
          />
          {err && <p className="mt-3 rounded-lg bg-rose-50 px-3 py-2 text-xs text-rose-600">{err}</p>}
          <button type="submit" className="btn-primary mt-4 w-full !py-2.5">
            进入
          </button>
        </form>
      ) : (
        <form onSubmit={submit} className="card mt-5">
          <label className="section-title mb-0">用户名</label>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="如 小明 或 xiaoming"
            className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm outline-none focus:border-brand-400"
          />

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
            添加后，学生打开 App 用「用户名 + 密码」即可登录。
          </p>
        </form>
      )}
    </div>
  );
}
