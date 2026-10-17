import { FormEvent, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../lib/auth';

// 登录页：学生用“用户名 + 密码”登录（账号由老师在后台设置）
export default function Login() {
  const { login } = useAuth();
  const nav = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password) {
      setErr('请输入用户名和密码');
      return;
    }
    setBusy(true);
    setErr('');
    try {
      await login(username, password);
      nav('/'); // 登录成功回首页，进度会自动从云端加载
    } catch (e: any) {
      // 服务端已经给出中文原因（账号不存在 / 密码不正确 / 登录已过期…），
      // 网络不通也会被翻译成一句人话，这里直接展示即可。
      const msg = String(e?.message || '');
      if (!msg && typeof navigator !== 'undefined' && navigator.onLine === false) {
        setErr('当前设备没有网络连接，无法登录。请连上网络后重试，或先离线使用。');
      } else {
        setErr(msg || '登录失败，请稍后重试。');
      }
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="page flex min-h-screen flex-col pb-10 pt-12">
      <div className="animate-fadeup">
        <div className="flex items-center gap-2">
          <span className="grid h-10 w-10 place-items-center rounded-2xl bg-gradient-to-br from-brand-600 to-brand-800 text-xl shadow-soft">
            📖
          </span>
          <div>
            <h1 className="text-2xl font-extrabold tracking-tight text-brand-900">航悦英语</h1>
            <p className="text-xs text-slate-500">登录后进度自动保存到云端</p>
          </div>
        </div>
      </div>

      <form onSubmit={submit} className="card mt-8 animate-fadeup">
        <label className="section-title mb-0">用户名</label>
        <input
          type="text"
          inputMode="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="老师给的用户名，如 小明 或 xiaoming"
          autoComplete="username"
          autoCapitalize="none"
          spellCheck={false}
          className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm outline-none focus:border-brand-400"
        />

        <label className="section-title mb-0 mt-4">密码</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="老师设置的密码"
          autoComplete="current-password"
          className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm outline-none focus:border-brand-400"
        />

        {err && <p className="mt-3 rounded-lg bg-rose-50 px-3 py-2 text-xs leading-5 text-rose-600">{err}</p>}

        <button
          type="submit"
          disabled={busy}
          className="btn-primary mt-5 w-full !py-3 text-base disabled:opacity-60"
        >
          {busy ? '登录中…' : '登录'}
        </button>
      </form>

      <p className="mt-4 text-center text-xs text-slate-400">
        账号由老师在 App 内的「老师后台」添加，用户名可以是中文或英文，自己无法注册。
      </p>

      <Link to="/" className="mt-auto pt-6 text-center text-sm text-brand-600">
        ← 返回首页（不登录也能先体验）
      </Link>
    </div>
  );
}
